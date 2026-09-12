"""CPU fixtures exercise real snapshot training without network or credentials."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from nanorsi import cli, loop
from nanorsi.config import ConfigError, load_config
from nanorsi.gitops import Git
from nanorsi.lineage import LineageStore
from nanorsi.surface import SurfacePolicy
from tests.test_v2_lifecycle import make_v2


EVALUATOR = '''import json,os,random
from pathlib import Path
rows=json.loads(Path(os.environ['NANORSI_TASK_MANIFEST']).read_text())['tasks']
rows=[r for r in rows if r['split']==os.environ['NANORSI_SPLIT']]
if os.environ['NANORSI_SPLIT']=='train' and len(rows)>4:
 rows=random.Random(int(os.environ['NANORSI_SEED'])).sample(rows,4)
score=json.loads(Path('target/model.json').read_text())['weight']
usage={'model_calls':0,'input_tokens':0,'output_tokens':0,'cost_usd':0}
cases=[{'task_id':r['task_id'],'group_id':r['group_id'],'repeat_id':int(os.environ['NANORSI_REPEAT_ID']),'score':score,'status':'ok','trace':[],'skill_hashes':{},'usage':usage,'duration_ms':0} for r in rows]
Path(os.environ['NANORSI_RESULT_PATH']).write_text(json.dumps({'schema_version':2,'status':'ok','metrics':{'score':score,'loss':1-score},'constraints':{},'case_results':cases,'usage':usage,'cost_usd':0,'duration_ms':0}))
'''
PROPOSER = '''import json,os
from pathlib import Path
out=Path(os.environ['NANORSI_PROPOSAL_DIR'])
(out/'proposal.diff').write_text('')
(out/'hypothesis.json').write_text(json.dumps({'hypothesis':'train from checkpoint'}))
'''
TRAINER = '''import hashlib,json,os
from pathlib import Path
p=Path(os.environ['NANORSI_CHECKPOINT_PATH'])
d=Path(os.environ['NANORSI_TRAINING_DATA_PATH'])
initial=hashlib.sha256(p.read_bytes()).hexdigest()
rows=json.loads(d.read_text())['tasks']
assert all(r['split']=='train' for r in rows)
p.write_text(json.dumps({'weight':min(1,json.loads(p.read_text())['weight']+1)}))
result={'schema_version':1,'status':'completed','checkpoint_path':str(p),'checkpoint_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'method':'fixture','steps':1,'duration_ms':0,'data_sha256':hashlib.sha256(d.read_bytes()).hexdigest(),'initial_checkpoint_sha256':initial}
Path(os.environ['NANORSI_TRAINING_RESULT_PATH']).write_text(json.dumps(result))
'''


def workspace(tmp, mode='model', trainer=TRAINER, conditions=None):
    root=Path(tmp)/'lab'
    for name in ['target','trainer','evaluator','proposer','tasks','adapters']:
        (root/name).mkdir(parents=True,exist_ok=True)
    final='' if conditions is None else 'final_conditions = '+json.dumps(conditions)+'\n'
    training='' if mode!='model' else '''[training]
command = ["python3", "trainer/train.py"]
compute_budget_s = 2
checkpoint = "target/model.json"
max_checkpoint_bytes = 1024
'''
    (root/'nanorsi.toml').write_text(f'''[experiment]
schema_version = 2
id = "cpu"
goal = "CPU fixture"
mode = "{mode}"
{final}[surface]
allow = ["target/**"]
[proposer]
command = ["python3", "proposer/propose.py"]
[evaluator]
command = ["python3", "evaluator/evaluate.py"]
primary_metric = "score"
[gate]
minimum_improvement = 0.1
[budget]
max_steps = 3
max_episodes = 40
[data]
manifest = "tasks/manifest.json"
{training}''')
    (root/'target/model.json').write_text('{"weight":0}')
    (root/'adapters/.keep').write_text('')
    (root/'trainer/train.py').write_text(trainer)
    (root/'proposer/propose.py').write_text(PROPOSER)
    (root/'evaluator/evaluate.py').write_text(EVALUATOR)
    rows=[{'task_id':s,'group_id':s,'split':s,'instruction':'predict', 'input_files':{'x':'1'},'expected_files':{'y':'1'}} for s in ['train','validation','test']]
    (root/'tasks/manifest.json').write_text(json.dumps({'schema_version':1,'tasks':rows}))
    (root/'.gitignore').write_text('.nanorsi/\nlineage.jsonl\nreports/\n__pycache__/\n')
    Git(root).init()
    return root


class MultilevelKernelTests(unittest.TestCase):
    def test_cli_accepts_explicit_legacy_fixture_names(self):
        for name in ['artifact-fixture','harness-fixture','model-contract']:
            with self.subTest(name=name):
                args=cli._parser().parse_args(['new',name,'/tmp/nanorsi-parser-fixture'])
                self.assertEqual(args.template,name)

    def test_modes_default_conditions_and_optional_agent(self):
        for mode in ['artifact','model']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                config=load_config(workspace(tmp,mode)/'nanorsi.toml')
                self.assertEqual(config.agent,{})
                self.assertEqual(config.experiment.final_conditions,['baseline','candidate'])
        with tempfile.TemporaryDirectory() as tmp:
            config=load_config(make_v2(tmp)/'nanorsi.toml')
            self.assertEqual(config.experiment.final_conditions,['baseline','no-skills','candidate'])

    def test_explicit_condition_contract_rejects_missing_duplicate_unknown(self):
        for conditions in [['candidate'],['baseline','candidate','candidate'],['baseline','other','candidate']]:
            with self.subTest(conditions=conditions), tempfile.TemporaryDirectory() as tmp:
                with self.assertRaisesRegex(ConfigError,'final_conditions'):
                    load_config(workspace(tmp,conditions=conditions)/'nanorsi.toml')

    def test_training_changes_checkpoint_and_final_reloads_frozen_commits(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp)
            baseline=cli._baseline(root)
            self.assertEqual(baseline['gate_metrics']['score'],0)
            candidate=cli._step(root)
            self.assertEqual(candidate['decision'],'accepted')
            self.assertEqual(candidate['training']['method'],'fixture')
            self.assertEqual(candidate['training']['steps'],1)
            self.assertIn('target/model.json',candidate['changed_paths'])
            train=candidate['training']
            data=json.loads((root/train['data_path']).read_text())
            self.assertEqual([r['split'] for r in data['tasks']],['train'])
            self.assertNotEqual(train['checkpoint_sha256'],train['initial_checkpoint_sha256'])
            config=load_config(root/'nanorsi.toml')
            frozen=loop.freeze(root,config,1)
            self.assertEqual(frozen['conditions'],['baseline','candidate'])
            self.assertEqual(frozen['mode'],'model')
            self.assertEqual(frozen['metric'],{'name':'score','direction':'maximize'})
            (root/'target/model.json').write_text('{"weight":42}')
            with patch('nanorsi.training.run_training', side_effect=AssertionError('final retrained')):
                report=json.loads(loop.final_test(root,config).read_text())
            self.assertEqual([r['metrics']['score'] for r in report['results']],[0,1])
            self.assertEqual(report['results'][1]['checkpoint']['sha256'],train['checkpoint_sha256'])
            LineageStore.initialize(root).verify()

    def test_successful_training_without_checkpoint_change_is_noop(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp,trainer=TRAINER.replace("min(1,json.loads(p.read_text())['weight']+1)","json.loads(p.read_text())['weight']"))
            (root/'target/model.json').write_text(json.dumps({'weight':0}))
            cli._baseline(root)
            outcome=cli._step(root)
            self.assertEqual(outcome['decision'],'no-op')
            self.assertEqual(outcome['training']['status'],'completed')
            self.assertFalse(Git(root).ref_exists('nanorsi/gen-1'))

    def test_training_failures_preserve_evidence_and_never_promote(self):
        variants={
            'exit': 'raise SystemExit(7)',
            'timeout': 'import time;time.sleep(5)',
            'output': 'print("x"*2000000)',
            'missing_result': 'pass',
            'invalid_result': TRAINER+"\nPath(os.environ['NANORSI_TRAINING_RESULT_PATH']).write_text('{}')\n",
            'result_nan': TRAINER+"\nresult['loss']=float('nan');Path(os.environ['NANORSI_TRAINING_RESULT_PATH']).write_text(json.dumps(result))\n",
            'result_cost': TRAINER+"\nresult['cost_usd']='invalid';Path(os.environ['NANORSI_TRAINING_RESULT_PATH']).write_text(json.dumps(result))\n",
            'data_tamper': TRAINER+"\nd.write_text('{}')\n",
            'missing': TRAINER+"\np.unlink()\n",
            'oversize': TRAINER+"\np.write_bytes(b'x'*2048)\n",
            'symlink': TRAINER+"\np.unlink();p.symlink_to('other.json')\n",
            'hash': TRAINER.replace("'checkpoint_sha256':hashlib.sha256(p.read_bytes()).hexdigest()","'checkpoint_sha256':'wrong'"),
            'ignored': TRAINER+"\nPath('.nanorsi').mkdir();Path('.nanorsi/tamper').write_text('bad')\n",
            'tamper': TRAINER+"\nPath('evaluator/evaluate.py').write_text('# tampered')\n",
        }
        for name,trainer in variants.items():
            with self.subTest(name=name),tempfile.TemporaryDirectory() as tmp:
                root=workspace(tmp,trainer=trainer)
                cli._baseline(root)
                with self.assertRaises(Exception):
                    cli._step(root)
                store=LineageStore.initialize(root)
                self.assertEqual(store.latest_accepted()['generation'],0)
                failed=store.events()[-1]
                self.assertEqual(failed['event_type'],'attempt_failed')
                evidence=next((root/ref['path'] for key,ref in failed['artifacts'].items() if key=='training/evidence.json'),None)
                self.assertIsNotNone(evidence)
                self.assertEqual(json.loads(evidence.read_text())['status'],'failed')
                store.verify()

    def test_comparison_hash_binds_execution_contract_but_not_experimental_factors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp)
            from nanorsi.contracts import comparison_hash
            config=load_config(root/'nanorsi.toml')
            original=comparison_hash(root,config)
            for name in ['trainer/train.py','proposer/propose.py','evaluator/evaluate.py','adapters/bridge.py','target/model.json']:
                with self.subTest(file=name):
                    path=root/name;old=path.read_bytes() if path.exists() else None
                    path.write_bytes((old or b'')+b'\n# altered')
                    self.assertNotEqual(comparison_hash(root,config),original)
                    path.unlink() if old is None else path.write_bytes(old)
            path=root/'nanorsi.toml';old=path.read_text()
            for replacement in ['max_steps = 4','max_episodes = 41','minimum_improvement = 0.2','compute_budget_s = 3']:
                key=replacement.split(' = ')[0]
                import re
                path.write_text(re.sub(key+r' = [^\n]+',replacement,old))
                self.assertNotEqual(comparison_hash(root,load_config(path)),original)
            path.write_text(old.replace('id = "cpu"','id = "other"\narm = "self-use"\nseed = 31'))
            self.assertEqual(comparison_hash(root,load_config(path)),original)
            path.write_text(old)
            from dataclasses import replace
            self.assertEqual(comparison_hash(root,replace(config,agent={'api_key_file':'/a'})),comparison_hash(root,replace(config,agent={'api_key_file':'/b'})))

    def test_explicit_final_subset_and_legacy_freeze_fallback(self):
        for legacy in [False,True]:
            with self.subTest(legacy=legacy),tempfile.TemporaryDirectory() as tmp:
                root=make_v2(tmp)
                path=root/'nanorsi.toml'
                if not legacy:
                    path.write_text(path.read_text().replace('schema_version = 2','schema_version = 2\nfinal_conditions = ["candidate", "baseline"]'))
                cli._baseline(root)
                config=load_config(path)
                if legacy:
                    store=LineageStore.initialize(root);baseline=store.latest_accepted()
                    store.append({'event_type':'freeze','repeats':1,'baseline_commit':baseline['candidate_commit'],'candidate_commit':baseline['candidate_commit'],'manifest_hash':loop.identity(root,config),'comparison_hash':'legacy','experiment_id':config.experiment.id,'arm':config.experiment.arm,'seed':config.experiment.seed})
                else:
                    loop.freeze(root,config,1)
                report=json.loads(loop.final_test(root,config).read_text())
                expected=['baseline','no-skills','candidate'] if legacy else ['candidate','baseline']
                self.assertEqual([r['condition'] for r in report['results']],expected)

    def test_model_evaluation_cannot_retrain_or_mutate_saved_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp)
            path=root/'evaluator/evaluate.py'
            path.write_text(path.read_text()+"\nPath('target/model.json').write_text('{\"weight\":1}')\n")
            with self.assertRaisesRegex(RuntimeError,'checkpoint'):
                cli._baseline(root)
            self.assertFalse(any(e.get('event_type')=='generation' for e in LineageStore.initialize(root).events()))

    def test_comparison_allows_different_reported_repeat_counts(self):
        identities=[]
        for repeats in [1,2]:
            with tempfile.TemporaryDirectory() as tmp:
                root=workspace(tmp)
                cli._baseline(root)
                frozen=loop.freeze(root,load_config(root/'nanorsi.toml'),repeats)
                self.assertEqual(frozen['repeats'],repeats)
                identities.append(frozen['comparison_hash'])
        self.assertEqual(*identities)

    def test_doctor_cpu_mode_does_not_require_agent(self):
        from nanorsi.doctor import doctor
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp)
            ready,output=doctor(root)
            self.assertTrue(ready,output)
            self.assertIn('checkpoint:',output)
            self.assertNotIn('model connection: not checked',output)
            ready,output=doctor(root,check_model=True)
            self.assertFalse(ready)
            self.assertIn('configured agent',output)

    def test_thinking_configure_and_bridge_check(self):
        from nanorsi.configure import configure
        from nanorsi.doctor import _check_model
        from nanorsi.process import ProcessResult
        with tempfile.TemporaryDirectory() as tmp:
            root=make_v2(tmp)
            configure(root,model='fixture',base_url='http://localhost:8000/v1',no_api_key=True,thinking='disabled')
            config=load_config(root/'nanorsi.toml')
            self.assertEqual(config.agent['thinking'],'disabled')
            args=cli._parser().parse_args(['configure','--model','fixture','--base-url','http://localhost:8000/v1','--no-api-key','--thinking','disabled'])
            self.assertEqual(args.thinking,'disabled')
            response=ProcessResult((),0,json.dumps({'content':json.dumps({'tool':'final'})}),'',False)
            with patch('nanorsi.doctor.run_argv',return_value=response) as bridge:
                self.assertTrue(_check_model(root,config)[0])
                self.assertEqual(json.loads(bridge.call_args.kwargs['input_text'])['thinking'],'disabled')
            path=root/'nanorsi.toml';path.write_text(path.read_text().replace('thinking = "disabled"','thinking = "other"'))
            with self.assertRaisesRegex(ConfigError,'thinking'):
                load_config(path)

    def test_reservations_count_pending_worst_case_and_actual_once(self):
        reservation={'event_type':'episode_reservation','reservation_id':'a','episodes':5,'phase':'search'}
        started={'event_type':'evaluation_started','reservation_id':'a','episodes':2,'phase':'search'}
        settled={'event_type':'episode_reservation_settled','reservation_id':'a'}
        self.assertEqual(loop.search_episode_count([reservation,started]),5)
        self.assertEqual(loop.search_episode_count([reservation,started,settled]),2)

    def test_trainer_is_immutable_even_if_surface_is_broad(self):
        with self.assertRaisesRegex(ValueError,'mutable surface'):
            SurfacePolicy(['**'],[]).validate_paths(['trainer/train.py'])

    def test_v2_rejects_mutable_local_training_scripts_and_executables(self):
        commands=[['python3','-mtarget.future'],['python3','-Imtarget.future'],['env','-C','target','python3','future.py'],['env','-S','python3 target/future.py'],['env','TRAIN_MODE=train','python3','target/future.py'],['sh','-e','target/future.sh'],['python3','-m','target.future'],['env','python3','target/future.py'],['sh','target/train.sh'],['python3','-m','target.train'],['env','python3','target/train.py'],['python3','target/train.py'],['python3','target/not-created.py'],['python3','-u','target/train.py'],
                  ['python3','-X','utf8','target/train.py'],['./target/train'],
                  ['python3','trainer/linked.py']]
        for command in commands:
            with self.subTest(command=command),tempfile.TemporaryDirectory() as tmp:
                root=workspace(tmp)
                (root/'target/train.py').write_text(TRAINER)
                (root/'target/train').write_text(TRAINER)
                (root/'trainer/linked.py').symlink_to('../target/train.py')
                path=root/'nanorsi.toml'
                path.write_text(path.read_text().replace('["python3", "trainer/train.py"]',json.dumps(command)))
                with self.assertRaisesRegex(ConfigError,'training.command.*mutable'):
                    load_config(path)

    def test_shell_argument_options_require_a_protected_wrapper(self):
        for option in ['--rcfile','--init-file']:
            with self.subTest(option=option),tempfile.TemporaryDirectory() as tmp:
                root=workspace(tmp);path=root/'nanorsi.toml'
                (root/'trainer/rc').write_text('')
                (root/'target/train.sh').write_text('exit 0')
                command=['bash',option,'trainer/rc','target/train.sh']
                path.write_text(path.read_text().replace('["python3", "trainer/train.py"]',json.dumps(command)))
                with self.assertRaisesRegex(ConfigError,'protected wrapper'):
                    load_config(path)

    def test_v1_custom_proposer_retains_legacy_surface_list(self):
        from nanorsi.templates import render_template
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'legacy'
            render_template('artifact-fixture',root,goal='legacy compatibility')
            path=root/'proposer/propose.py'
            source=path.read_text().replace('output = Path',"context = json.loads(Path(os.environ['NANORSI_CONTEXT_PATH']).read_text())\nassert isinstance(context['surface'], list)\noutput = Path")
            path.write_text('import json\n'+source)
            Git(root).init()
            cli._baseline(root)
            self.assertEqual(cli._step(root)['decision'],'accepted')
            context=json.loads(next((root/'.nanorsi/runs').glob('*/proposal/context.json')).read_text())
            self.assertEqual(context['surface'],load_config(root/'nanorsi.toml').surface.allow)

    def test_training_guard_preserves_protected_external_module_and_v1_commands(self):
        commands=[['python3','trainer/train.py'],['python3','-m','installed_trainer'],
                  ['/external/installed/trainer'],['env','python3','-m','installed_trainer'],
                  ['sh','trainer/train.sh'],['python3','-c','print("trainer")'],['sh','-c','python3 trainer/train.py']]
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp);path=root/'nanorsi.toml';original=path.read_text()
            for command in commands:
                with self.subTest(command=command):
                    path.write_text(original.replace('["python3", "trainer/train.py"]',json.dumps(command)))
                    self.assertEqual(load_config(path).training['command'],command)
            (root/'target/train.py').write_text(TRAINER)
            path.write_text(original.replace('schema_version = 2','schema_version = 1').replace('trainer/train.py','target/train.py'))
            self.assertEqual(load_config(path).training['command'],['python3','target/train.py'])

    def test_absent_mutable_module_cannot_start_or_reach_final(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp);path=root/'nanorsi.toml'
            path.write_text(path.read_text().replace('["python3", "trainer/train.py"]','["python3", "-m", "target.future"]'))
            for command in ['baseline','step','freeze','final-test']:
                with self.subTest(command=command):
                    from tests.test_end_to_end import run_cli
                    result=run_cli(command,'--workspace',str(root))
                    self.assertNotEqual(result.returncode,0)
                    self.assertIn('training.command references a mutable',result.stderr)
            self.assertFalse((root/'lineage.jsonl').exists())
            self.assertFalse((root/'reports/final.json').exists())

    def test_candidate_training_revalidates_config_before_subprocess(self):
        from nanorsi.training import run_training
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp);config=load_config(root/'nanorsi.toml');parent=cli._baseline(root)
            git=Git(root);run_dir=root/'.nanorsi/runs/revalidate'
            with git.worktree(parent['candidate_commit'],root/'.nanorsi/worktrees/revalidate') as candidate:
                path=candidate/'nanorsi.toml'
                path.write_text(path.read_text().replace('["python3", "trainer/train.py"]','["python3", "-m", "target.future"]'))
                with self.assertRaisesRegex(ConfigError,'training.command.*mutable'):
                    run_training(root,config,candidate,run_dir,git,parent['candidate_commit'],parent)
                self.assertEqual(json.loads((candidate/'target/model.json').read_text())['weight'],0)
            evidence=json.loads((run_dir/'training/evidence.json').read_text())
            self.assertEqual(evidence['status'],'failed')
            self.assertNotIn('process',evidence)
            loop.freeze(root,config,1)
            report=json.loads(loop.final_test(root,config).read_text())
            self.assertEqual([r['metrics']['score'] for r in report['results']],[0,0])

    def test_model_training_config_and_checkpoint_are_bounded(self):
        for old,new in [('compute_budget_s = 2','compute_budget_s = 0'),('max_checkpoint_bytes = 1024','max_checkpoint_bytes = 0'),('checkpoint = "target/model.json"','checkpoint = "evaluator/model.json"')]:
            with self.subTest(new=new), tempfile.TemporaryDirectory() as tmp:
                root=workspace(tmp)
                path=root/'nanorsi.toml';path.write_text(path.read_text().replace(old,new))
                with self.assertRaises(ConfigError):
                    load_config(path)

    def test_promote_false_returns_candidate_evidence_without_generation_or_tag(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=workspace(tmp)
            path=root/'nanorsi.toml';path.write_text(path.read_text().replace('allow = ["target/**"]','allow = ["target/**"]\ndeny = ["target/private/**"]'))
            parent=cli._baseline(root);config=load_config(root/'nanorsi.toml');store=LineageStore.initialize(root)
            before=sum(e['event_type']=='generation' for e in store.events())
            result=cli._attempt(root,config,Git(root),store,parent,1,root/'.nanorsi/runs/candidate-only',promote=False,proposal_context={'operator':'mutate'})
            self.assertEqual(result['decision'],'accepted')
            self.assertEqual(sum(e['event_type']=='generation' for e in store.events()),before)
            self.assertFalse(Git(root).ref_exists('nanorsi/gen-1'))
            context=json.loads((root/'.nanorsi/runs/candidate-only/proposal/context.json').read_text())
            self.assertEqual(context['operator'],'mutate')
            self.assertEqual(context['surface'],{'allow':['target/**'],'deny':['target/private/**']})


if __name__=='__main__':
    unittest.main()
