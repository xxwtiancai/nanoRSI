"""Contract and semantic checks for the authored coding starter pack."""
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "examples/coding_tasks/prepare.py"
MANIFEST = ROOT / "src/nanorsi/templates/coding/tasks/manifest.json"


def load_generator():
    spec = importlib.util.spec_from_file_location("coding_prepare", GENERATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_task(task, files):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for name, source in {**files, **task["grading"]["public_tests"],
                             **task["grading"]["private_tests"]}.items():
            (root / name).write_text(source, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".", "-v"],
            cwd=root, capture_output=True, text=True, timeout=task["grading"]["timeout_s"] + 1,
        )


class CodingTaskTests(unittest.TestCase):
    def test_pack_shape_and_disjoint_groups(self):
        manifest = load_generator().build_manifest()
        self.assertEqual(manifest["schema_version"], 1)
        tasks = manifest["tasks"]
        self.assertEqual(Counter(t["split"] for t in tasks),
                         {"train": 4, "validation": 4, "test": 4})
        self.assertEqual(len({t["task_id"] for t in tasks}), 12)
        self.assertEqual(len({t["group_id"] for t in tasks}), 12)
        for task in tasks:
            with self.subTest(task=task["task_id"]):
                self.assertEqual(set(task["input_files"]), {"solution.py"})
                self.assertEqual(set(task["expected_files"]), {"solution.py"})
                self.assertTrue(task["instruction"])
                self.assertEqual(task["grading"]["kind"], "python-unittest")
                self.assertEqual(task["grading"]["timeout_s"], 2)
                self.assertEqual(set(task["grading"]["public_tests"]), {"test_public.py"})
                self.assertEqual(set(task["grading"]["private_tests"]), {"test_private.py"})

    def test_generated_manifest_is_deterministic_and_current(self):
        generator = load_generator()
        self.assertEqual(generator.build_manifest(), generator.build_manifest())
        with tempfile.TemporaryDirectory() as tmp:
            first = generator.write_manifest(Path(tmp) / "first.json")
            second = generator.write_manifest(Path(tmp) / "second.json")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            self.assertEqual(first.read_bytes(), MANIFEST.read_bytes())

    def test_every_starter_fails_and_every_reference_passes(self):
        for task in load_generator().build_manifest()["tasks"]:
            with self.subTest(task=task["task_id"]):
                starter = run_task(task, task["input_files"])
                self.assertNotEqual(starter.returncode, 0, "Starter unexpectedly solved")
                self.assertIn("FAIL", starter.stderr, starter.stderr)
                reference = run_task(task, task["expected_files"])
                self.assertEqual(reference.returncode, 0, reference.stderr)

    def test_semantically_equal_alternative_is_accepted(self):
        task = load_generator().build_manifest()["tasks"][0]
        alternative = {"solution.py": "def unique(items):\n"
                       "    result = []\n"
                       "    for item in items:\n"
                       "        if not any(item == old for old in result):\n"
                       "            result.append(item)\n"
                       "    return result\n"}
        self.assertNotEqual(alternative, task["expected_files"])
        result = run_task(task, alternative)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_cli_validates_pack_without_writing_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "not-created.json"
            result = subprocess.run(
                [sys.executable, str(GENERATOR), str(output), "--check"],
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Starter passes: 0/12; reference passes: 12/12", result.stdout)
            self.assertIn("not model performance", result.stdout)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
