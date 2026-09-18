"""Rejected-edit memory tests: with/without memory compared on repeat-proposal rate.

ADOPTION item 14. The mechanism injects bounded summaries of recently rejected or
failed proposals into the proposer context. Fixture proposers simulate a model that
either ignores the memory (always re-proposes the same rejected edit) or uses it
(switches to a different edit after seeing the rejection). Real-model effect is a
separate live question; these tests measure the plumbing and the controlled delta.
"""
import json
import tempfile
import unittest

from nanorsi.loop import rejected_recent
from tests.test_end_to_end import run_cli
from tests.test_v2_lifecycle import make_v2

MEMORYLESS = '''import difflib,json,sys
r=json.load(sys.stdin)
request=json.loads(r['messages'][1]['content'])
p='target/agent/skills/inspect/SKILL.md'
old=request['parent_files'][p]
new=old+'\\nmarker-x\\n'
diff='diff --git a/'+p+' b/'+p+'\\n'+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+p,tofile='b/'+p))
print(json.dumps({'content':json.dumps({'diff':diff,'hypothesis':{'reason':'append marker x'}}),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''

MEMORY_AWARE = '''import difflib,json,sys
r=json.load(sys.stdin)
request=json.loads(r['messages'][1]['content'])
p='target/agent/skills/inspect/SKILL.md'
old=request['parent_files'][p]
marker='marker-y' if request.get('rejected_recent') else 'marker-x'
new=old+'\\n'+marker+'\\n'
diff='diff --git a/'+p+' b/'+p+'\\n'+''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='a/'+p,tofile='b/'+p))
print(json.dumps({'content':json.dumps({'diff':diff,'hypothesis':{'reason':'append '+marker}}),'usage':{'model_calls':1,'input_tokens':10,'output_tokens':10,'cost_usd':None}}))
'''


class RejectedMemoryTests(unittest.TestCase):
    def build(self, tmp, adapter):
        root = make_v2(tmp, steps=3)
        (root / 'adapters/fixture.py').write_text(adapter)
        return root

    def attempts(self, root):
        events = [json.loads(line) for line in (root / 'lineage.jsonl').read_text().splitlines()]
        return [e for e in events if e.get('attempt_id') and e.get('event_type') in {'generation', 'attempt_failed'}]

    def test_memory_fields_are_bounded_and_exclude_metrics_and_diffs(self):
        events = [
            {'event_type': 'attempt_failed', 'attempt_id': 1, 'decision': 'failed', 'reason': 'x' * 500,
             'hypothesis': {'reason': 'y' * 500}, 'changed_paths': ['target/a']},
            {'event_type': 'generation', 'attempt_id': 2, 'decision': 'rejected', 'reason': 'improvement below minimum',
             'gate_metrics': {'score': 0.5}, 'hypothesis': {'reason': 'no gain'}, 'changed_paths': []},
            {'event_type': 'generation', 'attempt_id': 3, 'decision': 'accepted', 'reason': 'improvement'},
        ] * 4
        memory = rejected_recent(events, limit=5)
        self.assertEqual(len(memory), 5)
        self.assertTrue(all(entry['decision'] in {'rejected', 'failed', 'no-op'} for entry in memory))
        self.assertTrue(all(len(entry['gate_reason']) <= 200 for entry in memory))
        self.assertNotIn('gate_metrics', json.dumps(memory))
        self.assertNotIn('diff', json.dumps(memory))

    def test_without_memory_the_same_rejected_edit_is_repeated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp, MEMORYLESS)
            self.assertEqual(run_cli('run', '--workspace', str(root)).returncode, 0)
            attempts = self.attempts(root)
            self.assertEqual([a['decision'] for a in attempts], ['rejected'] * 3)
            reasons = [a['hypothesis']['reason'] for a in attempts]
            self.assertEqual(reasons, ['append marker x'] * 3)

    def test_with_memory_the_proposer_switches_after_a_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp, MEMORY_AWARE)
            self.assertEqual(run_cli('run', '--workspace', str(root)).returncode, 0)
            attempts = self.attempts(root)
            self.assertEqual([a['decision'] for a in attempts], ['rejected'] * 3)
            reasons = [a['hypothesis']['reason'] for a in attempts]
            self.assertEqual(reasons, ['append marker-x', 'append marker-y', 'append marker-y'])

    def test_context_carries_the_memory_for_every_attempt_after_the_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.build(tmp, MEMORYLESS)
            self.assertEqual(run_cli('baseline', '--workspace', str(root)).returncode, 0)
            self.assertEqual(run_cli('step', '--workspace', str(root)).returncode, 0)
            contexts = [json.loads(p.read_text()) for p in (root / '.nanorsi/runs').glob('*/proposal/context.json')]
            self.assertEqual(len(contexts), 1)
            self.assertEqual(contexts[0]['rejected_recent'], [])
            self.assertEqual(run_cli('step', '--workspace', str(root)).returncode, 0)
            contexts = sorted((p, json.loads(p.read_text())) for p in (root / '.nanorsi/runs').glob('*/proposal/context.json'))
            second = [c for _, c in contexts if c['rejected_recent']]
            self.assertEqual(len(second), 1)
            self.assertEqual(second[0]['rejected_recent'][0]['decision'], 'rejected')
            self.assertEqual(second[0]['rejected_recent'][0]['attempt_id'], 1)


if __name__ == '__main__':
    unittest.main()


class RejectedMemoryToggleTests(unittest.TestCase):
    def test_the_memory_can_be_disabled_per_workspace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp, steps=2)
            (root / 'adapters/fixture.py').write_text(MEMORYLESS)
            config = root / 'nanorsi.toml'
            config.write_text(config.read_text().replace('[proposer]', '[proposer]\nrejected_memory = false'))
            self.assertEqual(run_cli('baseline', '--workspace', str(root)).returncode, 0)
            self.assertEqual(run_cli('step', '--workspace', str(root)).returncode, 0)
            context = next(json.loads(p.read_text()) for p in (root / '.nanorsi/runs').glob('*/proposal/context.json'))
            self.assertNotIn('rejected_recent', context)
            self.assertEqual(run_cli('step', '--workspace', str(root)).returncode, 0)
            contexts = [json.loads(p.read_text()) for p in (root / '.nanorsi/runs').glob('*/proposal/context.json')]
            self.assertTrue(all('rejected_recent' not in c for c in contexts))

    def test_a_non_boolean_value_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_v2(tmp)
            config = root / 'nanorsi.toml'
            config.write_text(config.read_text().replace('[proposer]', '[proposer]\nrejected_memory = "yes"'))
            result = run_cli('baseline', '--workspace', str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('boolean', result.stderr)
