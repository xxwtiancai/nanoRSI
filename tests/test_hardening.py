from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

from nanorsi.locking import Lock, LockBusy


ROOT = Path(__file__).parents[1]


def cli(*args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    return subprocess.run(
        [sys.executable, "-m", "nanorsi.cli", *args],
        env=env,
        text=True,
        capture_output=True,
        timeout=20,
    )


def make_workspace(kind: str) -> Path:
    destination = Path(tempfile.mkdtemp(prefix=f"nanorsi-{kind}-")) / "workspace"
    created = cli("new", {"artifact": "artifact-fixture", "harness": "harness-fixture", "model": "model-contract"}.get(kind, kind), str(destination))
    assert created.returncode == 0, created.stderr
    return destination


class HardeningTests(unittest.TestCase):
    def test_second_thread_cannot_enter_active_experiment(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            results: list[Exception | None] = []
            with Lock(root):
                thread = threading.Thread(target=lambda: results.append(self._try_lock(root)))
                thread.start()
                thread.join()
            self.assertIsInstance(results[0], LockBusy)

    def _try_lock(self, root: Path) -> Exception | None:
        try:
            with Lock(root):
                return None
        except Exception as error:
            return error

    def test_killed_step_preserves_parent_and_recover_clears_stale_lock(self):
        workspace = make_workspace("artifact")
        evaluator = workspace / "evaluator" / "evaluate.py"
        evaluator.write_text(
            "\n".join(
                [
                    "import importlib.util, json, os, time",
                    "from pathlib import Path",
                    "cases = {'gate': ([3, 9, 2], 9), 'train': ([1, 4, 2], 4), 'heldout': ([-1, 5, 7], 7)}",
                    "values, expected = cases[os.environ['NANORSI_SPLIT']]",
                    "spec = importlib.util.spec_from_file_location('s', Path.cwd() / 'target' / 'search.py')",
                    "module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)",
                    "actual = module.best(values)",
                    "result = Path(os.environ['NANORSI_RESULT_PATH'])",
                    "if actual == expected: result.with_suffix('.started').touch(); time.sleep(15)",
                    "payload = {'schema_version':1,'status':'ok','metrics':{'score':float(actual == expected)},'constraints':{'tests_passed':True},'case_results':[],'cost_usd':None,'duration_ms':0}",
                    "result.write_text(json.dumps(payload))",
                ]
            ),
            encoding="utf-8",
        )
        self.assertEqual(cli("baseline", "--workspace", str(workspace)).returncode, 0)
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        process = subprocess.Popen(
            [sys.executable, "-m", "nanorsi.cli", "step", "--workspace", str(workspace)],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            if next((workspace / ".nanorsi").rglob("*.started"), None):
                break
            time.sleep(0.05)
        else:
            self.fail("candidate evaluator did not start")
        process.kill()
        process.wait(timeout=5)
        if process.stdout:
            process.stdout.close()
        if process.stderr:
            process.stderr.close()
        self.assertFalse((workspace / ".git" / "refs" / "tags" / "nanorsi" / "gen-1").exists())
        self.assertTrue((workspace / ".nanorsi" / "lock").exists())
        recovered = cli("recover", "--workspace", str(workspace))
        self.assertEqual(recovered.returncode, 0, recovered.stderr)
        self.assertFalse((workspace / ".nanorsi" / "lock").exists())
        self.assertEqual(cli("verify", "--workspace", str(workspace)).returncode, 0)

    def test_proposal_cannot_mutate_evaluator(self):
        workspace = make_workspace("artifact")
        proposer = workspace / "proposer" / "propose.py"
        proposer.write_text(
            "\n".join(
                [
                    "import os",
                    "from pathlib import Path",
                    "output = Path(os.environ['NANORSI_PROPOSAL_DIR'])",
                    "diff = 'diff --git a/evaluator/evaluate.py b/evaluator/evaluate.py\\n--- a/evaluator/evaluate.py\\n+++ b/evaluator/evaluate.py\\n'",
                    "(output / 'proposal.diff').write_text(diff)",
                    "(output / 'hypothesis.json').write_text('{}')",
                ]
            ),
            encoding="utf-8",
        )
        self.assertEqual(cli("baseline", "--workspace", str(workspace)).returncode, 0)
        rejected = cli("step", "--workspace", str(workspace))
        self.assertEqual(rejected.returncode, 1)
        self.assertIn("outside mutable surface", rejected.stderr)
        self.assertFalse((workspace / ".git" / "refs" / "tags" / "nanorsi" / "gen-1").exists())

    def test_doctor_reports_local_subprocess_boundary(self):
        workspace = make_workspace("artifact")
        doctor = cli("doctor", "--workspace", str(workspace))
        self.assertEqual(doctor.returncode, 0)
        self.assertIn("execution: local subprocess", doctor.stdout)


if __name__ == "__main__":
    unittest.main()
