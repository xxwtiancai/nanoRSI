from __future__ import annotations

import json
from pathlib import Path

from .lineage import write_json


def cost_summary(events: list[dict], phase: str) -> dict:
    starts = [e for e in events if e.get('event_type') == 'evaluation_started' and e.get('phase') == phase]
    completed = {e.get('invocation_id'): e for e in events if e.get('event_type') == 'evaluation_finished'}
    costs = [completed.get(e['invocation_id'], {}).get('cost_usd') for e in starts]
    if phase == 'search':
        proposals = {e.get('attempt_id'): e for e in events if e.get('event_type') == 'proposal_finished'}
        costs += [proposals.get(e['attempt_id'], {}).get('cost_usd') for e in events if e.get('event_type') == 'proposal_started']
    known = [c for c in costs if c is not None]
    return {'known_usd': sum(known) if known else None, 'total_usd': sum(known) if costs and len(known) == len(costs) else None,
            'known_count': len(known), 'total_count': len(costs), 'coverage': len(known) / len(costs) if costs else 0.0}


def write_report(root: Path, events: list[dict]) -> Path:
    reports = root / 'reports'
    write_json(reports / 'report.json', events)
    markdown = reports / 'report.md'
    generations = [e for e in events if e.get('event_type') == 'generation']
    decisions = [e for e in events if e.get('decision') and e.get('event_type') != 'baseline_started']
    lines = ['# nanoRSI Report', '', f'- Recorded events: {len(events)}',
             '- Local trusted execution; version checks do not provide filesystem isolation.',
             f'- Search cost (unknown remains null): `{json.dumps(cost_summary(events, "search"), sort_keys=True)}`',
             '', '| Attempt | Gen | Parent | Decision | Metrics | Candidate tree |',
             '| ---: | ---: | ---: | --- | --- | --- |']
    for event in generations:
        metrics = json.dumps(event.get('gate_metrics') or {}, sort_keys=True)
        lines.append(f"| {event.get('attempt_id', 0)} | {event.get('generation')} | {event.get('parent_generation')} | "
                     f"{event.get('decision')} | `{metrics}` | `{event.get('candidate_tree', '')}` |")
    failures = [e for e in events if e.get('event_type') == 'attempt_failed']
    lines.extend(['', '## Non-promoted attempts', ''])
    lines.extend(f"- Attempt {e.get('attempt_id')}: {e.get('decision')} — {e.get('reason')}" for e in failures)
    lines.extend(['', f"Decision: {decisions[-1].get('decision', '') if decisions else 'not evaluated'}", ''])
    markdown.write_text('\n'.join(lines), encoding='utf-8')
    return markdown
