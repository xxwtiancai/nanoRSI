"""Prepare the fixed digits split and optional NumPy training adapter."""
from __future__ import annotations
import argparse
import csv
import gzip
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT / 'src'))
from nanorsi.hashing import canonical_hash
from nanorsi.gitops import Git
from nanorsi.templates import render_template

SPLIT_SEED = 20260912
SETTINGS = {
    'sft': {'lr': .3, 'multiplier': 9, 'steps': 24, 'balanced': True},
    'rl': {'lr': .3, 'multiplier': 3, 'steps': 8, 'balanced': False},
    'lora': {'lr': .3, 'multiplier': 3, 'steps': 24, 'balanced': False},
}
POLICIES = ('frozen', 'self-use', 'uniform', 'random')


def build_manifest():
    import numpy as np  # Optional example tooling; not a nanoRSI dependency.
    source = Path(__file__).with_name('data') / 'digits.csv.gz'
    with gzip.open(source, 'rt') as stream:
        data = [[int(float(value)) for value in row] for row in csv.reader(stream)]
    if len(data) != 1797 or any(len(row) != 65 for row in data):
        raise ValueError('unexpected digits source shape')
    if len({tuple(row[:64]) for row in data}) != len(data):
        raise ValueError('duplicate images require a grouped split before running')
    labels = np.asarray([row[-1] for row in data])
    rng = np.random.default_rng(SPLIT_SEED)
    indices = {split: [] for split in ['train', 'validation', 'test']}
    for label in range(10):
        selected = np.flatnonzero(labels == label)
        rng.shuffle(selected)
        a, b = int(len(selected) * .6), int(len(selected) * .8)
        for split, ids in [('train', selected[:a]), ('validation', selected[a:b]), ('test', selected[b:])]:
            indices[split].extend(int(index) for index in ids)
    tasks = []
    for split, ids in indices.items():
        for index, source_id in enumerate(ids):
            tasks.append({'task_id': f'{split}-{index:04d}', 'group_id': f'digits-row-{source_id:04d}',
                          'split': split, 'instruction': 'Predict digit 0 to 9 from its 64 pixel values.',
                          'input_files': {'features.json': json.dumps(data[source_id][:64])},
                          'expected_files': {'label.txt': str(data[source_id][-1])}})
    manifest = {'schema_version': 1, 'tasks': tasks}
    metadata = {'dataset': 'UCI optical digits / scikit-learn 1797-row subset, resplit',
                'source_sha256': sha256(source.read_bytes()).hexdigest(), 'split_seed': SPLIT_SEED,
                'counts': {split: len(ids) for split, ids in indices.items()},
                'split_sha256': canonical_hash(indices), 'manifest_sha256': canonical_hash(manifest),
                'numpy_version': np.__version__}
    return manifest, metadata


def runtime_module():
    path = Path(__file__).with_name('runtime') / 'network.py'
    spec = importlib.util.spec_from_file_location('digits_network', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_workspace(workspace, *, method, seed, policy, rounds=6, manifest=None, settings=None, plan_hash=None):
    workspace = Path(workspace)
    if method not in SETTINGS or policy not in POLICIES or type(seed) is not int or seed < 0 or type(rounds) is not int or rounds < 1:
        raise ValueError('invalid method, seed, policy or rounds')
    goal = 'Measure additional checkpoint-reuse benefit under matched training budgets'
    if plan_hash is not None:
        goal += '; plan_sha256=' + plan_hash
    render_template('model', workspace, goal=goal)
    runtime = Path(__file__).with_name('runtime')
    shutil.copy2(runtime / 'network.py', workspace / 'trainer/network.py')
    shutil.copy2(runtime / 'propose.py', workspace / 'proposer/propose.py')
    evaluator = workspace / 'evaluator/evaluate.py'
    evaluator.write_text(evaluator.read_text().replace('max(range(3),', 'max(range(model["classes"]),'))
    model = runtime_module().initial_model(seed)
    (workspace / 'target/model.json').write_text(json.dumps(model, indent=2, sort_keys=True) + '\n')
    recipe = {'method': method, 'seed': seed, 'batch_size': 32, 'attempt': 0,
              'policy': 'prioritized' if policy in {'frozen', 'self-use'} else policy,
              'focus_task_ids': [], **(settings or SETTINGS[method])}
    (workspace / 'target/recipe.json').write_text(json.dumps(recipe, indent=2, sort_keys=True) + '\n')
    manifest = manifest or build_manifest()[0]
    (workspace / 'tasks/manifest.json').write_text(json.dumps(manifest, sort_keys=True) + '\n')
    counts = {split: sum(t['split'] == split for t in manifest['tasks']) for split in ['train', 'validation', 'test']}
    config = workspace / 'nanorsi.toml'
    content = config.read_text().replace('id = "learner-lab"', f'id = "digits-{method}-{seed}-{policy}"')
    content = content.replace('seed = 0', f'seed = {seed}', 1).replace('arm = "self-use"', f'arm = "{"frozen" if policy == "frozen" else "self-use"}"')
    content = content.replace('primary_metric = "score"', 'primary_metric = "loss"').replace('direction = "maximize"', 'direction = "minimize"')
    content = content.replace('heldout_enabled = false', f'heldout_enabled = false\ntrain_limit = {counts["train"]}')
    content = content.replace('max_steps = 3', f'max_steps = {rounds}')
    episodes = counts['validation'] + rounds * (counts['train'] + 2 * counts['validation'])
    content = content.replace('max_episodes = 1000', f'max_episodes = {episodes}').replace('max_output_bytes = 1000000', 'max_output_bytes = 8000000')
    content = content.replace('compute_budget_s = 10', 'compute_budget_s = 60').replace('timeout_s = 20', 'timeout_s = 60')
    config.write_text(content)
    Git(workspace).init()
    return workspace


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('workspace', type=Path)
    parser.add_argument('--method', choices=SETTINGS, default='sft')
    parser.add_argument('--policy', choices=POLICIES, default='self-use')
    parser.add_argument('--seed', type=int, default=10)
    args = parser.parse_args()
    print(prepare_workspace(args.workspace, method=args.method, seed=args.seed, policy=args.policy))
