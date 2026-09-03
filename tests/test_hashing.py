import unittest
from pathlib import Path

from nanorsi.hashing import canonical_hash, tree_hash


class HashingTests(unittest.TestCase):
    def test_canonical_hash_is_key_order_insensitive(self):
        self.assertEqual(
            canonical_hash({"b": 2, "a": 1}),
            canonical_hash({"a": 1, "b": 2}),
        )

    def test_tree_hash_ignores_excluded_paths_and_captures_content(self):
        with __import__("tempfile").TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "target").mkdir()
            (root / "runs").mkdir()
            (root / "target" / "a.txt").write_text("same", encoding="utf-8")
            (root / "runs" / "b.txt").write_text("ignored", encoding="utf-8")
            first = tree_hash(root, exclude=["runs/**"])
            (root / "runs" / "b.txt").write_text("changed", encoding="utf-8")
            self.assertEqual(first, tree_hash(root, exclude=["runs/**"]))
            (root / "target" / "a.txt").write_text("different", encoding="utf-8")
            self.assertNotEqual(first, tree_hash(root, exclude=["runs/**"]))


if __name__ == "__main__":
    unittest.main()
