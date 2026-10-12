"""Offline checks for the HumanEval coding pack (benchmark track).

Covers pack determinism, split hygiene, the withheld-reference rule, the
grading-contract shape, and a stub-fails/canonical-passes sample of the
wrapped upstream tests. Live evidence lives in examples/results/.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACK = Path(__file__).resolve().parent.parent / "examples" / "humaneval_tasks"

_spec = importlib.util.spec_from_file_location("humaneval_pack_prepare", PACK / "prepare.py")
prepare = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(prepare)


def _selected_rows() -> list[dict]:
    """Rebuild the row-per-task mapping with the generator's own selection."""
    rows = [json.loads(line) for line
            in (PACK / "data/HumanEval.jsonl").read_text().splitlines() if line.strip()]
    rows = [row for row in rows if row["task_id"] not in prepare.EXCLUDED_UPSTREAM]
    rows.sort(key=lambda row: row["task_id"])
    selected = (prepare._sample(rows, prepare.TRAIN_COUNT, 0)
                + prepare._sample(rows, prepare.VALIDATION_COUNT, 1)
                + prepare._sample(rows, prepare.TEST_COUNT, 2))
    return selected


class HumanEvalPackTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import tempfile
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name)
        cls.path = prepare.write_pack(cls.root / "out")
        cls.manifest = json.loads(cls.path.read_text())

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_pack_is_deterministic(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as other:
            second = prepare.write_pack(Path(other) / "out")
            self.assertEqual(self.path.read_text(), second.read_text())

    def test_split_sizes_and_hygiene(self) -> None:
        from collections import Counter
        splits = Counter(task["split"] for task in self.manifest["tasks"])
        self.assertEqual(splits, {"train": 20, "validation": 25, "test": 36})
        ids = [task["task_id"] for task in self.manifest["tasks"]]
        self.assertEqual(len(set(ids)), len(ids))
        for task in self.manifest["tasks"]:
            self.assertEqual(task["expected_files"]["solution.py"], prepare.WITHHELD)

    def test_reference_solutions_never_enter_the_manifest(self) -> None:
        text = self.path.read_text()
        for row in _selected_rows():
            self.assertNotIn(row["canonical_solution"].strip()[:40], text)

    def test_grading_contract_shape(self) -> None:
        for task in self.manifest["tasks"]:
            grading = task["grading"]
            self.assertEqual(set(grading), {"kind", "public_tests", "private_tests", "timeout_s"})
            self.assertEqual(grading["kind"], "python-unittest")
            self.assertTrue(grading["public_tests"] and grading["private_tests"])
            self.assertGreater(grading["timeout_s"], 0)
            for name in list(grading["public_tests"]) + list(grading["private_tests"]):
                self.assertRegex(name, r"test_[A-Za-z0-9_]+\.py")
            self.assertIn("callable(getattr(solution",
                          grading["public_tests"]["test_public.py"])

    def test_stub_fails_and_canonical_passes(self) -> None:
        rows = _selected_rows()
        for task, row in list(zip(self.manifest["tasks"], rows))[::9]:
            with tempfile.TemporaryDirectory() as d:
                Path(d, "test_public.py").write_text(task["grading"]["public_tests"]["test_public.py"])
                Path(d, "test_private.py").write_text(task["grading"]["private_tests"]["test_private.py"])
                Path(d, "solution.py").write_text(task["input_files"]["solution.py"])
                stub = subprocess.run([sys.executable, "-m", "unittest", "test_private"],
                                      cwd=d, capture_output=True, text=True, timeout=60)
                self.assertNotEqual(stub.returncode, 0, task["task_id"])
                Path(d, "solution.py").write_text(row["prompt"] + row["canonical_solution"] + "\n")
                solved = subprocess.run([sys.executable, "-m", "unittest", "test_private", "test_public"],
                                        cwd=d, capture_output=True, text=True, timeout=60)
                self.assertEqual(solved.returncode, 0, (task["task_id"], solved.stderr[-300:]))


if __name__ == "__main__":
    unittest.main()
