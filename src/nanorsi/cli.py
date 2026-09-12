from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from pathlib import Path

from .config import load_config
from .gate import decide
from .gitops import Git, GitError
from .lineage import LineageStore, artifact
from .locking import Lock
from . import loop
from .proposer import ProposalError, run_proposer
from .report import write_report
from .surface import SurfacePolicy
from .templates import render_template


def _baseline(root: Path) -> dict:
    git = Git(root)
    git.ensure_repository()
    with Lock(root):
        config = load_config(root / 'nanorsi.toml')
        store = LineageStore.initialize(root)
        loop.guard(root, config, store)
        existing = [e for e in store.events() if e.get('decision') == 'baseline' and 'gate_metrics' in e]
        if existing:
            return existing[0]
        if git.ref_exists('HEAD') and not git.is_clean():
            raise GitError('workspace must be clean before baseline')
        commit = git.resolve_ref('HEAD') if git.ref_exists('HEAD') else git.commit_all('Establish a reproducible experiment starting point')
        if not git.ref_exists('nanorsi/gen-0'):
            git.tag(commit, 'nanorsi/gen-0')
        run_dir = root / '.nanorsi' / 'baseline' / uuid.uuid4().hex[:10]
        contract = loop.identity(root, config)
        store.append({'event_type': 'baseline_started', 'decision': 'baseline', 'manifest_hash': contract})
        with git.worktree(commit, root / '.nanorsi/worktrees/baseline') as checkout:
            split = 'validation' if config.experiment.schema_version == 2 else 'gate'
            gate = loop.evaluate(root, config, checkout, split, run_dir / 'gate.json', store)
            heldout = loop.evaluate(root, config, checkout, 'heldout', run_dir / 'heldout.json', store) if config.evaluator.heldout_enabled and config.experiment.schema_version == 1 else None
        event = store.append({'event_type': 'generation', 'experiment_id': config.experiment.id,
                              'generation': 0, 'parent_generation': None, 'decision': 'baseline',
                              'candidate_commit': commit, 'candidate_tree': git.tree_hash(commit),
                              'gate_metrics': gate.metrics, 'gate_constraints': gate.constraints,
                              'heldout_metrics': heldout.metrics if heldout else None,
                              'evaluator_fingerprint': loop.fingerprint(root), 'manifest_hash': contract,
                              'artifacts': _artifacts(root, run_dir)})
        write_report(root, store.events())
        return event


def _artifacts(root, directory):
    return {p.relative_to(directory).as_posix(): artifact(root, p) for p in directory.rglob('*') if p.is_file() and not p.is_symlink()}


def _step(root: Path) -> dict:
    config, git = load_config(root / 'nanorsi.toml'), Git(root)
    with Lock(root):
        store = LineageStore.initialize(root)
        store.verify()
        parent = loop.prepare_parent(root, config, git, store)
        attempt = loop.begin_attempt(root, config, store)
        run_dir = root / '.nanorsi/runs' / uuid.uuid4().hex[:10]
        try:
            event = _attempt(root, config, git, store, parent, attempt, run_dir)
        except Exception as error:
            loop.record_proposal(store, run_dir, attempt)
            store.append({'event_type': 'attempt_failed', 'attempt_id': attempt, 'decision': 'failed',
                          'reason': str(error), 'artifacts': _artifacts(root, run_dir)})
            raise
        finally:
            write_report(root, store.events())
        return event


def _attempt(root, config, git, store, parent, attempt, run_dir):
    ref = parent['candidate_commit']
    with git.worktree(ref, root / '.nanorsi/worktrees' / run_dir.name) as checkout:
        feedback = loop.train_feedback(root, config, checkout, run_dir, store)
        store.append({'event_type': 'proposal_started', 'attempt_id': attempt})
        proposal, proposer_commit = _propose(root, config, git, checkout, parent, attempt, feedback, run_dir)
        loop.record_proposal(store, run_dir, attempt)
        if git.changed_paths(checkout, ref):
            raise ProposalError('proposer modified the parent checkout directly')
        if not proposal.diff.strip():
            return store.append({'event_type': 'attempt_failed', 'attempt_id': attempt, 'decision': 'no-op',
                                 'reason': 'proposal changes no files', 'proposer_harness_commit': proposer_commit,
                                 'artifacts': _artifacts(root, run_dir)})
        git.apply_diff(checkout, proposal.diff)
        changed = git.changed_paths(checkout, ref)
        SurfacePolicy(config.surface.allow, config.surface.deny).validate_paths(changed)
        if loop.fingerprint(checkout) != parent.get('evaluator_fingerprint'):
            raise RuntimeError('candidate evaluator differs from baseline')
        if loop.identity(checkout, config) != parent['manifest_hash']:
            raise RuntimeError('candidate changed frozen experiment contract')
        commit = git.commit_paths(checkout, changed, 'Measure a proposed improvement before adoption')
        split = 'validation' if config.experiment.schema_version == 2 else 'gate'
        if config.experiment.schema_version == 2:
            with git.worktree(ref, root / '.nanorsi/worktrees' / (run_dir.name + '-parent')) as old:
                measured_parent = loop.evaluate(root, config, old, split, run_dir / 'parent.json', store)
        else:
            measured_parent = None
        gate = loop.evaluate(root, config, checkout, split, run_dir / 'gate.json', store)
        heldout = loop.evaluate(root, config, checkout, 'heldout', run_dir / 'heldout.json', store) if config.evaluator.heldout_enabled and config.experiment.schema_version == 1 else None
        return _record(root, config, git, store, parent, proposal, changed, commit, gate, heldout,
                       attempt, proposer_commit, measured_parent, run_dir)


def _propose(root, config, git, checkout, parent, attempt, feedback, run_dir):
    proposer_commit = git.resolve_ref('nanorsi/gen-0') if config.experiment.arm == 'frozen' else parent['candidate_commit']
    context = {'goal': config.experiment.goal, 'surface': config.surface.allow, 'attempt_id': attempt,
               'parent_generation': parent['generation'], 'parent_commit': parent['candidate_commit'],
               'proposer_harness_commit': proposer_commit, 'agent': config.agent, 'train_results': feedback}
    if config.experiment.schema_version == 1:
        context['gate_metrics'] = parent['gate_metrics']
        return run_proposer(config, checkout, run_dir / 'proposal', context), proposer_commit
    with git.worktree(proposer_commit, root / '.nanorsi/worktrees' / (run_dir.name + '-proposer')) as source:
        return run_proposer(config, checkout, run_dir / 'proposal', context,
                            extra_env={'NANORSI_PROPOSER_HARNESS': str(source)}), proposer_commit


def _record(root, config, git, store, parent, proposal, changed, commit, gate, heldout,
            attempt, proposer_commit, measured_parent, run_dir):
    decision = decide(config.gate, parent=measured_parent.metrics if measured_parent else parent['gate_metrics'],
                      child={**gate.metrics, 'constraints': gate.constraints},
                      parent_heldout=parent.get('heldout_metrics'), child_heldout=heldout.metrics if heldout else None,
                      metric=config.evaluator.primary_metric, direction=config.evaluator.direction)
    generation = parent['generation'] + (decision.decision == 'accepted')
    event = store.append({'event_type': 'generation', 'experiment_id': config.experiment.id,
                          'attempt_id': attempt, 'generation': generation, 'parent_generation': parent['generation'],
                          'decision': decision.decision, 'reason': decision.reason, 'candidate_commit': commit,
                          'candidate_tree': git.tree_hash(commit), 'changed_paths': changed, 'hypothesis': proposal.hypothesis,
                          'gate_metrics': gate.metrics, 'gate_constraints': gate.constraints,
                          'heldout_metrics': heldout.metrics if heldout else None,
                          'evaluator_fingerprint': parent['evaluator_fingerprint'], 'manifest_hash': parent['manifest_hash'],
                          'proposer_harness_commit': proposer_commit, 'artifacts': _artifacts(root, run_dir)})
    if decision.decision == 'accepted':
        git.tag(commit, f'nanorsi/gen-{generation}')
    return event


def _evaluate(root, split, ref):
    config, store = load_config(root / 'nanorsi.toml'), LineageStore.initialize(root)
    with Lock(root):
        loop.guard(root, config, store, search=True)
        if config.experiment.schema_version == 2 and split not in {'train', 'validation'}:
            raise RuntimeError('v2 evaluate permits train/validation; use freeze then final-test for test')
        selected = ref or store.latest_accepted()['candidate_commit']
        output = root / '.nanorsi' / f'evaluation-{uuid.uuid4().hex}.json'
        with Git(root).worktree(selected, root / '.nanorsi/worktrees/evaluate') as checkout:
            result = loop.evaluate(root, config, checkout, split, output, store)
        return {'metrics': result.metrics, 'constraints': result.constraints, 'split': split}


def _recover(root):
    lock = root / '.nanorsi/lock'
    if lock.exists():
        try:
            os.kill(int(lock.read_text().strip()), 0)
        except ProcessLookupError:
            lock.unlink()
        else:
            raise RuntimeError('lock is still owned by a live process')
    with Lock(root):
        git = Git(root)
        git.prune_worktrees()
        worktrees = root / '.nanorsi/worktrees'
        if worktrees.exists():
            shutil.rmtree(worktrees)
        git.prune_worktrees()
        store = LineageStore.initialize(root)
        store.recover_attempts()
        for event in store.events():
            if event.get('decision') == 'accepted' and not git.ref_exists(f"nanorsi/gen-{event['generation']}"):
                git.tag(event['candidate_commit'], f"nanorsi/gen-{event['generation']}")


def _configure_parser(sub):
    command = sub.add_parser('configure', allow_abbrev=False, help='Configure a model before baseline; never pass the API key as an argument')
    command.add_argument('--workspace', type=Path, default=Path.cwd())
    command.add_argument('--model', required=True, help='Exact provider model ID')
    command.add_argument('--base-url', required=True, help='Compatible chat-completions API base URL')
    auth = command.add_mutually_exclusive_group(required=True)
    auth.add_argument('--prompt-key', action='store_true', help='Hidden terminal input; store key outside workspace')
    auth.add_argument('--api-key-file', type=Path, help='Existing external key file')
    auth.add_argument('--no-api-key', action='store_true', help='Endpoint accepts anonymous requests')
    command.add_argument('--max-steps', type=int, help='Maximum search attempts')
    command.add_argument('--max-episodes', type=int, help='Maximum search task episodes (final panel separate)')
    command.add_argument('--token-parameter', choices=['max_tokens', 'max_completion_tokens'])


def _parser():
    parser = argparse.ArgumentParser(prog='nanorsi')
    sub = parser.add_subparsers(dest='command', required=True)
    _configure_parser(sub)
    new = sub.add_parser('new')
    new.add_argument('template', choices=['artifact', 'harness', 'model', 'skills', 'coding'])
    new.add_argument('destination', type=Path)
    new.add_argument('--goal', default='Improve the target')
    for name in ['baseline', 'step', 'run', 'report', 'verify', 'doctor', 'recover', 'freeze', 'final-test', 'evaluate']:
        command = sub.add_parser(name)
        command.add_argument('--workspace', type=Path, default=Path.cwd())
        if name == 'report':
            command.add_argument('--format', choices=['markdown', 'html'], default='markdown')
        if name == 'doctor':
            command.add_argument('--check-model', action='store_true', help='Send one model request; may incur API cost outside experiment accounting')
        if name in {'freeze', 'final-test'}:
            command.add_argument('--repeats', type=int, default=3 if name == 'freeze' else None)
        if name == 'evaluate':
            command.add_argument('--split', default='gate', choices=['train', 'gate', 'heldout', 'validation'])
            command.add_argument('--ref')
    return parser


def _dispatch(args, root):
    command = args.command
    if command == 'configure':
        from .configure import configure
        keys = ['model', 'base_url', 'api_key_file', 'prompt_key', 'no_api_key', 'max_steps', 'max_episodes', 'token_parameter']
        return configure(root, **{key: getattr(args, key) for key in keys})
    if command == 'baseline':
        return _baseline(root)
    if command == 'step':
        event = _step(root)
        return {key: event[key] for key in ['attempt_id', 'generation', 'decision', 'candidate_tree', 'reason'] if key in event}
    if command == 'evaluate':
        return _evaluate(root, args.split, args.ref)
    if command == 'run':
        _baseline(root)
        return loop.bounded_run(root, load_config(root / 'nanorsi.toml'), _step)
    if command in {'freeze', 'final-test'}:
        fn = loop.freeze if command == 'freeze' else loop.final_test
        return fn(root, load_config(root / 'nanorsi.toml'), args.repeats)
    if command == 'report':
        return write_report(root, LineageStore.initialize(root).verify(), format=args.format)
    if command == 'verify':
        LineageStore.initialize(root).verify()
        return 'lineage: ok'
    if command == 'recover':
        _recover(root)
        return 'recovered stale nanoRSI state'
    from .doctor import doctor
    ok, output = doctor(root, check_model=args.check_model)
    if not ok:
        raise RuntimeError(output.strip())
    return output


def main(argv=None):
    args = _parser().parse_args(argv)
    try:
        if args.command == 'new':
            files = render_template(args.template, args.destination, goal=args.goal)
            Git(args.destination).init()
            print(f'created {args.template} workspace with {len(files)} files')
            if args.template in {'coding', 'skills'}:
                print('Next: nanorsi configure --help (set model, endpoint and authentication before baseline)')
            return 0
        result = _dispatch(args, args.workspace.resolve())
        print(json.dumps(result, sort_keys=True) if isinstance(result, (dict, list)) else str(result))
        return 0
    except Exception as error:
        print(f'nanorsi: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
