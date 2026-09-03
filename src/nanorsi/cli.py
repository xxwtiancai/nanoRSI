from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import uuid
from pathlib import Path

from .config import load_config
from .evaluator import EvaluationError, run_evaluation
from .gate import decide
from .gitops import Git, GitError
from .hashing import tree_hash
from .lineage import LineageStore
from .locking import Lock
from .proposer import ProposalError, load_proposal, run_proposer
from .report import write_report
from .templates import render_template


def _store(root: Path) -> LineageStore:
    return LineageStore.initialize(root)


def _baseline(root: Path) -> dict:
    config = load_config(root / "nanorsi.toml")
    git = Git(root)
    git.ensure_repository()
    store = _store(root)
    existing = [event for event in store.events() if event.get("decision") == "baseline"]
    if existing:
        return existing[0]
    if not git.ref_exists("HEAD"):
        commit = git.commit_all("nanoRSI generation 0")
    else:
        if not git.is_clean():
            raise GitError("workspace must be clean before baseline")
        commit = git.resolve_ref("HEAD")
    git.tag(commit, "nanorsi/gen-0")
    with git.worktree("nanorsi/gen-0", root / ".nanorsi/worktrees/baseline") as checkout:
        gate = run_evaluation(config, checkout, "gate", root / ".nanorsi/baseline-gate.json")
        heldout = run_evaluation(config, checkout, "heldout", root / ".nanorsi/baseline-heldout.json") if config.evaluator.heldout_enabled else None
    event = store.append(
        {
            "event_type": "generation", "experiment_id": config.experiment.id, "generation": 0,
            "parent_generation": None, "decision": "baseline", "candidate_commit": commit,
            "candidate_tree": git.tree_hash(commit), "gate_metrics": gate.metrics,
            "gate_constraints": gate.constraints, "heldout_metrics": heldout.metrics if heldout else None,
            "evaluator_fingerprint": tree_hash(root / "evaluator"),
        }
    )
    write_report(root, store.events())
    return event


def _step(root: Path) -> dict:
    config = load_config(root / "nanorsi.toml")
    git = Git(root)
    git.ensure_repository()
    store = _store(root)
    store.verify()
    parent = store.latest_accepted()
    if parent["generation"] >= config.budget.max_steps:
        raise RuntimeError("generation budget reached")
    run_id = uuid.uuid4().hex[:10]
    run_dir = root / ".nanorsi" / "runs" / run_id
    generation = parent["generation"] + 1
    parent_ref = f"nanorsi/gen-{parent['generation']}"
    worktree = root / ".nanorsi" / "worktrees" / run_id
    with Lock(root), git.worktree(parent_ref, worktree) as checkout:
        proposal = run_proposer(
            config, checkout, run_dir / "proposal",
            {"goal": config.experiment.goal, "surface": config.surface.allow, "parent_generation": parent["generation"], "gate_metrics": parent.get("gate_metrics")},
        )
        if git.changed_paths(checkout, parent_ref):
            raise ProposalError("proposer modified the parent checkout directly")
        git.apply_diff(checkout, proposal.diff)
        changed = git.changed_paths(checkout, parent_ref)
        from .surface import SurfacePolicy
        SurfacePolicy(config.surface.allow, config.surface.deny).validate_paths(changed)
        evaluator_fingerprint = tree_hash(checkout / "evaluator")
        if evaluator_fingerprint != parent.get("evaluator_fingerprint"):
            raise RuntimeError("candidate evaluator differs from baseline")
        commit = git.commit_paths(checkout, changed, f"nanoRSI generation {generation}")
        gate = run_evaluation(config, checkout, "gate", run_dir / "gate.json")
        heldout = None
        if config.evaluator.heldout_enabled:
            heldout = run_evaluation(config, checkout, "heldout", run_dir / "heldout.json")
        return _record_generation(root, config, git, store, parent, proposal, changed, commit, gate, heldout, generation)


def _record_generation(root, config, git, store, parent, proposal, changed, commit, gate, heldout, generation):
    decision = decide(
        config.gate,
        parent={"score": parent["gate_metrics"][config.evaluator.primary_metric]},
        child={"score": gate.metrics[config.evaluator.primary_metric], "constraints": gate.constraints},
        parent_heldout={"score": parent["heldout_metrics"][config.evaluator.primary_metric]} if parent.get("heldout_metrics") else None,
        child_heldout={"score": heldout.metrics[config.evaluator.primary_metric]} if heldout else None,
        metric=config.evaluator.primary_metric,
        direction=config.evaluator.direction,
    )
    event = store.append(
        {
            "event_type": "generation", "experiment_id": config.experiment.id,
            "generation": generation, "parent_generation": parent["generation"],
            "decision": decision.decision, "reason": decision.reason,
            "candidate_commit": commit, "candidate_tree": git.tree_hash(commit),
            "changed_paths": changed, "hypothesis": proposal.hypothesis,
            "gate_metrics": gate.metrics, "gate_constraints": gate.constraints,
            "heldout_metrics": heldout.metrics if heldout else None,
        }
    )
    if decision.decision == "accepted":
        git.tag(commit, f"nanorsi/gen-{generation}")
    write_report(root, store.events())
    return event


def _evaluate(root: Path, split: str, ref: str | None) -> dict:
    config = load_config(root / "nanorsi.toml")
    git = Git(root)
    git.ensure_repository()
    store = _store(root)
    selected = ref or f"nanorsi/gen-{store.latest_accepted()['generation']}"
    result_path = root / ".nanorsi" / f"evaluation-{split}-{uuid.uuid4().hex[:8]}.json"
    with git.worktree(selected, root / ".nanorsi/worktrees/evaluate") as checkout:
        result = run_evaluation(config, checkout, split, result_path)
    return {"metrics": result.metrics, "constraints": result.constraints, "split": split}


def _recover(root: Path) -> None:
    lock = root / ".nanorsi" / "lock"
    if lock.exists():
        process_id = int(lock.read_text(encoding="utf-8").strip())
        try:
            os.kill(process_id, 0)
        except ProcessLookupError:
            lock.unlink()
        else:
            raise RuntimeError("lock is still owned by a live process")
    git = Git(root)
    git.ensure_repository()
    git.prune_worktrees()
    worktrees = root / ".nanorsi" / "worktrees"
    if worktrees.exists():
        shutil.rmtree(worktrees)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="nanorsi")
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("new")
    new.add_argument("template", choices=["artifact", "harness", "model"])
    new.add_argument("destination", type=Path)
    new.add_argument("--goal", default="Improve the target")
    for name in ["baseline", "step", "report", "verify", "doctor", "recover"]:
        command = sub.add_parser(name)
        command.add_argument("--workspace", type=Path, default=Path.cwd())
    evaluate = sub.add_parser("evaluate")
    evaluate.add_argument("--workspace", type=Path, default=Path.cwd())
    evaluate.add_argument("--split", default="gate", choices=["train", "gate", "heldout"])
    evaluate.add_argument("--ref")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "new":
        files = render_template(args.template, args.destination, goal=args.goal)
        Git(args.destination).init()
        print(f"created {args.template} workspace with {len(files)} files")
        return 0
    root = args.workspace.resolve()
    try:
        if args.command == "baseline":
            print(json.dumps(_baseline(root), sort_keys=True))
        elif args.command == "step":
            event = _step(root)
            print(json.dumps({"generation": event["generation"], "decision": event["decision"], "candidate_tree": event["candidate_tree"]}, sort_keys=True))
        elif args.command == "evaluate":
            print(json.dumps(_evaluate(root, args.split, args.ref), sort_keys=True))
        elif args.command == "report":
            print(write_report(root, _store(root).verify()))
        elif args.command == "verify":
            _store(root).verify()
            print("lineage: ok")
        elif args.command == "recover":
            _recover(root)
            print("recovered stale nanoRSI state")
        elif args.command == "doctor":
            from .doctor import doctor
            ok, output = doctor(root)
            print(output, end="")
            return 0 if ok else 1
    except Exception as error:
        print(f"nanorsi: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
