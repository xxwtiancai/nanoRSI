"""Generate fresh disjoint numeric classification rows, never winning weights."""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import random


def build_manifest(seed=0):
    tasks = []
    for split_index, split in enumerate(("train", "validation", "test")):
        rng = random.Random(seed * 1009 + split_index * 100003)
        for index in range(120):
            label = index % 3
            angle = label * 2 * math.pi / 3
            # Overlapping Gaussian clusters plus two nuisance features.
            # Each observation is an independent source group.
            features = [rng.gauss(1.5 * math.cos(angle), 0.95),
                        rng.gauss(1.5 * math.sin(angle), 0.95),
                        rng.gauss(0, 1), rng.gauss(0, 1)]
            task_id = f"{split}-{index:03d}"
            tasks.append({"task_id": task_id, "group_id": f"seed-{seed}-{task_id}",
                          "split": split, "instruction": "Predict class 0, 1, or 2 from the four numeric features.",
                          "input_files": {"features.json": json.dumps(features)},
                          "expected_files": {"label.txt": str(label)}})
    return {"schema_version": 1, "tasks": tasks}


def write_manifest(output, seed=0):
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_manifest(seed), indent=2, sort_keys=True) + "\n")
    return output


def prepare_workspace(workspace, *, method="sft", seed=0, arm="self-use", rounds=3):
    """Configure an already-created learner workspace before its first baseline."""
    workspace = Path(workspace)
    if (workspace / ".nanorsi").exists():
        raise ValueError("prepare requires a fresh workspace without experiment state")
    if method not in ("sft", "rl", "lora") or arm not in ("self-use", "frozen"):
        raise ValueError("unsupported method or proposer arm")
    spec = importlib.util.spec_from_file_location("learner_network", workspace / "trainer/network.py")
    network = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(network)
    (workspace / "target/model.json").write_text(json.dumps(network.initial_model(seed), indent=2, sort_keys=True) + "\n")
    recipe = {"method": method, "seed": seed, "steps": 200, "lr": 0.12,
              "batch_size": 24, "focus_task_ids": []}
    (workspace / "target/recipe.json").write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n")
    write_manifest(workspace / "tasks/manifest.json", seed)
    config_path = workspace / "nanorsi.toml"
    text = config_path.read_text()
    text = text.replace('id = "learner-lab"', f'id = "learner-{method}-{seed}-{arm}"')
    text = text.replace('seed = 0', f'seed = {seed}', 1)
    text = text.replace('arm = "self-use"', f'arm = "{arm}"', 1)
    text = text.replace('max_steps = 3', f'max_steps = {rounds}', 1)
    text = text.replace('max_episodes = 1000', f'max_episodes = {120 + rounds * 244}', 1)
    config_path.write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace", type=Path)
    parser.add_argument("--method", choices=("sft", "rl", "lora"), default="sft")
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--arm", choices=("frozen", "self-use"), default="self-use")
    parser.add_argument("--rounds", type=int, default=3)
    args = parser.parse_args()
    prepare_workspace(args.workspace, method=args.method, seed=args.seed, arm=args.arm, rounds=args.rounds)
    print(f"Prepared {args.method} CPU teaching demo, seed {args.seed}; no training performed.")


if __name__ == "__main__":
    main()
