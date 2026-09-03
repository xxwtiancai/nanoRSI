import tempfile
import unittest
from pathlib import Path

from nanorsi.lineage import LineageError, LineageStore


class LineageTests(unittest.TestCase):
    def test_appends_sequenced_hmac_protected_events(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = LineageStore.initialize(Path(tmp))
            store.append({"event_type": "baseline", "generation": 0})
            store.append(
                {
                    "event_type": "generation",
                    "generation": 1,
                    "parent_generation": 0,
                    "decision": "accepted",
                }
            )
            events = store.events()
            self.assertEqual([event["seq"] for event in events], [1, 2])
            self.assertTrue(all(event["receipt"] for event in events))
            self.assertEqual(store.latest_accepted()["generation"], 1)

    def test_verify_rejects_forged_score_and_sequence_gap(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            store = LineageStore.initialize(root)
            store.append({"event_type": "baseline", "generation": 0})
            path = root / "lineage.jsonl"
            forged = store.events()[0].copy()
            forged["gate_metrics"] = {"score": 1.0}
            path.write_text(
                __import__("json").dumps(forged, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(LineageError):
                store.verify()


if __name__ == "__main__":
    unittest.main()
