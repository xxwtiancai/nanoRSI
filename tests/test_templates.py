import tempfile
import unittest
from pathlib import Path

from nanorsi.templates import TemplateError, render_template


class TemplateTests(unittest.TestCase):
    def test_renders_artifact_harness_and_model(self):
        for template in ["artifact", "harness", "model"]:
            with self.subTest(template=template):
                with tempfile.TemporaryDirectory() as tmp:
                    destination = Path(tmp) / template
                    files = render_template(template, destination, goal="Improve demo")
                    self.assertTrue((destination / "nanorsi.toml").is_file())
                    self.assertGreater(len(files), 5)
                    self.assertFalse(any("__pycache__" in file or file.endswith(".pyc") for file in files))

    def test_rejects_unknown_template(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(TemplateError):
                render_template("joint", Path(tmp) / "x", goal="No")


if __name__ == "__main__":
    unittest.main()
