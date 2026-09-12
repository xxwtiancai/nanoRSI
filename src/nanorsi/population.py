"""Bounded local population search using the ordinary proposal/evaluation kernel.

Workers own unsigned evidence journals; only the locked coordinator writes root
HMAC lineage or promotes an incumbent. This is local thread concurrency, not a
remote execution protocol.
"""
from __future__ import annotations

import json
import math
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from . import cli, loop
from .config import load_config
from .gate import decide
from .gitops import Git
from .lineage import LineageStore, write_json
from .locking import Lock
from .report import write_report
from .surface import SurfacePolicy


class _WorkerStore:
    """Persist worker evidence before external calls without sharing a root writer."""

    def __init__(self, snapshot, path, candidate_id, attempt):
        self.snapshot = [e for e in snapshot if e.get('event_type') not in {
            'episode_reservation', 'episode_reservation_settled'}]
        self.path, self.candidate_id, self.attempt = path, candidate_id, attempt
        self.records = []
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()

    def events(self):
        return self.snapshot + list(self.records)

    def append(self, event):
        record = {**event, 'candidate_id': self.candidate_id, 'attempt_id': self.attempt,
                  'reservation_id': self.candidate_id}
        with self.path.open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, sort_keys=True, allow_nan=False) + '\n')
            handle.flush()
        self.records.append(record)
        return record


def _execute(root, config, parent, job, snapshot):
    run_dir = root / job['run_dir']
    buffer = _WorkerStore(snapshot, run_dir / 'worker-events.jsonl', job['candidate_id'], job['attempt_id'])
    try:
        evidence = cli._attempt(root, config, Git(root), buffer, parent, job['attempt_id'], run_dir,
                                promote=False, proposal_context=job['proposal_context'])
    except Exception as error:
        loop.record_proposal(buffer, run_dir, job['attempt_id'])
        evidence = {'event_type': 'attempt_failed', 'decision': 'failed', 'reason': str(error)}
    write_json(run_dir / 'worker-result.json', evidence)
    return evidence, buffer.records


def _candidate(event):
    return {**event, 'candidate_id': event.get('candidate_id', f"generation-{event['generation']:06d}")}


def _eligible(candidate, config):
    try:
        score = float(candidate['gate_metrics'][config.evaluator.primary_metric])
    except (KeyError, TypeError, ValueError):
        return False
    return math.isfinite(score) and all(candidate.get('gate_constraints', {}).get(name)
                                        for name in config.gate.required_constraints or [])


def _rank(candidates, config, size):
    metric = config.evaluator.primary_metric
    direction = -1 if config.evaluator.direction == 'maximize' else 1
    unique = {c['candidate_id']: c for c in candidates if _eligible(c, config)}
    ranked = sorted(unique.values(), key=lambda c: (direction * float(c['gate_metrics'][metric]), c['candidate_id']))
    commits, retained = set(), []
    for candidate in ranked:
        if candidate['candidate_commit'] not in commits:
            commits.add(candidate['candidate_commit'])
            retained.append(candidate)
    return retained[:size]


def _source(git, commit, config):
    """Read bounded mutable regular blobs, never task fixtures or credentials."""
    policy = SurfacePolicy(config.surface.allow, config.surface.deny)
    files, total = {}, 0
    listing = git._run('ls-tree', '-r', '-z', commit, '--', 'target').stdout
    for entry in listing.split(b'\0'):
        if not entry:
            continue
        metadata, raw_path = entry.split(b'\t', 1)
        mode, kind, blob = metadata.decode().split()
        path = raw_path.decode('utf-8')
        if mode not in {'100644', '100755'} or kind != 'blob':
            continue
        parts = Path(path).parts
        private = {'.git', '.nanorsi', '__pycache__', 'evaluator', 'proposer', 'tasks', 'adapters',
                   'reports', 'runs', 'nanorsi.toml', 'lineage.jsonl', 'credentials', 'secrets'}
        if any(part.lower().startswith('.env') or part.lower().endswith(('.pem', '.key'))
               or part.lower() in private for part in parts):
            continue
        try:
            policy.validate_paths([path])
        except ValueError:
            continue
        size = int(git._run('cat-file', '-s', blob).stdout)
        if size > 64000 or total + size > 192000 or len(files) >= 64:
            continue
        data = git._run('cat-file', 'blob', blob).stdout
        try:
            content = data.decode('utf-8')
        except UnicodeDecodeError:
            continue
        if '\0' not in content:
            files[path], total = content, total + size
    return files


def _initial_population(events, incumbent, config, size):
    candidates = {e['candidate_id']: e for e in events if e.get('event_type') == 'candidate_evaluated'}
    retained = next((e for e in reversed(events) if e.get('event_type') == 'population_retained'), {})
    return _rank([incumbent, *(candidates[c] for c in retained.get('candidate_ids', []) if c in candidates)], config, size) or [incumbent]


def _reserve(root, config, store, retained, size, search_id, round_id):
    events = store.events()
    started = sum(e.get('event_type') == 'attempt_started' for e in events)
    legacy = sum(e.get('event_type') == 'generation' and e.get('decision') != 'baseline' and 'attempt_id' not in e for e in events)
    remaining = config.budget.max_steps - started - legacy
    panel = loop.tasks(root, config)
    episodes = min(4, sum(t['split'] == 'train' for t in panel)) + 2 * sum(t['split'] == 'validation' for t in panel)
    available = config.budget.max_episodes - loop.search_episode_count(events)
    count = min(size, remaining, available // episodes)
    jobs = []
    for index in range(max(0, count)):
        attempt = started + legacy + index + 1
        candidate_id = f'candidate-{attempt:06d}'
        parent = retained[index % len(retained)]
        operator = 'draft' if round_id == 0 and len(retained) == 1 else ('improve' if index % 2 == 0 else 'debug')
        context = {'candidate_id': candidate_id, 'parent_candidate_id': parent['candidate_id'],
                   'population_round': round_id, 'operator': operator, 'extra_parents': []}
        parents = [parent['candidate_id']]
        if len(retained) > 1 and index == count - 1:
            extra = retained[(index + 1) % len(retained)]
            context.update(operator='crossover', extra_parents=[{
                'candidate_id': extra['candidate_id'], 'candidate_commit': extra['candidate_commit'],
                'parent_files': _source(Git(root), extra['candidate_commit'], config)}])
            parents.append(extra['candidate_id'])
        job = {'attempt_id': attempt, 'candidate_id': candidate_id, 'search_id': search_id,
               'population_round': round_id, 'parent_candidate_id': parent['candidate_id'],
               'parent_commit': parent['candidate_commit'], 'crossover_parents': parents if len(parents) > 1 else [],
               'candidate_parents': parents, 'crossover_parent_commits':
                   [parent['candidate_commit'], extra['candidate_commit']] if len(parents) > 1 else [],
               'run_dir': f'.nanorsi/runs/{search_id}-{candidate_id}',
               'proposal_context': context}
        jobs.append((job, parent))
    for job, _ in jobs:
        store.append({'event_type': 'attempt_started', **{k: v for k, v in job.items() if k != 'proposal_context'}})
        store.append({'event_type': 'episode_reservation', 'reservation_id': job['candidate_id'],
                      'attempt_id': job['attempt_id'], 'phase': 'search', 'episodes': episodes})
    return jobs


def _collect(root, git, store, job, evidence, records):
    for record in records:
        store.append(record)
    common = {k: v for k, v in job.items() if k != 'proposal_context'}
    common['operator'] = job['proposal_context']['operator']
    common['artifacts'] = cli._artifacts(root, root / job['run_dir'])
    if 'candidate_commit' in evidence:
        commit = evidence['candidate_commit']
        ancestry = git._run('rev-list', '--parents', '-n', '1', commit, check=False).stdout.decode().split()
        if ancestry != [commit, job['parent_commit']]:
            evidence = {'decision': 'failed', 'reason': 'candidate commit has unexpected Git parent',
                        'failed_candidate_commit': commit, 'observed_ancestry': ancestry}
    if 'candidate_commit' in evidence:
        ref = f"refs/nanorsi/candidates/{job['candidate_id']}"
        git._run('update-ref', ref, evidence['candidate_commit'], '0' * 40)
        result = store.append({**evidence, **common, 'event_type': 'candidate_evaluated',
                               'decision': 'evaluated', 'kernel_decision': evidence['decision'],
                               'candidate_ref': ref})
    else:
        result = store.append({**evidence, **common, 'event_type': 'attempt_failed'})
    store.append({'event_type': 'episode_reservation_settled', 'reservation_id': job['candidate_id'],
                  'attempt_id': job['attempt_id']})
    return result


def _promote(root, config, git, store, incumbent, selected):
    decision = decide(config.gate, parent=incumbent['gate_metrics'],
                      child={**selected['gate_metrics'], 'constraints': selected.get('gate_constraints', {})},
                      parent_heldout=None, child_heldout=None, metric=config.evaluator.primary_metric,
                      direction=config.evaluator.direction)
    if selected['candidate_commit'] == incumbent['candidate_commit'] or decision.decision != 'accepted':
        return incumbent
    generation = incumbent['generation'] + 1
    event = {**selected, 'event_type': 'generation', 'decision': 'accepted', 'reason': decision.reason,
             'generation': generation, 'parent_generation': incumbent['generation'],
             'incumbent_parent_commit': incumbent['candidate_commit']}
    event.pop('seq', None)
    event.pop('receipt', None)
    promoted = store.append(event)
    git.tag(selected['candidate_commit'], f'nanorsi/gen-{generation}')
    return promoted


def add_parser(sub):
    command = sub.add_parser('population', help='Search a bounded population with local concurrent workers')
    command.add_argument('--workspace', type=Path, default=Path.cwd())
    for name, default in [('size', 3), ('generations', 2), ('workers', 2)]:
        command.add_argument('--' + name, type=int, default=default)


def _settings(root, size, generations, workers, config):
    for name, value, cap in [('size', size, 32), ('generations', generations, 32), ('workers', workers, 8)]:
        if type(value) is not int or not 1 <= value <= cap:
            raise ValueError(f'{name} must be between 1 and {cap}')
    persisted = load_config(root / 'nanorsi.toml')
    if config is not None and config != persisted:
        raise ValueError('population config must match the immutable workspace contract')
    if persisted.experiment.schema_version != 2:
        raise RuntimeError('population search requires a schema-v2 experiment')
    return persisted


def run_population(root: Path, *, size=3, generations=2, workers=2, config=None):
    """Retain validation-ranked branches and promote one final global champion.

    A search has at most 32 candidates per round, 32 rounds, and 8 concurrent
    local workers, and remains constrained by the experiment's attempt and
    episode budgets. Test data is never evaluated or passed to the proposer.
    """
    root = Path(root).resolve()
    _settings(root, size, generations, workers, config)
    cli._baseline(root)
    with Lock(root):
        config = _settings(root, size, generations, workers, config)
        git, store = Git(root), LineageStore.initialize(root)
        loop.guard(root, config, store, search=True)
        loop.require_settled(store.events())
        incumbent = _candidate(loop.prepare_parent(root, config, git, store))
        retained = _initial_population(store.events(), incumbent, config, size)
        search_id, rounds, stop_reason = uuid.uuid4().hex[:12], 0, 'generations'
        store.append({'event_type': 'population_started', 'search_id': search_id, 'size': size,
                      'generations': generations, 'workers': workers, 'execution': 'local_threads'})
        try:
            with ThreadPoolExecutor(max_workers=workers, thread_name_prefix='nanorsi-candidate') as pool:
                for round_id in range(generations):
                    jobs = _reserve(root, config, store, retained, size, search_id, round_id)
                    if not jobs:
                        stop_reason = 'budget'
                        break
                    snapshot = store.events()
                    futures = [pool.submit(_execute, root, config, parent, job, snapshot) for job, parent in jobs]
                    evaluated = [_collect(root, git, store, job, *future.result())
                                 for (job, _), future in zip(jobs, futures)]
                    retained = _rank([*retained, *(e for e in evaluated if e.get('event_type') == 'candidate_evaluated')], config, size) or [incumbent]
                    rounds += 1
                    store.append({'event_type': 'population_retained', 'search_id': search_id, 'population_round': round_id,
                                  'candidate_ids': [c['candidate_id'] for c in retained],
                                  'candidate_commits': [c['candidate_commit'] for c in retained]})
            selected = _promote(root, config, git, store, incumbent, retained[0])
            result = {'search_id': search_id, 'candidate_id': selected['candidate_id'],
                      'candidate_commit': selected['candidate_commit'], 'generation': selected['generation'],
                      'retained': [c['candidate_id'] for c in retained], 'rounds': rounds, 'stop_reason': stop_reason}
            store.append({'event_type': 'population_finished', **result})
            store.verify()
            return result
        finally:
            write_report(root, store.events())
