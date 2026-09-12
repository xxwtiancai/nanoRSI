"""Bounded experiment accounting and the search/final-test boundary."""
from __future__ import annotations

import json
import random
import uuid
from hashlib import sha256
from pathlib import Path

from .evaluator import run_evaluation
from .gitops import Git
from .hashing import canonical_hash, tree_hash
from .lineage import LineageStore, artifact, write_json
from .locking import Lock
from .paths import contained_path, normalize_relative_path


def tasks(root, config):
    path = contained_path(root, config.data["manifest"])
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("tasks", [])
    if payload.get("schema_version") != 1 or not rows:
        raise ValueError("task manifest must have schema_version 1 and nonempty tasks")
    seen, groups, splits = set(), {}, set()
    for row in rows:
        task, group, split = row.get("task_id"), row.get("group_id"), row.get("split")
        if not isinstance(task, str) or not task or task in seen or not isinstance(group, str) or not group:
            raise ValueError("task and group identities must be nonempty and tasks unique")
        if split not in {"train", "validation", "test"} or groups.get(group, split) != split:
            raise ValueError("source groups must not cross train/validation/test splits")
        if not isinstance(row.get("instruction"), str) or not row["instruction"]:
            raise ValueError("task instruction required")
        for key in ["input_files", "expected_files"]:
            if not isinstance(row.get(key), dict) or not row[key]:
                raise ValueError(f"{key} must be nonempty file mapping")
            for name, content in row[key].items():
                normalize_relative_path(name)
                if not isinstance(content, str):
                    raise ValueError("task files must contain text")
        seen.add(task)
        groups[group], splits = split, splits | {split}
    if splits != {"train", "validation", "test"}:
        raise ValueError("train, validation and test must all be nonempty")
    return rows


def fingerprint(root):
    return tree_hash(root / "evaluator", exclude=["**/__pycache__/**", "__pycache__/**", "__pycache__"])


def identity(root, config):
    fixed = ["nanorsi.toml", "evaluator", "proposer", "adapters"]
    if config.experiment.schema_version == 2:
        tasks(root, config)
        fixed.append(config.data["manifest"])
        if config.training or (root / "trainer").exists():
            fixed.append("trainer")
    hashes = {}
    for name in fixed:
        path = contained_path(root, name)
        hashes[name] = tree_hash(path, exclude=["__pycache__", "__pycache__/**", "**/__pycache__/**"]) if path.is_dir() else sha256(path.read_bytes()).hexdigest() if path.exists() else None
    return canonical_hash(hashes)


def guard(root, config, store, *, search=False):
    events = store.verify()
    baseline = next((e for e in events if e.get("manifest_hash")), None)
    if baseline and baseline["manifest_hash"] != identity(root, config):
        raise RuntimeError("frozen experiment contract changed; create a new workspace")
    if search and any(e.get("event_type") == "freeze" for e in events):
        raise RuntimeError("experiment is frozen; search cannot consume final-test feedback")


def prepare_parent(root, config, git, store):
    parent = store.latest_accepted()
    if "manifest_hash" not in parent:
        if config.experiment.schema_version != 1:
            raise RuntimeError("v2 requires a fresh baseline; legacy data cannot be reclassified")
        baseline = next(e for e in store.events() if e.get("generation") == 0)
        with git.worktree(baseline["candidate_commit"], root / ".nanorsi/worktrees/legacy-contract") as original:
            contract, evaluator = identity(original, config), fingerprint(original)
        if contract != identity(root, config):
            raise RuntimeError("legacy protected files changed since baseline")
        parent = {**parent, "manifest_hash": contract, "evaluator_fingerprint": evaluator}
        if not any(e.get("event_type") == "legacy_contract" for e in store.events()):
            store.append({"event_type": "legacy_contract", "manifest_hash": contract})
    return parent


def require_settled(events):
    done = {e.get("attempt_id") for e in events if e.get("event_type") in {"generation", "attempt_failed", "candidate_evaluated"}}
    if any(e["attempt_id"] not in done for e in events if e.get("event_type") == "attempt_started"):
        raise RuntimeError("interrupted attempt; run recover first")


def begin_attempt(root, config, store):
    guard(root, config, store, search=True)
    events = store.events()
    started = [e for e in events if e.get("event_type") == "attempt_started"]
    require_settled(events)
    legacy = sum(e.get("event_type") == "generation" and e.get("decision") != "baseline" and "attempt_id" not in e for e in events)
    if len(started) + legacy >= config.budget.max_steps:
        raise RuntimeError("attempt budget reached")
    attempt = len(started) + legacy + 1
    store.append({"event_type": "attempt_started", "attempt_id": attempt})
    return attempt


def search_episode_count(events):
    starts = [e for e in events if e.get("event_type") == "evaluation_started" and e.get("phase") == "search"]
    spent = sum(e.get("episodes", 0) for e in starts)
    settled = {e.get("reservation_id") for e in events if e.get("event_type") == "episode_reservation_settled"}
    for event in events:
        if event.get("event_type") == "episode_reservation" and event["reservation_id"] not in settled:
            actual = sum(e.get("episodes", 0) for e in starts if e.get("reservation_id") == event["reservation_id"])
            spent += max(0, event["episodes"] - actual)
    return spent


def evaluate(root, config, checkout, split, output, store, *, repeat=0, agent=None):
    panel = [t for t in tasks(checkout, config) if t["split"] == split] if config.experiment.schema_version == 2 else []
    if split == "train" and len(panel) > 4:
        panel = random.Random(config.experiment.seed).sample(panel, 4)
    count = len(panel)
    phase = "test" if split == "test" else "search"
    spent = search_episode_count(store.events())
    if phase == "search" and spent + count > config.budget.max_episodes:
        raise RuntimeError("episode budget reached")
    invocation = uuid.uuid4().hex
    store.append({"event_type": "evaluation_started", "invocation_id": invocation,
                  "phase": phase, "split": split, "episodes": count})
    env = {"PYTHONDONTWRITEBYTECODE": "1", "NANORSI_REPEAT_ID": str(repeat)}
    if config.experiment.schema_version == 2:
        env.update(NANORSI_AGENT_CONFIG=json.dumps(agent if agent is not None else config.agent),
                   NANORSI_TASK_MANIFEST=str(contained_path(checkout, config.data["manifest"])),
                   NANORSI_TRAIN_LIMIT="4", NANORSI_SEED=str(config.experiment.seed))
    try:
        from .training import checkpoint
        model = checkpoint(checkout, config) if config.experiment.schema_version == 2 and config.experiment.mode == "model" else None
        result = run_evaluation(config, checkout, split, output, extra_env=env)
        if model and checkpoint(checkout, config) != model:
            raise RuntimeError("evaluation mutated the saved checkpoint")
        if config.experiment.schema_version == 2:
            expected = {(t["task_id"], t["group_id"], repeat) for t in panel}
            actual = result.case_results
            if len(actual) != count or {(c["task_id"], c["group_id"], c["repeat_id"]) for c in actual} != expected:
                raise ValueError("evaluator results do not match the reserved task/repeat panel")
    except Exception as error:
        store.append({"event_type": "evaluation_finished", "invocation_id": invocation, "status": "error",
                      "reason": str(error), "artifacts": {"result": artifact(root, output)} if output.is_file() else {}})
        raise
    store.append({"event_type": "evaluation_finished", "invocation_id": invocation, "status": "ok",
                  "phase": phase, "cost_usd": result.cost_usd, "duration_ms": result.duration_ms,
                  "usage": result.usage, "artifacts": {"result": artifact(root, output)}})
    return result


def train_feedback(root, config, checkout, run_dir, store):
    if config.experiment.schema_version != 2:
        return []
    result = evaluate(root, config, checkout, "train", run_dir / "train.json", store)
    return result.case_results


def record_proposal(store, run_dir, attempt):
    events = [e for e in store.events() if e.get("attempt_id") == attempt]
    if not any(e.get("event_type") == "proposal_started" for e in events) or any(e.get("event_type") == "proposal_finished" for e in events):
        return
    from .evaluator import _validate_usage
    path = run_dir / "proposal/usage.json"
    try:
        usage = _validate_usage(json.loads(path.read_text()), "proposal usage") if path.is_file() else {}
    except (ValueError, OSError):
        usage = {}
    store.append({"event_type": "proposal_finished", "attempt_id": attempt,
                  "usage": usage, "cost_usd": usage.get("cost_usd")})


def bounded_run(root, config, step):
    store = LineageStore.initialize(root)
    guard(root, config, store, search=True)
    outcomes = []
    while len([e for e in store.events() if e.get("event_type") == "attempt_started"]) < config.budget.max_steps:
        before = len(store.events())
        try:
            outcomes.append(step(root))
        except Exception as error:
            if "budget" in str(error):
                break
            if len(store.events()) == before:
                raise
            outcomes.append({"decision": "failed", "reason": str(error)})
    return {"attempts": outcomes, "stop_reason": "budget", "parent": store.latest_accepted()["generation"]}


def freeze(root, config, repeats=3):
    if config.experiment.schema_version != 2:
        raise RuntimeError("freeze requires a schema-v2 experiment")
    if type(repeats) is not int or not 1 <= repeats <= 10:
        raise ValueError("test repeats must be between 1 and 10")
    with Lock(root):
        store = LineageStore.initialize(root)
        guard(root, config, store)
        require_settled(store.events())
        existing = next((e for e in store.events() if e.get("event_type") == "freeze"), None)
        if existing:
            if existing["repeats"] != repeats:
                raise RuntimeError("test repeats are already frozen")
            return existing
        parent = store.latest_accepted()
        baseline = next(e for e in store.events() if e.get("generation") == 0)
        with Git(root).worktree(baseline["candidate_commit"], root / ".nanorsi/worktrees/comparison") as original:
            from .contracts import comparison_hash
            comparison = comparison_hash(original, config)
        return store.append({"event_type": "freeze", "decision": "frozen", "repeats": repeats,
                             "comparison_hash": comparison, "mode": config.experiment.mode,
                             "conditions": config.experiment.final_conditions,
                             "metric": {"name": config.evaluator.primary_metric, "direction": config.evaluator.direction},
                             "manifest_hash": identity(root, config), "baseline_commit": baseline["candidate_commit"],
                             "candidate_commit": parent["candidate_commit"], "experiment_id": config.experiment.id,
                             "arm": config.experiment.arm, "seed": config.experiment.seed})


def final_test(root, config, repeats=None):
    with Lock(root):
        store = LineageStore.initialize(root)
        guard(root, config, store)
        frozen = next((e for e in store.events() if e.get("event_type") == "freeze"), None)
        if not frozen:
            raise RuntimeError("freeze all experiment choices before final-test")
        if repeats is not None and repeats != frozen["repeats"]:
            raise RuntimeError("test repeats differ from frozen plan")
        for condition in frozen.get("conditions", ["baseline", "no-skills", "candidate"]):
            for repeat in range(frozen["repeats"]):
                _final_episode(root, config, store, frozen, condition, repeat)
        return final_report(root, store, frozen)


def _final_episode(root, config, store, frozen, condition, repeat):
    key = f"{condition}-{repeat}"
    if any(e.get("event_type") == "final_result" and e.get("key") == key for e in store.events()):
        return
    if any(e.get("event_type") == "final_started" and e.get("key") == key for e in store.events()):
        raise RuntimeError(f"incomplete final evaluation {key}; retain failed record, do not select a retry")
    store.append({"event_type": "final_started", "key": key})
    commit = frozen["candidate_commit"] if condition == "candidate" else frozen["baseline_commit"]
    output = root / ".nanorsi" / "final" / f"{key}.json"
    from .config import load_config
    from .training import checkpoint
    with Git(root).worktree(commit, root / ".nanorsi" / "worktrees" / f"test-{key}") as checkout:
        saved = load_config(checkout / "nanorsi.toml")
        agent = dict(saved.agent)
        if condition == "no-skills":
            agent["skills"] = []
        model = checkpoint(checkout, saved) if saved.experiment.mode == "model" else None
        result = evaluate(root, saved, checkout, "test", output, store, repeat=repeat, agent=agent)
        if model and checkpoint(checkout, saved) != model:
            raise RuntimeError("final evaluation mutated the frozen checkpoint")
    record = {"condition": condition, "repeat_id": repeat, "case_results": result.case_results,
              "cost_usd": result.cost_usd, "duration_ms": result.duration_ms, "metrics": result.metrics,
              "constraints": result.constraints, "usage": result.usage, "checkpoint": model}
    store.append({"event_type": "final_result", "key": key, "result": record,
                  "artifacts": {"result": artifact(root, output)}})


def final_report(root, store, frozen):
    from .report import cost_summary
    result = {key: frozen[key] for key in ["manifest_hash", "comparison_hash", "experiment_id", "arm", "seed"]}
    result.update({key: frozen[key] for key in ["mode", "conditions", "metric", "repeats"] if key in frozen})
    result.update(schema_version=2, results=[e["result"] for e in store.events() if e.get("event_type") == "final_result"])
    result["search_evaluations"] = [e for e in store.events() if e.get("phase") == "search"]
    result["search_proposals"] = [e for e in store.events() if e.get("event_type") == "proposal_finished"]
    result["search_cost_usd"] = cost_summary(store.events(), "search")
    result["test_cost_usd"] = cost_summary(store.events(), "test")
    path = root / "reports" / "final.json"
    write_json(path, result)
    return path
