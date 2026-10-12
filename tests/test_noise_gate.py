"""Noise-band derivation and the opt-in noise-aware gate (ADOPTION item 38, phase 1)."""
from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from nanorsi.gate import GateConfig, decide
from nanorsi.noise import band_from_events, band_from_final, write_report
from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

PARENT, METRICS = {"score": 0.5}, {"score": 0.5, "constraints": {"tests_passed": True}}


def _child(score: float) -> dict:
    return {"score": score, "constraints": {"tests_passed": True}}


class GateNoiseTests(unittest.TestCase):

    def test_zero_band_keeps_historical_behavior(self) -> None:
        config = GateConfig(minimum_improvement=0.01, noise_band=0.0)
        rejected = decide(config, parent=PARENT, child=_child(0.505),
                          parent_heldout=None, child_heldout=None)
        self.assertEqual((rejected.decision, rejected.reason),
                         ("rejected", "improvement below minimum: 0.005000"))
        accepted = decide(config, parent=PARENT, child=_child(0.75),
                          parent_heldout=None, child_heldout=None)
        self.assertEqual((accepted.decision, accepted.reason), ("accepted", "improvement 0.250000"))

    def test_band_raises_the_acceptance_threshold(self) -> None:
        config = GateConfig(minimum_improvement=0.01, noise_band=0.2)
        blocked = decide(config, parent=PARENT, child=_child(0.6),
                         parent_heldout=None, child_heldout=None)
        self.assertEqual(blocked.decision, "rejected")
        self.assertIn("noise-adjusted minimum", blocked.reason)
        self.assertIn("band 0.200000", blocked.reason)
        passed = decide(config, parent=PARENT, child=_child(0.75),
                        parent_heldout=None, child_heldout=None)
        self.assertEqual(passed.decision, "accepted")

    def test_band_applies_to_minimize_direction(self) -> None:
        config = GateConfig(minimum_improvement=0.0, noise_band=0.2)
        blocked = decide(config, parent=PARENT, child=_child(0.4), parent_heldout=None,
                         child_heldout=None, direction="minimize")
        self.assertEqual(blocked.decision, "rejected")
        passed = decide(config, parent=PARENT, child=_child(0.2), parent_heldout=None,
                        child_heldout=None, direction="minimize")
        self.assertEqual(passed.decision, "accepted")


class NoiseDerivationTests(unittest.TestCase):

    def test_parent_remeasures_grouped_by_generation(self) -> None:
        events = [
            {"event_type": "generation", "attempt_id": None, "generation": 0, "gate_metrics": {"score": 0.88}},
            {"event_type": "generation", "attempt_id": 1, "parent_generation": 0, "parent_gate_metrics": {"score": 1.0}},
            {"event_type": "generation", "attempt_id": 2, "parent_generation": 0, "parent_gate_metrics": {"score": 1.0}},
            {"event_type": "generation", "attempt_id": 3, "parent_generation": 1, "parent_gate_metrics": {"score": 0.5}},
        ]
        report = band_from_events(events)
        self.assertEqual(report["by_parent_generation"]["0"]["values"], [0.88, 1.0, 1.0])
        self.assertEqual(report["by_parent_generation"]["0"]["spread"], 0.12)
        self.assertNotIn("1", report["by_parent_generation"])  # single measurement, no band
        self.assertEqual(report["largest_band"], 0.12)

    def test_final_repeats_spread_and_flip_rate(self) -> None:
        final = {"results": [
            {"condition": "baseline", "metrics": {"score": 0.9}, "case_results": [
                {"task_id": "a", "score": 1.0}, {"task_id": "a", "score": 0.0},
                {"task_id": "b", "score": 1.0}, {"task_id": "b", "score": 1.0}]},
            {"condition": "no-skills", "metrics": {"score": 1.0}, "case_results": [
                {"task_id": "a", "score": 1.0}, {"task_id": "a", "score": 1.0}]},
        ]}
        report = band_from_final(final)
        self.assertEqual(report["conditions"]["baseline"]["unstable_tasks"], 1)
        self.assertEqual(report["conditions"]["baseline"]["flip_rate"], 0.5)
        self.assertEqual(report["conditions"]["no-skills"]["unstable_tasks"], 0)
        self.assertEqual(report["conditions"]["no-skills"]["flip_rate"], 0.0)

    def test_write_report_skips_bare_roots(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = write_report(Path(tmp))
        self.assertIsNone(result["noise_band"])
        self.assertIn("skipped", result)


class NoiseReportIntegration(unittest.TestCase):

    def call(self, root, *args):
        result = run_cli(*args, '--workspace', str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_report_emits_noise_band_on_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root, 'run')
            self.call(root, 'report')
            payload = json.loads((root / 'reports' / 'noise-band.json').read_text())
            self.assertEqual(payload["schema_version"], 1)
            self.assertEqual(payload["configured_gate_band"], 0.0)
            self.assertEqual(payload["parent_remeasures"]["source"], "parent-remeasures")
            self.call(root, 'freeze', '--repeats', '2')
            self.call(root, 'final-test')
            self.call(root, 'report')
            payload = json.loads((root / 'reports' / 'noise-band.json').read_text())
            self.assertIn("final_repeats", payload)
            self.assertIn("conditions", payload["final_repeats"])

    def test_noise_band_gate_blocks_small_fixture_improvement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            toml = root / "nanorsi.toml"
            toml.write_text(toml.read_text().replace("[gate]", "[gate]\nnoise_band = 1.1"))
            self.call(root, 'baseline')
            self.call(root, 'run')
            events = [json.loads(line) for line in (root / "lineage.jsonl").read_text().splitlines()]
            gated = [e for e in events if e.get("event_type") == "generation" and e.get("attempt_id")]
            self.assertTrue(gated)
            self.assertTrue(all(e.get("decision") != "accepted" for e in gated),
                            [e.get("decision") for e in gated])
            self.assertTrue(all("noise-adjusted" in (e.get("reason") or "") for e in gated))
            payload = json.loads((root / "reports" / "noise-band.json").read_text())
            self.assertEqual(payload["configured_gate_band"], 1.1)


if __name__ == "__main__":
    unittest.main()
