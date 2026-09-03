from __future__ import annotations

import json
import math
from dataclasses import dataclass
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


def parse_evaluation(payload: dict) -> EvaluationResult:
    if not isinstance(payload, dict) or payload.get("schema_version") != 1 or payload.get("status") != "ok":
        raise EvaluationError("evaluation must be schema_version 1 with status ok")
    metrics = payload.get("metrics")
    constraints = payload.get("constraints")
    if not isinstance(metrics, dict) or not metrics or not isinstance(constraints, dict):
        raise EvaluationError("metrics and constraints must be objects")
    clean_metrics: dict[str, float] = {}
    for name, value in metrics.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise EvaluationError(f"metric {name!r} must be finite")
        clean_metrics[str(name)] = float(value)
    duration = payload.get("duration_ms")
    cost = payload.get("cost_usd")
    if isinstance(duration, bool) or not isinstance(duration, int) or duration < 0:
        raise EvaluationError("duration_ms must be a non-negative integer")
    if cost is not None and (isinstance(cost, bool) or not isinstance(cost, (int, float))):
        raise EvaluationError("cost_usd must be null or numeric")
    cases = payload.get("case_results", [])
    if not isinstance(cases, list):
        raise EvaluationError("case_results must be an array")
    return EvaluationResult(clean_metrics, constraints, cases, None if cost is None else float(cost), duration)


def run_evaluation(config: Config, candidate: Path, split: str, result_path: Path) -> EvaluationResult:
    result_path.parent.mkdir(parents=True, exist_ok=True)
    if result_path.exists():
        result_path.unlink()
    result = run_argv(
        config.evaluator.command,
        cwd=candidate,
        timeout_s=config.evaluator.timeout_s,
        extra_env={"NANORSI_SPLIT": split, "NANORSI_RESULT_PATH": str(result_path)},
    )
    if result.timed_out or result.exit_code != 0 or not result_path.is_file():
        detail = result.stderr.strip() or result.stdout.strip() or "evaluator produced no result"
        raise EvaluationError(detail)
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise EvaluationError(f"invalid evaluator JSON: {error}") from error
    evaluation = parse_evaluation(payload)
    if config.evaluator.primary_metric not in evaluation.metrics:
        raise EvaluationError(f"primary metric missing: {config.evaluator.primary_metric}")
    return evaluation
