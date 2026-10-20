"""Offline checks for the ALFWorld task pack (ADOPTION item 37, phase 2).

The propose-mode contract and evaluator grading are checked everywhere (CI
included). Game-dependent checks require a local ALFWorld installation and
downloaded games (Python 3.12 + alfworld + alfworld-download); they skip
gracefully when absent. Live evidence lives in examples/results/alfworld-phase2/.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

PACK = Path(__file__).resolve().parent.parent / "examples" / "alfworld_tasks"

import importlib.util  # noqa: E402

try:
    _spec = importlib.util.spec_from_file_location("alfworld_pack_prepare", PACK / "prepare.py")
    prepare = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(prepare)
    HAS_PACK = True
except (ImportError, OSError):
    HAS_PACK = False

CACHE = Path.home() / ".cache/alfworld/json_2.1.1"
HAS_GAMES = HAS_PACK and CACHE.is_dir() and any(CACHE.rglob("game.tw-pddl"))
ALF_PYTHON = Path("/opt/miniconda3/envs/alf312/bin/python")
HAS_ALF = ALF_PYTHON.is_file()

STUB = """import json
import sys

request = json.load(sys.stdin)
last = request["messages"][-1]["content"]
try:
    context = json.loads(last) if last.startswith("{") else {}
except ValueError:
    context = {}
if "goal" in context and "parent_files" in context:
    proposal = {"files": {"target/agent/skills/alfworld/SKILL.md": "# skill v1\\n\\ntest guidance\\n"},
                "hypothesis": {"reason": "smoke"}}
    print(json.dumps({"content": json.dumps(proposal), "usage": {"input_tokens": 9, "output_tokens": 4}}))
else:
    print(json.dumps({"content": json.dumps({"action": "look"}), "usage": {"input_tokens": 9, "output_tokens": 4}}))
"""


def _write_pack(target: Path, with_manifest: bool = True) -> dict[str, str]:
    paths = {}
    for path in prepare.write_pack(target, with_manifest=with_manifest):
        paths[path.name] = path.read_text()
    return paths


@unittest.skipUnless(HAS_PACK, "alfworld pack generator unavailable")
class ALFWorldPackTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        import tempfile
        cls._tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls._tmp.name)
        cls.pack = _write_pack(cls.root / "out", with_manifest=HAS_GAMES)

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp.cleanup()

    def test_pack_is_deterministic(self) -> None:
        import tempfile
        with tempfile.TemporaryDirectory() as other:
            second = _write_pack(Path(other) / "out", with_manifest=HAS_GAMES)
        self.assertEqual(self.pack, second)

    @unittest.skipUnless(HAS_GAMES, "local ALFWorld games required for manifest selection")
    def test_manifest_splits_and_groups(self) -> None:
        from collections import Counter
        manifest = json.loads(self.pack["manifest.json"])
        splits = Counter(task["split"] for task in manifest["tasks"])
        groups = Counter(task["group_id"] for task in manifest["tasks"])
        self.assertEqual(splits, {"train": 4, "validation": 6, "test": 12})
        self.assertEqual(groups, {"train-games": 4, "validation-seen": 3,
                                  "validation-unseen": 3, "test-seen": 6, "test-unseen": 6})
        games = [json.loads(task["input_files"]["game.json"])["game_file"]
                 for task in manifest["tasks"]]
        self.assertEqual(len(games), len(set(games)))

    @unittest.skipUnless(HAS_GAMES, "local ALFWorld games required for manifest selection")
    def test_validation_shares_the_test_distribution_and_stays_disjoint(self) -> None:
        # The 2026-10-20 gate-ability diagnostic: validation must see the same
        # layout distribution the frozen test panel measures, without overlap.
        manifest = json.loads(self.pack["manifest.json"])
        pools = {"train": set(), "validation": set(), "test": set()}
        for task in manifest["tasks"]:
            path = json.loads(task["input_files"]["game.json"])["game_file"]
            pools[task["split"]].add(path)
        self.assertFalse(pools["validation"] & pools["test"])
        self.assertFalse(pools["validation"] & pools["train"])
        for path in pools["validation"]:
            self.assertRegex(path, r"json_2\.1\.1/valid_(seen|unseen)/")

    def test_runner_compiles_on_any_python(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "run.py"
            path.write_text(self.pack["run.py"])
            completed = subprocess.run([sys.executable, "-m", "py_compile", str(path)],
                                       capture_output=True, text=True)
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_propose_mode_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target/agent/skills/alfworld").mkdir(parents=True)
            (root / "target/agent/skills/alfworld/SKILL.md").write_text("# old\n")
            (root / "stub_model.py").write_text(STUB)
            runner = root / "target/agent/run.py"
            runner.write_text(self.pack["run.py"])
            request = {"mode": "propose",
                       "context": {"goal": "improve",
                                   "parent_files": {"target/agent/skills/alfworld/SKILL.md": "# old\n"},
                                   "train_results": [],
                                   "surface": {"allow": ["target/agent/skills/**"], "deny": []}},
                       "agent": {"model_command": [sys.executable, "stub_model.py"],
                                 "skills": [], "timeout_s": 30, "max_turns": 8}}
            completed = subprocess.run([sys.executable, str(runner)], cwd=root,
                                       input=json.dumps(request), capture_output=True,
                                       text=True, timeout=120)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["hypothesis"], {"reason": "smoke"})
        self.assertIn("diff --git a/target/agent/skills/alfworld/SKILL.md", result["diff"])
        self.assertEqual(result["usage"]["model_calls"], 1)

    def test_evaluator_grades_engine_success(self) -> None:
        namespace: dict = {}
        source = self.pack["evaluate.py"]
        start, end = source.index("def _grade("), source.index("def _training_feedback(")
        exec(compile(source[start:end], "grade.py", "exec"), namespace)  # noqa: S102 - fixture
        grade = namespace["_grade"]
        won = {"status": "ok", "won": True, "trace": [], "usage": {}}
        lost = {"status": "ok", "won": False, "trace": [], "usage": {}}
        timed_out = {"status": "error", "trace": [{"event": "model_error", "code": "model_timeout"}]}
        self.assertEqual(grade({}, won), (1.0, "ok"))
        self.assertEqual(grade({}, lost), (0.0, "task_failure"))
        self.assertEqual(grade({}, timed_out), (0.0, "timeout"))

    @unittest.skipUnless(HAS_GAMES and HAS_ALF, "local ALFWorld games and interpreter required")
    def test_task_mode_plays_a_real_game(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "target/agent/skills/alfworld").mkdir(parents=True)
            (root / "target/agent/skills/alfworld/SKILL.md").write_text("# skill\n")
            (root / "stub_model.py").write_text(STUB)
            runner = root / "target/agent/run.py"
            runner.write_text(self.pack["run.py"])
            manifest = json.loads(self.pack["manifest.json"])
            task = next(t for t in manifest["tasks"] if t["split"] == "validation")
            request = {"mode": "task", "task": task,
                       "agent": {"model_command": [sys.executable, "stub_model.py"],
                                 "skills": ["alfworld"], "timeout_s": 30, "max_turns": 8}}
            completed = subprocess.run([str(ALF_PYTHON), str(runner)], cwd=root,
                                       input=json.dumps(request), capture_output=True,
                                       text=True, timeout=600)
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["won"])
        actions = [item for item in result["trace"] if item.get("event") == "action"]
        self.assertGreaterEqual(len(actions), 10)
        self.assertIn("look", actions[0]["command"])


if __name__ == "__main__":
    unittest.main()
