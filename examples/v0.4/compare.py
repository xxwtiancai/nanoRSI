"""Validate and compare final nanoRSI harness experiment reports.

The summary uses task-macro scores: repeats are averaged within each task
before task means are averaged.  This is pilot analysis of protocol fixtures,
not evidence for benchmark-level claims.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


CONDITIONS = ("baseline", "no-skills", "candidate")


def _finite(value: Any, label: str, *, allow_none: bool = False,
            minimum: float | None = None, maximum: float | None = None) -> float | None:
    if value is None and allow_none:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite number or null")
    try:
        number = float(value)
    except (OverflowError, ValueError) as error:
        raise ValueError(f"{label} must be finite") from error
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    if minimum is not None and number < minimum:
        raise ValueError(f"{label} must be >= {minimum}")
    if maximum is not None and number > maximum:
        raise ValueError(f"{label} must be <= {maximum}")
    return number


def _nonnegative_int(value: Any, label: str) -> tuple[str, int]:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a nonnegative integer")
    return "int", value


def _require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _percentile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = max(0, math.ceil(fraction * len(ordered)) - 1)
    return ordered[index]


def _cost_summary(values: list[float | None]) -> dict[str, float | int | None]:
    known = [value for value in values if value is not None]
    try:
        known_total = math.fsum(known) if known else None
    except (OverflowError, ValueError) as error:
        raise ValueError("cost total must be finite") from error
    if known_total is not None and not math.isfinite(known_total):
        raise ValueError("cost total must be finite")
    all_known = len(known) == len(values)
    return {
        "known_usd": known_total,
        "total_usd": known_total if all_known else None,
        "known_count": len(known),
        "total_count": len(values),
        "coverage": len(known) / len(values) if values else 0.0,
    }


def _timing_summary(values: list[float | None]) -> dict[str, float | int | None]:
    known = [value for value in values if value is not None]
    try:
        mean = statistics.fmean(known) if known else None
    except (OverflowError, ValueError) as error:
        raise ValueError("timing mean must be finite") from error
    return {
        "mean_ms": mean,
        "median_ms": statistics.median(known) if known else None,
        "p95_ms": _percentile(known, 0.95),
        "known_count": len(known),
        "total_count": len(values),
        "coverage": len(known) / len(values) if values else 0.0,
    }


def _delta_pp(left: float | None, right: float) -> float | None:
    return None if left is None else round((left - right) * 100, 12)


def _condition_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    task_scores: dict[str, list[float]] = defaultdict(list)
    for record in records:
        for case in record["case_results"]:
            task_scores[case["task_id"]].append(case["score"])
    task_means = {task_id: statistics.fmean(scores) for task_id, scores in task_scores.items()}
    case_durations = [case["duration_ms"] for record in records for case in record["case_results"]]
    return {
        "task_macro": statistics.fmean(list(task_means.values())) if task_means else None,
        "task_count": len(task_means),
        "case_count": sum(len(record["case_results"]) for record in records),
        "repeat_count": len(records),
        "task_scores": dict(sorted(task_means.items())),
        "cost_usd": _cost_summary([record["cost_usd"] for record in records]),
        "duration_ms": _timing_summary(case_durations),
    }


def _equal_run_condition_summary(reports: list[dict[str, Any]], condition: str) -> dict[str, Any]:
    per_run = [_condition_summary(report["records"][condition]) for report in reports]
    task_scores: dict[str, list[float]] = defaultdict(list)
    for summary in per_run:
        for task_id, score in summary["task_scores"].items():
            task_scores[task_id].append(score)
    averaged_tasks = {task_id: statistics.fmean(scores) for task_id, scores in task_scores.items()}
    combined_records = [record for report in reports for record in report["records"][condition]]
    result = _condition_summary(combined_records)
    result["task_scores"] = dict(sorted(averaged_tasks.items()))
    result["task_macro"] = statistics.fmean(list(averaged_tasks.values())) if averaged_tasks else None
    return result


def _validate_report(report: dict[str, Any]) -> tuple[dict[str, Any], dict[str, str]]:
    if not isinstance(report, dict):
        raise ValueError("each report must be an object")
    if report.get("schema_version") != 2:
        raise ValueError("report schema_version must be 2")
    for key in ("manifest_hash", "comparison_hash", "experiment_id", "arm", "seed", "results"):
        if key not in report:
            raise ValueError(f"report is missing {key}")
    manifest_hash = _require_text(report["manifest_hash"], "manifest_hash")
    comparison_hash = _require_text(report["comparison_hash"], "comparison_hash")
    experiment_id = _require_text(report["experiment_id"], "experiment_id")
    arm = _require_text(report["arm"], "arm")
    seed_identity = _nonnegative_int(report["seed"], "seed")
    results = report["results"]
    if not isinstance(results, list) or not results:
        raise ValueError("report results must be a non-empty list")

    condition_names = report.get("conditions", list(CONDITIONS))
    if not isinstance(condition_names, list) or not all(isinstance(c, str) for c in condition_names) or len(set(condition_names)) != len(condition_names):
        raise ValueError("invalid condition declaration")
    if not {"baseline", "candidate"} <= set(condition_names) <= set(CONDITIONS):
        raise ValueError("conditions require baseline and candidate")
    metric = report.get("metric", {"name": "score", "direction": "maximize"})
    if metric != {"name": "score", "direction": "maximize"}:
        raise ValueError("comparison supports normalized score/maximize only; use the per-experiment report for other metrics")
    by_condition: dict[str, list[dict[str, Any]]] = {condition: [] for condition in condition_names}
    seen_result_keys: set[tuple[str, tuple[str, Any]]] = set()
    task_groups: dict[str, str] = {}
    for index, record in enumerate(results):
        if not isinstance(record, dict):
            raise ValueError(f"results[{index}] must be an object")
        condition = record.get("condition")
        if condition not in condition_names:
            raise ValueError(f"results[{index}] has unknown condition")
        if "repeat_id" not in record:
            raise ValueError(f"results[{index}] is missing repeat_id")
        repeat_identity = _nonnegative_int(record["repeat_id"], f"results[{index}].repeat_id")
        result_key = (condition, repeat_identity)
        if result_key in seen_result_keys:
            raise ValueError(f"duplicate result for {condition!r}, repeat {record['repeat_id']!r}")
        seen_result_keys.add(result_key)
        cases = record.get("case_results")
        if not isinstance(cases, list) or not cases:
            raise ValueError(f"results[{index}].case_results must be a non-empty list")
        cost = _finite(record.get("cost_usd"), f"results[{index}].cost_usd",
                       allow_none=True, minimum=0)
        duration = _finite(record.get("duration_ms"), f"results[{index}].duration_ms",
                           allow_none=True, minimum=0)
        pairs: set[tuple[str, tuple[str, Any]]] = set()
        normalized_cases = []
        for case_index, case in enumerate(cases):
            if not isinstance(case, dict):
                raise ValueError(f"results[{index}].case_results[{case_index}] must be an object")
            task_id = _require_text(case.get("task_id"), "case task_id")
            group_id = _require_text(case.get("group_id"), "case group_id")
            if "repeat_id" not in case or _nonnegative_int(case["repeat_id"], "case repeat_id") != repeat_identity:
                raise ValueError(f"case {task_id!r} has a repeat_id different from its result")
            score = _finite(case.get("score"), f"score for {task_id}", minimum=0, maximum=1)
            case_duration = _finite(case.get("duration_ms"), f"duration for {task_id}",
                                    allow_none=True, minimum=0)
            pair = (task_id, repeat_identity)
            if pair in pairs:
                raise ValueError(f"duplicate case pair {task_id!r}, repeat {case['repeat_id']!r}")
            pairs.add(pair)
            previous_group = task_groups.setdefault(task_id, group_id)
            if previous_group != group_id:
                raise ValueError(f"task {task_id!r} has inconsistent group_id")
            normalized_cases.append({**case, "task_id": task_id, "group_id": group_id,
                                     "score": score, "duration_ms": case_duration})
        by_condition[condition].append({
            "condition": condition,
            "repeat_id": record["repeat_id"],
            "case_results": normalized_cases,
            "cost_usd": cost,
            "duration_ms": duration,
            "pairs": pairs,
        })

    if any(not by_condition[condition] for condition in condition_names):
        raise ValueError("report must contain every declared final condition")
    expected_pairs = {pair for record in by_condition["baseline"] for pair in record["pairs"]}
    for condition in condition_names[1:]:
        pairs = {pair for record in by_condition[condition] for pair in record["pairs"]}
        if pairs != expected_pairs:
            raise ValueError(f"{condition} task/repeat pairs do not match baseline")
    clean = {condition: [{key: value for key, value in record.items() if key != "pairs"}
                         for record in records]
             for condition, records in by_condition.items()}
    metadata = {
        "manifest_hash": manifest_hash,
        "comparison_hash": comparison_hash,
        "experiment_id": experiment_id,
        "arm": arm,
        "seed": report["seed"],
        "seed_identity": seed_identity,
        "conditions": condition_names,
        "mode": report.get("mode", "harness"),
    }
    return {"metadata": metadata, "records": clean, "task_groups": task_groups}, task_groups


def _report_summary(validated: dict[str, Any]) -> dict[str, Any]:
    metadata = validated["metadata"]
    conditions = {condition: _condition_summary(validated["records"][condition]) for condition in metadata["conditions"]}
    baseline = conditions["baseline"]["task_macro"]
    candidate = conditions["candidate"]["task_macro"]
    no_skills = conditions.get("no-skills", {}).get("task_macro")
    return {
        **{key: metadata[key] for key in
           ("experiment_id", "arm", "seed", "manifest_hash", "comparison_hash")},
        "conditions": conditions,
        "candidate_baseline_delta_pp": _delta_pp(candidate, baseline),
        "no_skills_delta_pp": _delta_pp(no_skills, baseline),
    }


def _arm_summaries(reports: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for report in reports:
        grouped[report["arm"]].append(report)
    summaries = {}
    for arm, arm_reports in sorted(grouped.items()):
        candidate_deltas = [report["candidate_baseline_delta_pp"] for report in arm_reports]
        no_skills_deltas = [report["no_skills_delta_pp"] for report in arm_reports if report["no_skills_delta_pp"] is not None]
        summaries[arm] = {
            "run_count": len(arm_reports),
            "mean_candidate_baseline_delta_pp": statistics.fmean(candidate_deltas),
            "candidate_baseline_delta_pp_range": [min(candidate_deltas), max(candidate_deltas)],
            "mean_no_skills_delta_pp": statistics.fmean(no_skills_deltas) if no_skills_deltas else None,
            "no_skills_delta_pp_range": [min(no_skills_deltas), max(no_skills_deltas)] if no_skills_deltas else None,
        }
    return summaries


def summarize(reports: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(reports, list) or not reports:
        raise ValueError("summarize expects at least one report")
    validated_reports = []
    seen_runs: set[tuple[str, str, tuple[str, Any]]] = set()
    expected_tasks: dict[str, str] | None = None
    comparison_hash: str | None = None
    comparison_shape = None
    for report in reports:
        validated, task_groups = _validate_report(report)
        metadata = validated["metadata"]
        shape = (metadata["mode"], tuple(metadata["conditions"]))
        if comparison_shape is None:
            comparison_shape = shape
        elif shape != comparison_shape:
            raise ValueError("reports must use the same mode and final conditions")
        run_key = (metadata["experiment_id"], metadata["arm"], metadata["seed_identity"])
        if run_key in seen_runs:
            raise ValueError("duplicate experiment_id/arm/seed report")
        seen_runs.add(run_key)
        report_comparison_hash = metadata["comparison_hash"]
        if comparison_hash is None:
            comparison_hash = report_comparison_hash
        elif report_comparison_hash != comparison_hash:
            raise ValueError("reports must use the same comparison_hash")
        if expected_tasks is None:
            expected_tasks = task_groups
        elif task_groups != expected_tasks:
            raise ValueError("reports must use the same task and group IDs")
        validated_reports.append(validated)

    conditions = {condition: _equal_run_condition_summary(validated_reports, condition)
                  for condition in validated_reports[0]["metadata"]["conditions"]}
    baseline = conditions["baseline"]["task_macro"]
    candidate = conditions["candidate"]["task_macro"]
    no_skills = conditions.get("no-skills", {}).get("task_macro")
    individual = [_report_summary(report) for report in validated_reports]
    arms = _arm_summaries(individual)
    overall = {
        "scope": "descriptive equal-run-weight aggregate across arms",
        "candidate_baseline_delta_pp": _delta_pp(candidate, baseline),
        "no_skills_delta_pp": _delta_pp(no_skills, baseline),
    }
    return {
        "schema_version": 1,
        "report_count": len(reports),
        "comparison_hash": comparison_hash,
        "aggregation": "equal_run_weight",
        "task_ids": sorted(expected_tasks or {}),
        "group_ids": sorted(set((expected_tasks or {}).values())),
        "conditions": conditions,
        "candidate_baseline_delta_pp": _delta_pp(candidate, baseline),
        "no_skills_delta_pp": _delta_pp(no_skills, baseline),
        "arms": arms,
        "overall": overall,
        "reports": individual,
        "experiments": individual,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compare validated nanoRSI experiment reports.")
    parser.add_argument("reports", nargs="+", help="report JSON files, or - for stdin")
    args = parser.parse_args(argv)
    loaded = []
    for report_path in args.reports:
        if report_path == "-":
            loaded.append(json.load(sys.stdin))
        else:
            loaded.append(json.loads(Path(report_path).read_text(encoding="utf-8")))
    try:
        result = summarize(loaded)
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
