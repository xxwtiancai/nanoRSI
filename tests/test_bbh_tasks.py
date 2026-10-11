"""Offline checks for the vendored BBH task packs (ADOPTION item 37, phase 1).

Covers manifest determinism, split hygiene, weak-but-plausible initial solvers,
oracle reachability (the data is solvable to 1.0) and an example-specific
hardcoding screen. Live evidence lives in examples/results/bbh-phase1/.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

PACK = Path(__file__).resolve().parent.parent / "examples" / "bbh_tasks"
sys.path.insert(0, str(PACK))

import prepare  # noqa: E402


def _build_once(target: Path) -> dict[str, dict]:
    prepare.write_packs(target)
    packs = {}
    for name, _data, _program, _instruction in prepare.PACKS:
        manifest = json.loads((target / name / "tasks" / "manifest.json").read_text())
        program = (target / name / "target" / "program.py").read_text()
        packs[name] = {"manifest": manifest, "program": program}
    return packs


def _split_tasks(manifest: dict, split: str) -> list[dict]:
    return [task for task in manifest["tasks"] if task["split"] == split]


class BBHPackTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import tempfile
        cls._tmp = tempfile.TemporaryDirectory()
        cls.packs = _build_once(Path(cls._tmp.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_manifest_is_deterministic(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as other:
            second = _build_once(Path(other))
        self.assertEqual(self.packs, second)

    def test_split_sizes_and_unique_ids(self) -> None:
        for name, pack in self.packs.items():
            tasks = pack["manifest"]["tasks"]
            ids = [task["task_id"] for task in tasks]
            splits = [task["split"] for task in tasks]
            with self.subTest(pack=name):
                self.assertEqual(len(tasks), 250)
                self.assertEqual(len(set(ids)), 250)
                self.assertEqual(splits.count("train"), 50)
                self.assertEqual(splits.count("validation"), 50)
                self.assertEqual(splits.count("test"), 150)
                inputs = [task["input_files"]["records.json"] for task in tasks]
                self.assertEqual(len(set(inputs)), 250)

    def test_weak_solver_is_weak_but_functional(self) -> None:
        bounds = {"dyck": (0.60, 0.95), "bool": (0.70, 0.98)}
        for name, pack in self.packs.items():
            namespace: dict = {}
            exec(compile(pack["program"], "program.py", "exec"), namespace)  # noqa: S102 - fixture
            tasks = _split_tasks(pack["manifest"], "validation")
            hits = 0
            for task in tasks:
                prompt = json.loads(task["input_files"]["records.json"])["input"]
                wanted = json.loads(task["expected_files"]["summary.json"])["answer"]
                hits += namespace["solve"](prompt) == wanted
            share = hits / len(tasks)
            low, high = bounds[name]
            with self.subTest(pack=name):
                self.assertGreaterEqual(share, low)
                self.assertLess(share, high)

    def test_oracle_solvers_reach_perfection(self) -> None:
        oracles = {"dyck": self._dyck_oracle, "bool": self._bool_oracle}
        for name, pack in self.packs.items():
            for split in ("validation", "test"):
                tasks = _split_tasks(pack["manifest"], split)
                for task in tasks:
                    prompt = json.loads(task["input_files"]["records.json"])["input"]
                    wanted = json.loads(task["expected_files"]["summary.json"])["answer"]
                    with self.subTest(pack=name, split=split, task=task["task_id"]):
                        self.assertEqual(oracles[name](prompt), wanted)

    def test_no_example_specific_hardcoding(self) -> None:
        for name, pack in self.packs.items():
            program = pack["program"]
            for task in pack["manifest"]["tasks"]:
                prompt = json.loads(task["input_files"]["records.json"])["input"]
                body = prompt.split("Input:", 1)[-1].strip()
                if len(body) >= 12:
                    with self.subTest(pack=name, task=task["task_id"]):
                        self.assertNotIn(body, program)

    @staticmethod
    def _dyck_oracle(text: str) -> str:
        pairs = {"(": ")", "[": "]", "{": "}", "<": ">"}
        stack = []
        for token in text.split("Input:", 1)[1].split():
            if token in pairs:
                stack.append(token)
            elif stack and pairs[stack[-1]] == token:
                stack.pop()
        return " ".join(pairs[token] for token in reversed(stack))

    @staticmethod
    def _bool_oracle(text: str) -> str:
        expression = text.strip()
        if expression.endswith(" is"):
            expression = expression[:-3]
        return str(eval(expression))  # noqa: S307 - trusted BBH fixture data


if __name__ == "__main__":
    unittest.main()
