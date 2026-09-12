import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

path = Path(__file__).parents[1] / 'examples/demos/export.py'
spec = importlib.util.spec_from_file_location('evidence_export', path)
export = importlib.util.module_from_spec(spec)
spec.loader.exec_module(export)


class EvidenceExportTests(unittest.TestCase):
    def test_derived_report_cannot_replace_verified_outcomes(self):
        record = {'condition': 'candidate', 'case_results': [{'score': 0.0}]}
        events = [{'event_type': 'final_result', 'result': record}]
        final = {'results': [copy.deepcopy(record)], 'seed': 0}
        self.assertEqual(export.checked_final(final, events, {'seed': 0})['results'], [record])
        final['results'][0]['case_results'][0]['score'] = 1.0
        with self.assertRaisesRegex(ValueError, 'lineage'):
            export.checked_final(final, events, {'seed': 0})

    def test_frozen_metadata_cannot_be_relabelled(self):
        with self.assertRaisesRegex(ValueError, 'frozen metadata'):
            export.checked_final({'results': [], 'mode': 'model'}, [], {'mode': 'artifact'})

    def test_derived_costs_rebuilt_and_unverified_extras_excluded(self):
        events = [
            {'event_type': 'evaluation_started', 'phase': 'search', 'invocation_id': 'one'},
            {'event_type': 'evaluation_finished', 'phase': 'search', 'invocation_id': 'one', 'cost_usd': None},
            {'event_type': 'proposal_started', 'attempt_id': 1},
            {'event_type': 'proposal_finished', 'attempt_id': 1, 'cost_usd': 0.5},
        ]
        final = {'results': [], 'seed': 0, 'private_note': 'do not publish',
                 'search_cost_usd': {'total_usd': 999}, 'search_evaluations': [{'score': 999}],
                 'search_proposals': [], 'test_cost_usd': {'total_usd': 999}}
        public = export.checked_final(final, events, {'seed': 0})
        self.assertNotIn('private_note', public)
        self.assertEqual(public['search_cost_usd'], {'known_usd': 0.5, 'total_usd': None,
                                                   'known_count': 1, 'total_count': 2, 'coverage': 0.5})
        self.assertEqual(len(public['search_evaluations']), 2)
        self.assertEqual(public['search_proposals'][0]['cost_usd'], 0.5)
        self.assertIsNone(public['test_cost_usd']['total_usd'])

    def make_workspace(self, root, name, *, model=False, baseline=0.5, candidate=0.0, failed=False):
        lab = root / name
        (lab / 'target').mkdir(parents=True)
        (lab / 'target/program.py').write_text('def score(): return 0\n')
        if model:
            (lab / 'target/recipe.json').write_text(json.dumps({'method': 'sft', 'seed': 0}))
        subprocess.run(['git', 'init', '-q', str(lab)], check=True)
        subprocess.run(['git', '-C', str(lab), 'add', 'target'], check=True)
        subprocess.run(['git', '-C', str(lab), '-c', 'user.name=Test', '-c', 'user.email=test@example.org',
                        'commit', '-qm', 'Fixture'], check=True)
        commit = export.git(lab, 'rev-parse', 'HEAD').decode().strip()
        store = export.LineageStore.initialize(lab)
        store.append({'event_type': 'generation', 'decision': 'baseline', 'generation': 0,
                      'candidate_commit': commit})
        store.append({'event_type': 'attempt_started', 'attempt_id': 1})
        training, artifacts = None, {}
        if model:
            training = {'method': 'sft', 'status': 'completed', 'data_sha256': 'training-data',
                        'checkpoint_sha256': 'trained-checkpoint', 'initial_checkpoint_sha256': 'initial-checkpoint',
                        'process': {'argv': ['/private/python']}, 'data_path': '/private/train.json',
                        'result': {'method': 'sft', 'checkpoint_path': '/private/model.json', 'train_examples': 120}}
            for name, data in [('training/evidence.json', training), ('training/result.json', training['result'])]:
                artifact_path = lab / '.nanorsi/runs/one' / name
                export.write(artifact_path, data)
                artifacts[name] = {'path': artifact_path.relative_to(lab).as_posix(),
                                   'sha256': export.sha256(artifact_path.read_bytes()).hexdigest()}
        store.append({'event_type': 'generation', 'attempt_id': 1, 'decision': 'rejected',
                      'generation': 1, 'candidate_commit': commit,
                      'training': training, 'artifacts': artifacts})
        if failed:
            store.append({'event_type': 'attempt_started', 'attempt_id': 2})
            store.append({'event_type': 'attempt_failed', 'attempt_id': 2, 'decision': 'failed', 'reason': 'training failed'})
        frozen = store.append({'event_type': 'freeze', 'decision': 'frozen', 'repeats': 1,
                               'baseline_commit': commit, 'candidate_commit': commit,
                               'experiment_id': 'learner-sft-0-frozen' if model else 'demo-' + name,
                               'seed': 0, 'arm': 'frozen', 'mode': 'model' if model else 'artifact',
                               'conditions': ['baseline', 'candidate'], 'metric': {'name': 'score', 'direction': 'maximize'},
                               'comparison_hash': 'comparison', 'manifest_hash': 'manifest'})
        results = []
        for condition, score in [('baseline', baseline), ('candidate', candidate)]:
            record = {'condition': condition, 'repeat_id': 0,
                      'case_results': [{'task_id': 'test-1', 'repeat_id': 0, 'score': score}],
                      'metrics': {'accuracy': score, 'loss': 1.0 - score},
                      'checkpoint': {'path': 'target/model.json', 'sha256': condition, 'bytes': 12} if model else None}
            results.append(record)
            store.append({'event_type': 'final_result', 'key': condition + '-0', 'result': record})
        final = {key: frozen[key] for key in ['experiment_id', 'seed', 'arm', 'mode', 'conditions', 'metric', 'repeats',
                                             'comparison_hash', 'manifest_hash']}
        final.update(results=results, private_note='do not publish', search_cost_usd={'total_usd': 999})
        export.write(lab / 'reports/final.json', final)
        row = {'status': 'completed', 'workspace': str(lab) if model else name, 'seed': 999,
               'arm': 'self-use', 'private_note': 'do not publish', 'decisions': {'accepted': 999},
               'training_rounds': 999, 'candidate_commit': 'wrong', 'manifest_hash': 'wrong'}
        if model:
            row.update(method='lora', baseline_accuracy=1.0, candidate_accuracy=1.0,
                       baseline_loss=0.0, candidate_loss=0.0, baseline_checkpoint={}, candidate_checkpoint={})
        else:
            row.update(kind=name, scores={'baseline': 1.0, 'candidate': 1.0}, delta_pp=999, accepted=999)
        return lab, row

    def run_export(self, root, live_rows, parameter_rows, **extra):
        live, parameters, output = root / 'live', root / 'parameters', root / 'public'
        export.write(live / 'summary.json', {'schema_version': 1, 'runs': live_rows, 'plan': {'model': 'fixture', 'private_note': 'do not publish'},
                                            'cumulative_requests': 999, 'provider_results': [{'cost_usd': 999}],
                                            'private_note': 'do not publish', **extra})
        request = {'event': 'request_finished', 'id': 'request-1', 'status': 'ok', 'private_note': 'do not publish',
                   'provider': {'model': 'fixture', 'request_id': 'provider-1', 'private_note': 'do not publish'},
                   'usage': {'model_calls': 1, 'input_tokens': 3, 'output_tokens': 2, 'cost_usd': None,
                             'private_note': 'do not publish'}}
        (live / 'requests.jsonl').write_text(json.dumps({'event': 'request_started', 'id': 'request-1'}) + '\n' + json.dumps(request) + '\n')
        export.write(parameters / 'summary.json', {'runs': parameter_rows, 'groups': [{'mean_candidate_accuracy': 999}],
                                                  'paired_proposer_controls': [{'self_use_minus_frozen_accuracy': 999}],
                                                  'private_note': 'do not publish'})
        with patch.object(sys, 'argv', ['export', '--live', str(live), '--parameters', str(parameters), '--output', str(output)]):
            export.main()
        return output

    def test_live_summary_recomputed_and_provider_ledger_is_unsigned(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, row = self.make_workspace(root / 'live', 'program')
            failed = {'kind': 'agent', 'workspace': 'agent', 'status': 'failed', 'error': 'original failure', 'private_note': 'do not publish'}
            output = self.run_export(root, [row, failed], [])
            summary = json.loads((output / 'live/summary.json').read_text())
            public = summary['runs'][0]
            self.assertEqual(public['scores'], {'baseline': 0.5, 'candidate': 0.0})
            self.assertEqual(public['delta_pp'], -50.0)
            self.assertEqual((public['seed'], public['arm'], public['accepted']), (0, 'frozen', 0))
            self.assertEqual(public['manifest_hash'], 'manifest')
            self.assertEqual(summary['runs'][1]['error'], 'original failure')
            self.assertFalse(summary['runs'][1].get('audit', {}).get('locally_verified', False))
            self.assertEqual(summary['cumulative_requests'], 1)
            self.assertEqual(summary['provider_results'][0]['usage']['cost_usd'], None)
            self.assertFalse(summary['provenance']['provider_requests']['hmac_verified'])
            for file in output.rglob('*.json'):
                self.assertNotIn('private_note', file.read_text(), file)

    def test_cpu_rows_and_groups_recomputed_without_losing_failed_measurements(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, row = self.make_workspace(root / 'parameters', 'sft-seed-0-frozen', model=True)
            _, failed = self.make_workspace(root / 'parameters', 'failed-with-final', model=True, failed=True)
            failed['status'], failed['error'] = 'failed', 'original failed attempt'
            zero = {'method': 'sft', 'arm': 'self-use', 'seed': 0, 'status': 'failed',
                    'workspace': str(root / 'parameters/missing'), 'error': 'earlier failure'}
            output = self.run_export(root, [], [row, failed, zero])
            summary = json.loads((output / 'parameter-learning/summary.json').read_text())
            self.assertEqual(len(summary['runs']), 3)
            first = summary['runs'][0]
            self.assertEqual((first['method'], first['arm'], first['seed']), ('sft', 'frozen', 0))
            self.assertEqual((first['baseline_accuracy'], first['candidate_accuracy']), (0.5, 0.0))
            self.assertEqual(first['candidate_checkpoint']['sha256'], 'candidate')
            self.assertEqual(first['decisions'], {'baseline': 1, 'rejected': 1})
            self.assertEqual(first['training_rounds'], 1)
            attempt = json.loads((output / 'parameter-learning/sft-seed-0-frozen/attempts/001.json').read_text())
            evidence = attempt['training/evidence.json']
            self.assertTrue(evidence['sanitized'])
            self.assertEqual(evidence['data']['data_sha256'], 'training-data')
            self.assertEqual(evidence['data']['checkpoint_sha256'], 'trained-checkpoint')
            self.assertEqual(attempt['training/result.json']['data']['train_examples'], 120)
            self.assertNotIn('/private/', json.dumps(attempt))
            observations = json.loads((output / 'parameter-learning/sft-seed-0-frozen/observations.json').read_text())
            self.assertEqual(observations[1]['training']['initial_checkpoint_sha256'], 'initial-checkpoint')
            self.assertEqual(summary['runs'][1]['status'], 'failed')
            self.assertEqual(summary['runs'][1]['candidate_accuracy'], 0.0)
            self.assertEqual(summary['runs'][1]['decisions']['failed'], 1)
            group = next(g for g in summary['groups'] if g['arm'] == 'frozen')
            self.assertEqual((group['completed_runs'], group['failed_runs'], group['accuracy_regressions']), (1, 1, 1))
            self.assertEqual(group['mean_accuracy_delta'], -0.5)
            self.assertEqual(summary['paired_proposer_controls'], [])
            self.assertNotIn('final_report', summary['runs'][2])

    def test_completed_run_requires_all_frozen_final_panels(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lab, row = self.make_workspace(root / 'live', 'program')
            lines = (lab / 'lineage.jsonl').read_text().splitlines()
            (lab / 'lineage.jsonl').write_text('\n'.join(lines[:-1]) + '\n')
            report = json.loads((lab / 'reports/final.json').read_text())
            report['results'].pop()
            export.write(lab / 'reports/final.json', report)
            with self.assertRaisesRegex(ValueError, 'incomplete'):
                self.run_export(root, [row], [])

    def test_failed_partial_final_is_retained_without_completed_audit(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            lab, row = self.make_workspace(root / 'live', 'program')
            row.update(status='failed', error='final evaluation failed')
            lines = (lab / 'lineage.jsonl').read_text().splitlines()
            (lab / 'lineage.jsonl').write_text('\n'.join(lines[:-1]) + '\n')
            report = json.loads((lab / 'reports/final.json').read_text())
            report['results'].pop()
            export.write(lab / 'reports/final.json', report)
            output = self.run_export(root, [row], [])
            public = json.loads((output / 'live/summary.json').read_text())['runs'][0]
            self.assertEqual(public['status'], 'failed')
            self.assertEqual(public['error'], 'final evaluation failed')
            self.assertNotIn('scores', public)
            self.assertFalse(public['audit']['final_complete'])
            final = json.loads((output / 'live/program/final.json').read_text())
            self.assertEqual(len(final['results']), 1)

    def test_snapshot_omits_private_names_and_symlinks(self):
        with tempfile.TemporaryDirectory() as temp:
            lab, _ = self.make_workspace(Path(temp), 'program')
            (lab / 'target/Credentials').mkdir()
            for name in ['Credentials/demo.txt', '.ENV', 'EXAMPLE.KEY']:
                (lab / 'target' / name).write_text('fixture private text')
            (lab / 'target/link.py').symlink_to('/private/example.py')
            subprocess.run(['git', '-C', str(lab), 'add', 'target'], check=True)
            subprocess.run(['git', '-C', str(lab), '-c', 'user.name=Test', '-c', 'user.email=test@example.org',
                            'commit', '-qm', 'Private-name fixtures'], check=True)
            self.assertEqual(set(export.snapshot(lab, 'HEAD')), {'target/program.py'})
