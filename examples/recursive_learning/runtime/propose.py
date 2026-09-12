"""Score the selected checkpoint's full TRAIN panel and propose a curriculum."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "trainer"))
from network import (example, example_losses, sampling_distribution,
                     sampling_fingerprint, select_focus, validate_model)


def propose():
    context = json.loads(Path(os.environ["NANORSI_CONTEXT_PATH"]).read_text())
    harness = Path(os.environ["NANORSI_PROPOSER_HARNESS"])
    checkpoint_bytes = (harness / "target/model.json").read_bytes()
    model = validate_model(json.loads(checkpoint_bytes))
    rows = []
    for case in context["train_results"]:
        task = case["task"]
        if (not isinstance(task.get("task_id"), str) or not task["task_id"].startswith("train-")
                or case.get("task_id", task["task_id"]) != task["task_id"]
                or task.get("split", "train") != "train" or case.get("split", "train") != "train"):
            raise ValueError("proposer feedback must contain train rows only")
        rows.append(example({**task, "expected_files": case["feedback"]["expected_files"]}))
    recipe_path = Path.cwd() / "target/recipe.json"
    original = recipe_path.read_text()
    recipe = json.loads(original)
    recipe["attempt"] = context["attempt_id"]
    if type(recipe["attempt"]) is not int or recipe["attempt"] < 1:
        raise ValueError("proposer requires a positive attempt identity")
    if recipe["seed"] != model["metadata"]["initialization_seed"]:
        raise ValueError("recipe seed must match the selected checkpoint initialization seed")
    # Uniform and random controls perform this same checkpoint-scoring workload.
    values = example_losses(model, rows)
    recipe["focus_task_ids"] = select_focus(rows, values, recipe)
    distribution = sampling_distribution(rows, recipe)
    updated = json.dumps(recipe, indent=2, sort_keys=True, allow_nan=False) + "\n"
    patch = "".join(difflib.unified_diff(original.splitlines(keepends=True), updated.splitlines(keepends=True),
                                       fromfile="a/target/recipe.json", tofile="b/target/recipe.json"))
    if patch:
        patch = "diff --git a/target/recipe.json b/target/recipe.json\n" + patch
    output = Path(os.environ["NANORSI_PROPOSAL_DIR"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "proposal.diff").write_text(patch)
    hypothesis = {
        "hypothesis": f"Continue {recipe['method']} training for attempt {recipe['attempt']} using {recipe['policy']} sampling after scoring all {len(rows)} TRAIN examples with the selected checkpoint.",
        "expected_metrics": {},
        "risks": ["Prioritization can worsen validation loss.",
                  "Additional recursive benefit must be measured against the frozen and sampling controls."],
    }
    (output / "hypothesis.json").write_text(json.dumps(hypothesis, indent=2) + "\n")
    usage = {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": []}
    (output / "usage.json").write_text(json.dumps(usage) + "\n")
    trace = [{
        "event": "checkpoint_curriculum", "checkpoint_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
        "scored_examples": len(rows), "attempt": recipe["attempt"], "policy": recipe["policy"],
        "balanced": recipe["balanced"], "multiplier": recipe["multiplier"],
        "example_losses": [{"task_id": row["task_id"], "loss": loss} for row, loss in zip(rows, values)],
        "focus_task_ids": recipe["focus_task_ids"],
        "sampling_sha256": sampling_fingerprint(rows, distribution),
    }]
    (output / "trace.json").write_text(json.dumps(trace, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    propose()
