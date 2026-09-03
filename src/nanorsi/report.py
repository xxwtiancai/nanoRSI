from __future__ import annotations

import json
from pathlib import Path


def write_report(root: Path, events: list[dict]) -> Path:
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "report.json").write_text(json.dumps(events, indent=2, sort_keys=True), encoding="utf-8")
    markdown = reports / "report.md"
    lines = [
        "# nanoRSI Report",
        "",
        f"- Experiment: `{events[0].get('experiment_id', 'experiment')}`",
        f"- Events: `{len(events)}`",
        "",
        "| Gen | Parent | Decision | Gate score | Heldout score | Candidate tree |",
        "| ---: | ---: | --- | ---: | ---: | --- |",
    ]
    for event in events:
        gate = event.get("gate_metrics", {}).get("score")
        heldout = event.get("heldout_metrics", {}).get("score", "")
        lines.append(
            f"| {event.get('generation', 0)} | {event.get('parent_generation', '')} | "
            f"{event.get('decision', '')} | {gate if gate is not None else ''} | {heldout} | "
            f"`{event.get('candidate_tree', '')}` |"
        )
    lines.extend(["", f"Decision: {events[-1].get('decision', '')}", ""])
    markdown.write_text("\n".join(lines), encoding="utf-8")
    return markdown
