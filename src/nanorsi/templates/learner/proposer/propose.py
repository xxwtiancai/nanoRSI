"""Use the selected proposer checkpoint to weight difficult train examples."""
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "trainer"))
from network import example, probabilities, validate_model


def propose():
    output = Path(os.environ["NANORSI_PROPOSAL_DIR"])
    output.mkdir(parents=True, exist_ok=True)
    context = json.loads(Path(os.environ["NANORSI_CONTEXT_PATH"]).read_text())
    harness = Path(os.environ["NANORSI_PROPOSER_HARNESS"])
    checkpoint_bytes = (harness / "target/model.json").read_bytes()
    model = validate_model(json.loads(checkpoint_bytes))
    losses = []
    for case in context["train_results"]:
        task = case["task"]
        if not task["task_id"].startswith("train-"):
            raise ValueError("proposer feedback must contain train rows only")
        row = example({**task, "expected_files": case["feedback"]["expected_files"]})
        probs = probabilities(model, row["features"])
        losses.append({"task_id": row["task_id"], "loss": -math.log(max(probs[row["label"]], 1e-15))})
    ranked = sorted(losses, key=lambda row: (-row["loss"], row["task_id"]))
    focus = [row["task_id"] for row in ranked[:max(1, len(ranked) // 2)]]
    recipe_path = Path.cwd() / "target/recipe.json"
    original = recipe_path.read_text()
    recipe = json.loads(original)
    recipe["focus_task_ids"] = focus
    updated = json.dumps(recipe, indent=2, sort_keys=True) + "\n"
    patch = "".join(difflib.unified_diff(original.splitlines(keepends=True), updated.splitlines(keepends=True),
                                        fromfile="a/target/recipe.json", tofile="b/target/recipe.json"))
    if patch:
        patch = "diff --git a/target/recipe.json b/target/recipe.json\n" + patch
    # Empty recipe diff is legitimate: the kernel still performs actual training.
    (output / "proposal.diff").write_text(patch)
    hypothesis = {
        "hypothesis": f"Continue {recipe['method']} gradients from the parent checkpoint; triple sampling weight of the {len(focus)} highest-loss train feedback examples under the selected proposer checkpoint.",
        "expected_metrics": {},
        "risks": ["A four-example feedback panel can give a noisy curriculum.",
                  "Training or curriculum changes can worsen validation and held-out accuracy.",
                  "This tiny classifier demonstrates learning mechanics, not LLM fine-tuning or established recursive benefit."],
    }
    (output / "hypothesis.json").write_text(json.dumps(hypothesis, indent=2) + "\n")
    (output / "usage.json").write_text(json.dumps({"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": []}) + "\n")
    (output / "trace.json").write_text(json.dumps([{
        "event": "checkpoint_curriculum", "checkpoint_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
        "example_losses": losses, "focus_task_ids": focus,
    }], indent=2) + "\n")


if __name__ == "__main__":
    propose()
