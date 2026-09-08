"""Deterministic protocol tests, not evidence of real model improvement."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from nanorsi.templates import render_template
from nanorsi.gitops import Git
from nanorsi.lineage import LineageStore
from tests.test_end_to_end import run_cli


FIXTURE_MODEL = '''import difflib,json,sys
r=json.load(sys.stdin)
system=r['messages'][0]['content']
request=json.loads(r['messages'][1]['content'])
if 'proposal agent' in system:
    p='target/agent/skills/inspect/SKILL.md'
    old=request['parent_files'][p]
    new=old+'\\nfixture-approved\\n'
    diff='diff --git a/'+p+' b/'+p+'\\n'+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+p,tofile='b/'+p))
    action={'diff': '' if 'fixture-approved' in old else diff,'hypothesis':{'hypothesis':'CI protocol fixture only'}}
elif 'fixture-approved' in system and len(r['messages'])==2:
    action={'tool':'write','path':'a.txt','content':'new'}
else:
    action={'tool':'final'}
print(json.dumps({'content':json.dumps(action),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''


def make_v2(directory, arm='frozen', steps=3, episodes=400):
    root = Path(directory)/'lab'
    render_template('skills',root,goal='Exercise the protocol')
    config = root/'nanorsi.toml'
    text = config.read_text().replace('adapters/model.py','adapters/fixture.py')
    text = text.replace('arm = "frozen"',f'arm = "{arm}"').replace('max_steps = 5',f'max_steps = {steps}')
    config.write_text(text.replace('max_episodes = 400',f'max_episodes = {episodes}'))
    (root/'adapters/fixture.py').write_text(FIXTURE_MODEL)
    tasks = [{'task_id':s,'group_id':s,'split':s,'instruction':'Replace old with new in a.txt',
              'input_files':{'a.txt':'old'},'expected_files':{'a.txt':'new'}} for s in ['train','validation','test']]
    (root/'tasks/manifest.json').write_text(json.dumps({'schema_version':1,'tasks':tasks}))
    Git(root).init()
    return root


def events(root):
    return [json.loads(line) for line in (root/'lineage.jsonl').read_text().splitlines()]


class V2LifecycleTests(unittest.TestCase):
    def call(self, root, *args):
        result = run_cli(*args,'--workspace',str(root))
        self.assertEqual(result.returncode,0,result.stderr)
        return result

    def test_run_freeze_test_isolated_and_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root,'run')
            before = events(root)
            self.assertEqual(len([e for e in before if e.get('event_type')=='attempt_started']),3)
            self.assertFalse(any(e.get('split')=='test' for e in before))
            self.assertEqual([e['generation'] for e in before if e.get('decision')=='accepted'],[1])
            for path in (root/'.nanorsi/runs').glob('*/proposal/context.json'):
                context = json.loads(path.read_text())
                self.assertEqual([c['task_id'] for c in context['train_results']],['train'])
                self.assertNotIn('gate_metrics',context)
            self.assertNotEqual(run_cli('final-test','--workspace',str(root)).returncode,0)
            self.call(root,'freeze','--repeats','1')
            self.assertNotEqual(run_cli('step','--workspace',str(root)).returncode,0)
            self.call(root,'final-test')
            report = json.loads((root/'reports/final.json').read_text())
            self.assertEqual([r['condition'] for r in report['results']],['baseline','no-skills','candidate'])
            self.assertEqual([r['case_results'][0]['score'] for r in report['results']],[0,0,1])
            self.assertIsNone(report['results'][2]['cost_usd'])
            self.assertEqual(len(report['search_proposals']),3)
            self.assertTrue(all(e['usage']['model_calls']==1 for e in report['search_proposals']))
            prior = len(events(root))
            self.call(root,'final-test')
            self.assertEqual(len(events(root)),prior)
            self.call(root,'verify')

    def test_proposer_actually_loads_frozen_or_accepted_skills(self):
        for arm in ['frozen','self-use']:
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as tmp:
                root = make_v2(tmp,arm=arm,steps=2)
                initial = hashlib.sha256((root/'target/agent/skills/inspect/SKILL.md').read_bytes()).hexdigest()
                self.call(root,'run')
                contexts = [(p,json.loads(p.read_text())) for p in (root/'.nanorsi/runs').glob('*/proposal/context.json')]
                path, context = next((p,c) for p,c in contexts if c['attempt_id']==2)
                trace = json.loads(path.with_name('trace.json').read_text())
                loaded = next(t['sha256'] for t in trace if t.get('event')=='skill_loaded' and t.get('name')=='inspect')
                self.assertEqual(loaded==initial,arm=='frozen')
                self.assertEqual(context['proposer_harness_commit']==context['parent_commit'],arm=='self-use')

    def test_contract_changes_and_episode_cap_prevent_calls(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp,episodes=1)
            self.call(root,'baseline')
            result = run_cli('step','--workspace',str(root))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('episode budget',result.stderr)
            self.assertEqual(len([e for e in events(root) if e.get('event_type')=='evaluation_started']),1)
            config = root/'nanorsi.toml'
            config.write_text(config.read_text().replace('max_turns = 8','max_turns = 7'))
            result = run_cli('step','--workspace',str(root))
            self.assertIn('contract changed',result.stderr)

    def test_artifact_tamper_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root,'baseline')
            path = next((root/'.nanorsi/baseline').glob('*/gate.json'))
            path.write_text('{}')
            result = run_cli('verify','--workspace',str(root))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('artifact',result.stderr)

    def test_freeze_requires_recovery_of_dangling_attempt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            self.call(root,'baseline')
            LineageStore.initialize(root).append({'event_type':'attempt_started','attempt_id':1})
            result = run_cli('freeze','--workspace',str(root))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('recover',result.stderr)
            self.call(root,'recover')
            self.call(root,'freeze')

    def test_v2_cannot_downgrade_result_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            evaluator=root/'evaluator/evaluate.py'
            evaluator.write_text('''import json,os
from pathlib import Path
p={'schema_version':1,'status':'ok','metrics':{'score':1},'constraints':{},'cost_usd':None,'duration_ms':0,'case_results':[{'task_id':'validation','group_id':'validation','repeat_id':0}]}
Path(os.environ['NANORSI_RESULT_PATH']).write_text(json.dumps(p))
''')
            result=run_cli('baseline','--workspace',str(root))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('schema',result.stderr)

    def test_training_panel_must_match_reserved_seed_selection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            manifest = root/'tasks/manifest.json'
            data = json.loads(manifest.read_text())
            data['tasks'] += [{**data['tasks'][0],'task_id':f'train{i}'} for i in range(4)]
            manifest.write_text(json.dumps(data))
            (root/'evaluator/evaluate.py').write_text('''import json,os
from pathlib import Path
rows=json.loads(Path(os.environ['NANORSI_TASK_MANIFEST']).read_text())['tasks']
rows=[r for r in rows if r['split']==os.environ['NANORSI_SPLIT']][:4]
usage={'model_calls':0,'input_tokens':0,'output_tokens':0,'cost_usd':0}
cases=[{'task_id':r['task_id'],'group_id':r['group_id'],'repeat_id':0,'score':0,'status':'task_failure','trace':[],'skill_hashes':{},'usage':usage,'duration_ms':0} for r in rows]
Path(os.environ['NANORSI_RESULT_PATH']).write_text(json.dumps({'schema_version':2,'status':'ok','metrics':{'score':0},'constraints':{},'case_results':cases,'usage':usage,'cost_usd':0,'duration_ms':0}))
''')
            self.call(root,'baseline')
            result=run_cli('step','--workspace',str(root))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('reserved task/repeat panel',result.stderr)
