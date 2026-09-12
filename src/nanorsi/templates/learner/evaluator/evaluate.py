"""Read a saved checkpoint; never train while measuring validation or final test."""
import hashlib
import json
import math
import os
from pathlib import Path
import random
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "trainer"))
from network import example, probabilities, validate_model


def usage():
    # No API/LLM calls; CPU wall time is measured separately, money is unknown.
    return {"model_calls": 0, "input_tokens": None, "output_tokens": None,
            "cost_usd": None, "errors": []}


def evaluate():
    started = time.monotonic()
    split = os.environ["NANORSI_SPLIT"]
    if split not in ("train", "validation", "test"):
        raise ValueError("unknown evaluation split")
    checkpoint_bytes = (Path.cwd() / "target/model.json").read_bytes()
    checkpoint_hash = hashlib.sha256(checkpoint_bytes).hexdigest()
    model = validate_model(json.loads(checkpoint_bytes))
    payload = json.loads(Path(os.environ["NANORSI_TASK_MANIFEST"]).read_text())
    tasks = [task for task in payload["tasks"] if task["split"] == split]
    limit = int(os.environ.get("NANORSI_TRAIN_LIMIT", "4"))
    if split == "train" and len(tasks) > limit:
        tasks = random.Random(int(os.environ.get("NANORSI_SEED", "0"))).sample(tasks, limit)
    if not tasks:
        raise ValueError("empty evaluation panel")
    cases = []
    for task in sorted(tasks, key=lambda task: task["task_id"]):
        case_started = time.monotonic()
        row = example(task)
        probs = probabilities(model, row["features"])
        prediction = max(range(3), key=probs.__getitem__)
        score = float(prediction == row["label"])
        loss = -math.log(max(probs[row["label"]], 1e-15))
        case = {
            "task_id": task["task_id"], "group_id": task["group_id"],
            "repeat_id": int(os.environ.get("NANORSI_REPEAT_ID", "0")),
            "score": score, "loss": loss, "status": "ok" if score else "task_failure",
            "trace": [{"event": "checkpoint_inference", "checkpoint_sha256": checkpoint_hash}],
            "skill_hashes": {}, "usage": usage(),
            "duration_ms": max(0, int((time.monotonic() - case_started) * 1000)),
        }
        if split == "train":
            case["task"] = {"task_id": task["task_id"], "instruction": task["instruction"],
                            "input_files": task["input_files"]}
            case["feedback"] = {"expected_files": task["expected_files"],
                                "actual_files": {"label.txt": str(prediction)},
                                "probabilities": probs}
        cases.append(case)
    accuracy = sum(case["score"] for case in cases) / len(cases)
    return {
        "schema_version": 2, "status": "ok",
        "metrics": {"score": accuracy, "accuracy": accuracy,
                    "loss": sum(case["loss"] for case in cases) / len(cases)},
        "constraints": {"checkpoint_valid": True}, "case_results": cases,
        "usage": usage(), "cost_usd": None,
        "duration_ms": max(0, int((time.monotonic() - started) * 1000)),
    }


def main():
    try:
        result = evaluate()
    except (OSError, ValueError, KeyError, TypeError) as error:
        result = {"schema_version": 2, "status": "error", "metrics": {"score": 0.0},
                  "constraints": {"checkpoint_valid": False}, "case_results": [],
                  "usage": {**usage(), "errors": [str(error)]}, "cost_usd": None, "duration_ms": 0}
    Path(os.environ["NANORSI_RESULT_PATH"]).write_text(json.dumps(result, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
