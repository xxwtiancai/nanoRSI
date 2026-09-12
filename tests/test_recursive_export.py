import importlib.util
from pathlib import Path
import unittest


class RecursiveExportTests(unittest.TestCase):
    def test_training_export_preserves_measurements_and_excludes_private_extras(self):
        path = Path(__file__).resolve().parents[1] / 'examples/recursive_learning/export.py'
        spec = importlib.util.spec_from_file_location('digits_export', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertTrue(callable(getattr(module, 'public_training', None)), 'explicit training allowlist is required')
        record = {'status': 'completed', 'method': 'sft', 'steps': 24,
                  'process': {'argv': ['/private/command']}, 'private_config': 'DO-NOT-PUBLISH',
                  'result': {'method': 'sft', 'examples_seen': 768, 'sampling_sha256': 'a' * 64,
                             'checkpoint_path': '/private/checkpoint', 'task_ids': ['train-secret'],
                             'api_key': 'DO-NOT-PUBLISH', 'unrecognized_notes': 'private'}}
        public = module.public_training(record)
        self.assertEqual(public['steps'], 24)
        self.assertEqual(public['result'], {'method': 'sft', 'examples_seen': 768, 'sampling_sha256': 'a' * 64})
        self.assertNotIn('process', public)
        self.assertNotIn('private_config', public)
