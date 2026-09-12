"""Optional NumPy linear-softmax experiment; the nanoRSI core remains stdlib.

Raw 8x8 image pixels are divided by 16 and augmented with a bias. The effective
matrix is W + A @ B, with shapes (65, 10), (65, 4), and (4, 10). SFT and sampled
REINFORCE update W; LoRA updates A and B while freezing W.
"""
from __future__ import annotations

import hashlib
import json
import math
import os

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np


def initial_model(seed=0):
    if type(seed) is not int or seed < 0:
        raise ValueError("initialization seed must be a nonnegative integer")
    rng = np.random.default_rng(seed)
    return {
        "schema_version": 1, "kind": "recursive-digits-softmax",
        "input_dim": 64, "classes": 10, "rank": 4,
        "weights": rng.normal(0, .01, (65, 10)).tolist(),
        "lora_a": rng.normal(0, .1, (65, 4)).tolist(),
        "lora_b": np.zeros((4, 10)).tolist(),
        "metadata": {"initialization_seed": seed, "training_steps": 0},
    }


def validate_model(model):
    if not isinstance(model, dict) or model.get("schema_version") != 1 or model.get("kind") != "recursive-digits-softmax":
        raise ValueError("unsupported checkpoint schema or model kind")
    if (model.get("input_dim"), model.get("classes"), model.get("rank")) != (64, 10, 4):
        raise ValueError("checkpoint requires 64 inputs, 10 classes, rank 4")
    for name, nrows, ncols in (("weights", 65, 10), ("lora_a", 65, 4), ("lora_b", 4, 10)):
        matrix = model.get(name)
        if not isinstance(matrix, list) or len(matrix) != nrows:
            raise ValueError(f"invalid {name} shape")
        for row in matrix:
            if not isinstance(row, list) or len(row) != ncols:
                raise ValueError(f"invalid {name} shape")
            if any(type(value) not in (int, float) or not math.isfinite(value) for value in row):
                raise ValueError(f"non-finite or nonnumeric {name}")
    metadata = model.get("metadata", {})
    for key in ("initialization_seed", "training_steps"):
        if type(metadata.get(key)) is not int or metadata[key] < 0:
            raise ValueError(f"invalid metadata.{key}")
    return model


def _features(features):
    if not isinstance(features, list) or len(features) != 64:
        raise ValueError("examples require 64 pixel features")
    if any(type(value) not in (int, float) or not math.isfinite(value) or not 0 <= value <= 16 for value in features):
        raise ValueError("pixel features must be finite numbers in [0, 16]")
    return features


def example(task):
    features = _features(json.loads(task["input_files"]["features.json"]))
    label = int(task["expected_files"]["label.txt"].strip())
    if label not in range(10):
        raise ValueError("label must be a class from 0 through 9")
    if not isinstance(task.get("task_id"), str) or not task["task_id"]:
        raise ValueError("a task identity is required")
    return {"task_id": task["task_id"], "features": features, "label": label}


def _training_rows(rows):
    if not isinstance(rows, list) or not rows:
        raise ValueError("nonempty train rows are required")
    for row in rows:
        if not isinstance(row.get("task_id"), str) or not row["task_id"].startswith("train-") or row.get("split", "train") != "train":
            raise ValueError("trainer accepts train rows only")
        _features(row["features"])
        if type(row.get("label")) is not int or row["label"] not in range(10):
            raise ValueError("label must be a class from 0 through 9")
    if len({row["task_id"] for row in rows}) != len(rows):
        raise ValueError("training task identities must be unique")
    return rows


def training_examples(payload):
    if payload.get("schema_version") != 1 or not isinstance(payload.get("tasks"), list) or not payload["tasks"]:
        raise ValueError("nonempty schema-version 1 training data required")
    if any(task.get("split") != "train" for task in payload["tasks"]):
        raise ValueError("trainer accepts train rows only")
    return _training_rows([example(task) for task in payload["tasks"]])


def _arrays(model):
    return tuple(np.asarray(model[key], dtype=float) for key in ("weights", "lora_a", "lora_b"))


def _inputs(rows):
    if not rows:
        raise ValueError("cannot evaluate an empty panel")
    pixels = np.asarray([_features(row["features"]) for row in rows], dtype=float)
    return np.column_stack([pixels / 16.0, np.ones(len(rows))])


def _predict(w, a, b, x):
    logits = x @ (w + a @ b)
    logits -= logits.max(1, keepdims=True)
    probabilities = np.exp(logits)
    return probabilities / probabilities.sum(1, keepdims=True)


def probabilities(model, features):
    x = np.asarray([_features(features)], dtype=float) / 16.0
    return _predict(*_arrays(model), np.column_stack([x, np.ones(1)]))[0].tolist()


def example_losses(model, rows):
    probabilities = _predict(*_arrays(model), _inputs(rows))
    labels = np.asarray([row["label"] for row in rows])
    return (-np.log(np.maximum(probabilities[np.arange(len(rows)), labels], 1e-15))).tolist()


def metrics(model, rows):
    probabilities = _predict(*_arrays(model), _inputs(rows))
    labels = np.asarray([row["label"] for row in rows])
    return {"accuracy": float((probabilities.argmax(1) == labels).mean()),
            "loss": float(-np.log(np.maximum(probabilities[np.arange(len(rows)), labels], 1e-15)).mean())}


def validate_recipe(recipe):
    allowed = {"method", "seed", "steps", "lr", "batch_size", "multiplier", "balanced", "policy", "attempt", "focus_task_ids"}
    if not isinstance(recipe, dict) or set(recipe) - allowed:
        raise ValueError("unsupported recipe fields; matrix overrides are not allowed")
    if recipe.get("method") not in ("sft", "rl", "lora"):
        raise ValueError("method must be sft, rl, or lora")
    for key, minimum, maximum in (("seed", 0, 2**32 - 1), ("steps", 1, 10000), ("batch_size", 1, 256), ("attempt", 0, 1000000)):
        if type(recipe.get(key)) is not int or not minimum <= recipe[key] <= maximum:
            raise ValueError(f"{key} must be an integer in [{minimum}, {maximum}]")
    lr = recipe.get("lr")
    if type(lr) not in (int, float) or not math.isfinite(lr) or not 0 < lr <= 1:
        raise ValueError("lr must be finite and in (0, 1]")
    if type(recipe.get("multiplier")) is not int or recipe["multiplier"] not in (3, 9):
        raise ValueError("multiplier must be 3 or 9")
    if type(recipe.get("balanced")) is not bool:
        raise ValueError("balanced must be a boolean")
    if recipe.get("policy") not in ("prioritized", "uniform", "random"):
        raise ValueError("policy must be prioritized, uniform, or random")
    focus = recipe.get("focus_task_ids")
    if not isinstance(focus, list) or any(not isinstance(value, str) for value in focus) or len(set(focus)) != len(focus):
        raise ValueError("focus_task_ids must contain unique train identities")
    return recipe


def select_focus(rows, losses, recipe):
    """Select the pilot's global or within-class top quartile in task order."""
    _training_rows(rows)
    validate_recipe(recipe)
    losses = np.asarray(losses, dtype=float)
    if losses.shape != (len(rows),) or not np.isfinite(losses).all():
        raise ValueError("one finite loss per train example is required")
    order = np.argsort(-losses, kind="stable")
    if recipe["policy"] == "random":
        rng = np.random.default_rng(recipe["seed"] * 10000 + recipe["attempt"] - 1 + 900000)
        order = rng.permutation(len(rows))
    if recipe["policy"] == "uniform":
        return []
    if recipe["balanced"]:
        labels = np.asarray([row["label"] for row in rows])
        focus = []
        for cls in range(10):
            members = order[labels[order] == cls]
            focus.extend(members[:max(1, len(members) // 4)])
    else:
        focus = order[:len(rows) // 4]
    return [rows[index]["task_id"] for index in focus]


def sampling_distribution(rows, recipe):
    _training_rows(rows)
    validate_recipe(recipe)
    focus = set(recipe["focus_task_ids"])
    if focus - {row["task_id"] for row in rows}:
        raise ValueError("focus_task_ids must identify available train rows")
    weights = np.ones(len(rows))
    if recipe["policy"] != "uniform":
        weights[[index for index, row in enumerate(rows) if row["task_id"] in focus]] = recipe["multiplier"]
        if recipe["balanced"]:
            labels = np.asarray([row["label"] for row in rows])
            for cls in range(10):
                members = np.flatnonzero(labels == cls)
                if len(members):
                    weights[members] *= len(members) / weights[members].sum()
    return (weights / weights.sum()).tolist()


def sampling_fingerprint(rows, distribution):
    payload = {"task_ids": [row["task_id"] for row in rows], "probabilities": distribution}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def classification_reward(row, action):
    """The environment reveals whether the sampled class was correct."""
    return float(action == row["label"])


def train(model, rows, recipe, *, reward_fn=classification_reward):
    validate_model(model)
    distribution = sampling_distribution(rows, recipe)
    if recipe["attempt"] < 1:
        raise ValueError("training requires a positive attempt identity")
    if recipe["seed"] != model["metadata"]["initialization_seed"]:
        raise ValueError("recipe seed must match the checkpoint initialization seed")
    method, steps, lr, batch_size = (recipe[key] for key in ("method", "steps", "lr", "batch_size"))
    training_seed = recipe["seed"] * 10000 + recipe["attempt"] - 1 + 12345
    rng = np.random.default_rng(training_seed)
    x = _inputs(rows)
    y = np.asarray([row["label"] for row in rows])
    w, a, b = _arrays(model)
    before = metrics(model, rows)
    baseline, reward_sum, reward_count = 0.0, 0.0, 0
    batch_hash = hashlib.sha256()
    for _ in range(steps):
        ids = rng.choice(len(rows), size=batch_size, p=distribution)
        batch_hash.update(ids.astype("<i8").tobytes())
        prob = _predict(w, a, b, x[ids])
        delta = prob.copy()
        if method == "rl":
            actions = (rng.random(len(ids))[:, None] > prob.cumsum(1)).sum(1)
            rewards = np.asarray([float(reward_fn(rows[index], int(action))) for index, action in zip(ids, actions)])
            if not np.isfinite(rewards).all():
                raise ValueError("environment reward must be finite")
            delta[np.arange(len(ids)), actions] -= 1
            delta *= (rewards - baseline)[:, None]
            baseline = .9 * baseline + .1 * rewards.mean()
            reward_sum += float(rewards.sum())
            reward_count += len(ids)
        else:
            delta[np.arange(len(ids)), y[ids]] -= 1
        grad = x[ids].T @ delta / len(ids)
        if method == "lora":
            grad_a, grad_b = grad @ b.T, a.T @ grad
            a -= lr * grad_a
            b -= lr * grad_b
        else:
            w -= lr * grad
    if not all(np.isfinite(matrix).all() for matrix in (w, a, b)):
        raise ValueError("training produced non-finite parameters")
    model.update(weights=w.tolist(), lora_a=a.tolist(), lora_b=b.tolist())
    model["metadata"]["training_steps"] += steps
    model["metadata"]["last_method"] = method
    model["metadata"]["last_attempt"] = recipe["attempt"]
    validate_model(model)
    after = metrics(model, rows)
    return {"method": method, "steps": steps, "batch_size": batch_size,
            "examples_seen": steps * batch_size, "train_examples": len(rows),
            "loss_before": before["loss"], "loss_after": after["loss"],
            "accuracy_before": before["accuracy"], "accuracy_after": after["accuracy"],
            "sampled_actions": reward_count,
            "sampled_reward_mean": reward_sum / reward_count if reward_count else None,
            "training_rng_seed": training_seed, "attempt": recipe["attempt"],
            "policy": recipe["policy"], "training_scoring_examples": 2 * len(rows),
            "sampling_sha256": sampling_fingerprint(rows, distribution),
            "sampled_batch_sha256": batch_hash.hexdigest()}
