import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

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

    def test_concurrent_first_initializers_share_key_and_preserve_signed_receipts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            waiting, signed = threading.Barrier(2), threading.Event()
            keys, errors = {}, []
            def key_bytes(count):
                waiting.wait(timeout=5)
                if threading.current_thread().name == 'second':
                    self.assertTrue(signed.wait(timeout=5))
                    return b'B' * count
                return b'A' * count
            def initialize():
                try:
                    store = LineageStore.initialize(root)
                    keys[threading.current_thread().name] = store._key()
                    if threading.current_thread().name == 'first':
                        store.append({'event_type': 'generation', 'decision': 'baseline', 'generation': 0})
                        signed.set()
                except BaseException as error:
                    errors.append(error)
            with patch('nanorsi.lineage.secrets.token_bytes', side_effect=key_bytes):
                threads = [threading.Thread(target=initialize, name=name) for name in ['first', 'second']]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join(timeout=10)
            self.assertFalse(any(thread.is_alive() for thread in threads))
            self.assertEqual(errors, [])
            self.assertEqual(keys, {'first': b'A' * 32, 'second': b'A' * 32})
            store = LineageStore.initialize(root)
            self.assertEqual(len(store.verify()), 1)
            self.assertEqual(store._key(), b'A' * 32)
            self.assertEqual(store.key_path.stat().st_mode & 0o777, 0o600)
            self.assertEqual([p.name for p in (root / '.nanorsi').iterdir()], ['lineage.key'])

    def test_initialization_rejects_invalid_existing_key_without_replacing_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / '.nanorsi').mkdir()
            key = root / '.nanorsi/lineage.key'
            key.write_bytes(b'broken-key')
            with self.assertRaisesRegex(LineageError, '32 bytes'):
                LineageStore.initialize(root)
            self.assertEqual(key.read_bytes(), b'broken-key')

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
