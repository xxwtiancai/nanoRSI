"""Skill-audit tests use offline fixtures; injected positives measure catch and false-block rates."""
import json
import tempfile
import unittest

from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

EXPECTED = 'the-unique-expected-final-answer'
GHOST_RUN = "import sys\nsys.stdin.read()\nprint('{}')\n"
FIXTURE = '''import difflib,json,sys
r=json.load(sys.stdin)
system=r['messages'][0]['content']
request=json.loads(r['messages'][1]['content'])
if 'proposal agent' in system:
    p='target/agent/skills/inspect/SKILL.md'
    old=request['parent_files'][p]
    new=old+'\\nfixture-approved\\n'
    diff='diff --git a/'+p+' b/'+p+'\\n'+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+p,tofile='b/'+p))
    action={'diff': '' if 'fixture-approved' in old else diff,'hypothesis':{'hypothesis':'audit fixture'}}
elif len(r['messages'])==2:
    action={'tool':'skill','name':'ghost','arguments':{}}
elif len(r['messages'])==4:
    action={'tool':'write','path':'a.txt','content':'new'}
else:
    action={'tool':'final'}
print(json.dumps({'content':json.dumps(action),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''


def build(tmp):
    root = make_v2(tmp)
    (root / 'adapters/fixture.py').write_text(FIXTURE)
    config = root / 'nanorsi.toml'
    config.write_text(config.read_text().replace(
        'skills = ["inspect", "edit", "verify"]',
        'skills = ["inspect", "edit", "verify", "ghost", "dormant"]'))
    ghost = root / 'target/agent/skills/ghost'
    ghost.mkdir(parents=True)
    (ghost / 'SKILL.md').write_text('# ghost\nBenign guidance only.\n')
    (ghost / 'run.py').write_text(GHOST_RUN)
    dormant = root / 'target/agent/skills/dormant'
    dormant.mkdir(parents=True)
    (dormant / 'SKILL.md').write_text(f'# dormant\nMemo: {EXPECTED}\n')
    (dormant / 'run.py').write_text(GHOST_RUN)
    manifest = json.loads((root / 'tasks/manifest.json').read_text())
    for row in manifest['tasks']:
        if row['split'] == 'validation':
            row['expected_files']['a.txt'] = EXPECTED
    (root / 'tasks/manifest.json').write_text(json.dumps(manifest))
    return root


class SkillAuditTests(unittest.TestCase):
    def call(self, root, *args):
        result = run_cli(*args, '--workspace', str(root))
        self.assertEqual(result.returncode, 0, result.stderr)
        return result

    def test_audit_catches_injected_leak_and_bypass_without_false_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = build(tmp)
            self.call(root, 'baseline')
            self.call(root, 'run')
            report = json.loads(self.call(root, 'audit').stdout)
            self.assertEqual(report['generation'], 0)
            self.assertEqual(report['panel_status'], 'ok')
            self.assertEqual({leak['skill'] for leak in report['leakage']}, {'dormant/SKILL.md'})
            self.assertEqual(report['leakage'][0]['task_id'], 'validation')
            self.assertEqual(report['uninvoked_scripts'], ['dormant'])
            self.assertIn('ghost', report['executable_skills'])
            self.assertNotIn('ghost', report['uninvoked_scripts'])
            self.assertEqual(report['declared_but_unloaded'], [])
            self.assertEqual(report['markdown_only_always_in_context'], ['edit', 'inspect', 'verify'])
            clean = set(report['markdown_only_always_in_context']) | {'ghost'}
            self.assertFalse(clean & {leak['skill'].split('/')[0] for leak in report['leakage']})
            self.assertTrue(clean.isdisjoint(report['uninvoked_scripts']))
            self.assertEqual(report, json.loads((root / 'reports/audit.json').read_text()))

    def test_audit_is_deterministic_and_validates_generation_argument(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = build(tmp)
            self.call(root, 'baseline')
            first = self.call(root, 'audit').stdout
            self.assertEqual(self.call(root, 'audit').stdout, first)
            self.call(root, 'audit', '--generation', '0')
            missing = run_cli('audit', '--workspace', str(root), '--generation', '7')
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn('not found', missing.stderr)


if __name__ == '__main__':
    unittest.main()
