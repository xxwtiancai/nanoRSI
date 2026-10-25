"""Offline double-scoring of gate decisions (selector-study false-block accounting).

The selector-study protocol requires reporting false-blocks (candidates the
selector rejected that the control gate would have accepted) and false-admits
(selector acceptances the control would reject). Two modes:

- **Recompute (default, zero cost):** for every recorded attempt, replay the
  pure gate decision under a control GateConfig (strict minimum, no band)
  using the journal's own parent/child metrics. Works on any completed
  workspace, including archived studies.

- **Re-evaluate (--evaluate-blocked):** for attempts whose proposal produced
  a diff but no gate metrics (pre-evaluation selectors such as a judge
  pre-rank, not yet implemented in the core), apply the archived proposal
  diff to a fresh worktree of the parent commit and run the frozen
  evaluator on the validation panel. Offline fixtures cost nothing; live
  workspaces pay measurement-only episode costs outside the search budget.

The script never modifies the workspace; it writes double-scoring.json next
to the study or prints it. It is accounting, not selection.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile

from nanorsi.config import load_config
from nanorsi.gate import GateConfig, decide


def control_config(config, minimum: float) -> GateConfig:
    gate = config.gate
    return GateConfig(minimum_improvement=max(minimum, 0.0),
                      required_constraints=gate.required_constraints,
                      max_heldout_regression=gate.max_heldout_regression,
                      noise_band=0.0)


def _events(root: Path) -> list[dict]:
    return [json.loads(line) for line in (root / "lineage.jsonl").read_text().splitlines()]


def recompute(root: Path, minimum: float) -> dict:
    config = load_config(root / "nanorsi.toml")
    control = control_config(config, minimum)
    rows = []
    for event in _events(root):
        if event.get("event_type") != "generation" or not event.get("attempt_id"):
            continue
        parent, child = event.get("parent_gate_metrics"), event.get("gate_metrics")
        if not isinstance(parent, dict) or not isinstance(child, dict):
            rows.append({"attempt": event.get("attempt_id"), "selector_decision": event.get("decision"),
                         "control_decision": "unevaluated", "class": "not_double_scoreable"})
            continue
        verdict = decide(control, parent=parent,
                         child={**child, "constraints": event.get("gate_constraints") or {}},
                         parent_heldout=event.get("heldout_metrics"), child_heldout=event.get("heldout_metrics"),
                         metric=config.evaluator.primary_metric, direction=config.evaluator.direction)
        selector = event.get("decision")
        if selector == "accepted" and verdict.decision != "accepted":
            klass = "false_admit"
        elif selector != "accepted" and verdict.decision == "accepted":
            klass = "false_block"
        else:
            klass = "agree"
        rows.append({"attempt": event.get("attempt_id"), "selector_decision": selector,
                     "selector_reason": (event.get("reason") or "")[:120],
                     "control_decision": verdict.decision, "control_reason": verdict.reason,
                     "class": klass})
    counts = {name: sum(row["class"] == name for row in rows)
              for name in ("agree", "false_block", "false_admit", "not_double_scoreable")}
    return {"schema_version": 1, "mode": "recompute", "control_minimum_improvement": max(minimum, 0.0),
            "attempts": rows, "counts": counts}


def _parent_commit(events: list[dict], event: dict, git=None) -> str | None:
    """Resolve the measured parent program: the accepted-generation tag chain.

    Every accepted generation and the baseline are tagged nanorsi/gen-N, and a
    generation event records parent_generation, so the tag is the reliable
    anchor even for minimal baseline events.
    """
    generation = event.get("parent_generation")
    if not isinstance(generation, int) or git is None:
        return None
    resolved = git._run("rev-parse", f"nanorsi/gen-{generation}", check=False)
    return resolved.stdout.decode().strip() if resolved.returncode == 0 else None


def _artifact_text(root: Path, event: dict, suffix: str) -> str | None:
    entry = (event.get("artifacts") or {}).get(suffix)
    if not entry:
        return None
    path = root / entry.get("path", "")
    return path.read_text() if entry.get("path") and path.is_file() else None


def reevaluate_blocked(root: Path, minimum: float) -> dict:
    """Apply archived proposal diffs to parent worktrees and re-run the frozen evaluator."""
    from nanorsi.gitops import Git
    from nanorsi.lineage import LineageStore
    from nanorsi import loop

    config = load_config(root / "nanorsi.toml")
    control = control_config(config, minimum)
    git = Git(root)
    events = _events(root)
    rows = []
    with tempfile.TemporaryDirectory(prefix="nanorsi-double-") as tmp:
        for event in events:
            if event.get("event_type") != "generation" or not event.get("attempt_id"):
                continue
            if isinstance(event.get("gate_metrics"), dict):
                continue  # already measured; use recompute()
            diff = _artifact_text(root, event, "proposal/proposal.diff")
            parent_commit = _parent_commit(events, event, git)
            if not diff or not parent_commit:
                rows.append({"attempt": event.get("attempt_id"), "class": "not_reconstructable"})
                continue
            worktree = Path(tmp) / f"attempt-{event.get('attempt_id')}"
            with git.worktree(parent_commit, worktree):
                applied = Git(worktree)._run("apply", "--recount", "--whitespace=nowarn", "-",
                                             input_bytes=diff.encode(), check=False)
                if applied.returncode != 0:
                    rows.append({"attempt": event.get("attempt_id"), "class": "diff_not_applicable"})
                    continue
                # Audit measurements must not append to the source study or
                # leave derived artifacts in it. Keep both in a disposable
                # root while evaluating the archived checkout.
                score_root = Path(tmp) / f"score-{event.get('attempt_id')}"
                score_store = LineageStore.initialize(score_root)
                metrics = loop.evaluate(score_root, config, worktree, "validation",
                                        score_root / "double-score.json", score_store)
                parent = event.get("parent_gate_metrics") or _parent_metrics(events, event)
                verdict = decide(control, parent=parent, child={**metrics.metrics, "constraints": metrics.constraints},
                                 parent_heldout=None, child_heldout=None,
                                 metric=config.evaluator.primary_metric, direction=config.evaluator.direction)
                rows.append({"attempt": event.get("attempt_id"), "control_decision": verdict.decision,
                             "control_reason": verdict.reason,
                             "class": "control_accepted" if verdict.decision == "accepted" else "control_rejected"})
    return {"schema_version": 1, "mode": "re-evaluate-blocked", "attempts": rows,
            "counts": {"control_accepted": sum(r.get("class") == "control_accepted" for r in rows),
                       "control_rejected": sum(r.get("class") == "control_rejected" for r in rows),
                       "not_reconstructable": sum(r.get("class") == "not_reconstructable" for r in rows),
                       "diff_not_applicable": sum(r.get("class") == "diff_not_applicable" for r in rows)}}


def _parent_metrics(events: list[dict], event: dict) -> dict:
    anchor = None
    for candidate in events:
        if candidate.get("attempt_id") and candidate.get("attempt_id") < (event.get("attempt_id") or 0) \
                and candidate.get("decision") == "accepted":
            anchor = candidate
        elif candidate.get("decision") == "baseline":
            anchor = candidate
    return (anchor or {}).get("gate_metrics") or {}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Double-score gate decisions under a control gate.")
    parser.add_argument("workspace")
    parser.add_argument("--control-minimum", type=float, default=0.0,
                        help="control gate minimum_improvement (default 0 = strict)")
    parser.add_argument("--evaluate-blocked", action="store_true",
                        help="re-evaluate attempts whose proposals never reached measurement")
    parser.add_argument("--out", help="write the report here (default: print)")
    args = parser.parse_args(argv)
    root = Path(args.workspace).resolve()
    if not (root / "lineage.jsonl").is_file():
        raise SystemExit("workspace has no lineage.jsonl")
    report = reevaluate_blocked(root, args.control_minimum) if args.evaluate_blocked else recompute(root, args.control_minimum)
    text = json.dumps(report, indent=2, sort_keys=True)
    if args.out:
        Path(args.out).write_text(text + "\n")
        print(args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
