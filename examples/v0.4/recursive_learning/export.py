"""Publish compact, unsigned extracts of locally verified study evidence."""
import argparse
from contextlib import ExitStack
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path


def sibling(name):
    spec = importlib.util.spec_from_file_location('digits_export_' + name, Path(__file__).with_name(name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + '\n')


def line(stream, data):
    stream.write((json.dumps(data, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode())


def public_training(record):
    keys = ['status', 'method', 'steps', 'duration_ms', 'compute_budget_s', 'data_sha256',
            'source_sha256', 'trainer_sha256', 'initial_checkpoint_sha256', 'checkpoint_sha256', 'checkpoint_bytes']
    value = {key: record[key] for key in keys if key in record}
    result_keys = keys + ['schema_version', 'accuracy_after', 'accuracy_before', 'attempt', 'batch_size',
                         'examples_seen', 'loss_after', 'loss_before', 'policy', 'sampled_actions',
                         'sampled_batch_sha256', 'sampled_reward_mean', 'sampling_sha256',
                         'train_examples', 'training_rng_seed', 'training_scoring_examples', 'cost_usd']
    result = record.get('result', {})
    value['result'] = {key: result[key] for key in result_keys if key in result}
    return value


def export(study, output):
    if output.exists():
        raise ValueError('public output must be new; previous results are never overwritten')
    runner, analyze = sibling('run'), sibling('analyze')
    plan = json.loads((study / 'plan.json').read_text())
    runner.require_all_frozen(study, plan)
    output.mkdir(parents=True)
    rows, digests, checkpoint_hashes = [], [], set()
    with ExitStack() as stack:
        compressed = {}
        for name in ['outcomes', 'curricula', 'training', 'checkpoints']:
            raw = stack.enter_context((output / (name + '.jsonl.gz')).open('wb'))
            compressed[name] = stack.enter_context(gzip.GzipFile(filename='', fileobj=raw, mode='wb', mtime=0))
        attempts = stack.enter_context((output / 'attempts.jsonl').open('wb'))
        def checkpoint(lab, commit):
            raw = analyze.git(lab, 'show', commit + ':target/model.json')
            digest = sha256(raw).hexdigest()
            if digest not in checkpoint_hashes:
                line(compressed['checkpoints'], {'sha256': digest, 'bytes': len(raw), 'text': raw.decode()})
                checkpoint_hashes.add(digest)
            return digest
        for factor in plan['runs']:
            lab = study / factor['name']
            row = {**factor, **analyze.read_run(lab)}
            rows.append(row)
            events = analyze.verified_events(lab)
            digests.append({'name': factor['name'], 'journal_sha256': sha256((lab / 'lineage.jsonl').read_bytes()).hexdigest(),
                            'event_count': len(events), 'artifact_references': row['artifact_references']})
            for event in events:
                if event.get('event_type') == 'final_result':
                    result = event['result']
                    line(compressed['outcomes'], {'run': factor['name'], 'condition': result['condition'],
                        'checkpoint_sha256': result['checkpoint']['sha256'], 'metrics': result['metrics'],
                        'cases': [{k: case[k] for k in ['task_id', 'group_id', 'score', 'loss', 'status']} for case in result['case_results']]})
                if event.get('event_type') not in {'generation', 'attempt_failed'} or not event.get('attempt_id'):
                    continue
                public = {'run': factor['name'], **{key: event[key] for key in ['attempt_id', 'generation', 'decision', 'reason', 'parent_commit', 'candidate_commit', 'proposer_harness_commit', 'gate_metrics', 'parent_gate_metrics'] if key in event}}
                for name in ['parent_commit', 'candidate_commit', 'proposer_harness_commit']:
                    if public.get(name):
                        public[name.replace('_commit', '_checkpoint_sha256')] = checkpoint(lab, public[name])
                line(attempts, public)
                artifacts = event.get('artifacts', {})
                trace_ref = artifacts.get('proposal/trace.json')
                if trace_ref:
                    line(compressed['curricula'], {'run': factor['name'], 'attempt_id': event['attempt_id'],
                          'source_sha256': trace_ref['sha256'], 'trace': json.loads((lab / trace_ref['path']).read_text())})
                training_ref = artifacts.get('training/evidence.json')
                if training_ref:
                    original = json.loads((lab / training_ref['path']).read_text())
                    value = public_training(original)
                    line(compressed['training'], {'run': factor['name'], 'attempt_id': event['attempt_id'],
                         'source_sha256': training_ref['sha256'], 'sanitized': True, 'data': value})
            checkpoint(lab, row['baseline_commit'])
            checkpoint(lab, row['candidate_commit'])
    summary = analyze.summarize(rows, plan=plan)
    summary['plan_sha256'] = plan['plan_sha256']
    summary['evidence_status'] = 'unsigned public extract; original local HMAC journals and referenced bytes verified; no keys published'
    write(output / 'summary.json', summary)
    write(output / 'plan.json', plan)
    write(output / 'journal-digests.json', digests)
    write(output / 'all-frozen.json', json.loads((study / 'all-frozen.json').read_text()))
    manifest = {'schema_version': 1, 'runs': len(rows), 'checkpoints': len(checkpoint_hashes),
                'public_extract_signed': False, 'original_implementation_commit': plan['implementation_commit'],
                'files': {p.name: {'sha256': sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size} for p in sorted(output.iterdir()) if p.is_file()}}
    write(output / 'evidence-manifest.json', manifest)
    print(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('study', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    export(args.study, args.output)
