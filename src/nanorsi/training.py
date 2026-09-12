"""Bounded external training with committed, independently hashed checkpoints."""
from __future__ import annotations

import json
import math
from dataclasses import asdict
from hashlib import sha256
from pathlib import Path

from .contracts import source_hash
from .gitops import Git
from .lineage import write_json
from .paths import contained_path
from .process import run_argv
from .surface import SurfacePolicy


class TrainingError(ValueError):
    pass


def checkpoint(root, config):
    relative = config.training['checkpoint']
    path = root / relative
    if any((root / Path(*Path(relative).parts[:i])).is_symlink() for i in range(1, len(Path(relative).parts) + 1)):
        raise TrainingError('checkpoint must not be a symlink')
    path = contained_path(root, relative)
    SurfacePolicy(config.surface.allow, config.surface.deny).validate_paths([relative])
    if not path.is_file():
        raise TrainingError('checkpoint is missing or not a regular file')
    size = path.stat().st_size
    if not 0 < size <= config.training['max_checkpoint_bytes']:
        raise TrainingError('checkpoint is empty or exceeds max_checkpoint_bytes')
    return {'path': relative, 'sha256': sha256(path.read_bytes()).hexdigest(), 'bytes': size}


def _result(path, config, candidate, data_hash, initial):
    if path.is_symlink() or not path.is_file() or path.stat().st_size > config.budget.max_output_bytes:
        raise TrainingError('training result missing, symlinked, or exceeds output byte limit')
    result = json.loads(path.read_text(encoding='utf-8'))
    json.dumps(result, allow_nan=False)
    if not isinstance(result, dict) or type(result.get('schema_version')) is not int or result['schema_version'] != 1 or result.get('status') != 'completed':
        raise TrainingError('training result requires schema_version 1 and completed status')
    if not isinstance(result.get('method'), str) or not result['method'].strip():
        raise TrainingError('training result requires a method')
    cost = result.get('cost_usd')
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (int, float)) or not math.isfinite(cost) or cost < 0):
        raise TrainingError('training cost_usd must be finite and nonnegative or null')
    for name in ['steps', 'duration_ms']:
        if type(result.get(name)) is not int or result[name] < 0:
            raise TrainingError(f'training {name} must be a nonnegative integer')
    saved = checkpoint(candidate, config)
    if Path(result.get('checkpoint_path', '')).absolute() != contained_path(candidate, saved['path']):
        raise TrainingError('training checkpoint_path differs from configured checkpoint')
    for name, expected in [('checkpoint_sha256', saved['sha256']), ('data_sha256', data_hash),
                           ('initial_checkpoint_sha256', initial)]:
        if name in result and result[name] != expected:
            raise TrainingError(f'training {name} does not match measured bytes')
    return {**result, 'checkpoint_sha256': saved['sha256'], 'checkpoint_bytes': saved['bytes']}


def _check_candidate(candidate, config, git, ref, parent):
    from .loop import identity
    changed = git.changed_paths(candidate, ref)
    ignored = Git(candidate)._run('ls-files', '--others', '-z').stdout.decode('utf-8')
    changed = list(dict.fromkeys([*changed, *filter(None, ignored.split('\0'))]))
    SurfacePolicy(config.surface.allow, config.surface.deny).validate_paths(changed)
    if identity(candidate, config) != parent['manifest_hash']:
        raise TrainingError('training changed frozen experiment contract')
    return changed


def run_training(root, config, candidate, run_dir, git, ref, parent):
    from .loop import tasks
    from .config import load_config, _fixed_training_command
    directory = run_dir / 'training'
    data_path, result_path = directory / 'data.json', directory / 'result.json'
    write_json(data_path, {'schema_version': 1, 'tasks': [row for row in tasks(candidate, config) if row['split'] == 'train']})
    evidence = {'status': 'started', 'checkpoint_path': config.training['checkpoint'],
                'source_sha256': source_hash(candidate / 'target'),
                'trainer_sha256': source_hash(candidate / 'trainer'), 'data_sha256': sha256(data_path.read_bytes()).hexdigest(),
                'data_path': data_path.relative_to(root).as_posix(), 'compute_budget_s': config.training['compute_budget_s']}
    try:
        saved = load_config(candidate / 'nanorsi.toml')
        _fixed_training_command(candidate, config.training['command'], {'allow': config.surface.allow, 'deny': config.surface.deny})
        if saved.training != config.training:
            raise TrainingError('candidate training configuration differs from frozen command')
        _check_candidate(candidate, config, git, ref, parent)
        initial = checkpoint(candidate, config)
        evidence['initial_checkpoint_sha256'] = initial['sha256']
        process = run_argv(config.training['command'], cwd=candidate, timeout_s=config.training['compute_budget_s'],
                           max_output_bytes=config.budget.max_output_bytes,
                           extra_env={'PYTHONDONTWRITEBYTECODE': '1', 'NANORSI_TRAINING_DATA_PATH': str(data_path),
                                      'NANORSI_TRAINING_RESULT_PATH': str(result_path),
                                      'NANORSI_CHECKPOINT_PATH': str(contained_path(candidate, config.training['checkpoint']))})
        evidence.update(process=asdict(process), duration_ms=process.duration_ms)
        _check_candidate(candidate, config, git, ref, parent)
        if process.timed_out or process.output_limited or process.exit_code != 0:
            raise TrainingError('trainer timed out, exceeded output limit, or failed')
        if sha256(data_path.read_bytes()).hexdigest() != evidence['data_sha256']:
            raise TrainingError('trainer changed training input data')
        result = _result(result_path, config, candidate, evidence['data_sha256'], initial['sha256'])
        evidence.update(result=result, method=result['method'], steps=result['steps'], status='completed',
                        checkpoint_sha256=result['checkpoint_sha256'], checkpoint_bytes=result['checkpoint_bytes'])
        return evidence
    except Exception as error:
        evidence.update(status='failed', reason=str(error))
        raise
    finally:
        write_json(directory / 'evidence.json', evidence)
