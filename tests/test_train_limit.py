"""Synthetic protocol fixtures; no model API calls or empirical test measurements."""
import json
import random
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from nanorsi import loop
from nanorsi.config import ConfigError, load_config
from nanorsi.contracts import comparison_hash
from nanorsi.lineage import LineageStore
from nanorsi.population import run_population
from nanorsi.templates import render_template
from tests.test_multilevel_kernel import workspace


def fixture(directory, limit=None, *, episodes=40):
    root = workspace(directory)
    path = root / 'nanorsi.toml'
    source = path.read_text().replace('max_episodes = 40', f'max_episodes = {episodes}')
    if limit is not None:
        source = source.replace('[evaluator]', f'[evaluator]\ntrain_limit = {limit}')
    path.write_text(source)
    evaluator = root / 'evaluator/evaluate.py'
    source = evaluator.read_text().replace(
        "if os.environ['NANORSI_SPLIT']=='train' and len(rows)>4:",
        "limit=int(os.environ['NANORSI_TRAIN_LIMIT'])\nif os.environ['NANORSI_SPLIT']=='train' and len(rows)>limit:")
    source = source.replace('sample(rows,4)', 'sample(rows,limit)')
    source = source.replace("'trace':[]", "'trace':[{'train_limit':limit}]")
    evaluator.write_text(source)
    manifest = root / 'tasks/manifest.json'
    rows = json.loads(manifest.read_text())['tasks']
    expanded = [{**row, 'task_id': f"{row['split']}-{index}"}
                for row, count in zip(rows, (7, 3, 2)) for index in range(count)]
    manifest.write_text(json.dumps({'schema_version': 1, 'tasks': expanded}))
    return root


def evaluate(root, config, split='train', *, repeat=2):
    store = LineageStore.initialize(root)
    output = root / '.nanorsi' / f'{split}-{repeat}.json'
    return loop.evaluate(root, config, root, split, output, store, repeat=repeat)


class TrainLimitTests(unittest.TestCase):
    def test_positive_integer_configuration_defaults_to_four(self):
        for value in (None, '1', '4', '12'):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, value)
                config = load_config(root / 'nanorsi.toml')
                self.assertEqual(getattr(config.evaluator, 'train_limit', None), int(value or 4))

    def test_rejects_bool_zero_negative_and_noninteger_limits(self):
        for value in ('true', 'false', '0', '-1', '1.5', '"2"'):
            with self.subTest(value=value), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, value)
                with self.assertRaisesRegex(ConfigError, r'evaluator\.train_limit.*integer >= 1'):
                    load_config(root / 'nanorsi.toml')

    def test_default_comparison_hash_matches_historical_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            original = comparison_hash(root, load_config(root / 'nanorsi.toml'))
            self.assertEqual(original, '75af9d1346233d4d95ca2de332683d80016ea1192e786e800fb68d7ea9c22a41')
            path = root / 'nanorsi.toml'
            path.write_text(path.read_text().replace('[evaluator]', '[evaluator]\ntrain_limit = 4'))
            self.assertEqual(comparison_hash(root, load_config(path)), original)

    def test_nondefault_comparison_hash_binds_limit_but_not_arm_or_seed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory)
            path = root / 'nanorsi.toml'
            source = path.read_text()
            hashes = []
            for limit in (4, 2, 12):
                path.write_text(source.replace('[evaluator]', f'[evaluator]\ntrain_limit = {limit}'))
                config = load_config(path)
                hashes.append(comparison_hash(root, config))
                other = replace(config, experiment=replace(config.experiment, arm='self-use', seed=19))
                self.assertEqual(comparison_hash(root, other), hashes[-1])
            self.assertEqual(len(set(hashes)), 3)

    def test_train_selection_environment_and_accounting_share_configured_limit(self):
        for limit in (None, '2', '6', '12'):
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, limit)
                config = load_config(root / 'nanorsi.toml')
                config = replace(config, experiment=replace(config.experiment, seed=19))
                result = evaluate(root, config)
                panel = [row for row in loop.tasks(root, config) if row['split'] == 'train']
                count = min(int(limit or 4), len(panel))
                expected = random.Random(19).sample(panel, count) if count < len(panel) else panel
                self.assertEqual([case['task_id'] for case in result.case_results],
                                 [row['task_id'] for row in expected])
                self.assertEqual({case['repeat_id'] for case in result.case_results}, {2})
                self.assertEqual([case['trace'] for case in result.case_results],
                                 [[{'train_limit': int(limit or 4)}]] * count)
                self.assertEqual(loop.search_episode_count(LineageStore.initialize(root).events()), count)

    def test_validation_and_test_protocol_panels_are_not_limited(self):
        for split, count in (('validation', 3), ('test', 2)):
            with self.subTest(split=split), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, '1')
                config = load_config(root / 'nanorsi.toml')
                result = evaluate(root, config, split)
                self.assertEqual([case['task_id'] for case in result.case_results],
                                 [f'{split}-{index}' for index in range(count)])
                starts = [e for e in LineageStore.initialize(root).events()
                          if e.get('event_type') == 'evaluation_started']
                self.assertEqual(starts[0]['episodes'], count)
                self.assertEqual(starts[0]['phase'], 'test' if split == 'test' else 'search')

    def test_custom_train_panel_rejects_wrong_task_group_repeat_and_count(self):
        substitutions = (
            ("'task_id':r['task_id']", "'task_id':'wrong' + r['task_id']"),
            ("'group_id':r['group_id']", "'group_id':'wrong'"),
            ("int(os.environ['NANORSI_REPEAT_ID'])", '0'),
            ('sample(rows,limit)', 'sample(rows,limit - 1)'),
        )
        for old, new in substitutions:
            with self.subTest(field=old), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, '2')
                path = root / 'evaluator/evaluate.py'
                path.write_text(path.read_text().replace(old, new))
                with self.assertRaisesRegex(ValueError, 'reserved task/repeat panel'):
                    evaluate(root, load_config(root / 'nanorsi.toml'))
                events = LineageStore.initialize(root).events()
                self.assertEqual(loop.search_episode_count(events), 2)
                self.assertEqual(events[-1]['status'], 'error')

    def test_budget_checks_configured_panel_before_external_call(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory, '6', episodes=5)
            with patch('nanorsi.loop.run_evaluation', side_effect=AssertionError('unexpected evaluator call')) as run:
                with self.assertRaisesRegex(RuntimeError, 'episode budget'):
                    evaluate(root, load_config(root / 'nanorsi.toml'))
                run.assert_not_called()
            self.assertEqual(LineageStore.initialize(root).verify(), [])

    def test_smaller_train_panel_fits_exact_episode_budget(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory, '2', episodes=2)
            config = load_config(root / 'nanorsi.toml')
            self.assertEqual(len(evaluate(root, config).case_results), 2)
            with self.assertRaisesRegex(RuntimeError, 'episode budget'):
                evaluate(root, config, repeat=3)
            self.assertEqual(loop.search_episode_count(LineageStore.initialize(root).events()), 2)

    def test_population_reserves_selected_train_and_two_full_validation_panels(self):
        for limit in (2, 6, 12):
            reserved = min(limit, 7) + 2 * 3
            with self.subTest(limit=limit), tempfile.TemporaryDirectory() as directory:
                root = fixture(directory, str(limit), episodes=3 + reserved)
                result = run_population(root, size=2, generations=2, workers=2)
                events = LineageStore.initialize(root).verify()
                reservations = [e for e in events if e.get('event_type') == 'episode_reservation']
                self.assertEqual([e['episodes'] for e in reservations], [reserved])
                settled = [e for e in events if e.get('event_type') == 'episode_reservation_settled']
                self.assertEqual([e['reservation_id'] for e in settled],
                                 [reservations[0]['reservation_id']])
                self.assertEqual(loop.search_episode_count(events), 3 + reserved)
                self.assertEqual(result['generation'], 1)
                self.assertEqual(result['stop_reason'], 'budget')
                self.assertFalse(any(e.get('split') == 'test' for e in events))

    def test_failed_population_settles_to_actual_custom_train_episodes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = fixture(directory, '2', episodes=11)
            (root / 'trainer/train.py').write_text('raise SystemExit(7)\n')
            result = run_population(root, size=2, generations=1)
            events = LineageStore.initialize(root).verify()
            reservations = [e for e in events if e.get('event_type') == 'episode_reservation']
            self.assertEqual([e['episodes'] for e in reservations], [8])
            self.assertEqual(loop.search_episode_count(events), 5)
            self.assertEqual(result['generation'], 0)
            self.assertEqual(sum(e.get('event_type') == 'attempt_failed' for e in events), 1)
            self.assertEqual(sum(e.get('event_type') == 'episode_reservation_settled' for e in events), 1)

    def test_v1_retains_legacy_result_shape_and_environment(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'legacy'
            render_template('artifact-fixture', root, goal='Legacy protocol fixture')
            path = root / 'nanorsi.toml'
            path.write_text(path.read_text().replace('[evaluator]', '[evaluator]\ntrain_limit = 2'))
            config = load_config(path)
            from nanorsi.loop import run_evaluation
            with patch('nanorsi.loop.run_evaluation', wraps=run_evaluation) as run:
                result = evaluate(root, config, 'gate')
            self.assertNotIn('NANORSI_TRAIN_LIMIT', run.call_args.kwargs['extra_env'])
            payload = json.loads((root / '.nanorsi/gate-2.json').read_text())
            self.assertEqual(payload['schema_version'], 1)
            self.assertEqual(result.usage, {})
            self.assertEqual(loop.search_episode_count(LineageStore.initialize(root).events()), 0)


if __name__ == '__main__':
    unittest.main()
