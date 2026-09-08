from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

from .config import Config
from .process import run_argv


class EvaluationError(ValueError):
    pass


@dataclass(frozen=True)
class EvaluationResult:
    metrics: dict[str, float]
    constraints: dict[str, object]
    case_results: list[dict]
    cost_usd: float | None
    duration_ms: int
    usage: dict = field(default_factory=dict)


_CASE_STATUSES = {"ok", "task_failure", "timeout", "runner_error", "provider_error", "invalid_output"}
_COUNT_FIELDS = {"model_calls", "input_tokens", "output_tokens", "cached_tokens"}
_USAGE_FIELDS = _COUNT_FIELDS | {"cost_usd"}


def _validate_usage(usage: object, label: str) -> dict:
    if not isinstance(usage, dict):
        raise EvaluationError(f"{label} must be an object")
    for name, value in usage.items():
        if name not in _USAGE_FIELDS:
            continue
        if value is None:
            continue
        if name in _COUNT_FIELDS:
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise EvaluationError(f"{label}.{name} must be null or a non-negative integer")
        elif isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise EvaluationError(f"{label}.{name} must be null or a finite non-negative number")
    return dict(usage)


def _validate_cost(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise EvaluationError("cost_usd must be null or a finite non-negative number")
    return float(value)


def _validate_duration(value: object, label: str = "duration_ms") -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise EvaluationError(f"{label} must be a non-negative integer")
    return value


def _validate_metrics_and_constraints(payload: dict) -> tuple[dict[str, float], dict[str, object]]:
    metrics = payload.get("metrics")
    constraints = payload.get("constraints")
    if not isinstance(metrics, dict) or not metrics or not isinstance(constraints, dict):
        raise EvaluationError("metrics and constraints must be objects")
    clean_metrics: dict[str, float] = {}
    for name, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise EvaluationError(f"metric {name!r} must be finite")
        clean_metrics[str(name)] = float(value)
    return clean_metrics, constraints


def _validate_case(case: object, index: int) -> dict:
    if not isinstance(case, dict):
        raise EvaluationError(f"case_results[{index}] must be an object")
    required = {"task_id", "group_id", "repeat_id", "score", "status", "trace", "skill_hashes", "usage", "duration_ms"}
    missing = sorted(required - set(case))
    if missing:
        raise EvaluationError(f"case_results[{index}] missing {missing[0]}")
    for name in ("task_id", "group_id"):
        if not isinstance(case[name], str) or not case[name]:
            raise EvaluationError(f"case_results[{index}].{name} must be a non-empty string")
    repeat_id = case["repeat_id"]
    if isinstance(repeat_id, bool) or not isinstance(repeat_id, int) or repeat_id < 0:
        raise EvaluationError(f"case_results[{index}].repeat_id must be a non-negative integer")
    score = case["score"]
    if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
        raise EvaluationError(f"case_results[{index}].score must be finite and between 0 and 1")
    if not isinstance(case["status"], str) or case["status"] not in _CASE_STATUSES:
        raise EvaluationError(f"case_results[{index}].status is invalid")
    if not isinstance(case["trace"], list):
        raise EvaluationError(f"case_results[{index}].trace must be an array")
    if not isinstance(case["skill_hashes"], dict):
        raise EvaluationError(f"case_results[{index}].skill_hashes must be an object")
    _validate_usage(case["usage"], f"case_results[{index}].usage")
    _validate_duration(case["duration_ms"], f"case_results[{index}].duration_ms")
    return case


def _validate_cases(cases: object, required: bool) -> list[dict]:
    if not isinstance(cases, list) or (required and not cases):
        raise EvaluationError("case_results must be a non-empty array" if required else "case_results must be an array")
    clean_cases = [_validate_case(case, index) for index, case in enumerate(cases)] if required else cases
    seen: set[tuple[str, int]] = set()
    for case in clean_cases:
        if required:
            identity = (case["task_id"], case["repeat_id"])
            if identity in seen:
                raise EvaluationError("case_results contains duplicate task_id/repeat_id")
            seen.add(identity)
    return clean_cases


def parse_evaluation(payload: dict) -> EvaluationResult:
    if not isinstance(payload, dict):
        raise EvaluationError("evaluation must be an object")
    schema = payload.get("schema_version")
    if isinstance(schema, bool) or not isinstance(schema, int) or payload.get("status") != "ok":
        raise EvaluationError("evaluation must have a supported schema_version with status ok")
    metrics, constraints = _validate_metrics_and_constraints(payload)
    cost = _validate_cost(payload.get("cost_usd"))
    duration = _validate_duration(payload.get("duration_ms"))
    if schema == 1:
        cases = _validate_cases(payload.get("case_results", []), required=False)
        return EvaluationResult(metrics, constraints, cases, cost, duration)
    if schema != 2:
        raise EvaluationError("evaluation schema_version must be 1 or 2")
    if "usage" not in payload:
        raise EvaluationError("schema_version 2 requires usage")
    usage = _validate_usage(payload["usage"], "usage")
    cases = _validate_cases(payload.get("case_results"), required=True)
    return EvaluationResult(metrics, constraints, cases, cost, duration, usage)


def run_evaluation(
    config: Config,
    candidate: Path,
    split: str,
    result_path: Path,
    extra_env: dict[str, str] | None = None,
) -> EvaluationResult:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    if result_path.exists():
        result_path.unlink()
    environment = dict(extra_env or {})
    environment.update({"NANORSI_SPLIT": split, "NANORSI_RESULT_PATH": str(result_path)})
    result = run_argv(
        config.evaluator.command,
        cwd=candidate,
        timeout_s=config.evaluator.timeout_s,
        extra_env=environment,
        max_output_bytes=config.budget.max_output_bytes,
    )
    if result.timed_out or result.output_limited or result.exit_code != 0 or not result_path.is_file():
        detail = result.stderr.strip() or result.stdout.strip() or "evaluator produced no result"
        raise EvaluationError(detail)
    try:
        if result_path.stat().st_size > config.budget.max_output_bytes:
            raise EvaluationError("evaluator result exceeds max_output_bytes")
    except OSError as error:
        raise EvaluationError(f"cannot inspect evaluator result: {error}") from error
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvaluationError(f"invalid evaluator JSON: {error}") from error
    if getattr(getattr(config, "experiment", None), "schema_version", 1) == 2 and (not isinstance(payload, dict) or payload.get("schema_version") != 2):
        raise EvaluationError("schema-v2 experiments require schema_version 2 evaluator results")
    evaluation = parse_evaluation(payload)
    if config.evaluator.primary_metric not in evaluation.metrics:
        raise EvaluationError(f"primary metric missing: {config.evaluator.primary_metric}")
    return evaluation
