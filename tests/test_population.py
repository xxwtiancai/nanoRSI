"""Local deterministic engineering fixtures, not evidence of empirical LLM gains."""
import importlib.util
import json
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from nanorsi import cli, loop
from nanorsi.config import load_config
from nanorsi.gitops import Git
from nanorsi.lineage import LineageStore, artifact, write_json
from nanorsi.locking import Lock, LockBusy
from tests.test_v2_lifecycle import make_v2


class PopulationTests(unittest.TestCase):
    def test_population_api_exists(self):
        self.assertIsNotNone(importlib.util.find_spec('nanorsi.population'))

    def fixture(self, directory, *, steps=12, episodes=400):
        root = make_v2(directory, arm='self-use', steps=steps, episodes=episodes)
        cli._baseline(root)
        return root

    def executor(self, calls, *, scores=None, fail=None, invalid=None):
        active = set()
        mutex = threading.Lock()

        def execute(root, config, git, store, parent, attempt, run_dir, *, promote=True, proposal_context=None):
            self.assertFalse(promote)
            with self.assertRaises(LockBusy):
                with Lock(root):
                    pass
            with mutex:
                active.add(attempt)
                calls.append({'attempt': attempt, 'parent': parent, 'context': proposal_context,
                              'active': len(active), 'run_dir': run_dir})
            run_dir.mkdir(parents=True, exist_ok=True)
            store.append({'event_type': 'evaluation_started', 'invocation_id': str(attempt),
                          'phase': 'search', 'split': 'validation', 'episodes': 1})
            time.sleep(0.03 * (4 - attempt % 3))
            try:
                if attempt == fail:
                    (run_dir / 'failure.txt').write_text('failed worker evidence')
                    raise RuntimeError('scripted worker failure')
                with git.worktree(parent['candidate_commit'], root / '.nanorsi/worktrees' / run_dir.name) as checkout:
                    path = checkout / 'target/agent/skills/inspect/SKILL.md'
                    path.write_text(path.read_text() + f'\ncandidate {attempt}\n')
                    commit = git.commit_paths(checkout, ['target/agent/skills/inspect/SKILL.md'], 'Exercise branch provenance')
                score = scores[attempt] if scores else attempt / 10
                write_json(run_dir / 'gate.json', {'metrics': {'score': score}})
                store.append({'event_type': 'evaluation_finished', 'invocation_id': str(attempt), 'phase': 'search',
                              'status': 'ok', 'artifacts': {'result': artifact(root, run_dir / 'gate.json')}})
                return {'event_type': 'generation', 'attempt_id': attempt, 'generation': parent['generation'] + 1,
                        'parent_generation': parent['generation'], 'decision': 'accepted', 'reason': 'fixture',
                        'candidate_commit': commit, 'candidate_tree': git.tree_hash(commit), 'gate_metrics': {'score': score},
                        'gate_constraints': {'tests_passed': attempt != invalid}, 'heldout_metrics': None, 'changed_paths': ['target/agent/skills/inspect/SKILL.md'],
                        'manifest_hash': parent['manifest_hash'], 'evaluator_fingerprint': parent['evaluator_fingerprint'],
                        'artifacts': cli._artifacts(root, run_dir)}
            finally:
                with mutex:
                    active.remove(attempt)
        return execute

    def test_concurrent_branching_crossover_and_only_final_champion_promotes(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            calls = []
            with patch('nanorsi.cli._attempt', side_effect=self.executor(calls)):
                result = run_population(root, size=3, generations=2, workers=3)
            events = LineageStore.initialize(root).verify()
            evaluated = [e for e in events if e.get('event_type') == 'candidate_evaluated']
            self.assertEqual([e['attempt_id'] for e in evaluated], list(range(1, 7)))
            second = sorted([c for c in calls if c['attempt'] > 3], key=lambda c: c['attempt'])
            self.assertGreaterEqual(len({c['parent']['candidate_commit'] for c in second}), 2)
            self.assertTrue(any(c['active'] > 1 for c in calls))
            cross = next(c for c in second if c['context']['operator'] == 'crossover')
            self.assertNotEqual(cross['context']['parent_candidate_id'], cross['context']['extra_parents'][0]['candidate_id'])
            self.assertTrue(cross['context']['extra_parents'][0]['parent_files'])
            for event in evaluated:
                self.assertEqual(Git(root).resolve_ref(event['candidate_commit'] + '^'), event['parent_commit'])
                self.assertEqual(Git(root).resolve_ref(event['candidate_ref']), event['candidate_commit'])
                self.assertTrue(event['artifacts'])
            promoted = [e for e in events if e.get('decision') == 'accepted']
            self.assertEqual(len(promoted), 1)
            self.assertEqual(promoted[0]['generation'], 1)
            self.assertEqual(promoted[0]['candidate_commit'], result['candidate_commit'])
            self.assertFalse(Git(root).ref_exists('nanorsi/gen-2'))
            self.assertEqual(result['candidate_id'], 'candidate-000006')
            self.assertFalse(any(e.get('split') == 'test' for e in events))
            self.assertEqual(loop.search_episode_count(events), 7)

    def test_tie_breaking_and_replay_order_ignore_worker_finish_order(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            calls = []
            with patch('nanorsi.cli._attempt', side_effect=self.executor(calls, scores={1: .5, 2: .5, 3: .5})):
                result = run_population(root, size=3, generations=1, workers=3)
            self.assertEqual(result['candidate_id'], 'candidate-000001')
            started = [e for e in LineageStore.initialize(root).events() if e.get('event_type') == 'evaluation_started' and 'attempt_id' in e]
            self.assertEqual([e['attempt_id'] for e in started], [1, 2, 3])

    def test_insufficient_budget_prevents_jobs_and_frozen_and_locked_search_block(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory, episodes=3)
            with patch('nanorsi.cli._attempt') as execute:
                result = run_population(root, size=3, generations=2, workers=2)
                execute.assert_not_called()
            self.assertEqual(result['stop_reason'], 'budget')
            self.assertFalse(any(e.get('event_type') == 'attempt_started' for e in LineageStore.initialize(root).events()))
            with Lock(root), self.assertRaises(LockBusy):
                run_population(root)
            loop.freeze(root, load_config(root / 'nanorsi.toml'), repeats=1)
            with self.assertRaisesRegex(RuntimeError, 'frozen'):
                run_population(root)

    def test_failed_worker_and_reserved_evidence_are_recorded(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            with patch('nanorsi.cli._attempt', side_effect=self.executor([], fail=2)):
                result = run_population(root, size=3, generations=1, workers=3)
            events = LineageStore.initialize(root).verify()
            failed = next(e for e in events if e.get('event_type') == 'attempt_failed')
            self.assertEqual(failed['attempt_id'], 2)
            self.assertIn('failure.txt', failed['artifacts'])
            self.assertTrue((root / failed['artifacts']['worker-events.jsonl']['path']).is_file())
            reservations = [e for e in events if e.get('event_type') == 'episode_reservation']
            self.assertEqual([e['episodes'] for e in reservations], [3, 3, 3])
            self.assertEqual(result['candidate_id'], 'candidate-000003')
            self.assertEqual(loop.search_episode_count(events), 4)
            self.assertEqual(len([e for e in events if e.get('event_type') == 'episode_reservation_settled']), 3)

    def test_constraints_and_global_incumbent_prevent_weaker_branch_promotion(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            with patch('nanorsi.cli._attempt', side_effect=self.executor([], scores={1: .8, 2: .6, 3: .7})):
                first = run_population(root, size=3, generations=1)
            with patch('nanorsi.cli._attempt', side_effect=self.executor([], scores={4: .75, 5: .65, 6: .7})):
                second = run_population(root, size=3, generations=1)
            self.assertEqual(first['candidate_commit'], second['candidate_commit'])
            self.assertEqual(len([e for e in LineageStore.initialize(root).verify() if e.get('decision') == 'accepted']), 1)

    def test_real_local_scripted_proposer_search_and_final_commit(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory, steps=2, episodes=7)
            result = run_population(root, size=2, generations=1, workers=2)
            self.assertEqual(result['generation'], 1)
            frozen = loop.freeze(root, load_config(root / 'nanorsi.toml'), repeats=1)
            self.assertEqual(frozen['candidate_commit'], result['candidate_commit'])
            path = loop.final_test(root, load_config(root / 'nanorsi.toml'))
            report = json.loads(path.read_text())
            candidate = next(row for row in report['results'] if row['condition'] == 'candidate')
            self.assertEqual(candidate['case_results'][0]['score'], 1)
            events = LineageStore.initialize(root).verify()
            self.assertEqual(loop.search_episode_count(events), 7)
            loop.require_settled(events)

    def test_duplicate_commits_do_not_crowd_out_distinct_retained_branches(self):
        from nanorsi.population import _rank
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            config = load_config(root / 'nanorsi.toml')
            candidates = [{'candidate_id': name, 'candidate_commit': commit, 'gate_metrics': {'score': score},
                           'gate_constraints': {'tests_passed': True}}
                          for name, commit, score in [('a', 'same', .9), ('b', 'same', .9), ('c', 'branch', .8)]]
            self.assertEqual([c['candidate_id'] for c in _rank(candidates, config, 2)], ['a', 'c'])

    def test_candidate_with_wrong_git_parent_is_failed_without_promotion(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            execute = self.executor([])
            def wrong_parent(*args, **kwargs):
                evidence = execute(*args, **kwargs)
                evidence['candidate_commit'] = args[4]['candidate_commit']
                return evidence
            with patch('nanorsi.cli._attempt', side_effect=wrong_parent):
                run_population(root, size=1, generations=1)
            events = LineageStore.initialize(root).verify()
            self.assertFalse(any(e.get('event_type') == 'candidate_evaluated' for e in events))
            failure = next(e for e in events if e.get('event_type') == 'attempt_failed')
            self.assertIn('Git parent', failure['reason'])

    def test_crossover_source_is_bounded_and_excludes_private_files_and_links(self):
        from nanorsi.population import _source
        with tempfile.TemporaryDirectory() as directory:
            root = make_v2(directory)
            skills = root / 'target/agent/skills/inspect'
            (skills / 'fake.pem').write_text('fixture private key, not a credential')
            (skills / 'oversized.md').write_text('x' * 64001)
            (skills / 'link.md').symlink_to('SKILL.md')
            cli._baseline(root)
            source = _source(Git(root), Git(root).resolve_ref('HEAD'), load_config(root / 'nanorsi.toml'))
            self.assertIn('target/agent/skills/inspect/SKILL.md', source)
            self.assertFalse(any(name.endswith(('fake.pem', 'oversized.md', 'link.md')) for name in source))
            self.assertLessEqual(sum(len(value.encode()) for value in source.values()), 192000)

    def test_failed_constraints_cannot_win_even_with_highest_validation_score(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            with patch('nanorsi.cli._attempt', side_effect=self.executor([], scores={1: .5, 2: 1, 3: .6}, invalid=2)):
                result = run_population(root, size=3, generations=1)
            self.assertEqual(result['candidate_id'], 'candidate-000003')
            evaluated = [e for e in LineageStore.initialize(root).verify() if e.get('event_type') == 'candidate_evaluated']
            self.assertEqual(len(evaluated), 3)

    def test_all_population_lineage_initialization_occurs_under_root_lock(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory, episodes=1)
            initialize = LineageStore.initialize
            def checked(path):
                self.assertTrue((path / '.nanorsi/lock').is_file(), 'lineage initialized outside root lock')
                return initialize(path)
            with patch.object(LineageStore, 'initialize', side_effect=checked):
                result = run_population(root)
            self.assertEqual(result['stop_reason'], 'budget')

    def test_interrupted_reservation_remains_charged_and_needs_recovery(self):
        from nanorsi.population import run_population
        with tempfile.TemporaryDirectory() as directory:
            root = self.fixture(directory)
            store = LineageStore.initialize(root)
            run_dir = root / '.nanorsi/runs/interrupted-candidate'
            run_dir.mkdir(parents=True)
            (run_dir / 'worker-events.jsonl').write_text('{\"untrusted\":true}\n')
            store.append({'event_type': 'attempt_started', 'attempt_id': 1, 'candidate_id': 'candidate-000001',
                          'run_dir': run_dir.relative_to(root).as_posix()})
            store.append({'event_type': 'episode_reservation', 'reservation_id': 'candidate-000001', 'attempt_id': 1,
                          'phase': 'search', 'episodes': 3})
            with self.assertRaisesRegex(RuntimeError, 'recover'):
                run_population(root)
            store.recover_attempts()
            self.assertEqual(loop.search_episode_count(store.events()), 4)
            interrupted = next(e for e in store.verify() if e.get('event_type') == 'attempt_failed')
            self.assertIn('worker-events.jsonl', interrupted['artifacts'])
            self.assertFalse(any(e.get('untrusted') for e in store.events()))


if __name__ == '__main__':
    unittest.main()
