import unittest

from nanorsi.surface import SurfacePolicy, changed_paths_from_unified_diff, check_paths


class SurfaceTests(unittest.TestCase):
    def test_implicit_protected_roots_always_win(self):
        violations = check_paths(
            ["target/a.py", "evaluator/run.py", "lineage.jsonl"],
            include=["target/**"],
        )
        self.assertEqual(violations, ["evaluator/run.py", "lineage.jsonl"])

    def test_custom_deny_wins_over_include(self):
        violations = check_paths(
            ["target/generated.py"],
            include=["target/**"],
            exclude=["target/generated.py"],
        )
        self.assertEqual(violations, ["target/generated.py"])

    def test_policy_rejects_absolute_and_parent_paths(self):
        policy = SurfacePolicy(include=["target/**"], exclude=[])
        with self.assertRaisesRegex(ValueError, "outside the workspace"):
            policy.validate_paths(["../escape.py"])
        with self.assertRaisesRegex(ValueError, "outside the workspace"):
            policy.validate_paths(["/etc/passwd"])

    def test_parses_unified_diff_paths_without_applying_it(self):
        diff = """diff --git a/target/a.py b/target/a.py
index 1..2 100644
--- a/target/a.py
+++ b/target/a.py
@@ -1 +1 @@
-old
+new
diff --git a/evaluator/b.py b/evaluator/b.py
index 3..4 100644
--- a/evaluator/b.py
+++ b/evaluator/b.py
@@ -1 +1 @@
-old
+new
"""
        paths = changed_paths_from_unified_diff(diff)
        self.assertEqual(paths, ["target/a.py", "evaluator/b.py"])


if __name__ == "__main__":
    unittest.main()
