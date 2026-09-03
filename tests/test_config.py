import tempfile
import unittest
from pathlib import Path

from nanorsi.config import Config, ConfigError, load_config


class ConfigTests(unittest.TestCase):
    def test_loads_minimal_complete_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nanorsi.toml"
            path.write_text(
                """
                [experiment]
                id = "demo"
                goal = "Improve the demo"
                mode = "artifact"

                [surface]
                allow = ["target/**"]

                [proposer]
                command = ["python3", "proposer/propose.py"]

                [evaluator]
                command = ["python3", "evaluator/evaluate.py"]
                primary_metric = "score"
                direction = "maximize"

                [gate]
                minimum_improvement = 0.1

                [budget]
                max_steps = 3
                """.strip(),
                encoding="utf-8",
            )
            config = load_config(path)
            self.assertIsInstance(config, Config)
            self.assertEqual(config.experiment.mode, "artifact")
            self.assertEqual(config.surface.allow, ["target/**"])
            self.assertEqual(config.gate.minimum_improvement, 0.1)
            self.assertEqual(config.evaluator.timeout_s, 60)

    def test_rejects_unknown_top_level_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nanorsi.toml"
            path.write_text("[experiment]\nid='x'\n[extra]\nx=1\n", encoding="utf-8")
            with self.assertRaisesRegex(ConfigError, "Unknown config sections"):
                load_config(path)

    def test_rejects_shell_string_and_bad_direction(self):
        values = {
            "proposer": "python3 proposer.py",
            "evaluator_direction": "up",
        }
        for key, value in values.items():
            with self.subTest(key=key):
                text = """
                    [experiment]
                    id = "demo"
                    goal = "Improve"
                    mode = "artifact"
                    [surface]
                    allow = ["target/**"]
                    [proposer]
                    command = ["python3", "proposer/propose.py"]
                    [evaluator]
                    command = ["python3", "evaluator/evaluate.py"]
                    primary_metric = "score"
                    direction = "maximize"
                    [gate]
                    minimum_improvement = 0.1
                    [budget]
                    max_steps = 1
                    """.replace("direction = \"maximize\"", f"direction = \"{value}\"")
                if key == "proposer":
                    text = text.replace(
                        'command = ["python3", "proposer/propose.py"]',
                        f"command = '{value}'",
                    )
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "nanorsi.toml"
                    path.write_text(text, encoding="utf-8")
                    with self.assertRaises(ConfigError):
                        load_config(path)

    def test_model_mode_requires_external_training_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "nanorsi.toml"
            path.write_text(
                """
                [experiment]
                id = "model"
                goal = "Adapt"
                mode = "model"
                [surface]
                allow = ["target/**"]
                [proposer]
                command = ["python3", "propose.py"]
                [evaluator]
                command = ["python3", "evaluate.py"]
                primary_metric = "score"
                direction = "maximize"
                [gate]
                minimum_improvement = 0.1
                [budget]
                max_steps = 1
                """.strip(),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ConfigError, "training.command"):
                load_config(path)


if __name__ == "__main__":
    unittest.main()
