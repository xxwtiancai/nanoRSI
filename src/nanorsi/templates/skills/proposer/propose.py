"""Proposal driver using a selected skills runner and parent source context."""

from __future__ import annotations

import fnmatch
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any


def _patterns(surface: Any) -> list[str]:
    if isinstance(surface, str):
        return [surface]
    if isinstance(surface, list):
        return [item for item in surface if isinstance(item, str)]
    if isinstance(surface, dict):
        value = surface.get("allow", [])
        return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []
    return ["target/**"]


def _gather_parent_files(context: dict[str, Any]) -> dict[str, str]:
    cwd = Path.cwd()
    patterns = _patterns(context.get("surface"))
    files: dict[str, str] = {}
    target = cwd / "target" / "agent"
    if not target.is_dir():
        return files
    for path in sorted(target.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        relative = path.relative_to(cwd).as_posix()
        if not any(fnmatch.fnmatch(relative, pattern) or fnmatch.fnmatch(relative, pattern.rstrip("/") + "/*") for pattern in patterns):
            continue
        try:
            files[relative] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
    return files


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def propose() -> dict[str, Any]:
    started = time.monotonic()
    proposal_dir = Path(os.environ["NANORSI_PROPOSAL_DIR"])
    context_path = Path(os.environ["NANORSI_CONTEXT_PATH"])
    harness = Path(os.environ["NANORSI_PROPOSER_HARNESS"]).resolve()
    runner = harness / "target" / "agent" / "run.py"
    if not runner.is_file():
        candidate = harness / "run.py"
        if candidate.is_file():
            runner = candidate
        else:
            raise ValueError("proposer harness has no target/agent/run.py")
    context = json.loads(context_path.read_text(encoding="utf-8"))
    if not isinstance(context, dict):
        raise ValueError("proposal context must be an object")
    agent = context.get("agent", {})
    if not isinstance(agent, dict):
        raise ValueError("proposal context agent must be an object")
    proposal_context = dict(context)
    proposal_context["parent_files"] = _gather_parent_files(context)
    request = {"mode": "propose", "context": proposal_context, "agent": agent}
    timeout = agent.get("timeout_s", 60)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise ValueError("agent.timeout_s must be a finite positive number")
    try:
        timeout_value = float(timeout)
    except (TypeError, ValueError, OverflowError) as error:
        raise ValueError("agent.timeout_s must be a finite positive number") from error
    if not math.isfinite(timeout_value) or timeout_value <= 0:
        raise ValueError("agent.timeout_s must be a finite positive number")
    max_turns = agent.get("max_turns", 8)
    if isinstance(max_turns, bool) or not isinstance(max_turns, int) or not 1 <= max_turns <= 8:
        raise ValueError("agent.max_turns must be an integer between 1 and 8")
    bounded_timeout = timeout_value + 10.0
    if not math.isfinite(bounded_timeout):
        raise ValueError("agent.timeout_s exceeds the platform timeout range")
    proposal_dir.mkdir(parents=True, exist_ok=True)
    for stale_name in ("proposal.diff", "hypothesis.json"):
        stale = proposal_dir / stale_name
        if stale.exists() or stale.is_symlink():
            stale.unlink()
    try:
        completed = subprocess.run([sys.executable, str(runner)], cwd=Path.cwd(), input=json.dumps(request), capture_output=True, text=True, timeout=bounded_timeout, check=False)
        try:
            result = json.loads(completed.stdout)
        except json.JSONDecodeError:
            result = {"status": "error", "trace": [{"event": "runner_error", "code": "invalid_json"}], "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_invalid_json"]}}
        if not isinstance(result, dict):
            result = {"status": "error", "trace": [{"event": "runner_error", "code": "invalid_result"}], "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_invalid_result"]}}
        if completed.returncode != 0:
            result["status"] = "error"
            if not isinstance(result.get("trace"), list):
                result["trace"] = []
            result["trace"].append({"event": "runner_error", "code": "exit"})
            if not isinstance(result.get("usage"), dict):
                result["usage"] = {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_exit"]}
    except subprocess.TimeoutExpired:
        result = {"status": "error", "trace": [{"event": "runner_error", "code": "timeout"}], "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["runner_timeout"]}}
    except (OverflowError, OSError) as error:
        result = {"status": "error", "trace": [{"event": "runner_error", "code": "start_error"}], "usage": {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": [f"runner_start_error:{str(error)[:80]}"]}}
    if result.get("status") == "ok" and isinstance(result.get("diff"), str) and "hypothesis" in result:
        (proposal_dir / "proposal.diff").write_text(result["diff"], encoding="utf-8")
        _write_json(proposal_dir / "hypothesis.json", result["hypothesis"])
    _write_json(proposal_dir / "usage.json", result.get("usage", {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": ["missing_usage"]}))
    _write_json(proposal_dir / "trace.json", result.get("trace", []))
    result["duration_ms"] = max(0, int((time.monotonic() - started) * 1000))
    return result


def main() -> None:
    try:
        result = propose()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        proposal_dir = Path(os.environ.get("NANORSI_PROPOSAL_DIR", "."))
        proposal_dir.mkdir(parents=True, exist_ok=True)
        _write_json(proposal_dir / "usage.json", {"model_calls": 0, "input_tokens": None, "output_tokens": None, "cost_usd": None, "errors": [str(error)[:120]]})
        _write_json(proposal_dir / "trace.json", [{"event": "driver_error", "code": str(error)[:120]}])
        result = {"status": "error"}
    print(json.dumps({"status": result.get("status", "error"), "duration_ms": result.get("duration_ms", 0)}))


if __name__ == "__main__":
    main()
