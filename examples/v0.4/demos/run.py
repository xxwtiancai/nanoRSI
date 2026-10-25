"""Run measured, request-capped live demos through the ordinary nanoRSI CLI.

No canned model responses or winning source patches are used. A result may
be positive, unchanged, negative, or failed; the summary retains every run.
"""
import argparse
from contextlib import ExitStack
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
from nanorsi.configure import _section
from nanorsi.hashing import tree_hash


def cli(lab, *args):
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'PATH': str(Path(sys.executable).parent) + os.pathsep + os.environ.get('PATH', '')}
    command = [sys.executable, '-m', 'nanorsi.cli', *args]
    if lab is not None:
        command += ['--workspace', str(lab)]
    result = subprocess.run(command, env=env, capture_output=True, text=True, timeout=1800)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:600] or f'command {args[0]} failed')
    return result.stdout.strip()


def batch_tasks():
    tasks = []
    for split, old, new in [('train', 'legacy_id', 'account_id'), ('validation', 'old_host', 'service_host'), ('test', 'v1_route', 'v2_route')]:
        inputs = {f'{split}/config_{i}.txt': f'name=service_{i}\n{old}=value_{i}\nkeep=unchanged_{i}\n' for i in range(6)}
        tasks.append({'task_id': split + '-batch-migration', 'group_id': split + '-independent-configs', 'split': split,
                      'instruction': f'Replace every exact occurrence of {old!r} with {new!r} in all provided files; preserve everything else. You have at most four actions including final.',
                      'input_files': inputs, 'expected_files': {name: value.replace(old, new) for name, value in inputs.items()}})
    return {'schema_version': 1, 'tasks': tasks}


def prepare(output, kind, args, ledger):
    template = {'population': 'program', 'recursive': 'agent', 'remote': 'program'}.get(kind, kind)
    lab = output / kind
    goal = ('Learn a reusable executable edit skill for batch text migration under a four-action limit. '
            'You may add target/agent/skills/edit/run.py and update its SKILL.md. Derive general behavior from training feedback; do not store task answers.'
            if kind == 'skills' else 'Improve the general implementation using training execution feedback; preserve the specified interface and fixed evaluation.')
    cli(None, 'new', template, str(lab), '--goal', goal)
    cli(lab, 'configure', '--model', args.model, '--base-url', args.base_url, '--api-key-file', str(args.api_key_file),
        '--max-steps', str(4 if kind == 'population' else 2), '--max-episodes', '200', '--thinking', args.thinking)
    shutil.copy2(Path(__file__).with_name('bounded_model.py'), lab / 'adapters/bounded_model.py')
    path = lab / 'nanorsi.toml'
    text = _section(path.read_text(), 'agent', {'model_command': [sys.executable, 'adapters/bounded_model.py', '--ledger', str(ledger), '--max-requests', str(args.max_requests)],
                                             'max_tokens': args.max_tokens, 'max_turns': 4, 'timeout_s': 120})
    text = _section(text, 'experiment', {'id': 'demo-' + kind, 'seed': args.seed, 'arm': 'self-use' if kind in {'recursive', 'skills'} else 'frozen'})
    if kind == 'skills':
        (lab / 'tasks/manifest.json').write_text(json.dumps(batch_tasks(), indent=2) + '\n')
        text = _section(text, 'proposer', {'timeout_s': 180})
    path.write_text(text)
    return lab


def summarize(lab, kind, error=None):
    result = {'kind': kind, 'workspace': kind, 'status': 'failed' if error else 'completed'}
    if error:
        result['error'] = str(error)
        return result
    report = json.loads((lab / 'reports/final.json').read_text())
    scores = {}
    for condition in report['conditions']:
        cases = [c for row in report['results'] if row['condition'] == condition for c in row['case_results']]
        scores[condition] = sum(c['score'] for c in cases) / len(cases)
    events = [json.loads(line) for line in (lab / 'lineage.jsonl').read_text().splitlines()]
    freeze = next(e for e in events if e.get('event_type') == 'freeze')
    result.update(scores=scores, delta_pp=100 * (scores['candidate'] - scores['baseline']),
                  conditions=report['conditions'], mode=report['mode'], arm=report['arm'], seed=report['seed'],
                  comparison_hash=report['comparison_hash'], manifest_hash=report['manifest_hash'],
                  baseline_commit=freeze['baseline_commit'], candidate_commit=freeze['candidate_commit'],
                  attempts=sum(e.get('event_type') == 'attempt_started' for e in events),
                  accepted=sum(e.get('event_type') == 'generation' and e.get('decision') == 'accepted' for e in events),
                  training_rounds=sum(e.get('event_type') == 'training_finished' for e in events),
                  candidate_nodes=sum(e.get('event_type') == 'candidate_evaluated' for e in events),
                  report=f'{kind}/reports/final.json', lineage=f'{kind}/lineage.jsonl')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--kinds', nargs='+', choices=['program', 'agent', 'recursive', 'skills', 'population', 'remote'], default=['program', 'agent', 'recursive', 'skills', 'population', 'remote'])
    parser.add_argument('--model', required=True)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--api-key-file', type=Path, required=True)
    parser.add_argument('--max-requests', type=int, default=60)
    parser.add_argument('--max-tokens', type=int, default=4096)
    parser.add_argument('--thinking', choices=['disabled', 'enabled'], default='disabled')
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--ledger', type=Path, help='Share a cumulative request cap across invocations')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        parser.error('output must be a new directory; previous outcomes are never overwritten')
    if not 1 <= args.max_requests <= 1000 or not 1 <= args.max_tokens <= 16384 or args.seed < 0:
        parser.error('invalid request/token/seed bounds')
    if len(set(args.kinds)) != len(args.kinds):
        parser.error('demo kinds must be unique')
    args.api_key_file = args.api_key_file.expanduser().resolve()
    output.mkdir(parents=True)
    ledger = (args.ledger or output / 'requests.jsonl').resolve()
    plan = {'schema_version': 1, 'model': args.model, 'base_url': args.base_url, 'max_requests': args.max_requests,
            'max_tokens': args.max_tokens, 'thinking': args.thinking, 'seed': args.seed, 'kinds': args.kinds,
            'created_at': datetime.now(timezone.utc).isoformat(), 'source_sha256': tree_hash(ROOT / 'src/nanorsi', exclude=['**/__pycache__/**', '__pycache__/**'])}
    (output / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    labs, failures = {}, {}
    with ExitStack() as cleanup:
        for kind in args.kinds:
            try:
                lab = prepare(output, kind, args, ledger)
                if kind == 'remote':
                    sys.path.insert(0, str(ROOT / 'examples/remote_workers'))
                    from demo import local_workers, probe_workers
                    import secrets
                    token = output / 'worker-token.key'
                    token.write_text(secrets.token_urlsafe(32)); token.chmod(0o600)
                    cleanup.callback(token.unlink, missing_ok=True)
                    nodes = cleanup.enter_context(local_workers(lab / 'tasks/manifest.json', token, count=2))
                    probes = probe_workers(nodes, token, lab / 'tasks/manifest.json', (lab / 'target/program.py').read_text())
                    shutil.copy2(ROOT / 'examples/remote_workers/remote_evaluate.py', lab / 'adapters/remote_evaluate.py')
                    config = lab / 'nanorsi.toml'
                    command = [sys.executable, 'adapters/remote_evaluate.py', '--urls', *[n['url'] for n in nodes], '--token-file', str(token)]
                    config.write_text(_section(config.read_text(), 'evaluator', {'command': command}))
                    (output / 'remote-workers.json').write_text(json.dumps(nodes, indent=2) + '\n')
                    (output / 'remote-probes.json').write_text(json.dumps(probes, indent=2) + '\n')
                cli(lab, 'baseline')
                cli(lab, 'population', '--size', '2', '--generations', '2', '--workers', '2') if kind == 'population' else cli(lab, 'run')
                cli(lab, 'freeze', '--repeats', '1')
                labs[kind] = lab
                print(f'{kind}: search frozen', flush=True)
            except Exception as error:
                failures[kind] = str(error)
                print(f'{kind}: failed; evidence retained', flush=True)
        # All study choices are frozen before any final test is examined.
        for kind, lab in labs.items():
            try:
                cli(lab, 'final-test'); cli(lab, 'report', '--format', 'html'); cli(lab, 'verify')
            except Exception as error:
                failures[kind] = str(error)
        rows = [summarize(output / kind, kind, failures.get(kind)) for kind in args.kinds]
    events = [json.loads(line) for line in ledger.read_text().splitlines()] if ledger.exists() else []
    summary = {'schema_version': 1, 'plan': plan, 'runs': rows,
               'cumulative_requests': sum(e.get('event') == 'request_started' for e in events),
               'provider_results': [e for e in events if e.get('event') == 'request_finished'],
               'limitations': ['Small authored demos, not general benchmarks or proof of general RSI.',
                               'Program/agent tasks execute locally; the LLM supplies improvement proposals.',
                               'Skills demo tests learned batch execution under a declared four-action budget.',
                               'Recursive source reuse does not by itself prove an advantage over frozen proposing.',
                               'Negative, unchanged and failed outcomes are retained; no gains are guaranteed.']}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2, allow_nan=False) + '\n')
    for row in rows:
        print(row['kind'], row['status'], row.get('scores', {}), row.get('delta_pp'))
    print(output / 'summary.json')
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
