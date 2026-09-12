from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SRC = ROOT / "src"


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    return subprocess.run(
        [sys.executable, "-m", "nanorsi.cli", *args],
        cwd=cwd,
        env=env,
        text=True,
        capture_output=True,
        timeout=30,
    )


class EndToEndTests(unittest.TestCase):
    def test_artifact_template_completes_accepted_generation_offline(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "artifact-demo"
            created = run_cli("new", "artifact-fixture", str(workspace), "--goal", "Improve search")
            self.assertEqual(created.returncode, 0, created.stderr)
            baseline = run_cli("baseline", "--workspace", str(workspace))
            self.assertEqual(baseline.returncode, 0, baseline.stderr)
            step = run_cli("step", "--workspace", str(workspace))
            self.assertEqual(step.returncode, 0, step.stderr)
            lineage = json.loads((workspace / "lineage.jsonl").read_text().splitlines()[-1])
            self.assertEqual(lineage["decision"], "accepted")
            self.assertGreater(lineage["generation"], 0)
            self.assertIn(lineage["candidate_tree"], step.stdout)
            report = run_cli("report", "--workspace", str(workspace))
            self.assertEqual(report.returncode, 0, report.stderr)
            self.assertIn("Decision: accepted", (workspace / "reports" / "report.md").read_text())
            verified = run_cli("verify", "--workspace", str(workspace))
            self.assertEqual(verified.returncode, 0, verified.stderr)

    def test_harness_template_completes_offline_and_keeps_private_rubric_private(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "harness-demo"
            self.assertEqual(run_cli("new", "harness-fixture", str(workspace)).returncode, 0)
            self.assertEqual(run_cli("baseline", "--workspace", str(workspace)).returncode, 0)
            step = run_cli("step", "--workspace", str(workspace))
            self.assertEqual(step.returncode, 0, step.stderr)
            lineage = json.loads((workspace / "lineage.jsonl").read_text().splitlines()[-1])
            self.assertEqual(lineage["decision"], "accepted")
            self.assertNotIn("expected", step.stdout)

    def test_model_template_is_contract_only_and_doctor_reports_external_training(self):
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp) / "model-demo"
            self.assertEqual(run_cli("new", "model-contract", str(workspace)).returncode, 0)
            doctor = run_cli("doctor", "--workspace", str(workspace))
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertIn("model: external training contract", doctor.stdout)
            self.assertIn("training command: python3 target/train.py", doctor.stdout)


if __name__ == "__main__":
    unittest.main()
