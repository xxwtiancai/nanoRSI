import json
import tempfile
import unittest
from pathlib import Path

from tests.test_end_to_end import run_cli
from nanorsi.lineage import LineageStore


class LifecycleTests(unittest.TestCase):
    def workspace(self, root):
        path = Path(root) / 'experiment'
        self.assertEqual(run_cli('new', 'harness', str(path)).returncode, 0)
        (path / 'proposer/propose.py').write_text('''import difflib, json, os
from pathlib import Path
p = Path('target/agent/policy.txt')
old = p.read_text()
context = json.loads(Path(os.environ['NANORSI_CONTEXT_PATH']).read_text())
new = 'mode: ' + ('evidence' if context['attempt_id'] != 2 else 'guess') + '\\n'
if old == new: new += '\\n'
out = Path(os.environ['NANORSI_PROPOSAL_DIR'])
diff = 'diff --git a/target/agent/policy.txt b/target/agent/policy.txt\\n'
diff += ''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/target/agent/policy.txt',tofile='b/target/agent/policy.txt'))
(out/'proposal.diff').write_text(diff)
(out/'hypothesis.json').write_text('{}')
''')
        evaluator = path/'evaluator/evaluate.py'
        original = 'sum(item["score"] for item in case_results) / len(case_results)'
        evaluator.write_text(evaluator.read_text().replace(original, original + ' * (0.4 + 0.2 * Path("target/agent/policy.txt").read_text().count("\\n"))'))
        return path

    def test_accept_reject_attempt_budget_and_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.workspace(tmp)
            config = path/'nanorsi.toml'
            config.write_text(config.read_text().replace('max_steps = 10','max_steps = 3'))
            self.assertEqual(run_cli('baseline','--workspace',str(path)).returncode,0)
            for attempt in range(3):
                result = run_cli('step','--workspace',str(path))
                self.assertEqual(result.returncode,0,result.stderr)
            events = [json.loads(x) for x in (path/'lineage.jsonl').read_text().splitlines()]
            attempts = [x for x in events if x.get('event_type') == 'generation' and x.get('attempt_id')]
            self.assertEqual([x['attempt_id'] for x in attempts],[1,2,3])
            self.assertEqual(attempts[0]['decision'],'accepted')
            self.assertEqual(attempts[1]['decision'],'rejected')
            self.assertEqual(attempts[2]['decision'],'accepted')
            self.assertEqual([e['generation'] for e in attempts],[1,1,2])
            self.assertTrue(all(x.get('evaluator_fingerprint') for x in attempts))
            result = run_cli('step','--workspace',str(path))
            self.assertNotEqual(result.returncode,0)
            self.assertIn('budget',result.stderr)

    def test_configured_metric_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.workspace(tmp)
            for relative in ['nanorsi.toml','evaluator/evaluate.py']:
                f = path/relative
                f.write_text(f.read_text().replace('"score"','"accuracy"'))
            self.assertEqual(run_cli('baseline','--workspace',str(path)).returncode,0)
            result = run_cli('step','--workspace',str(path))
            self.assertEqual(result.returncode,0,result.stderr)

    def test_legacy_receipted_baseline_can_adopt_explicit_contract(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = self.workspace(tmp)
            self.assertEqual(run_cli('baseline','--workspace',str(path)).returncode,0)
            store = LineageStore.initialize(path)
            baseline = next(e for e in store.events() if e.get('generation')==0)
            for key in ['manifest_hash','artifacts','seq','receipt']:
                baseline.pop(key,None)
            store.path.write_text('')
            store.append(baseline)
            result = run_cli('step','--workspace',str(path))
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertTrue(any(e.get('event_type')=='legacy_contract' for e in store.verify()))
