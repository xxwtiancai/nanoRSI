"""Offline validation of the multi-seed orchestrator (selector-study prerequisite).

Uses the standard v2 fixture as the template: a scripted offline proposer and
deterministic evaluator, so each seed is a genuine independent replicate of
the full lifecycle without model calls. Live templates use the same script.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from tests.test_v2_lifecycle import make_v2

SCRIPT = Path(__file__).resolve().parent.parent / "examples" / "multiseed" / "run.py"


class MultiSeedTests(unittest.TestCase):

    def test_two_offline_seeds_complete_the_lifecycle_and_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template = make_v2(tmp + "/template")
            out = Path(tmp) / "study"
            environment = {"PATH": __import__("os").environ["PATH"],
                           "PYTHONPATH": str(Path(__file__).resolve().parent.parent / "src")}
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(template), str(out), "--seeds", "0,1", "--repeats", "1"],
                capture_output=True, text=True, timeout=600, env=environment)
            self.assertEqual(completed.returncode, 0, completed.stderr[-800:])
            summary = json.loads((out / "summary.json").read_text())
            self.assertEqual(summary["schema_version"], 1)
            self.assertEqual(summary["seeds"], [0, 1])
            self.assertEqual(sorted(summary["conditions"]), ["baseline", "candidate", "no-skills"])
            self.assertIsInstance(summary["total_model_calls"], int)  # fixture records simulated calls
            for seed in (0, 1):
                workspace = out / f"seed-{seed}"
                self.assertTrue((workspace / "reports" / "final.json").is_file())
                self.assertTrue((workspace / "reports" / "evidence.jsonl").is_file())
                self.assertTrue((workspace / "lineage.jsonl").is_file())
            # each seed is an independently baselined workspace with its own seed
            for seed in (0, 1):
                toml = (out / f"seed-{seed}" / "nanorsi.toml").read_text()
                self.assertIn(f"seed = {seed}", toml)
            self.assertFalse((template / "lineage.jsonl").exists())  # template untouched

    def test_refuses_journalled_template_and_missing_toml(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            empty = Path(tmp) / "empty"
            empty.mkdir()
            with self.assertRaises(subprocess.CalledProcessError):
                subprocess.run([sys.executable, str(SCRIPT), str(empty), str(Path(tmp) / "o")],
                               capture_output=True, timeout=60, check=True)
            template = make_v2(tmp + "/template")
            environment = {"PATH": __import__("os").environ["PATH"],
                           "PYTHONPATH": str(Path(__file__).resolve().parent.parent / "src")}
            # baseline once so the journal exists
            subprocess.run([sys.executable, "-m", "nanorsi.cli", "baseline", "--workspace", str(template)],
                           capture_output=True, timeout=120, env=environment, check=True)
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), str(template), str(Path(tmp) / "o2")],
                capture_output=True, text=True, timeout=60, env=environment)
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("unbaselined", completed.stderr)


if __name__ == "__main__":
    unittest.main()
