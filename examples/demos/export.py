"""Export synthetic demo observations and source bytes without local secrets.

The public bundle is an unsigned extract of locally verified experiments.
Receipt keys and private workspace configurations are never copied.
"""
import argparse
import base64
from collections import Counter
import importlib.util
from hashlib import sha256
import json
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from nanorsi.lineage import LineageStore
from nanorsi.report import _final_comparison, _training_events, cost_summary

IDENTITY_KEYS = ['manifest_hash', 'comparison_hash', 'experiment_id', 'arm', 'seed']
FINAL_KEYS = IDENTITY_KEYS + ['conditions', 'mode', 'metric', 'repeats']


def select(record, keys):
    return {key: record[key] for key in keys if key in record}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n')


def git(lab, *args):
    return subprocess.check_output(['git', '-C', str(lab), *args])


def snapshot(lab, commit):
    result = {}
    entries = git(lab, 'ls-tree', '-r', '-z', commit, '--', 'target').split(b'\0')
    for entry in filter(None, entries):
        metadata, raw_name = entry.split(b'\t', 1)
        mode, kind, _ = metadata.decode().split()
        name = raw_name.decode('utf-8')
        parts = [part.lower() for part in Path(name).parts]
        if mode not in {'100644', '100755'} or kind != 'blob':
            continue
        if '__pycache__' in parts or name.lower().endswith(('.pyc', '.pyo', '.key', '.pem')) or any(part.startswith('.env') or part in {'secrets', 'credentials'} for part in parts):
            continue
        raw = git(lab, 'show', commit + ':' + name)
        record = {'sha256': sha256(raw).hexdigest(), 'bytes': len(raw)}
        try:
            record['text'] = raw.decode('utf-8')
        except UnicodeDecodeError:
            record['base64'] = base64.b64encode(raw).decode('ascii')
        result[name] = record
    return result


def checked_final(final, events, frozen):
    results = [e['result'] for e in events if e.get('event_type') == 'final_result']
    if final.get('results') != results:
        raise ValueError('derived final report differs from verified lineage results')
    for key in FINAL_KEYS:
        if key in frozen and final.get(key) != frozen[key]:
            raise ValueError('derived final report differs from frozen metadata')
    # Derived files are untrusted caches. Publish only signed facts and aggregates
    # recomputed from those facts; arbitrary report additions never cross here.
    public = select(frozen, FINAL_KEYS)
    event_keys = ['event_type', 'seq', 'phase', 'split', 'invocation_id', 'attempt_id',
                  'repeat_id', 'duration_ms', 'cost_usd', 'usage', 'status', 'metrics']
    public.update(schema_version=2, results=results,
                  search_evaluations=[select(e, event_keys) for e in events if e.get('phase') == 'search'],
                  search_proposals=[select(e, event_keys) for e in events if e.get('event_type') == 'proposal_finished'],
                  search_cost_usd=cost_summary(events, 'search'), test_cost_usd=cost_summary(events, 'test'))
    return public


def verified_workspace(lab, *, require_complete=True):
    events = LineageStore(lab / 'lineage.jsonl', lab / '.nanorsi/lineage.key').verify()
    frozen = next(e for e in events if e.get('event_type') == 'freeze')
    final = checked_final(json.loads((lab / 'reports/final.json').read_text()), events, frozen)
    if require_complete and _final_comparison(events) is None:
        raise ValueError('incomplete frozen final panel')
    if any(e.get('seq', 0) <= frozen['seq'] for e in events
           if e.get('split') == 'test' or e.get('event_type') == 'final_result'):
        raise ValueError('final test must follow freeze')
    return events, frozen, final


def public_training(record):
    keys = ['status', 'method', 'steps', 'batch_size', 'duration_ms', 'compute_budget_s',
            'data_sha256', 'source_sha256', 'trainer_sha256', 'checkpoint_sha256',
            'initial_checkpoint_sha256', 'checkpoint_bytes', 'train_examples', 'examples_seen',
            'accuracy_before', 'accuracy_after', 'loss_before', 'loss_after',
            'sampled_actions', 'sampled_reward_mean', 'cost_usd']
    result = select(record, keys)
    if isinstance(record.get('result'), dict):
        result['result'] = select(record['result'], keys)
    return result


def export_workspace(lab, destination, verified=None):
    events, frozen, final = verified or verified_workspace(lab)
    write(destination / 'final.json', final)
    write(destination / 'sources.json', {condition: {'commit': frozen[condition + '_commit'], 'files': snapshot(lab, frozen[condition + '_commit'])}
                                         for condition in ['baseline', 'candidate']})
    keys = ['event_type', 'attempt_id', 'generation', 'decision', 'kernel_decision', 'candidate_id', 'candidate_parents',
            'crossover_parents', 'operator', 'parent_candidate_id', 'parent_commit', 'candidate_commit', 'proposer_harness_commit',
            'gate_metrics', 'parent_gate_metrics', 'candidate_ids', 'candidate_commits', 'population_round', 'reason']
    observations = [{key: event[key] for key in keys if key in event} for event in events
                    if event.get('event_type') in {'generation', 'attempt_failed', 'candidate_evaluated', 'population_retained'}]
    for observation, event in zip(observations, [e for e in events if e.get('event_type') in {'generation', 'attempt_failed', 'candidate_evaluated', 'population_retained'}]):
        if isinstance(event.get('training'), dict):
            observation['training'] = public_training(event['training'])
    write(destination / 'observations.json', observations)
    for event in events:
        if event.get('event_type') != 'attempt_started':
            continue
        attempt = event['attempt_id']
        terminal = next((e for e in events if e.get('attempt_id') == attempt and e.get('event_type') in {'generation', 'attempt_failed', 'candidate_evaluated'}), None)
        if terminal:
            copied = {}
            for name, ref in terminal.get('artifacts', {}).items():
                if name in {'proposal/proposal.diff', 'proposal/hypothesis.json', 'proposal/trace.json', 'proposal/usage.json', 'gate.json', 'train.json'}:
                    source = lab / ref['path']
                    raw = source.read_bytes()
                    copied[name] = {'sha256': ref['sha256'], 'text': raw.decode('utf-8')}
                elif name in {'training/evidence.json', 'training/result.json'}:
                    # These records contain private absolute process/checkpoint paths.
                    copied[name] = {'source_sha256': ref['sha256'], 'sanitized': True,
                                    'data': public_training(json.loads((lab / ref['path']).read_text()))}
            if terminal.get('candidate_commit'):
                copied['candidate_snapshot'] = {'commit': terminal['candidate_commit'], 'files': snapshot(lab, terminal['candidate_commit'])}
            write(destination / 'attempts' / f'{attempt:03d}.json', copied)
    audit = {'locally_verified': True, 'final_complete': _final_comparison(events) is not None, 'event_count': len(events),
             'artifact_references': sum(len(e.get('artifacts', {})) for e in events),
             'frozen_before_test': all(e.get('seq', 0) > frozen['seq'] for e in events if e.get('split') == 'test'),
             'public_extract_signed': False, 'receipt_keys_published': False,
             'scope': 'workspace lineage, referenced artifacts, and recomputed measurements; excludes unsigned provider ledger'}
    write(destination / 'audit.json', audit)
    return audit


def export_row(row, root, destination, *, parameters=False):
    lab = root / row['workspace']
    name = lab.name
    public = select(row, ['status', 'error'] + (['method', 'arm', 'seed'] if parameters else ['kind']))
    public['workspace'] = name
    if row['status'] != 'completed' and not (lab / 'reports/final.json').is_file():
        public['provenance'] = 'unsigned failure record; no complete verified final panel'
        return public
    verified = verified_workspace(lab, require_complete=row['status'] == 'completed')
    events, frozen, final = verified
    comparison = _final_comparison(events)
    public.update(select(frozen, FINAL_KEYS + ['baseline_commit', 'candidate_commit']))
    public['decisions'] = dict(Counter(e['decision'] for e in events
                                      if e.get('event_type') in {'generation', 'attempt_failed', 'candidate_evaluated'}))
    public['training_rounds'] = len(_training_events(events))
    if parameters:
        recipe = json.loads(git(lab, 'show', frozen['baseline_commit'] + ':target/recipe.json'))
        method = recipe['method']
        if method not in {'sft', 'rl', 'lora'} or frozen['mode'] != 'model':
            raise ValueError('unsupported frozen parameter-learning recipe')
        if frozen['experiment_id'] != f"learner-{method}-{frozen['seed']}-{frozen['arm']}":
            raise ValueError('parameter-learning recipe differs from frozen experiment identity')
        if any(e.get('training', {}).get('method') != method for e in _training_events(events)
               if isinstance(e.get('training'), dict)):
            raise ValueError('signed training method differs from frozen recipe')
        public['method'] = method
        if comparison is not None:
            for condition in ['baseline', 'candidate']:
                records = [r for r in final['results'] if r['condition'] == condition]
                for metric in ['accuracy', 'loss']:
                    public[f'{condition}_{metric}'] = statistics.fmean(r['metrics'][metric] for r in records)
                checkpoints = [r['checkpoint'] for r in records]
                if not checkpoints[0] or any(c != checkpoints[0] for c in checkpoints):
                    raise ValueError('final repeats must measure the same frozen checkpoint')
                public[f'{condition}_checkpoint'] = checkpoints[0]
        if public['decisions'].get('failed') or public['decisions'].get('interrupted'):
            public['status'] = 'failed'
            public.setdefault('error', 'Search attempts failed; verified final measurements retained')
        public['final_report'] = name + '/final.json'
    else:
        kind = frozen['experiment_id'].removeprefix('demo-')
        if frozen['experiment_id'] != 'demo-' + kind or kind not in {'program', 'agent', 'recursive', 'skills', 'population', 'remote'}:
            raise ValueError('unsupported frozen live demo identity')
        name = kind
        public.update(kind=kind, workspace=kind)
        if comparison is not None:
            scores = comparison['scores']
            public.update(scores=scores, delta_pp=100 * (scores['candidate'] - scores['baseline']))
        public.update(attempts=sum(e.get('event_type') == 'attempt_started' for e in events),
                      accepted=sum(e.get('event_type') == 'generation' and e.get('decision') == 'accepted' for e in events),
                      candidate_nodes=sum(e.get('event_type') == 'candidate_evaluated' for e in events),
                      report=kind + '/final.json')
    if (destination / name).exists():
        raise ValueError('duplicate public workspace destination')
    public['audit'] = export_workspace(lab, destination / name, verified)
    return public


def public_request(record):
    result = select(record, ['event', 'id', 'model', 'recorded_at', 'request_number', 'request_sha256',
                             'duration_ms', 'status', 'error'])
    if 'provider' in record:
        result['provider'] = select(record['provider'], ['model', 'request_id'])
    if 'usage' in record:
        result['usage'] = select(record['usage'], ['cost_usd', 'input_tokens', 'output_tokens', 'model_calls'])
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', type=Path, required=True)
    parser.add_argument('--parameters', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--requests', type=Path, help='explicit shared unsigned provider ledger')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must be new; evidence is never overwritten')
    source = json.loads((args.live / 'summary.json').read_text())
    ledger = args.requests or args.live / 'requests.jsonl'
    requests = [public_request(json.loads(line)) for line in ledger.read_text().splitlines() if line.strip()] if ledger.is_file() else []
    unsigned = {'hmac_verified': False, 'source': 'separate unsigned provider request ledger',
                'ledger_available': ledger.is_file()}
    live = {'schema_version': 1,
            'plan': select(source.get('plan', {}), ['schema_version', 'model', 'base_url', 'max_requests', 'max_tokens',
                                                   'thinking', 'seed', 'kinds', 'created_at', 'source_sha256']),
            'runs': [export_row(row, args.live, args.output / 'live') for row in source['runs']],
            'cumulative_requests': sum(e.get('event') == 'request_started' for e in requests) if ledger.is_file() else None,
            'provider_results': [e for e in requests if e.get('event') == 'request_finished'],
            'provenance': {'provider_requests': unsigned, 'plan': 'unsigned execution plan',
                           'remote_workers_and_probes': 'unsigned transport observations'},
            'limitations': ['Small synthetic demos do not establish general recursive self-improvement.',
                            'Source failure records are retained; outcomes may be positive, zero, or negative.',
                            'Provider usage is self-reported unsigned data, not HMAC-verified lineage evidence.']}
    write(args.output / 'live/summary.json', live)
    for name, keys in [
        ('remote-workers.json', ['worker_id', 'pid', 'manifest_sha256', 'evaluator_sha256', 'url']),
        ('remote-probes.json', ['schema_version', 'worker_id', 'worker_pid', 'request_id', 'source_sha256',
                                'manifest_sha256', 'evaluator_sha256', 'split', 'seed', 'repeat_id', 'train_limit', 'score']),
    ]:
        if (args.live / name).is_file():
            write(args.output / 'live' / name, [select(r, keys) for r in json.loads((args.live / name).read_text())])
    write(args.output / 'live/requests.json', requests)
    source = json.loads((args.parameters / 'summary.json').read_text())
    rows = [export_row(row, args.parameters, args.output / 'parameter-learning', parameters=True) for row in source['runs']]
    spec = importlib.util.spec_from_file_location('parameter_summary', ROOT / 'examples/parameter_learning/run.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    write(args.output / 'parameter-learning/summary.json', runner.summarize(rows))
    print(args.output)


if __name__ == '__main__':
    main()
