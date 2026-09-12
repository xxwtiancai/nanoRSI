"""Scripted model fixtures prove integration, not learned model performance."""
import json
import tempfile
import unittest
from pathlib import Path

from nanorsi.gitops import Git
from nanorsi.templates import render_template
from tests.test_end_to_end import run_cli


MODEL = '''import difflib,json,sys
request=json.load(sys.stdin)
system=request['messages'][0]['content']
context=json.loads(request['messages'][1]['content'])
references=REFERENCES
if 'proposal agent' in system:
    path='target/agent/skills/inspect/SKILL.md'
    old=context['parent_files'][path]
    new=old+'\\nfixture-approved\\n'
    diff='diff --git a/'+path+' b/'+path+'\\n'+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+path,tofile='b/'+path))
    action={'diff':diff,'hypothesis':{'reason':'Scripted protocol fixture; not model learning'}}
elif 'fixture-approved' in system and len(request['messages'])==2:
    action={'tool':'write','path':'solution.py','content':references[context['instruction']]}
elif len(request['messages']) <= 4:
    action={'tool':'test'}
else:
    action={'tool':'final'}
print(json.dumps({'content':json.dumps(action),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''


def coding_workspace(directory):
    root = Path(directory) / 'coding'
    files = render_template('coding', root, goal='Offline integration fixture')
    assert 'evaluator/_skills.py' in files and 'adapters/python_tests.py' in files
    manifest_path = root / 'tasks/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    manifest['tasks'] = [next(t for t in manifest['tasks'] if t['split'] == split)
                         for split in ['train', 'validation', 'test']]
    manifest_path.write_text(json.dumps(manifest))
    references = {t['instruction']: t['expected_files']['solution.py'] for t in manifest['tasks']}
    (root / 'adapters/fixture.py').write_text(MODEL.replace('REFERENCES', repr(references)))
    config = root / 'nanorsi.toml'
    config.write_text(config.read_text().replace('adapters/model.py', 'adapters/fixture.py').replace('max_steps = 3', 'max_steps = 1'))
    Git(root).init()
    return root


class CodingLifecycleTests(unittest.TestCase):
    def call(self, root, *args):
        result = run_cli(*args, '--workspace', str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_coding_search_freeze_final_report_and_lineage(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = coding_workspace(tmp)
            self.call(root, 'run')
            events = [json.loads(line) for line in (root / 'lineage.jsonl').read_text().splitlines()]
            self.assertFalse(any(e.get('split') == 'test' for e in events))
            self.assertTrue(any(e.get('decision') == 'accepted' for e in events))
            context_path = next((root / '.nanorsi/runs').glob('*/proposal/context.json'))
            context = json.loads(context_path.read_text())
            feedback = context['train_results'][0]['feedback']
            self.assertIn('public_result', feedback)
            self.assertNotIn('expected_files', feedback)
            self.assertNotIn('private_tests', feedback)
            self.assertNotEqual(run_cli('final-test', '--workspace', str(root)).returncode, 0)
            self.call(root, 'report', '--format', 'html')
            self.assertIn('Final evaluation pending', (root / 'reports/report.html').read_text())
            self.call(root, 'freeze', '--repeats', '1')
            self.call(root, 'final-test')
            report = json.loads((root / 'reports/final.json').read_text())
            self.assertEqual([r['case_results'][0]['score'] for r in report['results']], [0, 0, 1])
            self.call(root, 'report', '--format', 'html')
            self.assertIn('+100.0 pp', (root / 'reports/report.html').read_text())
            self.call(root, 'verify')
            self.assertNotEqual(run_cli('step', '--workspace', str(root)).returncode, 0)

    def test_grading_helper_is_part_of_frozen_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = coding_workspace(tmp)
            self.call(root, 'baseline')
            helper = root / 'adapters/python_tests.py'
            helper.write_text(helper.read_text() + '\n# changed after baseline\n')
            result = run_cli('step', '--workspace', str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('frozen experiment contract changed', result.stderr)


if __name__ == '__main__':
    unittest.main()
