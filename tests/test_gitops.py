import tempfile
from concurrent.futures import ThreadPoolExecutor
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from nanorsi.gitops import Git


class GitOperationTests(unittest.TestCase):
    def test_worktree_administration_is_serial_but_bodies_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git = Git(repo)
            git.init()
            (repo / 'file.txt').write_text('shared baseline\n')
            ref = git.commit_all('baseline')
            begin, bodies = threading.Barrier(2), threading.Barrier(2)
            counter_lock, second_admin = threading.Lock(), threading.Event()
            state = {'active': 0, 'maximum': 0, 'first': True}
            original = Git._run

            def observed(instance, *args, **kwargs):
                if args[:2] not in {('worktree', 'add'), ('worktree', 'remove'), ('worktree', 'prune')}:
                    return original(instance, *args, **kwargs)
                with counter_lock:
                    first, state['first'] = state['first'], False
                    state['active'] += 1
                    state['maximum'] = max(state['maximum'], state['active'])
                    if state['active'] > 1:
                        second_admin.set()
                try:
                    if first:
                        second_admin.wait(0.5)
                    return original(instance, *args, **kwargs)
                finally:
                    with counter_lock:
                        state['active'] -= 1

            def worker(index):
                begin.wait(timeout=5)
                # Separate instances must coordinate shared Git administration.
                local = Git(repo)
                with local.worktree(ref, repo / 'children' / str(index)) as child:
                    self.assertEqual((child / 'file.txt').read_text(), 'shared baseline\n')
                    bodies.wait(timeout=10)
                local.prune_worktrees()

            with patch.object(Git, '_run', observed), ThreadPoolExecutor(max_workers=2) as pool:
                list(pool.map(worker, range(2)))
            self.assertEqual(state['maximum'], 1, 'worktree add/remove/prune overlapped')
            self.assertEqual(state['active'], 0)
            self.assertFalse((repo / 'children/0').exists())
            self.assertFalse((repo / 'children/1').exists())

    def test_worktree_cleanup_survives_body_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            git = Git(repo)
            git.init()
            (repo / 'file.txt').write_text('baseline\n')
            ref = git.commit_all('baseline')
            child = repo / 'child'
            with self.assertRaisesRegex(ValueError, 'body failure'):
                with git.worktree(ref, child):
                    raise ValueError('body failure')
            self.assertFalse(child.exists())
            with Git(repo).worktree(ref, child):
                self.assertTrue((child / 'file.txt').exists())

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
