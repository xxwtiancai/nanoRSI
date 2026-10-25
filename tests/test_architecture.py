"""The nano constraints: a small, standard-library core with a declared module map."""
import ast
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "nanorsi"
EXPECTED_MODULES = {
    "__init__.py", "cli.py", "config.py", "experience.py", "harness.py", "judge.py", "ledger.py", "model.py",
    "probe.py", "propose.py", "recursion.py", "report.py", "runner.py", "select.py", "tasks.py", "templates.py",
}


class ArchitectureTests(unittest.TestCase):
    def test_core_module_inventory_matches_specification(self):
        self.assertEqual({p.name for p in SRC.glob("*.py")}, EXPECTED_MODULES)
        spec = (ROOT / "docs" / "specification.md").read_text(encoding="utf-8")
        for module in sorted(EXPECTED_MODULES - {"__init__.py"}):
            self.assertIn(f"`src/nanorsi/{module}`", spec)

    def test_core_size_and_function_budgets(self):
        files = sorted(SRC.glob("*.py"))
        total = sum(len(p.read_text(encoding="utf-8").splitlines()) for p in files)
        self.assertLessEqual(total, 2500, "the nano core stays under 2,500 lines")
        for path in files:
            with self.subTest(path=path.name):
                self.assertLessEqual(len(path.read_text(encoding="utf-8").splitlines()), 300)
                for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        self.assertLessEqual(node.end_lineno - node.lineno + 1, 50, node.name)

    def test_runtime_has_no_third_party_imports(self):
        stdlib = set(sys.stdlib_module_names)
        for path in SRC.glob("*.py"):
            for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
                names = []
                if isinstance(node, ast.Import):
                    names = [alias.name.split(".")[0] for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    names = [node.module.split(".")[0]]
                for name in names:
                    self.assertTrue(name in stdlib or name == "nanorsi", f"{path.name} imports {name}")


if __name__ == "__main__":
    unittest.main()
