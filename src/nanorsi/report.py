from __future__ import annotations

import json
import html
import math
from pathlib import Path

from .lineage import write_json


def _training_events(events: list[dict]) -> list[dict]:
    unique = {}
    for event in events:
        has_artifacts = any(name.startswith('training/') for name in event.get('artifacts', {}))
        if isinstance(event.get('training'), dict) or has_artifacts:
            unique.setdefault(event.get('attempt_id'), event)
    return list(unique.values())


def cost_summary(events: list[dict], phase: str) -> dict:
    starts = [e for e in events if e.get('event_type') == 'evaluation_started' and e.get('phase') == phase]
    completed = {e.get('invocation_id'): e for e in events if e.get('event_type') == 'evaluation_finished'}
    costs = [completed.get(e['invocation_id'], {}).get('cost_usd') for e in starts]
    if phase == 'search':
        proposals = {e.get('attempt_id'): e for e in events if e.get('event_type') == 'proposal_finished'}
        costs += [proposals.get(e['attempt_id'], {}).get('cost_usd') for e in events if e.get('event_type') == 'proposal_started']
        costs += [(e.get('training') or {}).get('result', {}).get('cost_usd') for e in _training_events(events)]
    known = [c for c in costs if c is not None]
    return {'known_usd': sum(known) if known else None, 'total_usd': sum(known) if costs and len(known) == len(costs) else None,
            'known_count': len(known), 'total_count': len(costs), 'coverage': len(known) / len(costs) if costs else 0.0}


def _panel(record: dict) -> dict:
    result = {}
    for case in record['case_results']:
        key = (case['task_id'], case['repeat_id'])
        score = case['score']
        if key in result or case['repeat_id'] != record['repeat_id']:
            raise ValueError('duplicate or mismatched final task/repeat pair')
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError('final score must be finite and between zero and one')
        result[key] = score
    if not result:
        raise ValueError('final panel must contain tasks')
    return result


def _final_comparison(events: list[dict]) -> dict | None:
    frozen = next((e for e in events if e.get('event_type') == 'freeze'), None)
    if not frozen:
        return None
    conditions = frozen.get('conditions', ['baseline', 'no-skills', 'candidate'])
    if not isinstance(conditions, list) or len(set(conditions)) != len(conditions) or not {'baseline', 'candidate'} <= set(conditions) <= {'baseline', 'no-skills', 'candidate'}:
        raise ValueError('invalid frozen final conditions')
    panels, seen = {name: {} for name in conditions}, set()
    records = {name: [] for name in conditions}
    for event in events:
        if event.get('event_type') != 'final_result':
            continue
        record = event['result']
        condition, repeat = record['condition'], record['repeat_id']
        if condition not in panels or type(repeat) is not int or repeat not in range(frozen['repeats']) or (condition, repeat) in seen:
            raise ValueError('invalid or duplicate final condition/repeat')
        seen.add((condition, repeat))
        panels[condition].update(_panel(record))
        records[condition].append(record)
    if len(seen) != len(conditions) * frozen['repeats']:
        return None
    pairs = set(panels['baseline'])
    if any(set(panel) != pairs for panel in panels.values()):
        raise ValueError('final conditions must use matching task/repeat pairs')
    tasks = {task for task, _ in pairs}
    if len(pairs) != len(tasks) * frozen['repeats']:
        raise ValueError('every final task must have all frozen repeats')
    scores = {name: sum(sum(panel[(task, r)] for r in range(frozen['repeats'])) / frozen['repeats']
                       for task in tasks) / len(tasks) for name, panel in panels.items()}
    metric, values = _metric_values(frozen, records, scores)
    delta = values['candidate'] - values['baseline']
    return {'scores': scores, 'values': values, 'metric': metric, 'delta': delta, 'delta_pp': 100 * delta if metric['name'] == 'score' else None,
            'tasks': len(tasks), 'repeats': frozen['repeats'], 'frozen': frozen}


def _metric_values(frozen: dict, records: dict, scores: dict) -> tuple[dict, dict]:
    metric = frozen.get('metric', {'name': 'score', 'direction': 'maximize'})
    if not isinstance(metric, dict) or not isinstance(metric.get('name'), str) or metric.get('direction') not in {'maximize', 'minimize'}:
        raise ValueError('invalid frozen metric')
    if metric['name'] == 'score':
        return metric, scores
    values = {}
    for condition, rows in records.items():
        measured = [row.get('metrics', {}).get(metric['name']) for row in rows]
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in measured):
            raise ValueError('final primary metric missing or nonfinite')
        values[condition] = sum(measured) / len(measured)
    return metric, values


def _display_metric(summary: dict, value: float) -> str:
    return f'{value:.1%}' if summary['metric']['name'] == 'score' else f'{value:.6g}'


def _display_delta(summary: dict) -> str:
    if summary['delta_pp'] is not None:
        return f"{summary['delta_pp']:+.1f} pp"
    return f"{summary['delta']:+.6g} {summary['metric']['name']}"


def _comparison_lines(summary: dict | None) -> list[str]:
    if summary is None:
        return ['', '## Final evaluation pending', '', 'Freeze all choices and complete final-test before interpreting improvement.', '']
    lines = ['', '## Final comparison', '',
             f"{summary['tasks']} tasks × {summary['repeats']} repeats per condition; repeats are not independent evolution runs.", '',
             f"Primary metric: {summary['metric']['name']} ({summary['metric']['direction']}).", '',
             '| Condition | Value |', '| --- | ---: |']
    lines += [f'| {name} | {_display_metric(summary, value)} |' for name, value in summary['values'].items()]
    lines += ['', f"Candidate − baseline: **{_display_delta(summary)}**.", '',
              'Descriptive results from this experiment; no statistical significance or general capability claim.', '']
    return lines


def _html_table(headers: list[str], rows: list[list]) -> str:
    heading = ''.join(f'<th>{html.escape(str(value))}</th>' for value in headers)
    body = ''.join('<tr>' + ''.join(f'<td>{html.escape(str(value))}</td>' for value in row) + '</tr>' for row in rows)
    return f'<div class="table"><table><thead><tr>{heading}</tr></thead><tbody>{body}</tbody></table></div>'


def _html_comparison(summary: dict | None) -> str:
    if summary is None:
        return '<section><h2>Final evaluation pending</h2><p>Freeze all choices and complete final-test before interpreting improvement.</p></section>'
    rows = [[name, _display_metric(summary, value)] for name, value in summary['values'].items()]
    comparison = _html_table(['Condition', summary['metric']['name'] + ' (' + summary['metric']['direction'] + ')'], rows)
    identity = summary['frozen']
    label = html.escape(f"{identity.get('experiment_id', '')} · {identity.get('arm', '')} · seed {identity.get('seed', '')}")
    return (f'<section><h2>Final comparison</h2><p>{label}</p><p class="delta">{html.escape(_display_delta(summary))}</p>'
            f'<p>Candidate − baseline · {summary["tasks"]} tasks × {summary["repeats"]} repeats per condition</p>'
            f'{comparison}<p class="muted">Repeated deployments are not independent evolution runs. '
            'These are descriptive results, not a statistical significance or general capability claim.</p></section>')


def _evidence_tables(events: list[dict]) -> list[tuple]:
    tables = []
    retained = next((e.get('candidate_ids', []) for e in reversed(events) if e.get('event_type') == 'population_retained'), [])
    nodes = [[e.get('candidate_id'), ', '.join(e.get('candidate_parents', [])), e.get('operator'),
              json.dumps(e.get('gate_metrics', {}), sort_keys=True), 'retained' if e.get('candidate_id') in retained else 'evaluated']
             for e in events if e.get('event_type') == 'candidate_evaluated']
    if nodes:
        tables.append(('Population candidates', ['Candidate', 'Actual parents', 'Operator', 'Validation metrics', 'Pool status'], nodes))
    training = []
    for event in _training_events(events):
        data = event.get('training') or {}
        training.append([event.get('attempt_id'), data.get('method', 'unknown'), data.get('status', 'failed/interrupted'),
                         data.get('steps', (data.get('result') or {}).get('steps', 'unknown')), data.get('checkpoint_sha256', '')])
    if training:
        tables.append(('Training checkpoints', ['Attempt', 'Method', 'Status', 'Steps', 'Checkpoint SHA256'], training))
    return tables


def _write_html(path: Path, events: list[dict], summary: dict | None) -> None:
    scope = 'Frozen final evaluation' if summary else 'Final evaluation pending'
    rows = [[e.get('attempt_id', 0), e.get('generation', '—'), e.get('decision', ''),
             json.dumps(e.get('gate_metrics', {}), sort_keys=True), e.get('reason', ''), e.get('candidate_commit', '')[:12]]
            for e in events if e.get('event_type') in {'generation', 'attempt_failed'}]
    costs = []
    for phase in ['search', 'test']:
        cost = cost_summary(events, phase)
        total = f"${cost['total_usd']:.4f}" if cost['total_usd'] is not None else 'Unknown'
        known = f"${cost['known_usd']:.4f}" if cost['known_usd'] is not None else 'Unknown'
        costs.append([phase, total, known, f"{cost['known_count']}/{cost['total_count']} ({cost['coverage']:.0%})"])
    css = ('body{margin:0;background:#f4f5f7;color:#16212d;font:16px/1.6 system-ui,sans-serif}'
           'main{max-width:1080px;margin:auto;padding:40px 24px}header{border-bottom:3px solid #f4512c;margin-bottom:24px}'
           'h1{font-size:40px;letter-spacing:-1px;margin:0}h2{font-size:23px}.eyebrow{color:#b53519;font-weight:700}'
           'section{background:white;border:1px solid #dae0e7;border-radius:12px;padding:24px;margin:20px 0}'
           '.delta{font-size:40px;font-weight:750;margin:4px 0;color:#173a61}.muted,footer{color:#536170}'
           '.table{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:14px}'
           'th,td{text-align:left;padding:12px;border-bottom:1px solid #e4e8ee;overflow-wrap:anywhere}'
           'th{background:#f4f6f9}a{color:#164b8f}footer{font-size:14px}')
    body = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>nanoRSI experiment report</title><style>' + css + '</style></head><body><main>'
            '<header><p class="eyebrow">nanoRSI / EXPERIMENT EVIDENCE</p><h1>Did the agent improve?</h1>'
            f'<p>{len(events)} verified lineage events · {scope}</p></header>'
            + _html_comparison(summary)
            + '<section><h2>Search history</h2>' + _html_table(['Attempt', 'Gen', 'Decision', 'Validation metrics', 'Reason', 'Commit'], rows)
            + '</section>' + ''.join('<section><h2>' + title + '</h2>' + _html_table(headers, rows) + '</section>' for title, headers, rows in _evidence_tables(events))
            + '<section><h2>Cost coverage</h2>' + _html_table(['Phase', 'Total', 'Known subtotal', 'Recorded costs'], costs)
            + '<p class="muted">Unknown costs are never treated as zero.</p></section>'
            '<footer><p>Trusted local execution. Worktrees and receipts do not isolate hostile code. '
            'Task-suite results alone do not establish generalization to other benchmarks.</p>'
            '<p><a href="report.md">Markdown</a> · <a href="report.json">Lineage JSON</a></p></footer></main></body></html>')
    path.write_text(body, encoding='utf-8')


def write_report(root: Path, events: list[dict], *, format: str = 'markdown') -> Path:
    if format not in {'markdown', 'html'}:
        raise ValueError('report format must be markdown or html')
    summary = _final_comparison(events)
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
    lines.extend(_comparison_lines(summary))
    for title, headers, rows in _evidence_tables(events):
        lines += ['', '## ' + title, '', '| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join(['---'] * len(headers)) + ' |']
        lines += ['| ' + ' | '.join(str(v).replace('|', '\\|').replace('\n', ' ') for v in row) + ' |' for row in rows]
    markdown.write_text('\n'.join(lines), encoding='utf-8')
    _write_html(reports / 'report.html', events, summary)
    return reports / 'report.html' if format == 'html' else markdown
