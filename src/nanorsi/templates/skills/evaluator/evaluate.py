"""Offline evaluator bridge for the v2 skills harness."""

from __future__ import annotations

import json
import math
import os
from pathlib import Path, PurePosixPath
import random
import subprocess
import sys
import time
from typing import Any


def _path(value: Any) -> str:
    if not isinstance(value, str) or not value or "\x00" in value:
        raise ValueError("invalid relative path")
    normalized = value.replace("\\", "/")
    parsed = PurePosixPath(normalized)
    if parsed.is_absolute() or any(part in {"", ".", ".."} for part in parsed.parts):
        raise ValueError("invalid relative path")
    return "/".join(parsed.parts)


def _usage_accumulator() -> dict[str, Any]:
    return {"model_calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "_known": {"input_tokens": False, "output_tokens": False, "cost_usd": False}, "_seen": {"input_tokens": False, "output_tokens": False, "cost_usd": False}, "errors": []}


def _add_usage(total: dict[str, Any], usage: Any) -> None:
    if not isinstance(usage, dict):
        usage = {}
    calls = usage.get("model_calls")
    if isinstance(calls, int) and not isinstance(calls, bool) and calls >= 0:
        total["model_calls"] += calls
    else:
        total["errors"].append("invalid_model_calls")
    for key in ("input_tokens", "output_tokens", "cost_usd"):
        value = usage.get(key)
        if value is None:
            total["_seen"][key] = True
            total["_known"][key] = False
        elif isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(float(value)) and value >= 0:
            if not total["_seen"][key]:
                total["_known"][key] = True
            total["_seen"][key] = True
            if total["_known"][key]:
                total[key] += value
        else:
            total["_seen"][key] = True
            total["_known"][key] = False
            total["errors"].append(f"invalid_{key}")
    errors = usage.get("errors")
    if isinstance(errors, list):
        total["errors"].extend(str(item)[:120] for item in errors[:16])


def _finish_usage(total: dict[str, Any]) -> dict[str, Any]:
    return {"model_calls": total["model_calls"], **{key: total[key] if total["_known"][key] else None for key in ("input_tokens", "output_tokens", "cost_usd")}, "errors": total["errors"]}


def _manifest(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1 or not isinstance(payload.get("tasks"), list):
        raise ValueError("manifest must have schema_version 1 and tasks")
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for task in payload["tasks"]:
        if not isinstance(task, dict) or not isinstance(task.get("task_id"), str) or not isinstance(task.get("group_id"), str):
            raise ValueError("invalid task identity")
        task_id = task["task_id"]
        if task_id in seen:
            raise ValueError("duplicate task_id")
        seen.add(task_id)
        if task.get("split") not in {"train", "validation", "test"} or not isinstance(task.get("instruction"), str):
            raise ValueError("invalid task split or instruction")
        inputs = task.get("input_files")
        expected = task.get("expected_files")
        if not isinstance(inputs, dict) or not isinstance(expected, dict):
            raise ValueError("task files must be objects")
        normalized_inputs: dict[str, str] = {}
        normalized_expected: dict[str, str] = {}
        for raw, content in inputs.items():
            key = _path(raw)
            if not isinstance(content, str):
                raise ValueError("input content must be text")
            normalized_inputs[key] = content
        for raw, content in expected.items():
            key = _path(raw)
            if not isinstance(content, str):
                raise ValueError("expected content must be text")
            normalized_expected[key] = content
        tasks.append({**task, "input_files": normalized_inputs, "expected_files": normalized_expected})
    return tasks


def _select(tasks: list[dict[str, Any]], split: str, limit: int, seed: int) -> list[dict[str, Any]]:
    selected = [task for task in tasks if task["split"] == split]
    if split == "train" and limit >= 0 and len(selected) > limit:
        selected = random.Random(seed).sample(selected, limit)
    return sorted(selected, key=lambda task: task["task_id"])


def _timeout(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("agent.timeout_s must be a finite positive number")
    try:
        converted = float(value)
    except OverflowError as error:
        raise ValueError("agent.timeout_s must be a finite positive number") from error
    if not math.isfinite(converted) or converted <= 0:
        raise ValueError("agent.timeout_s must be a finite positive number")
    return converted


def _invoke(task: dict[str, Any], agent: dict[str, Any], repeat_id: str, runner: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    request = {"mode": "task", "task": {"task_id": task["task_id"], "instruction": task["instruction"], "input_files": task["input_files"]}, "agent": agent}
    timeout = agent.get("timeout_s", 60)
    try:
        max_turns = agent.get("max_turns", 8)
        if isinstance(max_turns, bool) or not isinstance(max_turns, int) or not 1 <= max_turns <= 8:
            raise ValueError("agent.max_turns must be an integer between 1 and 8")
        bounded_timeout = max(0.1, _timeout(timeout) * max_turns + 10.0)
        if not math.isfinite(bounded_timeout):
            raise ValueError("agent.timeout_s exceeds the platform timeout range")
    except (TypeError, ValueError, OverflowError) as error:
        return {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "invalid_timeout"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": [str(error)[:120]]}, "duration_ms": 0}, {"score": 0.0, "status": "runner_error"}
    try:
        completed = subprocess.run([sys.executable, str(runner)], cwd=Path.cwd(), input=json.dumps(request), capture_output=True, text=True, timeout=bounded_timeout, check=False)
    except subprocess.TimeoutExpired:
        return {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "timeout"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_timeout"]}, "duration_ms": int(bounded_timeout * 1000)}, {"score": 0.0, "status": "error"}
    except (OverflowError, OSError) as error:
        return {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "start_error"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": [f"runner_start_error:{str(error)[:80]}"]}, "duration_ms": 0}, {"score": 0.0, "status": "runner_error"}
    if completed.returncode != 0:
        return {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "exit"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_exit"]}, "duration_ms": 0}, {"score": 0.0, "status": "error"}
    try:
        runner_result = json.loads(completed.stdout)
    except json.JSONDecodeError:
        runner_result = {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "invalid_json"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_invalid_json"]}, "duration_ms": 0}
    if not isinstance(runner_result, dict):
        runner_result = {"status": "error", "output_files": {}, "trace": [{"event": "runner_error", "code": "invalid_result"}], "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_invalid_result"]}, "duration_ms": 0}
    return runner_result, {"score": 0.0, "status": "error"}


def _grade(task: dict[str, Any], runner_result: dict[str, Any]) -> tuple[float, str]:
    output = runner_result.get("output_files")
    if runner_result.get("status") != "ok" or not isinstance(output, dict):
        codes = {str(item.get("code", "")) for item in runner_result.get("trace", []) if isinstance(item, dict)}
        if "invalid_timeout" in codes:
            return 0.0, "runner_error"
        if any("timeout" in code for code in codes):
            return 0.0, "timeout"
        if any("invalid" in code for code in codes):
            return 0.0, "invalid_output"
        return 0.0, "runner_error"
    inputs = task["input_files"]
    expected = task["expected_files"]
    final_files = set(inputs) | set(expected)
    if set(output) != final_files:
        return 0.0, "task_failure"
    for path in final_files:
        target = expected[path] if path in expected else inputs[path]
        if output.get(path) != target:
            return 0.0, "task_failure"
    return 1.0, "ok"


def _training_feedback(task: dict[str, Any], runner_result: dict[str, Any]) -> dict[str, Any]:
    actual = runner_result.get("output_files") if isinstance(runner_result.get("output_files"), dict) else {}
    expected = task["expected_files"]
    return {
        "expected_files": expected,
        "actual_files": actual,
        "missing_files": sorted((set(task["input_files"]) | set(expected)) - set(actual)),
        "unexpected_files": sorted(set(actual) - (set(task["input_files"]) | set(expected))),
        "mismatched_files": sorted(path for path in expected if path in actual and actual[path] != expected[path]),
    }


def evaluate() -> dict[str, Any]:
    started = time.monotonic()
    split = os.environ.get("NANORSI_SPLIT", "validation")
    manifest_path = Path(os.environ["NANORSI_TASK_MANIFEST"]).resolve()
    result_path = Path(os.environ["NANORSI_RESULT_PATH"])
    agent = json.loads(os.environ.get("NANORSI_AGENT_CONFIG", "{}"))
    if not isinstance(agent, dict):
        raise ValueError("NANORSI_AGENT_CONFIG must be an object")
    repeat_id = int(os.environ.get("NANORSI_REPEAT_ID", "0"))
    seed = int(os.environ.get("NANORSI_SEED", "0"))
    limit = int(os.environ.get("NANORSI_TRAIN_LIMIT", "4"))
    tasks = _select(_manifest(manifest_path), split, limit, seed)
    runner = Path.cwd() / "target" / "agent" / "run.py"
    cases: list[dict[str, Any]] = []
    total_usage = _usage_accumulator()
    for task in tasks:
        runner_result, _ = _invoke(task, agent, repeat_id, runner)
        score, status = _grade(task, runner_result)
        case_usage = runner_result.get("usage") if isinstance(runner_result.get("usage"), dict) else {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["missing_usage"]}
        case_trace = runner_result.get("trace") if isinstance(runner_result.get("trace"), list) else [{"event": "runner_error", "code": "invalid_trace"}]
        case_hashes = runner_result.get("skill_hashes") if isinstance(runner_result.get("skill_hashes"), dict) else {}
        case_duration = runner_result.get("duration_ms", 0)
        if isinstance(case_duration, bool) or not isinstance(case_duration, int) or case_duration < 0:
            case_duration = 0
        _add_usage(total_usage, case_usage)
        case = {"task_id": task["task_id"], "group_id": task["group_id"], "repeat_id": repeat_id, "score": score, "status": status, "trace": case_trace, "skill_hashes": case_hashes, "usage": case_usage, "duration_ms": case_duration}
        if split == "train":
            case["task"] = {"task_id": task["task_id"], "instruction": task["instruction"], "input_files": task["input_files"]}
            case["feedback"] = _training_feedback(task, runner_result)
        cases.append(case)
    score = sum(case["score"] for case in cases) / len(cases) if cases else 0.0
    elapsed = max(0, int((time.monotonic() - started) * 1000))
    return {"schema_version": 2, "status": "ok", "metrics": {"score": score}, "constraints": {"tests_passed": True}, "case_results": cases, "cost_usd": total_usage["cost_usd"] if total_usage["_known"]["cost_usd"] else None, "duration_ms": elapsed, "usage": _finish_usage(total_usage)}


def main() -> None:
    result_path = Path(os.environ.get("NANORSI_RESULT_PATH", "result.json"))
    try:
        payload = evaluate()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        payload = {"schema_version": 2, "status": "error", "metrics": {"score": 0.0}, "constraints": {"tests_passed": False}, "case_results": [], "cost_usd": None, "duration_ms": 0, "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": [str(error)[:120]]}}
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
