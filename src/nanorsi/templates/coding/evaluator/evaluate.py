"""Behavioral Python grading with public feedback and private holdouts.

Generated programs run as trusted local code with bounded process resources;
this evaluator does not provide a security sandbox. Final file paths must equal
the union of input and expected paths; reference contents are never compared.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

import _skills


def _test_helpers():
    path = Path(__file__).resolve().parents[1] / "adapters/python_tests.py"
    spec = importlib.util.spec_from_file_location("_nanorsi_python_tests", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_python = _test_helpers()


def _manifest(path: Path) -> list[dict[str, Any]]:
    tasks = _skills._manifest(path, file_validator=_python.workspace_files)
    for task in tasks:
        grading = task.get("grading")
        if not isinstance(grading, dict) or set(grading) != {"kind", "public_tests", "private_tests", "timeout_s"} or grading.get("kind") != "python-unittest":
            raise ValueError("coding task requires python-unittest grading")
        _python.test_sources(grading["public_tests"])
        _python.test_sources(grading["private_tests"])
        _python.test_timeout(grading["timeout_s"])
    return tasks


def _invoke(task, agent, repeat_id, runner):
    grading = task["grading"]
    return _skills._invoke(task, agent, repeat_id, runner, task_fields={"public_tests": grading["public_tests"], "test_timeout_s": grading["timeout_s"]})


def _grade(task: dict[str, Any], runner_result: dict[str, Any]) -> tuple[float, str]:
    if runner_result.get("status") != "ok" or not isinstance(runner_result.get("output_files"), dict):
        return _skills._grade(task, runner_result)
    if set(runner_result["output_files"]) != set(task["input_files"]) | set(task["expected_files"]):
        return 0.0, "task_failure"
    grading = task["grading"]
    try:
        public = _python.run_tests(runner_result["output_files"], grading["public_tests"], grading["timeout_s"])
        runner_result["_public_feedback"] = public
        private = _python.run_tests(runner_result["output_files"], grading["private_tests"], grading["timeout_s"]) if public["passed"] else None
    except ValueError:
        return 0.0, "invalid_output"
    # Private test output and source stay in this stack frame, never in traces,
    # training feedback, or bridge requests. Duration includes grading execution.
    duration = runner_result.get("duration_ms", 0)
    if isinstance(duration, bool) or not isinstance(duration, int) or duration < 0:
        duration = 0
    runner_result["duration_ms"] = duration + public["duration_ms"] + (private["duration_ms"] if private else 0)
    verdict = private if private is not None else public
    return (1.0, "ok") if verdict["passed"] else (0.0, verdict["status"])


def _training_feedback(task: dict[str, Any], runner_result: dict[str, Any]) -> dict[str, Any]:
    return {"actual_files": runner_result.get("output_files", {}), "public_tests": task["grading"]["public_tests"], "public_result": runner_result.get("_public_feedback", {"status": "not_run", "passed": False})}


def evaluate() -> dict[str, Any]:
    return _skills.evaluate(manifest_loader=_manifest, invoke=_invoke, grade=_grade, training_feedback=_training_feedback)


if __name__ == "__main__":
    _skills.main(evaluator=evaluate)
