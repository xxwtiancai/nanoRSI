import tempfile
import unittest
from pathlib import Path

from nanorsi.locking import Lock, LockBusy


class LockingTests(unittest.TestCase):
    def test_lock_is_exclusive_and_removable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with Lock(root):
                with self.assertRaises(LockBusy):
                    with Lock(root):
                        pass
            with Lock(root):
                pass
            self.assertTrue((root / ".nanorsi" / "lock").exists() is False)


if __name__ == "__main__":
    unittest.main()
