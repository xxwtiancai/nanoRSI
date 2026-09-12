"""Tiny CPU softmax policy: teaching mechanics, not LLM fine-tuning or solved RSI.

SFT minimizes cross entropy. RL uses sampled actions and scalar rewards with an
EMA reward baseline. LoRA minimizes cross entropy through W + B A, keeping W
frozen. Everything is ordinary Python so the actual gradients are inspectable.
"""
from __future__ import annotations

import json
import math
import random


def initial_model(seed=0):
    rng = random.Random(seed)
    return {
        "schema_version": 1,
        "kind": "tiny-softmax-teaching-demo",
        "input_dim": 4,
        "classes": 3,
        "rank": 2,
        "weights": [[rng.gauss(0, 0.04) for _ in range(5)] for _ in range(3)],
        "lora_a": [[rng.gauss(0, 0.15) for _ in range(5)] for _ in range(2)],
        "lora_b": [[0.0] * 2 for _ in range(3)],
        "metadata": {"initialization_seed": seed, "training_steps": 0},
    }


def validate_model(model):
    if model.get("schema_version") != 1 or model.get("kind") != "tiny-softmax-teaching-demo":
        raise ValueError("unsupported checkpoint schema or model kind")
    if (model.get("input_dim"), model.get("classes"), model.get("rank")) != (4, 3, 2):
        raise ValueError("teaching checkpoint requires 4 inputs, 3 classes, rank 2")
    for name, rows, columns in (("weights", 3, 5), ("lora_a", 2, 5), ("lora_b", 3, 2)):
        matrix = model.get(name)
        if not isinstance(matrix, list) or len(matrix) != rows:
            raise ValueError(f"invalid {name} shape")
        for row in matrix:
            if not isinstance(row, list) or len(row) != columns:
                raise ValueError(f"invalid {name} shape")
            if any(type(x) not in (int, float) or not math.isfinite(x) for x in row):
                raise ValueError(f"non-finite {name}")
    return model


def example(task):
    features = json.loads(task["input_files"]["features.json"])
    label = int(task["expected_files"]["label.txt"].strip())
    if not isinstance(features, list) or len(features) != 4:
        raise ValueError("examples require four features")
    if any(type(x) not in (int, float) or not math.isfinite(x) for x in features):
        raise ValueError("features must be finite numbers")
    if label not in (0, 1, 2):
        raise ValueError("label must be class 0, 1, or 2")
    return {"task_id": task["task_id"], "features": features, "label": label}


def training_examples(payload):
    if payload.get("schema_version") != 1 or not payload.get("tasks"):
        raise ValueError("nonempty schema-version 1 training data required")
    if any(task.get("split") != "train" for task in payload["tasks"]):
        raise ValueError("trainer accepts train rows only")
    rows = [example(task) for task in payload["tasks"]]
    if len({row["task_id"] for row in rows}) != len(rows):
        raise ValueError("training task identities must be unique")
    return rows


def probabilities(model, features):
    x = [*features, 1.0]
    hidden = [sum(a * b for a, b in zip(row, x)) for row in model["lora_a"]]
    logits = [sum(w * value for w, value in zip(row, x)) +
              sum(b * value for b, value in zip(model["lora_b"][k], hidden))
              for k, row in enumerate(model["weights"])]
    peak = max(logits)
    exponentials = [math.exp(value - peak) for value in logits]
    total = sum(exponentials)
    return [value / total for value in exponentials]


def metrics(model, rows):
    correct, losses = 0, []
    for row in rows:
        probs = probabilities(model, row["features"])
        correct += max(range(len(probs)), key=probs.__getitem__) == row["label"]
        losses.append(-math.log(max(probs[row["label"]], 1e-15)))
    if not losses:
        raise ValueError("cannot evaluate an empty panel")
    return {"accuracy": correct / len(rows), "loss": sum(losses) / len(losses)}


def classification_reward(row, action):
    """The environment reveals only whether the sampled class was correct."""
    return float(action == row["label"])


def train(model, rows, recipe, *, reward_fn=classification_reward):
    validate_model(model)
    method, steps = recipe["method"], recipe["steps"]
    lr, batch_size = recipe["lr"], recipe.get("batch_size", 24)
    if method not in ("sft", "rl", "lora"):
        raise ValueError("method must be sft, rl, or lora")
    if type(steps) is not int or not 1 <= steps <= 10000:
        raise ValueError("steps must be between 1 and 10000")
    if type(batch_size) is not int or not 1 <= batch_size <= 256:
        raise ValueError("batch_size must be between 1 and 256")
    if type(lr) not in (int, float) or not math.isfinite(lr) or not 0 < lr <= 1:
        raise ValueError("lr must be finite and in (0, 1]")
    if not rows:
        raise ValueError("training examples are required")
    focus = set(recipe.get("focus_task_ids", []))
    unknown = focus - {row["task_id"] for row in rows}
    if unknown:
        raise ValueError("focus_task_ids must identify available train rows")
    sampling_weights = [3.0 if row["task_id"] in focus else 1.0 for row in rows]
    rng = random.Random(recipe.get("seed", 0) + model["metadata"].get("training_steps", 0))
    before = metrics(model, rows)
    baseline = 0.0
    reward_sum, reward_count = 0.0, 0
    for _ in range(steps):
        batch = rng.choices(rows, weights=sampling_weights, k=batch_size)
        grad_w = [[0.0] * 5 for _ in range(3)]
        grad_a = [[0.0] * 5 for _ in range(2)]
        grad_b = [[0.0] * 2 for _ in range(3)]
        batch_rewards = []
        for row in batch:
            x = [*row["features"], 1.0]
            probs = probabilities(model, row["features"])
            if method == "rl":
                action = rng.choices(range(3), weights=probs)[0]
                reward = float(reward_fn(row, action))
                if not math.isfinite(reward):
                    raise ValueError("environment reward must be finite")
                # REINFORCE: -advantage * grad(log pi(sampled action)).
                # Baseline uses preceding batches, independent of this action.
                delta = [(reward - baseline) * (p - float(k == action)) for k, p in enumerate(probs)]
                batch_rewards.append(reward)
            else:
                # Cross-entropy gradient; LoRA changes its parameterization below.
                delta = [p - float(k == row["label"]) for k, p in enumerate(probs)]
            if method == "lora":
                hidden = [sum(a * value for a, value in zip(a_row, x)) for a_row in model["lora_a"]]
                for k in range(3):
                    for r in range(2):
                        grad_b[k][r] += delta[k] * hidden[r]
                for r in range(2):
                    back = sum(model["lora_b"][k][r] * delta[k] for k in range(3))
                    for j in range(5):
                        grad_a[r][j] += back * x[j]
            else:
                for k in range(3):
                    for j in range(5):
                        grad_w[k][j] += delta[k] * x[j]
        if method == "lora":
            for name, gradient in (("lora_a", grad_a), ("lora_b", grad_b)):
                for r, grad_row in enumerate(gradient):
                    for c, value in enumerate(grad_row):
                        model[name][r][c] -= lr * value / batch_size
        else:
            for k in range(3):
                for j in range(5):
                    model["weights"][k][j] -= lr * grad_w[k][j] / batch_size
        if batch_rewards:
            mean_reward = sum(batch_rewards) / batch_size
            baseline = 0.9 * baseline + 0.1 * mean_reward
            reward_sum += sum(batch_rewards)
            reward_count += batch_size
    validate_model(model)
    model["metadata"]["training_steps"] = model["metadata"].get("training_steps", 0) + steps
    model["metadata"]["last_method"] = method
    after = metrics(model, rows)
    return {"method": method, "steps": steps, "batch_size": batch_size,
            "examples_seen": steps * batch_size, "train_examples": len(rows),
            "loss_before": before["loss"], "loss_after": after["loss"],
            "accuracy_before": before["accuracy"], "accuracy_after": after["accuracy"],
            "sampled_actions": reward_count,
            "sampled_reward_mean": reward_sum / reward_count if reward_count else None}
