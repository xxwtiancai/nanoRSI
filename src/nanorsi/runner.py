"""Task executors behind one protocol. A rollout runs one task under one harness
and returns a trajectory plus deliverables; the improver never sees scores here.

Protocol for `runner.kind = "command"` (how a real substrate such as OpenCode is
attached without the core knowing it): the command receives NANORSI_REQUEST, a
JSON file {task, harness_dir, output_dir, always_on}, runs with the workspace as
cwd, and writes NANORSI_RESULT: {ok, delivered, trajectory, deliverables:{name:text},
usage:{calls,input_tokens,output_tokens}, error}. The built-in loopback runner is a
document-reading agent on the configured chat model, for offline-style tasks."""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from . import harness
from .model import ModelError, parse_reply


@dataclass
class Rollout:
    label: str
    run_dir: Path
    ok: bool
    delivered: bool
    trajectory: str
    deliverables: dict = field(default_factory=dict)
    usage: dict = field(default_factory=dict)
    error: str = ""

    def record(self) -> dict:
        return {"label": self.label, "run_dir": str(self.run_dir), "ok": self.ok, "delivered": self.delivered,
                "usage": self.usage, "error": self.error, "trajectory_chars": len(self.trajectory),
                "deliverables": sorted(self.deliverables)}


def run(config, model, workspace: Path, task: dict, tree: dict[str, str], label: str, run_dir: Path) -> Rollout:
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    harness_dir = harness.write_tree(tree, run_dir / "harness")
    if config.runner.kind == "command":
        rollout = _command(config, workspace, task, tree, harness_dir, label, run_dir)
    else:
        rollout = _loopback(config, model, workspace, task, tree, label, run_dir)
    (run_dir / "trajectory.md").write_text(rollout.trajectory, encoding="utf-8")
    out = run_dir / "deliverables"
    out.mkdir(exist_ok=True)
    for name, text in rollout.deliverables.items():
        (out / Path(name).name).write_text(text, encoding="utf-8")
    return rollout


def _command(config, workspace, task, tree, harness_dir, label, run_dir) -> Rollout:
    request = run_dir / "request.json"
    result_path = run_dir / "result.json"
    request.write_text(json.dumps({"task": task, "harness_dir": str(harness_dir), "output_dir": str(run_dir),
                                   "always_on": harness.render_always_on(tree), "label": label},
                                  ensure_ascii=False, indent=1), encoding="utf-8")
    env = {**os.environ, "NANORSI_REQUEST": str(request), "NANORSI_RESULT": str(result_path)}
    try:
        proc = subprocess.run(config.runner.command, cwd=str(workspace), env=env, capture_output=True,
                              text=True, timeout=config.runner.timeout_s)
        (run_dir / "runner.log").write_text(proc.stdout[-20000:] + "\n--stderr--\n" + proc.stderr[-20000:], encoding="utf-8")
        if not result_path.is_file():
            return Rollout(label, run_dir, False, False, "", error=f"runner exit {proc.returncode} without result.json")
        data = json.loads(result_path.read_text(encoding="utf-8"))
    except subprocess.TimeoutExpired:
        return Rollout(label, run_dir, False, False, "", error="runner timed out")
    except (OSError, ValueError) as error:
        return Rollout(label, run_dir, False, False, "", error=f"runner protocol error: {error}")
    deliverables = data.get("deliverables") or {}
    return Rollout(label, run_dir, bool(data.get("ok")), bool(data.get("delivered")) and bool(deliverables),
                   str(data.get("trajectory") or ""), {str(k): str(v) for k, v in deliverables.items()},
                   data.get("usage") or {}, str(data.get("error") or ""))


TOOLS = """You act through one JSON action per turn. The first line of every reply MUST be exactly one JSON object:
{"action": "list_documents"} | {"action": "read_document", "name": "<file>"} | {"action": "write_deliverable", "filename": "<expected name>"} | {"action": "done"}
For write_deliverable only, put the COMPLETE document as markdown in ONE fenced block after the JSON line. Never put the document inside the JSON."""


def _loopback(config, model, workspace, task, tree, label, run_dir, max_turns: int = 16) -> Rollout:
    system = harness.render_always_on(tree) + "\n\n---\n\n" + TOOLS + \
        "\n\n# EXPECTED DELIVERABLES\n" + ", ".join(f"`{d}`" for d in task["deliverables"])
    messages = [{"role": "system", "content": system}, {"role": "user", "content": task["instruction"]}]
    trajectory, deliverables = [], {}
    usage = {"calls": 0, "input_tokens": 0, "output_tokens": 0}
    for turn in range(1, max_turns + 1):
        text, spent = model.call(messages)
        for key in usage:
            usage[key] += spent.get(key, 0)
        try:
            head, bodies = parse_reply(text)
        except ModelError as error:
            trajectory.append(f"[INVALID] {error}")
            messages += [{"role": "assistant", "content": text}, {"role": "user", "content": f"INVALID REPLY ({error}). One JSON action line first."}]
            continue
        observation = _observe(head, bodies, task, workspace, deliverables)
        trajectory.append(f"[ACTION] {json.dumps(head, ensure_ascii=False)[:200]}")
        if observation is None:
            break
        trajectory.append(f"[OBSERVATION] {observation[:300]}")
        messages += [{"role": "assistant", "content": text}, {"role": "user", "content": observation}]
    missing = [d for d in task["deliverables"] if d not in deliverables]
    return Rollout(label, run_dir, not missing, bool(deliverables), "\n".join(trajectory), deliverables, usage,
                   f"missing deliverables: {missing}" if missing else "")


def _observe(head, bodies, task, workspace, deliverables):
    action = head.get("action")
    if action == "list_documents":
        return "DOCUMENTS\n" + "\n".join(sorted(task["documents"])) if task["documents"] else "DOCUMENTS\n(none)"
    if action == "read_document":
        name = str(head.get("name", ""))
        if name not in task["documents"]:
            return f"ERROR: unknown document {name!r}"
        try:
            return (Path(workspace) / task["documents"][name]).read_text(encoding="utf-8", errors="replace")[:24000] or "(empty)"
        except OSError as error:
            return f"ERROR: cannot read {name}: {error}"
    if action == "write_deliverable":
        name = str(head.get("filename", ""))
        if name not in task["deliverables"]:
            return f"ERROR: {name!r} is not an expected deliverable"
        if not bodies or not bodies[0].strip():
            return "ERROR: write_deliverable needs one fenced markdown body"
        deliverables[name] = bodies[0]
        return f"wrote {name}"
    if action == "done":
        return None
    return f"ERROR: unknown action {action!r}"
