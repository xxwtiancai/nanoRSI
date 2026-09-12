"""Fixed JSON program grading; held-out labels stay in the evaluator.

Candidate code is trusted local code with bounded time/output, not sandboxed.
The only model calls happen in the proposal runner.
"""
from __future__ import annotations

from decimal import Decimal
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import time

import _skills
from nanorsi.process import run_argv


def _invoke(task, agent, repeat_id, runner):
    started = time.monotonic()
    program = Path.cwd() / "target/program.py"
    trace = [{"event": "program_loaded", "path": "target/program.py", "sha256": hashlib.sha256(program.read_bytes()).hexdigest()}]
    result = {"status": "error", "output_files": {}, "trace": trace, "skill_hashes": {}, "usage": {"model_calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "errors": []}}
    with tempfile.TemporaryDirectory(prefix="nanorsi-program-") as directory:
        completed = run_argv([sys.executable, str(program)], input_text=task["input_files"]["records.json"], timeout_s=2.0, cwd=Path(directory), max_output_bytes=1_000_000)
    if completed.timed_out or completed.output_limited or completed.exit_code != 0:
        trace.append({"event": "runner_error", "code": "timeout" if completed.timed_out else "output_limit" if completed.output_limited else "exit"})
    else:
        try:
            actual = json.loads(completed.stdout)
            if not isinstance(actual, dict):
                raise ValueError("program output must be an object")
            # Keep numeric lexemes intact for exact semantic comparison below.
            result["output_files"] = {**task["input_files"], "summary.json": completed.stdout}
            result["status"] = "ok"
        except (ValueError, UnicodeError):
            trace.append({"event": "runner_error", "code": "invalid_output"})
    result["duration_ms"] = max(0, int((time.monotonic() - started) * 1000))
    return result, {}


def _reject_constant(value):
    raise ValueError("invalid JSON numeric constant: " + value)


def _same_json(left, right):
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_same_json(left[key], right[key]) for key in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(_same_json(a, b) for a, b in zip(left, right))
    return left == right


def _grade(task, runner_result):
    output = runner_result.get("output_files")
    if runner_result.get("status") != "ok" or not isinstance(output, dict):
        return _skills._grade(task, runner_result)
    inputs, expected = task["input_files"], task["expected_files"]
    if set(output) != set(inputs) | set(expected):
        return 0.0, "task_failure"
    for path in set(inputs) - set(expected):
        if output[path] != inputs[path]:
            return 0.0, "task_failure"
    try:
        for path, reference in expected.items():
            actual = json.loads(output[path], parse_float=Decimal, parse_int=Decimal, parse_constant=_reject_constant)
            wanted = json.loads(reference, parse_float=Decimal, parse_int=Decimal, parse_constant=_reject_constant)
            if not _same_json(actual, wanted):
                return 0.0, "task_failure"
    except (TypeError, ValueError):
        return 0.0, "invalid_output"
    return 1.0, "ok"


def evaluate():
    return _skills.evaluate(invoke=_invoke, grade=_grade)


if __name__ == "__main__":
    _skills.main(evaluator=evaluate)
