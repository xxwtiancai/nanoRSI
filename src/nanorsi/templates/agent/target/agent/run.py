"""A bounded local workflow agent with reusable task/propose entry points.

Task input_files contains workflow.json: {steps: [...]} and ordinary JSON files.
Each step has a unique id, tool, depends_on (step IDs), and arguments. Supported
local tools: load(path), filter(source,field,equals), sum(source,field), and
write(source,path). A source names the result of an earlier dependency. A step
is executable only after all its dependencies finish. Return all input files
plus requested output files, encoded as sorted JSON with a trailing newline.

The initial planner visits the supplied step order once, which works for
already ordered workflows. Improve the scheduling policy to support arbitrary
acyclic step ordering. Keep tools, limits, workspace checks, and both modes.
Shared _skills.py handles live model proposals; the same edited run.py is
loaded again as the next self-use proposer entry point. run_propose executes
plan_steps on the supplied training workflows and sends its scheduling
diagnostics to the model. Improving the shared planner therefore changes
both task behavior and the construction of subsequent proposals.
"""
from __future__ import annotations

import json
from itertools import islice
from pathlib import Path
import tempfile

import _skills

MAX_STEPS = 32


def plan_steps(steps):
    """Return the execution order for a workflow."""
    return list(steps)


def run_task(request, agent, hashes, skill_text, trace, usage):
    task = request.get("task")
    if not isinstance(task, dict) or not isinstance(task.get("input_files"), dict):
        raise _skills.RunnerError("invalid workflow task")
    inputs = task["input_files"]
    try:
        workflow = json.loads(inputs["workflow.json"])
        steps = workflow["steps"]
    except (KeyError, TypeError, json.JSONDecodeError) as error:
        raise _skills.RunnerError("invalid workflow input") from error
    if not isinstance(steps, list) or not 1 <= len(steps) <= MAX_STEPS:
        raise _skills.RunnerError("workflow step limit")
    ids = [step.get("id") for step in steps if isinstance(step, dict)]
    if len(ids) != len(steps) or not all(isinstance(value, str) and value for value in ids) or len(set(ids)) != len(ids):
        raise _skills.RunnerError("invalid step identities")
    with tempfile.TemporaryDirectory(prefix="nanorsi-workflow-") as directory:
        workspace = Path(directory)
        for name, content in inputs.items():
            path = _skills._safe_path(workspace, name, allow_missing=True)
            if not isinstance(content, str):
                raise _skills.RunnerError("input files must contain text")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        values = {}
        for step in plan_steps(steps):
            dependencies = step.get("depends_on", [])
            if not isinstance(dependencies, list) or not all(isinstance(item, str) for item in dependencies):
                raise _skills.RunnerError("invalid dependencies")
            if not all(dependency in values for dependency in dependencies):
                _skills._trace_add(trace, {"event": "step_deferred", "step": step["id"], "dependencies": dependencies})
                continue
            tool = step.get("tool")
            args = step.get("arguments", {})
            if not isinstance(args, dict):
                raise _skills.RunnerError("invalid tool arguments")
            try:
                if tool == "load":
                    value = json.loads(_skills._read_text(_skills._safe_path(workspace, args["path"])))
                elif tool == "filter":
                    value = [row for row in values[args["source"]] if row.get(args["field"]) == args["equals"]]
                elif tool == "sum":
                    value = sum(row[args["field"]] for row in values[args["source"]])
                elif tool == "write":
                    path = _skills._safe_path(workspace, args["path"], allow_missing=True)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(json.dumps(values[args["source"]], sort_keys=True) + "\n", encoding="utf-8")
                    value = {"written": args["path"]}
                else:
                    raise _skills.RunnerError("unknown workflow tool")
            except (KeyError, TypeError, ValueError) as error:
                raise _skills.RunnerError("workflow tool failed: " + str(error)[:80]) from error
            values[step["id"]] = value
            _skills._trace_add(trace, {"event": "workflow_tool", "step": step["id"], "tool": tool})
        unresolved = sorted(set(ids) - set(values))
        _skills._trace_add(trace, {"event": "workflow_complete", "executed": len(values), "unresolved": unresolved})
        return {"status": "ok", "output_files": _skills._workspace_files(workspace), "trace": _skills._bounded_trace(trace), "skill_hashes": hashes, "usage": {"model_calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0, "errors": []}}


def run_propose(request, agent, hashes, skill_text, trace, usage):
    """Reuse this runner's planner to diagnose the supplied training workflows."""
    context = request.get("context")
    if not isinstance(context, dict):
        raise _skills.RunnerError("invalid proposal context")
    training = context.get("train_results", [])
    if not isinstance(training, list):
        raise _skills.RunnerError("train_results must be a list")
    enriched = []
    for case in training:
        if not isinstance(case, dict):
            enriched.append(case)
            continue
        task = case.get("task", {})
        inputs = task.get("input_files", {}) if isinstance(task, dict) else {}
        if not isinstance(inputs, dict) or "workflow.json" not in inputs:
            enriched.append(case)
            continue
        try:
            steps = json.loads(inputs["workflow.json"])["steps"]
            if not isinstance(steps, list) or not 1 <= len(steps) <= MAX_STEPS:
                raise _skills.RunnerError("workflow step limit")
            original_ids = [step["id"] for step in steps]
            if not all(isinstance(value, str) for value in original_ids) or len(set(original_ids)) != len(steps):
                raise _skills.RunnerError("invalid step identities")
            planned = list(islice(plan_steps(steps), MAX_STEPS + 1))
            planned_ids = [step["id"] for step in planned]
            if len(planned_ids) != len(original_ids) or set(planned_ids) != set(original_ids):
                raise _skills.RunnerError("planner must return each step once")
            available = set()
            blocked = []
            for step in planned:
                if not set(step.get("depends_on", [])) <= available:
                    blocked.append(step["id"])
                else:
                    available.add(step["id"])
            diagnostic = {"planned_step_ids": planned_ids, "dependency_order_valid": not blocked, "blocked_step_ids": blocked}
        except (ValueError, KeyError, TypeError) as error:
            diagnostic = {"planned_step_ids": [], "dependency_order_valid": False, "error": str(error)[:120]}
        feedback = case.get("feedback", {})
        enriched.append({**case, "feedback": {**(feedback if isinstance(feedback, dict) else {}), "proposal_planning": diagnostic}})
        _skills._trace_add(trace, {"event": "proposal_planner_used", "task_id": case.get("task_id"), **diagnostic})
    updated = {**request, "context": {**context, "train_results": enriched}}
    return _skills._run_propose(updated, agent, hashes, skill_text, trace, usage)


if __name__ == "__main__":
    _skills.main(task_runner=run_task, proposal_runner=run_propose, runner_path=Path(__file__))
