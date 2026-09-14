"""Per-revision evidence ledger: proposals, diffs, redacted outcomes, decisions."""
from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path

from .config import load_config
from .lineage import LineageStore

CASE_FIELDS = ("task_id", "group_id", "repeat_id", "score", "status")


def _artifact_text(root: Path, event: dict, key: str) -> dict | None:
    entry = (event.get("artifacts") or {}).get(key)
    if not entry:
        return None
    record = {"path": entry["path"], "sha256": entry["sha256"], "integrity": "missing", "text": None}
    try:
        data = (root / entry["path"]).read_bytes()
    except OSError:
        return record
    record["integrity"] = "ok" if sha256(data).hexdigest() == entry["sha256"] else "mismatch"
    record["text"] = data.decode("utf-8", "replace")
    return record


def _diff_stats(text: str) -> dict[str, list[int]]:
    stats: dict[str, list[int]] = {}
    target = None
    for line in text.splitlines():
        if line.startswith("+++ b/"):
            target = line[6:]
            stats.setdefault(target, [0, 0])
        elif line.startswith("--- a/"):
            continue
        elif target is not None and line.startswith("+"):
            stats[target][0] += 1
        elif target is not None and line.startswith("-"):
            stats[target][1] += 1
    return stats


def _cases(payload: dict | None) -> list[dict] | None:
    if payload is None:
        return None
    try:
        rows = json.loads(payload["text"])["case_results"]
    except (KeyError, TypeError, ValueError):
        return None
    return [{field: row.get(field) for field in CASE_FIELDS} for row in rows]


def _diff_summary(payload: dict | None) -> dict | None:
    if payload is None:
        return None
    return {"path": payload["path"], "sha256": payload["sha256"], "integrity": payload["integrity"],
            "stats": _diff_stats(payload["text"] or ""), "text": payload["text"]}


def _revision(root: Path, config, event: dict) -> dict:
    metric = config.evaluator.primary_metric
    parent_metrics, child_metrics = event.get("parent_gate_metrics") or {}, event.get("gate_metrics") or {}
    parent_value, child_value = parent_metrics.get(metric), child_metrics.get(metric)
    delta = child_value - parent_value if isinstance(parent_value, (int, float)) and isinstance(child_value, (int, float)) else None
    return {"schema_version": 1, "attempt_id": event.get("attempt_id"), "generation": event.get("generation"),
            "decision": event.get("decision"), "reason": event.get("reason"), "diagnosis": event.get("hypothesis"),
            "surface": event.get("changed_paths"), "candidate_commit": event.get("candidate_commit"),
            "proposer_harness_commit": event.get("proposer_harness_commit"),
            "metric": {"name": metric, "direction": config.evaluator.direction,
                       "parent": parent_value, "candidate": child_value, "delta": delta},
            "diff": _diff_summary(_artifact_text(root, event, "proposal/proposal.diff")),
            "evaluator": {"parent_cases": _cases(_artifact_text(root, event, "parent.json")),
                          "candidate_cases": _cases(_artifact_text(root, event, "gate.json"))}}


def revisions(root: Path) -> list[dict]:
    config = load_config(root / "nanorsi.toml")
    events = LineageStore.initialize(root).events()
    return [_revision(root, config, event) for event in events
            if event.get("attempt_id") and event.get("event_type") in {"generation", "attempt_failed"}]


def _case_table(record: dict) -> list[str]:
    parent = {(c["task_id"], c["group_id"], c["repeat_id"]): c for c in record["evaluator"]["parent_cases"] or []}
    child = {(c["task_id"], c["group_id"], c["repeat_id"]): c for c in record["evaluator"]["candidate_cases"] or []}
    lines = ["| Task | Group | Parent | Candidate |", "| --- | --- | --- | --- |"]
    for key in sorted(set(parent) | set(child)):
        before, after = parent.get(key), child.get(key)
        lines.append(f"| {key[0]} | {key[1]} | {_status(before)} | {_status(after)} |")
    return lines


def _status(case: dict | None) -> str:
    if case is None:
        return "—"
    score = case.get("score")
    return f"{case.get('status')}/{score}"


def _block(record: dict) -> list[str]:
    metric = record["metric"]
    lines = [f"## Attempt {record['attempt_id']} — {record['decision']} (generation {record.get('generation')})",
             f"- Reason: {record.get('reason')}", f"- Diagnosis: `{json.dumps(record.get('diagnosis'), sort_keys=True)}`",
             f"- Surface: {', '.join(record.get('surface') or []) or '—'}",
             f"- {metric['name']}: {metric['parent']} → {metric['candidate']} (Δ {metric['delta']})"]
    diff = record.get("diff")
    if diff:
        stats = ", ".join(f"{name} +{adds}/-{dels}" for name, (adds, dels) in sorted(diff["stats"].items()))
        lines.append(f"- Diff `{diff['path']}` sha256 `{diff['sha256'][:12]}`… integrity {diff['integrity']}: {stats or '—'}")
    if record["evaluator"]["candidate_cases"] is not None:
        lines.extend(["", "### Cases", ""] + _case_table(record))
    return lines + [""]


def _markdown(records: list[dict]) -> str:
    lines = ["# nanoRSI evidence ledger", "",
             "One record per proposal revision: diagnosis, candidate diff, redacted per-case",
             "evaluator evidence and the accept/reject decision, with artifact integrity flags.",
             "Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.", ""]
    if not records:
        lines.extend(["No recorded revisions yet.", ""])
    else:
        lines.extend(["| Attempt | Generation | Decision | Δ metric | Files |", "| ---: | ---: | --- | --- | --- |"])
        for record in records:
            metric = record["metric"]
            lines.append(f"| {record['attempt_id']} | {record.get('generation', '—')} | {record['decision']} "
                         f"| {metric['delta']} | {len(record.get('surface') or [])} |")
        lines.append("")
        for record in records:
            lines.extend(_block(record))
    return "\n".join(lines)


def write_ledger(root: Path) -> dict:
    if not (root / "nanorsi.toml").is_file():
        return {"jsonl": None, "markdown": None, "revisions": 0, "skipped": "no nanorsi.toml in workspace"}
    records = revisions(root)
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    jsonl = reports / "evidence.jsonl"
    jsonl.write_text("".join(json.dumps(record, sort_keys=True, allow_nan=False) + "\n" for record in records), encoding="utf-8")
    markdown = reports / "evidence.md"
    markdown.write_text(_markdown(records), encoding="utf-8")
    return {"jsonl": str(jsonl), "markdown": str(markdown), "revisions": len(records)}
