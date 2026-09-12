"""Train the supplied parent checkpoint using only the kernel's train data file."""
import hashlib
import json
import os
from pathlib import Path
import time

from network import train, training_examples, validate_model


def main():
    started = time.monotonic()
    data_path = Path(os.environ["NANORSI_TRAINING_DATA_PATH"])
    checkpoint_path = Path(os.environ["NANORSI_CHECKPOINT_PATH"])
    result_path = Path(os.environ["NANORSI_TRAINING_RESULT_PATH"])
    initial_bytes = checkpoint_path.read_bytes()
    data_bytes = data_path.read_bytes()
    rows = training_examples(json.loads(data_bytes))
    model = validate_model(json.loads(initial_bytes))
    recipe = json.loads((Path.cwd() / "target/recipe.json").read_text())
    stats = train(model, rows, recipe)
    checkpoint_bytes = (json.dumps(model, indent=2, sort_keys=True, allow_nan=False) + "\n").encode()
    checkpoint_path.write_bytes(checkpoint_bytes)
    result = {
        "schema_version": 1, "status": "completed", **stats,
        "checkpoint_path": str(checkpoint_path.resolve()),
        "checkpoint_sha256": hashlib.sha256(checkpoint_bytes).hexdigest(),
        "initial_checkpoint_sha256": hashlib.sha256(initial_bytes).hexdigest(),
        "data_sha256": hashlib.sha256(data_bytes).hexdigest(),
        "task_ids": [row["task_id"] for row in rows],
        "duration_ms": max(0, int((time.monotonic() - started) * 1000)),
    }
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
