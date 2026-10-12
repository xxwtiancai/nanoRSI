"""Derive measurement-noise bands from repeats already recorded in a workspace.

Phase 1 of ADOPTION item 38 (RRSI-style regularized transition): the strict
gate treats any positive delta as signal, but live studies measured swings
between repeated evaluations of identical conditions (a parent re-measured
0.88 then 1.0; identical-skill final conditions differing by one problem per
repeat). Two derivation sources, both zero-cost because the records exist:

- ``parent re-measurements`` in the search journal: the baseline score plus
  every attempt's freshly measured parent, grouped by parent generation
  (between acceptances the measured program is unchanged);
- ``final-test repeats``: per-condition repeat panels (repeats >= 2) from
  reports/final.json, with per-task outcome flip rates.

The report is read-only evidence (reports/noise-band.json). Applying a band
to acceptance is opt-in via ``[gate] noise_band`` (default 0 keeps the
historical strict behavior); nothing here feeds selection automatically.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _spread(values: list[float]) -> dict[str, Any] | None:
    if len(values) < 2:
        return None
    return {"n": len(values), "min": min(values), "max": max(values),
            "spread": max(values) - min(values),
            "values": sorted(values)}


def band_from_events(events: list[dict]) -> dict[str, Any]:
    groups: dict[int, list[float]] = {}
    for event in events:
        if event.get("event_type") != "generation":
            continue
        if event.get("attempt_id"):
            parent = event.get("parent_gate_metrics") or {}
            generation = event.get("parent_generation")
            measured = parent.get("score")
            if isinstance(measured, (int, float)) and isinstance(generation, int):
                groups.setdefault(generation, []).append(float(measured))
        else:
            baseline = (event.get("gate_metrics") or {}).get("score")
            if isinstance(baseline, (int, float)):
                groups.setdefault(int(event.get("generation") or 0), []).append(float(baseline))
    measured = {str(generation): _spread(values) for generation, values in sorted(groups.items())}
    bands = [entry["spread"] for entry in measured.values() if entry]
    return {"schema_version": 1, "source": "parent-remeasures",
            "by_parent_generation": {k: v for k, v in measured.items() if v},
            "largest_band": max(bands) if bands else None}


def band_from_final(final: dict) -> dict[str, Any]:
    per_condition: dict[str, dict[str, Any]] = {}
    for entry in final.get("results", []):
        condition = str(entry.get("condition"))
        score = (entry.get("metrics") or {}).get("score")
        cases = entry.get("case_results") or []
        record = per_condition.setdefault(condition, {"scores": [], "task_outcomes": {}})
        if isinstance(score, (int, float)):
            record["scores"].append(float(score))
        for case in cases:
            outcome = 1 if case.get("score") == 1.0 else 0
            record["task_outcomes"].setdefault(str(case.get("task_id")), []).append(outcome)
    report: dict[str, Any] = {"schema_version": 1, "source": "final-repeats", "conditions": {}}
    bands = []
    for condition, record in sorted(per_condition.items()):
        spread = _spread(record["scores"])
        unstable = sum(1 for outcomes in record["task_outcomes"].values()
                       if len(set(outcomes)) > 1)
        tasks = len(record["task_outcomes"])
        entry = {"score_spread": spread, "tasks": tasks, "unstable_tasks": unstable,
                 "flip_rate": (unstable / tasks) if tasks else None}
        report["conditions"][condition] = entry
        if spread:
            bands.append(spread["spread"])
    report["largest_band"] = max(bands) if bands else None
    return report


def write_report(root: Path) -> dict[str, Any]:
    if not (root / "nanorsi.toml").is_file():
        return {"noise_band": None, "skipped": "no nanorsi.toml in workspace"}
    from .config import load_config
    from .lineage import LineageStore
    events = LineageStore.initialize(root).events()
    payload: dict[str, Any] = {"schema_version": 1,
                               "configured_gate_band": config_gate_band(root, load_config(root / "nanorsi.toml")),
                               "parent_remeasures": band_from_events(events),
                               "note": "derived read-only from repeats already recorded; "
                                       "apply via [gate] noise_band (opt-in, default keeps the strict gate)"}
    final_path = root / "reports" / "final.json"
    if final_path.is_file():
        try:
            payload["final_repeats"] = band_from_final(json.loads(final_path.read_text()))
        except (OSError, ValueError):
            payload["final_repeats"] = {"error": "unreadable final.json"}
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    path = reports / "noise-band.json"
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")
    return {"noise_band": str(path)}


def config_gate_band(root: Path, config) -> float:
    return float(getattr(getattr(config, "gate", None), "noise_band", 0.0) or 0.0)
