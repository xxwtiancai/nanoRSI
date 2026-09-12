"""Synthetic-only checks for the optional recursive numerical experiment."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

try:
    import numpy as np
except ImportError:
    np = None


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "examples/recursive_learning/runtime"


def synthetic_rows(count=80):
    rows = []
    for index in range(count):
        label = index % 10
        features = [0.0] * 64
        features[label] = 16.0
        features[10 + label] = 8.0
        rows.append({"task_id": f"train-{index:04d}", "features": features, "label": label})
    return rows


def task(row, split="train"):
    return {"task_id": row["task_id"], "split": split,
            "input_files": {"features.json": json.dumps(row["features"])},
            "expected_files": {"label.txt": str(row["label"])}}


def recipe(**changes):
    result = {"method": "sft", "seed": 2, "steps": 8, "lr": 0.3,
              "batch_size": 32, "multiplier": 3, "balanced": False,
              "policy": "uniform", "attempt": 1, "focus_task_ids": []}
    result.update(changes)
    return result


@unittest.skipIf(np is None, "optional recursive numerical experiment requires NumPy")
class RecursiveRuntimeTests(unittest.TestCase):
    def network(self):
        path = RUNTIME / "network.py"
        self.assertTrue(path.is_file(), "recursive numerical backend is missing")
        spec = importlib.util.spec_from_file_location("recursive_network", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_initialization_matches_pilot_and_roundtrips_json(self):
        network = self.network()
        model = network.initial_model(2)
        rng = np.random.default_rng(2)
        self.assertEqual(model["kind"], "recursive-digits-softmax")
        np.testing.assert_array_equal(model["weights"], rng.normal(0, .01, (65, 10)))
        np.testing.assert_array_equal(model["lora_a"], rng.normal(0, .1, (65, 4)))
        np.testing.assert_array_equal(model["lora_b"], np.zeros((4, 10)))
        self.assertEqual(network.validate_model(json.loads(json.dumps(model))), model)
        self.assertEqual(model["metadata"]["training_steps"], 0)
        values = network.probabilities(model, synthetic_rows(1)[0]["features"])
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), 10)
        self.assertAlmostEqual(sum(values), 1)

    def test_sft_gradient_matches_finite_difference_with_normalization_and_bias(self):
        network = self.network()
        rows = synthetic_rows(1)
        model = network.initial_model(2)
        trained = copy.deepcopy(model)
        lr = 1e-3
        network.train(trained, rows, recipe(steps=1, lr=lr))
        for feature, label in ((0, 0), (0, 3), (10, 0), (64, 0), (64, 7), (60, 2)):
            epsilon = 1e-5
            plus, minus = copy.deepcopy(model), copy.deepcopy(model)
            plus["weights"][feature][label] += epsilon
            minus["weights"][feature][label] -= epsilon
            numerical = (network.metrics(plus, rows)["loss"] - network.metrics(minus, rows)["loss"]) / (2 * epsilon)
            actual = (model["weights"][feature][label] - trained["weights"][feature][label]) / lr
            self.assertAlmostEqual(actual, numerical, places=8)

    def test_real_learning_and_lora_frozen_base(self):
        network = self.network()
        rows = synthetic_rows()
        for method in ("sft", "rl", "lora"):
            with self.subTest(method=method):
                model = network.initial_model(2)
                original = copy.deepcopy(model)
                before = network.metrics(model, rows)
                stats = network.train(model, rows, recipe(method=method, steps=200))
                after = network.metrics(model, rows)
                self.assertLess(after["loss"], before["loss"])
                self.assertGreater(after["accuracy"], before["accuracy"] + .5)
                self.assertEqual(stats["steps"], 200)
                self.assertEqual(stats["examples_seen"], 6400)
                self.assertEqual(model["metadata"]["training_steps"], 200)
                if method == "lora":
                    self.assertEqual(model["weights"], original["weights"])
                    self.assertNotEqual(model["lora_a"], original["lora_a"])
                    self.assertNotEqual(model["lora_b"], original["lora_b"])
                else:
                    self.assertNotEqual(model["weights"], original["weights"])

    def test_rl_samples_actions_and_zero_rewards_leave_parameters_unchanged(self):
        network = self.network()
        model = network.initial_model(2)
        original = copy.deepcopy(model)
        actions = []

        def reward(row, action):
            actions.append(action)
            return 0.0

        stats = network.train(model, synthetic_rows(), recipe(method="rl"), reward_fn=reward)
        self.assertEqual(model["weights"], original["weights"])
        self.assertEqual(model["lora_a"], original["lora_a"])
        self.assertEqual(model["lora_b"], original["lora_b"])
        self.assertGreater(len(set(actions)), 1)
        self.assertEqual(stats["sampled_actions"], 256)
        self.assertEqual(stats["sampled_reward_mean"], 0)
        with self.assertRaisesRegex(ValueError, "reward"):
            network.train(model, synthetic_rows(), recipe(method="rl"), reward_fn=lambda row, action: float("nan"))

    def test_rejected_attempts_use_distinct_reproducible_sampling(self):
        network = self.network()
        first, second, repeat = [network.initial_model(2) for _ in range(3)]
        stats1 = network.train(first, synthetic_rows(), recipe(attempt=1))
        stats2 = network.train(second, synthetic_rows(), recipe(attempt=2))
        network.train(repeat, synthetic_rows(), recipe(attempt=2))
        self.assertNotEqual(first["weights"], second["weights"])
        self.assertEqual(second, repeat)
        self.assertEqual(stats1["training_rng_seed"], 32345)
        self.assertEqual(stats2["training_rng_seed"], 32346)
        self.assertNotEqual(stats1["sampled_batch_sha256"], stats2["sampled_batch_sha256"])

    def test_training_rejects_nontrain_duplicate_and_invalid_examples(self):
        network = self.network()
        rows = synthetic_rows(2)
        payload = {"schema_version": 1, "tasks": [task(row) for row in rows]}
        self.assertEqual(network.training_examples(payload), rows)
        for split in ("validation", "test", None):
            with self.assertRaisesRegex(ValueError, "train"):
                network.training_examples({"schema_version": 1, "tasks": [task(rows[0], split)]})
        with self.assertRaisesRegex(ValueError, "unique"):
            network.training_examples({"schema_version": 1, "tasks": [task(rows[0])] * 2})
        invalid = {**rows[0], "task_id": "test-0000"}
        with self.assertRaisesRegex(ValueError, "train"):
            network.train(network.initial_model(2), [invalid], recipe())
        for features in ([0] * 63, [17] * 64, [-1] * 64, [True] * 64, [float("nan")] * 64):
            with self.assertRaises(ValueError):
                network.example(task({**rows[0], "features": features}))
        with self.assertRaises(ValueError):
            network.example(task({**rows[0], "label": 10}))

    def test_invalid_models_and_recipe_matrix_overrides_are_rejected(self):
        network = self.network()
        for field, value in (("weights", [[0]]), ("lora_a", []), ("rank", 3), ("kind", "other")):
            invalid = network.initial_model(2)
            invalid[field] = value
            with self.assertRaises(ValueError):
                network.validate_model(invalid)
        for change in ({"weights": 4}, {"steps": True}, {"lr": float("nan")},
                       {"balanced": "yes"}, {"policy": "test"}, {"multiplier": 4},
                       {"focus_task_ids": ["test-0"]}, {"attempt": -1}):
            with self.assertRaises(ValueError):
                network.train(network.initial_model(2), synthetic_rows(), recipe(**change))

    def test_balanced_sampling_preserves_empirical_class_mass(self):
        network = self.network()
        rows = synthetic_rows(83)
        losses = list(range(len(rows)))
        for policy in ("prioritized", "random", "uniform"):
            config = recipe(policy=policy, balanced=True, multiplier=9)
            config["focus_task_ids"] = network.select_focus(rows, losses, config)
            q = np.asarray(network.sampling_distribution(rows, config))
            labels = np.asarray([row["label"] for row in rows])
            self.assertAlmostEqual(q.sum(), 1)
            for label in range(10):
                members = labels == label
                self.assertAlmostEqual(q[members].sum(), members.mean())
                if policy != "uniform":
                    self.assertAlmostEqual(q[members].max() / q[members].min(), 9)
            if policy == "uniform":
                np.testing.assert_allclose(q, 1 / len(rows))

    def test_tied_losses_keep_panel_order(self):
        network = self.network()
        rows = list(reversed(synthetic_rows(12)))
        focus = network.select_focus(rows, [1.0] * len(rows), recipe(policy="prioritized"))
        self.assertEqual(focus, [row["task_id"] for row in rows[:3]])

    def test_unmodified_trainer_attests_real_checkpoint_and_rejects_test_data(self):
        network = self.network()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for folder in (root / "trainer", root / "target"):
                folder.mkdir()
            source = ROOT / "src/nanorsi/templates/learner/trainer/train.py"
            shutil.copyfile(source, root / "trainer/train.py")
            shutil.copyfile(RUNTIME / "network.py", root / "trainer/network.py")
            model_path, data_path, result_path = [root / name for name in ("target/model.json", "train.json", "result.json")]
            model_path.write_text(json.dumps(network.initial_model(2)))
            (root / "target/recipe.json").write_text(json.dumps(recipe()))
            payload = {"schema_version": 1, "tasks": [task(row) for row in synthetic_rows()]}
            data_path.write_text(json.dumps(payload))
            original = model_path.read_bytes()
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "NANORSI_CHECKPOINT_PATH": str(model_path),
                   "NANORSI_TRAINING_DATA_PATH": str(data_path), "NANORSI_TRAINING_RESULT_PATH": str(result_path)}
            completed = subprocess.run([sys.executable, "trainer/train.py"], cwd=root, env=env,
                                       capture_output=True, text=True, timeout=30)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            stats = json.loads(result_path.read_text())
            self.assertEqual(stats["initial_checkpoint_sha256"], hashlib.sha256(original).hexdigest())
            self.assertEqual(stats["checkpoint_sha256"], hashlib.sha256(model_path.read_bytes()).hexdigest())
            self.assertEqual(stats["data_sha256"], hashlib.sha256(data_path.read_bytes()).hexdigest())
            self.assertEqual(stats["task_ids"], [row["task_id"] for row in payload["tasks"]])
            self.assertEqual(stats["examples_seen"], 256)
            self.assertEqual(stats["training_scoring_examples"], 160)
            self.assertNotEqual(original, model_path.read_bytes())
            self.assertEqual(source.read_bytes(), (root / "trainer/train.py").read_bytes())
            payload["tasks"][0]["split"] = "test"
            data_path.write_text(json.dumps(payload))
            result_path.unlink()
            previous = model_path.read_bytes()
            rejected = subprocess.run([sys.executable, "trainer/train.py"], cwd=root, env=env,
                                      capture_output=True, text=True, timeout=30)
            self.assertNotEqual(rejected.returncode, 0)
            self.assertEqual(previous, model_path.read_bytes())
            self.assertFalse(result_path.exists())

    def test_numerical_updates_match_validation_pilot_on_synthetic_rows(self):
        network = self.network()
        rows = synthetic_rows(83)
        x = np.column_stack([np.asarray([row["features"] for row in rows]) / 16, np.ones(len(rows))])
        y = np.asarray([row["label"] for row in rows])

        def predict(w, a, b, batch):
            logits = batch @ (w + a @ b)
            logits -= logits.max(1, keepdims=True)
            p = np.exp(logits)
            return p / p.sum(1, keepdims=True)

        for method in ("sft", "rl", "lora"):
            for balanced in (False, True):
                for policy in ("uniform", "prioritized", "random"):
                    with self.subTest(method=method, balanced=balanced, policy=policy):
                        model = network.initial_model(2)
                        w, a, b = [np.asarray(model[key]) for key in ("weights", "lora_a", "lora_b")]
                        config = recipe(method=method, balanced=balanced, policy=policy, attempt=3, multiplier=9)
                        p = predict(w, a, b, x)
                        loss = -np.log(np.maximum(p[np.arange(len(y)), y], 1e-15))
                        order = np.argsort(-loss, kind="stable")
                        if policy == "random":
                            order = np.random.default_rng(2 * 10000 + 2 + 900000).permutation(len(y))
                        weights = np.ones(len(y))
                        focus = []
                        if balanced:
                            for cls in range(10):
                                members = order[y[order] == cls]
                                chosen = members[:max(1, len(members) // 4)]
                                focus.extend(chosen)
                                weights[chosen] = 9
                                weights[members] *= len(members) / weights[members].sum()
                        else:
                            focus = order[:len(y) // 4].tolist()
                            weights[focus] = 9
                        if policy == "uniform":
                            weights[:] = 1
                            focus = []
                        config["focus_task_ids"] = network.select_focus(rows, loss.tolist(), config)
                        self.assertEqual(config["focus_task_ids"], [rows[i]["task_id"] for i in focus])
                        q = weights / weights.sum()
                        np.testing.assert_allclose(network.sampling_distribution(rows, config), q, rtol=1e-15)
                        rng = np.random.default_rng(2 * 10000 + 2 + 12345)
                        baseline = 0.
                        for _ in range(config["steps"]):
                            ids = rng.choice(len(y), size=32, p=q)
                            prob = predict(w, a, b, x[ids])
                            delta = prob.copy()
                            if method == "rl":
                                action = (rng.random(len(ids))[:, None] > prob.cumsum(1)).sum(1)
                                reward = (action == y[ids]).astype(float)
                                delta[np.arange(len(ids)), action] -= 1
                                delta *= (reward - baseline)[:, None]
                                baseline = .9 * baseline + .1 * reward.mean()
                            else:
                                delta[np.arange(len(ids)), y[ids]] -= 1
                            grad = x[ids].T @ delta / len(ids)
                            if method == "lora":
                                ga, gb = grad @ b.T, a.T @ grad
                                a -= .3 * ga
                                b -= .3 * gb
                            else:
                                w -= .3 * grad
                        network.train(model, rows, config)
                        for key, expected in (("weights", w), ("lora_a", a), ("lora_b", b)):
                            np.testing.assert_allclose(model[key], expected, rtol=1e-13, atol=1e-15)

    def run_proposer(self, root, harness, context, output):
        path = output.parent / "context.json"
        path.write_text(json.dumps(context))
        env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1",
               "NANORSI_CONTEXT_PATH": str(path), "NANORSI_PROPOSER_HARNESS": str(harness),
               "NANORSI_PROPOSAL_DIR": str(output)}
        return subprocess.run([sys.executable, str(root / "proposer/propose.py")],
                              cwd=root, env=env, capture_output=True, text=True, timeout=30)

    def test_proposer_scores_full_panel_using_selected_checkpoint_for_every_policy(self):
        network = self.network()
        with tempfile.TemporaryDirectory() as tmp:
            root, harness, output = [Path(tmp) / name for name in ("candidate", "harness", "proposal")]
            for folder in (root / "target", root / "trainer", root / "proposer", harness / "target"):
                folder.mkdir(parents=True)
            shutil.copyfile(RUNTIME / "network.py", root / "trainer/network.py")
            self.assertTrue((RUNTIME / "propose.py").is_file(), "recursive proposer is missing")
            shutil.copyfile(RUNTIME / "propose.py", root / "proposer/propose.py")
            rows = synthetic_rows(83)
            context = {"attempt_id": 3, "train_results": [
                {"task": {"task_id": row["task_id"], "input_files": task(row)["input_files"]},
                 "feedback": {"expected_files": task(row)["expected_files"]}} for row in rows]}
            checkpoint = json.dumps(network.initial_model(2)).encode()
            (harness / "target/model.json").write_bytes(checkpoint)
            # The candidate checkpoint deliberately differs from selected harness.
            (root / "target/model.json").write_text(json.dumps(network.initial_model(99)))
            for policy in ("prioritized", "uniform", "random"):
                config = recipe(policy=policy, balanced=True, attempt=0)
                original = json.dumps(config, sort_keys=True, indent=2) + "\n"
                (root / "target/recipe.json").write_text(original)
                result = self.run_proposer(root, harness, context, output)
                self.assertEqual(result.returncode, 0, result.stderr)
                trace = json.loads((output / "trace.json").read_text())[0]
                self.assertEqual(trace["checkpoint_sha256"], hashlib.sha256(checkpoint).hexdigest())
                self.assertEqual(trace["scored_examples"], 83)
                self.assertEqual(len(trace["example_losses"]), 83)
                self.assertEqual(trace["policy"], policy)
                self.assertEqual(trace["attempt"], 3)
                expected = -np.log(network.probabilities(network.initial_model(2), rows[0]["features"])[0])
                self.assertAlmostEqual(trace["example_losses"][0]["loss"], expected)
                self.assertEqual(len(trace["sampling_sha256"]), 64)
                self.assertEqual((root / "target/recipe.json").read_text(), original)
                patch = (output / "proposal.diff").read_text()
                self.assertIn('"attempt": 3', patch)
                self.assertIn("target/recipe.json", patch)
                self.assertEqual(json.loads((output / "usage.json").read_text())["model_calls"], 0)
                self.assertTrue((output / "hypothesis.json").is_file())
                applied = subprocess.run(["git", "apply", str(output / "proposal.diff")], cwd=root,
                                         capture_output=True, text=True, timeout=10)
                self.assertEqual(applied.returncode, 0, applied.stderr)
                proposed = json.loads((root / "target/recipe.json").read_text())
                self.assertEqual(proposed["attempt"], 3)
                self.assertEqual(proposed["focus_task_ids"], trace["focus_task_ids"])
                q = network.sampling_distribution(rows, proposed)
                self.assertEqual(network.sampling_fingerprint(rows, q), trace["sampling_sha256"])
            changed = network.initial_model(2)
            network.train(changed, rows, recipe())
            (harness / "target/model.json").write_text(json.dumps(changed))
            result = self.run_proposer(root, harness, context, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            updated = json.loads((output / "trace.json").read_text())[0]
            self.assertNotEqual(trace["checkpoint_sha256"], updated["checkpoint_sha256"])
            self.assertNotEqual(trace["example_losses"], updated["example_losses"])
            for invalid_case in (
                {"task": {**context["train_results"][0]["task"], "task_id": "test-0"}, "feedback": context["train_results"][0]["feedback"]},
                {**context["train_results"][0], "split": "validation"},
                {**context["train_results"][0], "task_id": "test-0"},
                {"task": {**context["train_results"][0]["task"], "split": "test"}, "feedback": context["train_results"][0]["feedback"]},
            ):
                bad = self.run_proposer(root, harness, {"attempt_id": 4, "train_results": [invalid_case]}, output)
                self.assertNotEqual(bad.returncode, 0)
                self.assertIn("train", bad.stderr.lower())


if __name__ == "__main__":
    unittest.main()
