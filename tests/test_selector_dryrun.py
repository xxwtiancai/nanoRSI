"""Offline smoke of the selector-study dry-run driver (machinery, not effects)."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent.parent / "examples" / "selector_dryrun" / "run.py"
REPO = SCRIPT.parents[1]


class SelectorDryRunTests(unittest.TestCase):

    def test_dry_run_produces_protocol_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), tmp, "--seeds", "0", "--band", "1.5", "--repeats", "1"],
                capture_output=True, text=True, timeout=1200,
                env={"PATH": __import__("os").environ["PATH"], "PYTHONPATH": str(REPO / "src")})
            self.assertEqual(completed.returncode, 0, completed.stderr[-800:])
            report = json.loads((Path(tmp) / "summary.json").read_text())
            strict, band = report["arms"]
            self.assertEqual(strict["per_seed"][0]["accepted"], 1)
            self.assertEqual(strict["per_seed"][0]["false_blocks"], 0)
            self.assertEqual(band["per_seed"][0]["accepted"], 0)
            self.assertEqual(band["per_seed"][0]["decisions"], ["rejected", "rejected", "rejected"])
            self.assertEqual(band["per_seed"][0]["false_blocks"], 3)
            self.assertEqual(report["conditions"]["strict/candidate"]["mean"], 1.0)
            self.assertEqual(report["conditions"]["noise-band/candidate"]["mean"], 0.0)
            self.assertIn("dry-run", report["verdict"])


if __name__ == "__main__":
    unittest.main()
