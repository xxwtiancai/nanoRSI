"""Run all searches and freezes before any final-test call; no model API calls."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from dataclasses import asdict
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))
from nanorsi.hashing import canonical_hash
from nanorsi.lineage import LineageStore
from nanorsi.config import load_config
from nanorsi.loop import identity


def sibling(name):
    spec = importlib.util.spec_from_file_location('digits_' + name, Path(__file__).with_name(name + '.py'))
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + '\n')


def command(root, row, label, args):
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'PYTHONDONTWRITEBYTECODE': '1',
           'OPENBLAS_NUM_THREADS': '1', 'OMP_NUM_THREADS': '1'}
    argv = [sys.executable, '-m', 'nanorsi.cli', *args, '--workspace', str(root / row['name'])]
    result = subprocess.run(argv, env=env, capture_output=True, text=True, timeout=900)
    write(root / 'commands' / row['name'] / (label + '.json'),
          {'argv': argv, 'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr})
    if result.returncode:
        raise RuntimeError(label + ': ' + result.stderr.strip())


def normalized_config(config):
    value = asdict(config)
    for key in ['id', 'arm', 'seed', 'goal']:
        value['experiment'].pop(key)
    return value


def require_all_frozen(root, plan):
    """Validate the entire assigned panel before creating or resuming its barrier."""
    plan_hash = plan.get('plan_sha256')
    if not plan_hash or canonical_hash({k: v for k, v in plan.items() if k != 'plan_sha256'}) != plan_hash:
        raise ValueError('frozen study plan hash is invalid')
    marker = None
    lock_path = root / 'all-frozen.json'
    if lock_path.exists():
        try:
            marker = json.loads(lock_path.read_text())
            if not isinstance(marker, dict) or marker.get('plan_sha256') != plan_hash or not isinstance(marker.get('runs'), list):
                raise ValueError('stale or malformed global freeze marker')
        except (OSError, ValueError) as error:
            raise ValueError('invalid global freeze marker') from error
    analyze = sibling('analyze')
    frozen, grouped, names = [], {}, set()
    for row in plan['runs']:
        if row['name'] in names or Path(row['name']).name != row['name']:
            raise ValueError('duplicate or invalid planned workspace name')
        names.add(row['name'])
        lab = root / row['name']
        if not (lab / 'lineage.jsonl').is_file():
            raise ValueError('all planned workspaces must be frozen before final testing')
        events = LineageStore(lab / 'lineage.jsonl', lab / '.nanorsi/lineage.key').verify()
        snapshots = [e for e in events if e.get('event_type') == 'freeze']
        if len(snapshots) != 1:
            raise ValueError('all planned workspaces must have exactly one frozen snapshot')
        snapshot = snapshots[0]
        test_events = [e for e in events if e.get('split') == 'test' or e.get('event_type') in {'final_started', 'final_result'}]
        if test_events and marker is None:
            raise ValueError('test access preceded the global freeze barrier')
        if any(e['seq'] <= snapshot['seq'] for e in test_events):
            raise ValueError('test access preceded workspace freeze')
        config = load_config(lab / 'nanorsi.toml')
        if not config.experiment.goal.endswith('; plan_sha256=' + plan_hash) or identity(lab, config) != snapshot['manifest_hash']:
            raise ValueError('frozen workspace no longer matches the complete study plan')
        method, seed, policy = row['method'], row['seed'], row['policy']
        arm = 'frozen' if policy == 'frozen' else 'self-use'
        expected_id = f'digits-{method}-{seed}-{policy}'
        if (config.experiment.id != expected_id or config.experiment.seed != seed or config.experiment.arm != arm
                or snapshot['experiment_id'] != expected_id or snapshot['seed'] != seed or snapshot['arm'] != arm
                or snapshot['repeats'] != 1 or snapshot['conditions'] != ['baseline', 'candidate']):
            raise ValueError('frozen factors or final conditions differ from study plan')
        baseline = snapshot['baseline_commit']
        saved = tomllib.loads(analyze.git(lab, 'show', baseline + ':nanorsi.toml').decode())
        if saved != tomllib.loads((lab / 'nanorsi.toml').read_text()):
            raise ValueError('baseline config differs from frozen workspace')
        if normalized_config(config) != plan.get('workspace_config') or config.budget.max_steps != plan['rounds']:
            raise ValueError('actual baseline config differs from planned config or rounds')
        recipe = json.loads(analyze.git(lab, 'show', baseline + ':target/recipe.json'))
        expected_recipe = {'method': method, 'seed': seed, 'batch_size': plan['batch_size'], 'attempt': 0,
                           'policy': 'prioritized' if policy in {'frozen', 'self-use'} else policy,
                           'focus_task_ids': [], **plan['settings'][method]}
        if recipe != expected_recipe:
            raise ValueError('actual baseline recipe differs from study plan settings')
        manifest = json.loads(analyze.git(lab, 'show', baseline + ':tasks/manifest.json'))
        counts = {split: sum(t['split'] == split for t in manifest['tasks']) for split in ['train', 'validation', 'test']}
        if (analyze.canonical_hash(manifest) != plan['dataset']['manifest_sha256'] or counts != plan['dataset']['counts']
                or config.evaluator.train_limit != counts['train']
                or config.budget.max_episodes != counts['validation'] + plan['rounds'] * (counts['train'] + 2 * counts['validation'])):
            raise ValueError('actual dataset or scoring budget differs from study plan')
        entry = {'name': row['name'], 'candidate_commit': snapshot['candidate_commit'],
                 'baseline_commit': baseline, 'comparison_hash': snapshot['comparison_hash'],
                 'design_hash': analyze.design_hash(lab, baseline), 'freeze_seq': snapshot['seq']}
        arms = grouped.setdefault((method, seed), {})
        if policy in arms:
            raise ValueError('duplicate planned study factors')
        arms[policy] = entry
        frozen.append(entry)
    for arms in grouped.values():
        if not {'frozen', 'self-use'} <= arms.keys():
            raise ValueError('plan requires a paired frozen and self-use arm')
        if arms['frozen']['comparison_hash'] != arms['self-use']['comparison_hash']:
            raise ValueError('paired comparison hashes differ before final testing')
        if len({arm['design_hash'] for arm in arms.values()}) != 1:
            raise ValueError('control design hashes differ beyond declared policy before final testing')
    methods = sorted({row['method'] for row in plan['runs']})
    if plan.get('primary_inference') != analyze.primary_inference(methods):
        raise ValueError('primary inference family must be fixed in the study plan before testing')
    if marker is not None and marker['runs'] != frozen:
        raise ValueError('global freeze marker differs from the exact frozen run/candidate list')
    return frozen


def parallel(rows, workers, function):
    results = []
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(function, row): row for row in rows}
        for future in as_completed(futures):
            row = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(row['name'] + ': ' + result.get('status', 'completed'), flush=True)
            except Exception as error:
                results.append({**row, 'status': 'failed', 'error': str(error)})
                print(row['name'] + ': failed; evidence retained', flush=True)
    return sorted(results, key=lambda row: row['name'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--phase', choices=['all', 'search', 'final'], default='all')
    parser.add_argument('--methods', nargs='+', choices=['sft', 'rl', 'lora'], default=['sft', 'rl', 'lora'])
    parser.add_argument('--seeds', nargs='+', type=int, default=list(range(10, 20)))
    parser.add_argument('--workers', type=int, default=2)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8 or any(seed < 0 for seed in args.seeds) or len(set(args.seeds)) != len(args.seeds) or len(set(args.methods)) != len(args.methods):
        parser.error('invalid/duplicate factors or worker limit')
    output = args.output.resolve()
    prepare = sibling('prepare')
    if args.phase != 'final':
        output.mkdir(parents=True, exist_ok=False)
        manifest, data = prepare.build_manifest()
        rows = [{'name': f'{method}-seed-{seed}-{policy}', 'method': method, 'seed': seed, 'policy': policy}
                for method in args.methods for seed in args.seeds for policy in prepare.POLICIES]
        plan = {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
                'implementation_commit': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
                'settings': prepare.SETTINGS, 'rounds': 6, 'batch_size': 32, 'dataset': data, 'runs': rows,
                'primary_outcome': 'self-use minus frozen final accuracy in percentage points',
                'selection': 'Settings chosen on validation seeds0,1,2; final confirmation seeds fixed before test.',
                'failure_handling': 'Keep all runs and candidate failures; do not start any final test if a planned workspace is not frozen.',
                'budget_basis': 'Same planned updates/batches/train rows/score panel and validation opportunities within method; report actual and retained work separately.',
                'primary_inference': sibling('analyze').primary_inference(args.methods)}
        # Save the complete configuration before signing the plan; identity fields
        # are checked separately and the eventual goal binds this plan hash.
        with tempfile.TemporaryDirectory() as directory:
            template = Path(directory) / 'contract'
            prepare.prepare_workspace(template, method=args.methods[0], seed=args.seeds[0], policy='frozen',
                                      rounds=plan['rounds'], manifest=manifest, settings=plan['settings'][args.methods[0]])
            plan['workspace_config'] = normalized_config(load_config(template / 'nanorsi.toml'))
        plan['plan_sha256'] = canonical_hash(plan)
        write(output / 'plan.json', plan)
        def search(row):
            prepare.prepare_workspace(output / row['name'], method=row['method'], seed=row['seed'], policy=row['policy'], manifest=manifest, rounds=plan['rounds'], settings=plan['settings'][row['method']], plan_hash=plan['plan_sha256'])
            command(output, row, '01-search', ['run'])
            command(output, row, '02-freeze', ['freeze', '--repeats', '1'])
            return {**row, 'status': 'frozen'}
        status = parallel(rows, args.workers, search)
        write(output / 'search-status.json', status)
        if any(row['status'] == 'failed' for row in status):
            write(output / 'summary.json', sibling('analyze').summarize(status, plan=plan))
            return 1
    else:
        plan = json.loads((output / 'plan.json').read_text())
        rows = plan['runs']
    frozen = require_all_frozen(output, plan)
    lock_path = output / 'all-frozen.json'
    if not lock_path.exists():
        write(lock_path, {'plan_sha256': plan['plan_sha256'], 'created_at': datetime.now(timezone.utc).isoformat(), 'runs': frozen})
    if args.phase == 'search':
        print('All planned workspaces frozen; no final-test calls made.', flush=True)
        return 0
    analyze = sibling('analyze')
    def final(row):
        error = None
        try:
            command(output, row, '03-final-test', ['final-test'])
            command(output, row, '04-verify', ['verify'])
        except Exception as failure:
            error = str(failure)
        # A command failure must not erase an already measured final panel.
        result = {**row, **analyze.read_run(output / row['name'])}
        if error:
            result.update(status='failed', protocol_status='failed', error=error)
        return result
    results = parallel(rows, args.workers, final)
    summary = analyze.summarize(results, plan=plan)
    summary['plan_sha256'] = plan['plan_sha256']
    write(output / 'summary.json', summary)
    print(output / 'summary.json', flush=True)
    return int(any(row['status'] != 'completed' for row in results))


if __name__ == '__main__':
    raise SystemExit(main())
