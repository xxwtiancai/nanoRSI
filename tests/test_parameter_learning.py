"""Real gradients, checkpoint identity, and split isolation for the CPU teaching demo."""
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


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "src/nanorsi/templates/learner"


def load(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ParameterLearningTests(unittest.TestCase):
    def modules(self):
        self.assertTrue((TEMPLATE / "trainer/network.py").is_file(), "CPU learner is missing")
        self.assertTrue((ROOT / "examples/parameter_learning/prepare.py").is_file(), "Generator is missing")
        return load(TEMPLATE / "trainer/network.py"), load(ROOT / "examples/parameter_learning/prepare.py")

    def test_generated_data_are_deterministic_and_disjoint(self):
        network, generator = self.modules()
        manifest = generator.build_manifest(seed=3)
        self.assertEqual(manifest, generator.build_manifest(seed=3))
        self.assertNotEqual(manifest, generator.build_manifest(seed=4))
        tasks = manifest["tasks"]
        self.assertEqual(len({t["task_id"] for t in tasks}), len(tasks))
        self.assertEqual(len({t["group_id"] for t in tasks}), len(tasks))
        self.assertEqual(len({t["input_files"]["features.json"] for t in tasks}), len(tasks))
        self.assertEqual({t["split"] for t in tasks}, {"train", "validation", "test"})
        self.assertEqual(len(network.training_examples({"schema_version": 1, "tasks": [t for t in tasks if t["split"] == "train"]})), 120)
        with self.assertRaisesRegex(ValueError, "train"):
            network.training_examples(manifest)

    def test_three_methods_learn_from_examples_and_reload(self):
        network, generator = self.modules()
        tasks = generator.build_manifest(seed=2)["tasks"]
        train = [network.example(t) for t in tasks if t["split"] == "train"]
        heldout = [network.example(t) for t in tasks if t["split"] == "test"]
        for method in ("sft", "rl", "lora"):
            with self.subTest(method=method):
                model = network.initial_model(seed=2)
                original = copy.deepcopy(model)
                before = network.metrics(model, heldout)
                stats = network.train(model, train, {"method": method, "seed": 2, "steps": 200, "lr": 0.12, "batch_size": 24})
                restored = json.loads(json.dumps(model))
                after = network.metrics(restored, heldout)
                self.assertEqual(network.metrics(model, heldout), after)
                self.assertGreater(after["accuracy"], before["accuracy"] + 0.15)
                self.assertLess(after["loss"], before["loss"])
                self.assertEqual(stats["steps"], 200)
                if method == "lora":
                    self.assertEqual(model["weights"], original["weights"])
                    self.assertNotEqual(model["lora_a"], original["lora_a"])
                    self.assertNotEqual(model["lora_b"], original["lora_b"])
                    self.assertLess(model["rank"], min(model["input_dim"] + 1, model["classes"]))
                else:
                    self.assertNotEqual(model["weights"], original["weights"])

    def test_policy_gradient_uses_sampled_environment_rewards(self):
        network, _ = self.modules()
        model = network.initial_model(seed=8)
        original = copy.deepcopy(model)
        rows = [{"task_id": "train-1", "features": [1.0, 0.0, 0.0, 0.0], "label": 0}]
        recipe = {"method": "rl", "seed": 8, "steps": 50, "lr": 0.1, "batch_size": 12}
        calls = []

        def no_reward(row, action):
            calls.append(action)
            return 0.0

        network.train(model, rows, recipe, reward_fn=no_reward)
        self.assertEqual(model["weights"], original["weights"])
        self.assertGreater(len(set(calls)), 1, "RL must sample multiple actions")
        trained = copy.deepcopy(original)
        network.train(trained, rows, recipe, reward_fn=lambda row, action: float(action == 2))
        self.assertGreater(network.probabilities(trained, rows[0]["features"])[2], network.probabilities(original, rows[0]["features"])[2])

    def test_training_command_attests_parent_checkpoint_and_train_only_data(self):
        network, generator = self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace"
            shutil.copytree(TEMPLATE, root)
            model_path = root / "target/model.json"
            initial = model_path.read_bytes()
            data_path = Path(tmp) / "train.json"
            rows = [t for t in generator.build_manifest()["tasks"] if t["split"] == "train"]
            data_path.write_text(json.dumps({"schema_version": 1, "tasks": rows}))
            result_path = Path(tmp) / "training-result.json"
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "NANORSI_TRAINING_DATA_PATH": str(data_path), "NANORSI_CHECKPOINT_PATH": str(model_path), "NANORSI_TRAINING_RESULT_PATH": str(result_path)}
            completed = subprocess.run([sys.executable, "trainer/train.py"], cwd=root, env=env, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(result_path.read_text())
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["initial_checkpoint_sha256"], hashlib.sha256(initial).hexdigest())
            self.assertEqual(result["checkpoint_sha256"], hashlib.sha256(model_path.read_bytes()).hexdigest())
            self.assertEqual(result["data_sha256"], hashlib.sha256(data_path.read_bytes()).hexdigest())
            self.assertNotEqual(initial, model_path.read_bytes())
            self.assertEqual(result["task_ids"], [r["task_id"] for r in rows])
            # A second round starts from the actual saved checkpoint.
            previous_hash = result["checkpoint_sha256"]
            completed = subprocess.run([sys.executable, "trainer/train.py"], cwd=root, env=env, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(result_path.read_text())["initial_checkpoint_sha256"], previous_hash)
            data_path.write_text(json.dumps(generator.build_manifest()))
            result_path.unlink()
            before = model_path.read_bytes()
            bad = subprocess.run([sys.executable, "trainer/train.py"], cwd=root, env=env, text=True, capture_output=True)
            self.assertNotEqual(bad.returncode, 0)
            self.assertEqual(before, model_path.read_bytes())
            self.assertFalse(result_path.exists())

    def test_evaluator_has_real_loss_and_train_only_feedback(self):
        network, _ = self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "workspace"
            shutil.copytree(TEMPLATE, root)
            result_path = Path(tmp) / "result.json"
            for split in ("train", "validation", "test"):
                env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "NANORSI_SPLIT": split, "NANORSI_TASK_MANIFEST": str(root / "tasks/manifest.json"), "NANORSI_RESULT_PATH": str(result_path), "NANORSI_REPEAT_ID": "2", "NANORSI_TRAIN_LIMIT": "4", "NANORSI_SEED": "0"}
                completed = subprocess.run([sys.executable, "evaluator/evaluate.py"], cwd=root, env=env, text=True, capture_output=True)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                result = json.loads(result_path.read_text())
                self.assertEqual(result["status"], "ok", result)
                self.assertGreater(result["metrics"]["loss"], 0)
                self.assertEqual(result["usage"]["model_calls"], 0)
                self.assertIsNone(result["cost_usd"])
                self.assertEqual(len(result["case_results"]), 4 if split == "train" else 120)
                for case in result["case_results"]:
                    self.assertEqual(case["repeat_id"], 2)
                    self.assertIn(case["score"], (0.0, 1.0))
                    self.assertEqual("feedback" in case, split == "train")
                    self.assertEqual("task" in case, split == "train")

    def test_proposer_loads_selected_harness_checkpoint(self):
        network, generator = self.modules()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "candidate"
            harness = Path(tmp) / "harness"
            shutil.copytree(TEMPLATE, root)
            shutil.copytree(TEMPLATE, harness)
            rows = [t for t in generator.build_manifest()["tasks"] if t["split"] == "train"][:8]
            context_path = Path(tmp) / "context.json"
            context_path.write_text(json.dumps({"attempt_id": 1, "train_results": [{"task": {"task_id": t["task_id"], "input_files": t["input_files"]}, "feedback": {"expected_files": t["expected_files"]}} for t in rows]}))
            out = Path(tmp) / "proposal"
            env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "NANORSI_CONTEXT_PATH": str(context_path), "NANORSI_PROPOSER_HARNESS": str(harness), "NANORSI_PROPOSAL_DIR": str(out)}
            original = (root / "target/recipe.json").read_bytes()
            completed = subprocess.run([sys.executable, "proposer/propose.py"], cwd=root, env=env, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            first = json.loads((out / "trace.json").read_text())[0]
            model = network.initial_model(seed=41)
            (harness / "target/model.json").write_text(json.dumps(model))
            completed = subprocess.run([sys.executable, "proposer/propose.py"], cwd=root, env=env, text=True, capture_output=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            second = json.loads((out / "trace.json").read_text())[0]
            self.assertNotEqual(first["checkpoint_sha256"], second["checkpoint_sha256"])
            self.assertNotEqual(first["example_losses"], second["example_losses"])
            self.assertEqual(original, (root / "target/recipe.json").read_bytes())
            self.assertIn("target/recipe.json", (out / "proposal.diff").read_text())

    def test_run_summary_preserves_regressions_and_failed_runs(self):
        runner_path = ROOT / "examples/parameter_learning/run.py"
        self.assertTrue(runner_path.is_file(), "CLI experiment runner is missing")
        runner = load(runner_path)
        rows = [
            {"method": "sft", "arm": "self-use", "seed": 0, "status": "completed", "baseline_accuracy": 0.5, "candidate_accuracy": 0.4, "baseline_loss": 1.0, "candidate_loss": 1.1},
            {"method": "sft", "arm": "self-use", "seed": 1, "status": "failed", "error": "trainer failed"},
        ]
        summary = runner.summarize(rows)
        self.assertEqual(summary["runs"], rows)
        group = summary["groups"][0]
        self.assertEqual(group["failed_runs"], 1)
        self.assertEqual(group["accuracy_regressions"], 1)
        self.assertLess(group["mean_accuracy_delta"], 0)

    def test_ordinary_cli_runs_one_real_training_trial(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "runs"
            env = {**os.environ, "PATH": str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]}
            completed = subprocess.run([sys.executable, str(ROOT / "examples/parameter_learning/run.py"), str(output), "--methods", "sft", "--seeds", "0", "--arms", "self-use", "--rounds", "1"], env=env, capture_output=True, text=True, timeout=60)
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            row = json.loads((output / "summary.json").read_text())["runs"][0]
            self.assertEqual(row["training_rounds"], 1)
            self.assertGreater(row["candidate_accuracy"], row["baseline_accuracy"])
            self.assertNotEqual(row["candidate_checkpoint"]["sha256"], row["baseline_checkpoint"]["sha256"])


if __name__ == "__main__":
    unittest.main()
