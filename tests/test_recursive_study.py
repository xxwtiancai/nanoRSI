"""Protocol controls for the digits study; no real held-out model scores here."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name):
    path = ROOT / 'examples/recursive_learning' / (name + '.py')
    if not path.is_file():
        raise AssertionError('recursive study ' + name + ' is missing')
    spec = importlib.util.spec_from_file_location('recursive_' + name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class RecursiveStudyTests(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec('numpy'), 'optional NumPy experiment tooling unavailable')
    def test_data_split_is_fixed_complete_and_source_disjoint(self):
        prepare = load('prepare')
        manifest, meta = prepare.build_manifest()
        self.assertEqual((manifest, meta), prepare.build_manifest())
        tasks = manifest['tasks']
        self.assertEqual(len(tasks), 1797)
        self.assertEqual(meta['counts'], {'train': 1074, 'validation': 359, 'test': 364})
        self.assertEqual(len({t['task_id'] for t in tasks}), 1797)
        self.assertEqual(len({t['group_id'] for t in tasks}), 1797)
        self.assertEqual(len({t['input_files']['features.json'] for t in tasks}), 1797)
        self.assertEqual(meta['split_seed'], 20260912)

    def test_paired_summary_keeps_failures_and_does_not_confuse_training_gain(self):
        analyze = load('analyze')
        rows = []
        for seed in [10, 11, 12]:
            for policy, score in [('frozen', .80), ('self-use', .86), ('uniform', .84), ('random', .82)]:
                rows.append({'method': 'sft', 'seed': seed, 'policy': policy, 'status': 'completed',
                             'comparison_hash': str(seed) if policy in ['frozen', 'self-use'] else policy,
                             'design_hash': str(seed), 'baseline_accuracy': .1, 'candidate_accuracy': score,
                             'candidate_loss': .5})
        rows.append({'method': 'sft', 'seed': 13, 'policy': 'frozen', 'status': 'failed'})
        result = analyze.summarize(rows)
        effect = result['comparisons'][0]
        self.assertEqual(effect['reference'], 'frozen')
        self.assertAlmostEqual(effect['mean_delta_pp'], 6)
        self.assertEqual(effect['complete_pairs'], 3)
        self.assertEqual(effect['incomplete_pairs'], 1)
        self.assertEqual(len(result['runs']), 13)
        self.assertEqual(effect['positive_seeds'], 3)
        self.assertEqual([round(x) for x in effect['bootstrap_95_ci_pp']], [6, 6])
        rows[1]['comparison_hash'] = 'mismatch'
        with self.assertRaisesRegex(ValueError, 'comparison'):
            analyze.summarize(rows)

    def test_all_planned_workspaces_must_be_frozen_before_any_final_test(self):
        runner = load('run')
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plan = {'runs': [{'name': 'one'}, {'name': 'two'}]}
            from nanorsi.hashing import canonical_hash
            plan['plan_sha256'] = canonical_hash(plan)
            for name in ['one', 'two']:
                (root / name).mkdir()
            with self.assertRaisesRegex(ValueError, 'frozen'):
                runner.require_all_frozen(root, plan)


def primary_rule(methods):
    return {'methods': sorted(methods), 'contrast': 'self-use minus frozen',
            'family_size': len(methods), 'familywise_alpha': .05,
            'adjustment': 'Bonferroni', 'minimum_gain_pp': 5,
            'requires_complete_matched_budget_panel': True}


class SummaryIntegrityTests(unittest.TestCase):
    def rows(self, methods=('sft',)):
        return [{'method': method, 'seed': seed, 'policy': policy, 'status': 'completed',
                 'final_status': 'completed', 'protocol_status': 'completed', 'budget_complete': True,
                 'comparison_hash': str(seed), 'design_hash': str(seed),
                 'candidate_accuracy': .8 if policy == 'frozen' else .9, 'candidate_loss': .5,
                 'actual_update_steps': 4, 'planned_update_steps': 4,
                 'examples_seen': 128, 'planned_examples_seen': 128,
                 'training_scored_examples': 32, 'planned_training_scored_examples': 32,
                 'proposer_scored_examples': 16, 'planned_proposer_scored_examples': 16,
                 'evaluation_scored_examples': 36, 'planned_evaluation_scored_examples': 36}
                for method in methods for seed in [10, 11, 12] for policy in ['frozen', 'self-use']]

    def test_failed_search_outcome_is_kept_but_blocks_matched_gain(self):
        rows = self.rows()
        rows[1].update(status='failed', protocol_status='failed', budget_complete=False)
        effect = load('analyze').summarize(rows)['comparisons'][0]
        self.assertEqual(effect['all_measured_outcomes']['pairs_count'], 3)
        self.assertEqual(effect['complete_case']['pairs_count'], 2)
        self.assertFalse(effect['clear_gain_target_met'])

    def test_claim_requires_actual_equal_planned_work_even_if_status_says_completed(self):
        for field in ['actual_update_steps', 'examples_seen', 'training_scored_examples',
                      'proposer_scored_examples', 'evaluation_scored_examples']:
            with self.subTest(field=field):
                rows = self.rows()
                rows[1][field] = 0
                self.assertFalse(load('analyze').summarize(rows)['comparisons'][0]['clear_gain_target_met'])

    def test_failure_counters_override_a_false_completion_flag(self):
        for field in ['failed_attempts', 'missing_attempts', 'unaccounted_attempts']:
            rows = self.rows()
            rows[1][field] = 1
            with self.subTest(field=field):
                self.assertFalse(load('analyze').summarize(rows)['comparisons'][0]['clear_gain_target_met'])

    def test_family_interval_lower_bound_controls_the_primary_claim(self):
        from unittest.mock import patch
        analyze = load('analyze')
        with patch.object(analyze, 'interval', side_effect=lambda values, draws=10000, confidence=.95:
                          [1, 12] if confidence == .95 else [-1, 12]):
            effect = analyze.summarize(self.rows(('sft', 'rl', 'lora')))['comparisons'][0]
        self.assertEqual(effect['bootstrap_95_ci_pp'], [1, 12])
        self.assertEqual(effect['bootstrap_family_adjusted_ci_pp'], [-1, 12])
        self.assertFalse(effect['clear_gain_target_met'])

    def test_summary_restores_all_assigned_seed_rows(self):
        rows = self.rows()
        plan = {'runs': [{k: row[k] for k in ['method', 'seed', 'policy']} for row in rows],
                'primary_inference': primary_rule(['sft'])}
        summary = load('analyze').summarize(rows[:2], plan=plan)
        self.assertEqual(len(summary['runs']), 6)
        self.assertEqual(sum(row['status'] == 'missing' for row in summary['runs']), 4)
        self.assertEqual(summary['comparisons'][0]['incomplete_pairs'], 2)
        self.assertFalse(summary['comparisons'][0]['clear_gain_target_met'])

    def test_primary_family_adjustment_is_dynamic_and_controls_descriptive(self):
        summary = load('analyze').summarize(self.rows(('sft', 'rl', 'lora')))
        for effect in summary['comparisons']:
            if effect['reference'] == 'frozen':
                self.assertAlmostEqual(effect['family_adjusted_confidence'], 1 - .05 / 3)
                self.assertEqual([round(x) for x in effect['bootstrap_family_adjusted_ci_pp']], [10, 10])
                self.assertTrue(effect['clear_gain_target_met'])
            else:
                self.assertIsNone(effect['bootstrap_family_adjusted_ci_pp'])
                self.assertFalse(effect['clear_gain_target_met'])
        single = load('analyze').summarize(self.rows())['comparisons'][0]
        self.assertEqual(single['family_adjusted_confidence'], .95)


@unittest.skipUnless(importlib.util.find_spec('numpy'), 'optional NumPy experiment tooling unavailable')
class SyntheticLifecycleTests(unittest.TestCase):
    """Tiny generated arrays exercise real CLI search/freeze/final; never digits data."""
    @classmethod
    def setUpClass(cls):
        from dataclasses import asdict
        import shutil
        from nanorsi.config import load_config
        from nanorsi.hashing import canonical_hash
        cls.directory = tempfile.TemporaryDirectory()
        cls.base = Path(cls.directory.name) / 'study'
        cls.base.mkdir()
        cls.runner, cls.analyze, prepare = load('run'), load('analyze'), load('prepare')
        tasks = []
        for split, count in [('train', 8), ('validation', 4), ('test', 4)]:
            for i in range(count):
                values = [0] * 64
                values[i % 2] = 16
                values[2] = i
                tasks.append({'task_id': f'{split}-{i}', 'group_id': f'{split}-group-{i}', 'split': split,
                              'instruction': 'Synthetic fixture prediction',
                              'input_files': {'features.json': json.dumps(values)},
                              'expected_files': {'label.txt': str(i % 2)}})
        cls.manifest = {'schema_version': 1, 'tasks': tasks}
        cls.settings = {'sft': {'lr': .3, 'multiplier': 3, 'steps': 2, 'balanced': False}}
        template = Path(cls.directory.name) / 'contract'
        prepare.prepare_workspace(template, method='sft', seed=10, policy='frozen', rounds=2,
                                  settings=cls.settings['sft'], manifest=cls.manifest)
        config = asdict(load_config(template / 'nanorsi.toml'))
        for key in ['id', 'arm', 'seed', 'goal']:
            config['experiment'].pop(key)
        cls.plan = {'runs': [{'name': 'sft-seed-10-' + policy, 'method': 'sft', 'seed': 10, 'policy': policy}
                             for policy in ['frozen', 'self-use']], 'rounds': 2, 'batch_size': 32,
                    'settings': cls.settings, 'workspace_config': config, 'primary_inference': primary_rule(['sft']),
                    'dataset': {'manifest_sha256': canonical_hash(cls.manifest),
                                'counts': {'train': 8, 'validation': 4, 'test': 4}}}
        cls.plan['plan_sha256'] = canonical_hash(cls.plan)
        cls.runner.write(cls.base / 'plan.json', cls.plan)
        for row in cls.plan['runs']:
            lab = cls.base / row['name']
            prepare.prepare_workspace(lab, method='sft', seed=10, policy=row['policy'], rounds=2,
                                      settings=cls.settings['sft'], manifest=cls.manifest,
                                      plan_hash=cls.plan['plan_sha256'])
            cls.runner.command(cls.base, row, 'search', ['run'])
            cls.runner.command(cls.base, row, 'freeze', ['freeze', '--repeats', '1'])
        cls.frozen = cls.runner.require_all_frozen(cls.base, cls.plan)
        cls.finalized = Path(cls.directory.name) / 'finalized'
        shutil.copytree(cls.base, cls.finalized)
        cls.runner.write(cls.finalized / 'all-frozen.json',
                         {'plan_sha256': cls.plan['plan_sha256'], 'runs': cls.frozen})
        for row in cls.plan['runs']:
            cls.runner.command(cls.finalized, row, 'final-test', ['final-test'])
            cls.runner.command(cls.finalized, row, 'verify', ['verify'])

    @classmethod
    def tearDownClass(cls):
        cls.directory.cleanup()

    def setUp(self):
        import shutil
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / 'study'
        shutil.copytree(self.base, self.root)
        self.addCleanup(self.temp.cleanup)

    def rewrite(self, lab, events):
        from nanorsi.lineage import LineageStore
        store = LineageStore(lab / 'lineage.jsonl', lab / '.nanorsi/lineage.key')
        store.path.unlink()
        for event in events:
            store.append({k: v for k, v in event.items() if k not in {'receipt', 'seq'}})

    def finalized_lab(self):
        import shutil
        lab = Path(self.temp.name) / 'final-lab'
        shutil.copytree(self.finalized / self.plan['runs'][0]['name'], lab)
        return lab

    def test_real_cli_two_arm_lifecycle_and_resume(self):
        from unittest.mock import patch
        for row in self.plan['runs']:
            events = self.analyze.verified_events(self.root / row['name'])
            self.assertFalse(any(e.get('split') == 'test' for e in events))
        with patch('sys.argv', ['run.py', str(self.root), '--phase', 'final', '--workers', '1']):
            self.assertEqual(self.runner.main(), 0)
        summary = json.loads((self.root / 'summary.json').read_text())
        self.assertEqual(len(summary['runs']), 2)
        for row in summary['runs']:
            self.assertEqual(row['final_status'], 'completed')
            self.assertEqual(row['protocol_status'], 'completed')
            self.assertEqual(row['actual_update_steps'], 4)
            self.assertEqual(row['planned_update_steps'], 4)
            self.assertTrue(row['budget_complete'])
        self.assertEqual(self.runner.require_all_frozen(self.root, self.plan), self.frozen)

    def test_first_barrier_rejects_existing_test_before_global_marker(self):
        from nanorsi.lineage import LineageStore
        lab = self.root / self.plan['runs'][0]['name']
        store = LineageStore(lab / 'lineage.jsonl', lab / '.nanorsi/lineage.key')
        store.append({'event_type': 'evaluation_started', 'split': 'test'})
        with self.assertRaisesRegex(ValueError, 'test.*global|global.*test'):
            self.runner.require_all_frozen(self.root, self.plan)

    def test_stale_or_malformed_marker_cannot_bypass_barrier(self):
        markers = [{}, {'plan_sha256': 'stale', 'runs': self.frozen},
                   {'plan_sha256': self.plan['plan_sha256'], 'runs': []},
                   {'plan_sha256': self.plan['plan_sha256'], 'runs': self.frozen * 2}]
        for marker in markers:
            with self.subTest(marker=marker):
                self.runner.write(self.root / 'all-frozen.json', marker)
                with self.assertRaisesRegex(ValueError, 'marker'):
                    self.runner.require_all_frozen(self.root, self.plan)
        (self.root / 'all-frozen.json').write_text('not-json')
        with self.assertRaisesRegex(ValueError, 'marker'):
            self.runner.require_all_frozen(self.root, self.plan)

    def test_paired_frozen_hash_mismatch_rejected_before_test(self):
        lab = self.root / self.plan['runs'][0]['name']
        events = self.analyze.verified_events(lab)
        next(e for e in events if e.get('event_type') == 'freeze')['comparison_hash'] = 'different'
        self.rewrite(lab, events)
        with self.assertRaisesRegex(ValueError, 'comparison'):
            self.runner.require_all_frozen(self.root, self.plan)

    def test_actual_baseline_recipe_and_config_must_match_frozen_plan(self):
        from unittest.mock import patch
        from nanorsi.hashing import canonical_hash
        # Keep the already committed goal identity intact; alter the expected plan input
        # and mock only its hash computation, so this specifically tests factor checks.
        for section, key, value in [('rounds', None, 3), ('batch_size', None, 16),
                                    ('settings', 'sft', {**self.settings['sft'], 'lr': .1}),
                                    ('dataset', 'manifest_sha256', 'different'),
                                    ('workspace_config', 'gate', {'minimum_improvement': .1})]:
            plan = json.loads(json.dumps(self.plan))
            if key is None:
                plan[section] = value
            else:
                plan[section][key] = value
            with self.subTest(section=section), patch.object(self.runner, 'canonical_hash', return_value=self.plan['plan_sha256']):
                with self.assertRaisesRegex(ValueError, 'plan|recipe|dataset|config'):
                    self.runner.require_all_frozen(self.root, plan)

    def test_successful_training_recovered_from_failed_attempt_artifacts(self):
        lab = self.finalized_lab()
        events = self.analyze.verified_events(lab)
        event = next(e for e in events if e.get('attempt_id') == 2 and e.get('training'))
        event.pop('training')
        event.update(event_type='attempt_failed', decision='failed', reason='validation failed after training')
        self.rewrite(lab, events)
        row = self.analyze.read_run(lab)
        self.assertEqual(row['actual_update_steps'], 4)
        self.assertEqual(row['examples_seen'], 128)
        self.assertEqual(row['final_status'], 'completed')
        self.assertEqual(row['protocol_status'], 'failed')
        self.assertEqual(row['failed_attempts'], 1)
        self.assertFalse(row['budget_complete'])
        self.assertIn('candidate_accuracy', row)

    def test_missing_training_evidence_never_becomes_completed_budget(self):
        lab = self.finalized_lab()
        events = self.analyze.verified_events(lab)
        event = next(e for e in events if e.get('attempt_id') == 2 and e.get('training'))
        event.pop('training')
        event['artifacts'] = {k: v for k, v in event['artifacts'].items() if not k.startswith('training/')}
        event.update(event_type='attempt_failed', decision='failed', reason='unaccounted training')
        self.rewrite(lab, events)
        row = self.analyze.read_run(lab)
        self.assertIsNone(row['actual_update_steps'])
        self.assertEqual(row['known_update_steps'], 2)
        self.assertEqual(row['unaccounted_attempts'], 1)
        self.assertFalse(row['budget_complete'])

    def test_focus_order_changes_do_not_count_as_curriculum_change(self):
        from nanorsi.lineage import artifact
        lab = self.finalized_lab()
        events = self.analyze.verified_events(lab)
        for event in events:
            ref = event.get('artifacts', {}).get('proposal/trace.json')
            if not ref:
                continue
            trace_path = lab / ref['path']
            trace = json.loads(trace_path.read_text())
            trace[0]['focus_task_ids'] = ['train-0', 'train-1'][::1 if event['attempt_id'] == 1 else -1]
            trace[0]['sampling_sha256'] = 'same-distribution'
            trace_path.write_text(json.dumps(trace))
            event['artifacts']['proposal/trace.json'] = artifact(lab, trace_path)
        self.rewrite(lab, events)
        self.assertEqual(self.analyze.read_run(lab)['focus_changes'], 0)


    def test_malformed_failed_training_evidence_does_not_erase_final_outcome(self):
        from nanorsi.lineage import artifact
        lab = self.finalized_lab()
        events = self.analyze.verified_events(lab)
        event = next(e for e in events if e.get('attempt_id') == 2 and e.get('training'))
        event.pop('training')
        event.update(event_type='attempt_failed', decision='failed')
        path = lab / event['artifacts']['training/evidence.json']['path']
        path.write_text('{partial')
        event['artifacts']['training/evidence.json'] = artifact(lab, path)
        self.rewrite(lab, events)
        row = self.analyze.read_run(lab)
        self.assertEqual(row['final_status'], 'completed')
        self.assertIsNone(row['actual_update_steps'])
        self.assertFalse(row['budget_complete'])

    def test_missing_planned_attempt_is_reported_with_observed_subtotal(self):
        lab = self.finalized_lab()
        events = [e for e in self.analyze.verified_events(lab) if e.get('attempt_id') != 2]
        self.rewrite(lab, events)
        row = self.analyze.read_run(lab)
        self.assertEqual(row['missing_attempts'], 1)
        self.assertEqual(row['actual_update_steps'], 2)
        self.assertEqual(row['planned_update_steps'], 4)
        self.assertFalse(row['budget_complete'])

    def test_incomplete_final_still_reports_actual_search_budget(self):
        lab = self.finalized_lab()
        events = [e for e in self.analyze.verified_events(lab) if e.get('event_type') != 'final_result']
        self.rewrite(lab, events)
        row = self.analyze.read_run(lab)
        self.assertEqual(row['final_status'], 'incomplete')
        self.assertEqual(row['actual_update_steps'], 4)
        self.assertNotEqual(row['status'], 'completed')

    def test_current_immutable_goal_must_still_bind_plan(self):
        lab = self.root / self.plan['runs'][0]['name']
        path = lab / 'nanorsi.toml'
        path.write_text(path.read_text().replace(self.plan['plan_sha256'], '0' * 64))
        with self.assertRaisesRegex(ValueError, 'plan'):
            self.runner.require_all_frozen(self.root, self.plan)

    def test_initial_main_runner_freezes_signed_config_and_primary_family(self):
        from unittest.mock import patch
        from nanorsi.hashing import canonical_hash
        prepare = load('prepare')
        output = Path(self.temp.name) / 'fresh-study'
        original = self.runner.sibling
        with patch.object(prepare, 'build_manifest', return_value=(self.manifest, self.plan['dataset'])), \
                patch.object(prepare, 'SETTINGS', self.settings), \
                patch.object(prepare, 'POLICIES', ('frozen', 'self-use')), \
                patch.object(self.runner, 'sibling', side_effect=lambda name: prepare if name == 'prepare' else original(name)), \
                patch('sys.argv', ['run.py', str(output), '--phase', 'search', '--methods', 'sft', '--seeds', '10', '--workers', '1']):
            self.assertEqual(self.runner.main(), 0)
        plan = json.loads((output / 'plan.json').read_text())
        self.assertEqual(plan['primary_inference'], primary_rule(['sft']))
        self.assertIn('workspace_config', plan)
        self.assertEqual(plan['plan_sha256'], canonical_hash({k: v for k, v in plan.items() if k != 'plan_sha256'}))
        for row in plan['runs']:
            self.assertFalse(any(e.get('split') == 'test' for e in self.analyze.verified_events(output / row['name'])))


if __name__ == '__main__':
    unittest.main()
