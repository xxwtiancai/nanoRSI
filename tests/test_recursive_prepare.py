import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(importlib.util.find_spec('numpy'), 'optional NumPy unavailable')
class RecursivePreparationTests(unittest.TestCase):
    def test_prepared_workspace_is_an_independent_git_experiment(self):
        spec = importlib.util.spec_from_file_location('digits_prepare', ROOT / 'examples/recursive_learning/prepare.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        tasks = [{'task_id': split + '-0000', 'group_id': split, 'split': split,
                  'instruction': 'Predict a digit', 'input_files': {'features.json': '[' + ','.join(['0'] * 64) + ']'},
                  'expected_files': {'label.txt': '0'}} for split in ['train', 'validation', 'test']]
        with tempfile.TemporaryDirectory() as tmp:
            lab = module.prepare_workspace(Path(tmp) / 'lab', method='sft', seed=0, policy='frozen', manifest={'schema_version': 1, 'tasks': tasks})
            result = subprocess.run(['git', '-C', str(lab), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(Path(result.stdout.strip()).resolve(), lab.resolve())
