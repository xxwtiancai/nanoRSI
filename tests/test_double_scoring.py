"""Offline validation of the double-scoring harness (selector-study accounting)."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

SCRIPT = Path(__file__).resolve().parent.parent / "examples" / "double_scoring" / "run.py"

_spec = importlib.util.spec_from_file_location("double_scoring_run", SCRIPT)
harness = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(harness)


class DoubleScoringTests(unittest.TestCase):

    def call(self, root, *args):
        result = run_cli(*args, '--workspace', str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_strict_workspace_agrees_with_control(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root, 'baseline')
            self.call(root, 'run')
            report = harness.recompute(root, 0.0)
            # the fixture makes one measured proposal (accepted) and two no-ops;
            # no-ops never reach measurement and are not double-scoreable
            self.assertEqual(report["counts"]["agree"], 1)
            self.assertEqual(report["counts"]["false_block"], 0)
            self.assertEqual(report["counts"]["false_admit"], 0)
            self.assertEqual(report["counts"]["not_double_scoreable"], 0)

    def test_noise_band_blocks_are_counted_as_false_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            toml = root / 'nanorsi.toml'
            toml.write_text(toml.read_text().replace('[gate]', '[gate]\nnoise_band = 1.5'))
            self.call(root, 'baseline')
            self.call(root, 'run')
            report = harness.recompute(root, 0.0)
            # with acceptance blocked the parent never advances, so the scripted
            # proposer re-proposes the same +1.0 edit and all three attempts are
            # measured, band-rejected, and control-accepted: three false blocks
            self.assertEqual(report["counts"]["false_block"], 3)
            self.assertEqual(report["counts"]["agree"], 0)
            rows = {row["attempt"]: row for row in report["attempts"]}
            for attempt in (1, 2, 3):
                self.assertEqual(rows[attempt]["selector_decision"], "rejected")
                self.assertIn("noise-adjusted", rows[attempt]["selector_reason"])
                self.assertEqual(rows[attempt]["control_decision"], "accepted")

    def test_reevaluate_blocked_reconstructs_an_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp, steps=1)
            self.call(root, 'baseline')
            self.call(root, 'run')
            # Simulate a pre-evaluation-blocked attempt: drop the metrics of the
            # measured attempt so only its archived proposal diff remains.
            path = root / 'lineage.jsonl'
            events = [json.loads(line) for line in path.read_text().splitlines()]
            for event in events:
                if event.get('event_type') == 'generation' and event.get('attempt_id'):
                    event['gate_metrics'], event['heldout_metrics'] = None, None
                    event['decision'], event['reason'] = 'blocked', 'pre-evaluation selector'
            path.write_text(''.join(json.dumps(e) + '\n' for e in events))
            report = harness.reevaluate_blocked(root, 0.0)
            self.assertEqual(report["counts"]["control_accepted"], 1)
            self.assertEqual(report["counts"]["control_rejected"], 0)
            self.assertEqual(report["attempts"][0]["class"], "control_accepted")


if __name__ == "__main__":
    unittest.main()
