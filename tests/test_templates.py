import tempfile
import sys
import unittest
from pathlib import Path

from nanorsi.templates import TemplateError, render_template
from nanorsi.config import load_config


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

    def test_v2_templates_pin_the_creating_python_interpreter(self):
        for template in ['coding', 'skills']:
            with self.subTest(template=template), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'lab'
                render_template(template, root, goal='portable interpreter')
                config = load_config(root / 'nanorsi.toml')
                for command in [config.agent['model_command'], config.proposer.command, config.evaluator.command]:
                    self.assertEqual(command[0], sys.executable)

    def test_canonical_types_are_live_and_legacy_fixtures_are_explicit(self):
        for template in ['artifact', 'harness', 'model']:
            with self.subTest(template=template), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'lab'
                render_template(template, root, goal='real implementation')
                config = load_config(root / 'nanorsi.toml')
                self.assertEqual(config.experiment.schema_version, 2)
                self.assertEqual(config.experiment.mode, template)
                if template == 'model':
                    self.assertTrue((root / config.training['checkpoint']).is_file())
        for template in ['artifact-fixture', 'harness-fixture', 'model-contract']:
            with self.subTest(template=template), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp) / 'lab'
                render_template(template, root, goal='legacy compatibility')
                self.assertEqual(load_config(root / 'nanorsi.toml').experiment.schema_version, 1)


if __name__ == "__main__":
    unittest.main()
