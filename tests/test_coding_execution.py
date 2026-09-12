import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'src/nanorsi/templates/skills'
CODING = ROOT / 'src/nanorsi/templates/coding'
PUBLIC = "import unittest\nfrom solution import add\nclass Public(unittest.TestCase):\n def test_add(self): self.assertEqual(add(1, 2), 3)\n"
PRIVATE = "import unittest\nfrom solution import add\nclass Private(unittest.TestCase):\n def test_negative(self): self.assertEqual(add(-4, 2), -2, 'PRIVATE_MARKER')\n"
REFERENCE = "# REFERENCE_MARKER\ndef add(a, b): return a + b\n"
ALTERNATE = "def add(a, b):\n return sum((a, b))\n"


def task():
    return {'task_id': 'add', 'group_id': 'arithmetic', 'split': 'train', 'instruction': 'Implement add', 'input_files': {'solution.py': 'def add(a,b): return 0\n'}, 'expected_files': {'solution.py': REFERENCE}, 'grading': {'kind': 'python-unittest', 'public_tests': {'test_public.py': PUBLIC}, 'private_tests': {'test_private.py': PRIVATE}, 'timeout_s': 2}}


class CodingExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.env_patch = patch.dict(os.environ, {"PYTHONPATH": str(ROOT / "src")})
        self.env_patch.start()
        self.addCleanup(self.env_patch.stop)
        shutil.copytree(SKILLS, self.root, dirs_exist_ok=True)
        shutil.copyfile(SKILLS / 'evaluator/evaluate.py', self.root / 'evaluator/_skills.py')
        if CODING.exists():
            shutil.copytree(CODING, self.root, dirs_exist_ok=True)

    def evaluator(self):
        self.assertTrue((CODING / 'evaluator/evaluate.py').is_file(), 'coding evaluator must exist')
        with patch.object(sys, 'path', [str(self.root / 'evaluator'), *sys.path]):
            sys.modules.pop('_skills', None)
            return runpy.run_path(str(self.root / 'evaluator/evaluate.py'))

    def bridge(self, actions):
        path = self.root / 'bridge.py'
        path.write_text('import json,sys\nr=json.load(sys.stdin)\nassert "PRIVATE_MARKER" not in json.dumps(r)\nassert "REFERENCE_MARKER" not in json.dumps(r)\nn=sum(m["role"]=="assistant" for m in r["messages"])\na=' + repr(actions) + '\nprint(json.dumps({"content":json.dumps(a[min(n,len(a)-1)]),"usage":{"input_tokens":1,"output_tokens":1,"cost_usd":0.01}}))\n')
        return {'model_command': [sys.executable, str(path)], 'skills': [], 'timeout_s': 2, 'max_turns': 8}

    def run_runner(self, selected, actions):
        result = subprocess.run([sys.executable, str(self.root / 'target/agent/run.py')], cwd=self.root, input=json.dumps({'mode': 'task', 'task': selected, 'agent': self.bridge(actions)}), text=True, capture_output=True, check=True)
        return json.loads(result.stdout)

    def test_public_test_tool_allows_test_fix_test_final(self):
        selected = {k: task()[k] for k in ('task_id', 'instruction', 'input_files')}
        selected.update(public_tests={'test_public.py': PUBLIC}, test_timeout_s=2)
        result = self.run_runner(selected, [{'tool': 'test'}, {'tool': 'write', 'path': 'solution.py', 'content': ALTERNATE}, {'tool': 'test'}, {'tool': 'final'}])
        self.assertEqual(result['status'], 'ok', result)
        self.assertEqual(result['output_files'], {'solution.py': ALTERNATE})
        tests = [entry for entry in result['trace'] if entry.get('tool') == 'test']
        self.assertEqual([entry['status'] for entry in tests], ['task_failure', 'ok'])
        self.assertEqual(result['usage']['model_calls'], 4)

    def test_behavioral_grading_accepts_alternative_and_rejects_wrong(self):
        module = self.evaluator()
        with patch('os.getcwd', return_value=str(self.root)):
            for code, expected in [(ALTERNATE, (1.0, 'ok')), ('def add(a,b): return 3\n', (0.0, 'task_failure'))]:
                result = {'status': 'ok', 'output_files': {'solution.py': code}, 'duration_ms': 0}
                self.assertEqual(module['_grade'](task(), result), expected)
                feedback = module['_training_feedback'](task(), result)
                self.assertNotIn('PRIVATE_MARKER', json.dumps(feedback))
                self.assertNotIn('REFERENCE_MARKER', json.dumps(feedback))

    def test_timeout_output_limit_and_untrusted_test_names(self):
        module = self.evaluator()
        with patch('os.getcwd', return_value=str(self.root)):
            for code, status in [('while True: pass\n', 'timeout'), ('print("x" * 200000)\ndef add(a,b):return a+b\n', 'output_limit'), ('def add(a,b):return 0\n', 'task_failure')]:
                selected = task()
                selected['grading']['timeout_s'] = 0.2
                result = {'status': 'ok', 'output_files': {'solution.py': code}, 'duration_ms': 0}
                self.assertEqual(module['_grade'](selected, result), (0.0, status))

    def test_manifest_rejects_invalid_grading(self):
        module = self.evaluator()
        invalid = [None, {}, {'kind': 'shell'}, {**task()['grading'], 'timeout_s': True}, {**task()['grading'], 'timeout_s': 11}, {**task()['grading'], 'public_tests': {'../test_escape.py': PUBLIC}}, {**task()['grading'], 'private_tests': {'test_x.py': 42}}, {**task()['grading'], 'public_tests': {}}, {**task()['grading'], 'private_tests': {}}]
        for grading in invalid:
            selected = task()
            selected['grading'] = grading
            path = self.root / 'manifest.json'
            path.write_text(json.dumps({'schema_version': 1, 'tasks': [selected]}))
            with self.subTest(grading=grading), self.assertRaises(ValueError):
                module['_manifest'](path)

    def test_training_and_validation_do_not_expose_hidden_tests_or_reference(self):
        module = self.evaluator()
        agent = self.bridge([{'tool': 'write', 'path': 'solution.py', 'content': ALTERNATE}, {'tool': 'test'}, {'tool': 'final'}])
        for split in ('train', 'validation'):
            selected = task()
            selected['split'] = split
            manifest = self.root / 'manifest.json'
            manifest.write_text(json.dumps({'schema_version': 1, 'tasks': [selected]}))
            env = {'NANORSI_SPLIT': split, 'NANORSI_TASK_MANIFEST': str(manifest), 'NANORSI_RESULT_PATH': str(self.root / 'result.json'), 'NANORSI_AGENT_CONFIG': json.dumps(agent)}
            with patch.dict(os.environ, env), patch('os.getcwd', return_value=str(self.root)):
                result = module['evaluate']()
            self.assertEqual(result['metrics']['score'], 1.0, result)
            self.assertEqual(result['schema_version'], 2)
            self.assertEqual(result['usage']['model_calls'], 3)
            self.assertNotIn('PRIVATE_MARKER', json.dumps(result))
            self.assertNotIn('REFERENCE_MARKER', json.dumps(result))

    def test_early_success_exit_cannot_pass_without_tests(self):
        module = self.evaluator()
        for code in ("import sys; sys.exit(0)\n", "import os; os._exit(0)\n"):
            result = {"status": "ok", "output_files": {"solution.py": code}}
            self.assertEqual(module["_grade"](task(), result), (0.0, "task_failure"))

    def test_success_marker_is_separate_from_candidate_output(self):
        module = self.evaluator()
        result = {"status": "ok", "output_files": {"solution.py": "print('diagnostic', end='')\n" + ALTERNATE}}
        self.assertEqual(module["_grade"](task(), result), (1.0, "ok"))
        self.assertNotIn("nanorsi-tests-passed:", json.dumps(module["_training_feedback"](task(), result)))

    def test_skipped_and_expected_failure_suites_cannot_pass(self):
        module = self.evaluator()
        sources = {
            "skipped": "import unittest\nclass Required(unittest.TestCase):\n @unittest.skip('unavailable')\n def test_required(self): self.fail()\n",
            "expected_failure": "import unittest\nclass Required(unittest.TestCase):\n @unittest.expectedFailure\n def test_required(self): self.fail()\n",
            "partially_skipped": "import unittest\nclass Required(unittest.TestCase):\n def test_executed(self): self.assertTrue(True)\n @unittest.skip('unavailable')\n def test_required(self): self.fail()\n",
        }
        for name, source in sources.items():
            for visibility in ("public_tests", "private_tests"):
                selected = task()
                selected["grading"][visibility] = {"test_required.py": source}
                result = {"status": "ok", "output_files": {"solution.py": ALTERNATE}}
                with self.subTest(name=name, visibility=visibility):
                    self.assertEqual(module["_grade"](selected, result), (0.0, "task_failure"))

    def test_empty_suite_cannot_pass(self):
        module = self.evaluator()
        selected = task()
        selected["grading"]["public_tests"] = {"test_empty.py": "pass\n"}
        result = {"status": "ok", "output_files": {"solution.py": ALTERNATE}}
        self.assertEqual(module["_grade"](selected, result), (0.0, "task_failure"))

    def test_unexpected_output_files_cannot_replace_tests(self):
        module = self.evaluator()
        for extra in ("unittest.py", "test_public.py", "../solution.py"):
            result = {"status": "ok", "output_files": {"solution.py": ALTERNATE, extra: "pass\n"}}
            self.assertEqual(module["_grade"](task(), result), (0.0, "task_failure"))


    def test_manifest_rejects_noncanonical_workspace_paths(self):
        module = self.evaluator()
        for name in ("./solution.py", "dir//solution.py", "dir/../solution.py", "a\\solution.py", "/solution.py", "__pycache__/solution.py"):
            selected = task()
            selected["input_files"] = {name: ALTERNATE}
            path = self.root / "manifest.json"
            path.write_text(json.dumps({"schema_version": 1, "tasks": [selected]}))
            with self.subTest(name=name), self.assertRaises(ValueError):
                module["_manifest"](path)

    def test_test_tool_rejects_command_override_and_invalid_timeout(self):
        selected = {k: task()[k] for k in ("task_id", "instruction", "input_files")}
        selected.update(public_tests={"test_public.py": PUBLIC}, test_timeout_s=2)
        result = self.run_runner(selected, [{"tool": "test", "command": "anything"}, {"tool": "final"}])
        self.assertEqual(result["status"], "error")
        self.assertIn("test accepts no arguments", json.dumps(result))
        selected["test_timeout_s"] = 11
        result = self.run_runner(selected, [{"tool": "final"}])
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["usage"]["model_calls"], 0)

    def test_evaluator_uses_protected_helper_not_target_code(self):
        self.assertTrue((self.root / "adapters/python_tests.py").is_file())
        (self.root / "target/agent/python_tests.py").write_text("raise RuntimeError('target helper loaded')\n")
        module = self.evaluator()
        result = {"status": "ok", "output_files": {"solution.py": ALTERNATE}}
        self.assertEqual(module["_grade"](task(), result), (1.0, "ok"))
        selected = {k: task()[k] for k in ("task_id", "instruction", "input_files")}
        selected.update(public_tests={"test_public.py": PUBLIC}, test_timeout_s=2)
        result = self.run_runner(selected, [{"tool": "test"}, {"tool": "final"}])
        self.assertEqual(result["status"], "ok")

    def test_test_tool_unavailable_without_public_tests(self):
        selected = {k: task()[k] for k in ('task_id', 'instruction', 'input_files')}
        result = self.run_runner(selected, [{'tool': 'test'}, {'tool': 'final'}])
        self.assertEqual(result['status'], 'error')


if __name__ == '__main__':
    unittest.main()
