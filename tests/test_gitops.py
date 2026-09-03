import tempfile
import unittest
from pathlib import Path

from nanorsi.gitops import Git


class GitOperationTests(unittest.TestCase):
    def test_snapshots_parent_and_child_trees(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git = Git(repo)
            git.init()
            (repo / "target").mkdir()
            (repo / "target" / "a.txt").write_text("one\n", encoding="utf-8")
            parent = git.commit_all("baseline")
            parent_tree = git.tree_hash(parent)
            diff = """diff --git a/target/a.txt b/target/a.txt
index 1..2 100644
--- a/target/a.txt
+++ b/target/a.txt
@@ -1 +1 @@
-one
+two
"""
            with git.worktree(parent, repo / "child") as child:
                git.apply_diff(child, diff)
                changed = git.changed_paths(child, parent)
                child_commit = git.commit_paths(child, changed, "candidate")
                self.assertEqual(git.tree_hash(child_commit), git.tree_hash(child_commit))
                self.assertEqual(changed, ["target/a.txt"])
                self.assertNotEqual(git.tree_hash(child_commit), parent_tree)
                self.assertEqual((child / "target" / "a.txt").read_text(), "two\n")


if __name__ == "__main__":
    unittest.main()
