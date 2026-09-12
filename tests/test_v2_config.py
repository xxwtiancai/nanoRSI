import tempfile
import unittest
from pathlib import Path

from nanorsi.config import ConfigError, load_config
from nanorsi.templates import render_template


class V2ConfigTests(unittest.TestCase):
    def test_skills_starter_has_explicit_v2_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'skills'
            render_template('skills',root,goal='Improve "skills"\ncarefully')
            config = load_config(root/'nanorsi.toml')
            self.assertEqual(config.experiment.schema_version,2)
            self.assertEqual(config.experiment.arm,'frozen')
            self.assertEqual(config.experiment.goal,'Improve "skills"\ncarefully')
            self.assertEqual(config.budget.max_episodes,400)

    def test_bad_attempt_budget_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)/'demo'
            render_template('artifact-fixture',root,goal='test')
            path = root/'nanorsi.toml'
            path.write_text(path.read_text().replace('max_steps = 10','max_steps = -1'))
            with self.assertRaises(ConfigError):
                load_config(path)
