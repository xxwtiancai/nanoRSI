import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SRC = ROOT / "src" / "nanorsi"
FORBIDDEN_MODULES = {
    "server.py",
    "dashboard.py",
    "plugin.py",
    "plugins.py",
    "distributed.py",
    "scheduler.py",
    "database.py",
}
EXPECTED_MODULES = {
    "__init__.py",
    "cli.py",
    "loop.py",
    "config.py",
    "configure.py",
    "contracts.py",
    "training.py",
    "population.py",
    "paths.py",
    "hashing.py",
    "surface.py",
    "gitops.py",
    "proposer.py",
    "evaluator.py",
    "gate.py",
    "lineage.py",
    "process.py",
    "report.py",
    "templates.py",
    "doctor.py",
    "locking.py",
}


class ArchitectureTests(unittest.TestCase):
    def test_core_module_inventory_matches_specification(self):
        actual = {path.name for path in SRC.glob("*.py")} if SRC.exists() else set()
        self.assertEqual(actual, EXPECTED_MODULES)
        self.assertFalse(actual & FORBIDDEN_MODULES)

    def test_core_size_and_function_budgets(self):
        if not SRC.exists():
            self.fail("nanorsi core source directory is missing")
        python_files = sorted(SRC.glob("*.py"))
        total = sum(len(path.read_text(encoding="utf-8").splitlines()) for path in python_files)
        self.assertLessEqual(total, 5000)
        for path in python_files:
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 300)
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.assertLessEqual(node.end_lineno - node.lineno + 1, 50)

    def test_specification_contains_every_module_and_transition(self):
        spec = (ROOT / "docs" / "specification.md")
        self.assertTrue(spec.exists(), "docs/specification.md is required")
        text = spec.read_text(encoding="utf-8")
        for module in sorted(EXPECTED_MODULES - {"__init__.py"}):
            self.assertIn(f"`src/nanorsi/{module}`", text)
        for state in ["NEW", "GEN0_SNAPSHOT", "CHILD_EVALUATED", "GATED_ACCEPTED", "GATED_REJECTED", "INCONCLUSIVE", "LINEAGE_RECORDED"]:
            self.assertIn(state, text)

    def test_runtime_has_no_third_party_imports(self):
        if not SRC.exists():
            self.fail("nanorsi core source directory is missing")
        allowed_roots = {"nanorsi", "__future__"}
        allowed_stdlib = {
            "argparse", "ast", "concurrent", "contextlib", "dataclasses", "datetime", "difflib",
            "enum", "fnmatch", "getpass", "hashlib", "hmac", "html", "importlib", "json", "math",
            "os", "pathlib", "random", "re", "secrets", "shlex", "shutil", "stat", "subprocess", "sys",
            "tempfile", "threading", "time", "tomllib", "typing", "unittest", "urllib", "uuid", "warnings",
        }
        for path in sorted(SRC.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        self.assertIn(root, allowed_roots | allowed_stdlib)
                elif isinstance(node, ast.ImportFrom) and node.level == 0:
                    root = (node.module or "").split(".")[0]
                    self.assertIn(root, allowed_roots | allowed_stdlib)


if __name__ == "__main__":
    unittest.main()
