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


MAX_SOURCE_FILE_BYTES = 64_000
MAX_SOURCE_TOTAL_BYTES = 192_000
MAX_SOURCE_FILES = 64
PRIVATE_COMPONENTS = frozenset({".git", ".nanorsi", "__pycache__", "evaluator", "proposer", "tasks", "adapters", "reports", "runs", "nanorsi.toml", "lineage.jsonl", ".env", "credentials", "secrets"})


def _patterns(surface: Any) -> list[str]:
    if isinstance(surface, str):
        return [surface]
    if isinstance(surface, list):
        return [item for item in surface if isinstance(item, str)]
    if isinstance(surface, dict):
        value = surface.get("allow", [])
        return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []
    return ["target/**"]


def _source_allowed(relative: str, context: dict[str, Any]) -> bool:
    path = Path(relative)
    if path.is_absolute() or "\\" in relative or "\x00" in relative or not path.parts or path.parts[0] != "target" or ".." in path.parts:
        return False
    if any(part.lower() in PRIVATE_COMPONENTS or part.lower().startswith(".env.") or part.lower().endswith((".pem", ".key")) for part in path.parts):
        return False
    surface = context.get("surface")
    deny = surface.get("deny", []) if isinstance(surface, dict) else []
    if isinstance(deny, list) and any(isinstance(pattern, str) and fnmatch.fnmatch(relative, pattern) for pattern in deny):
        return False
    return any(fnmatch.fnmatch(relative, pattern) for pattern in _patterns(surface))


def _bounded_source(files: dict[str, Any], context: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    total = 0
    for relative, source in sorted(files.items()):
        if not isinstance(relative, str) or not isinstance(source, str) or not _source_allowed(relative, context) or "\x00" in source:
            continue
        size = len(source.encode("utf-8"))
        if size > MAX_SOURCE_FILE_BYTES or total + size > MAX_SOURCE_TOTAL_BYTES or len(result) >= MAX_SOURCE_FILES:
            continue
        result[relative] = source
        total += size
    return result


def _gather_parent_files(context: dict[str, Any], *, root: Path | None = None) -> dict[str, str]:
    cwd = (Path.cwd() if root is None else root).resolve()
    files: dict[str, str] = {}
    target = cwd / "target"
    if not target.is_dir() or target.is_symlink():
        return files
    for path in sorted(target.rglob("*")):
        if any(parent.is_symlink() for parent in (path, *path.parents)) or not path.is_file():
            continue
        relative = path.relative_to(cwd).as_posix()
        if not _source_allowed(relative, context):
            continue
        try:
            if path.stat().st_size <= MAX_SOURCE_FILE_BYTES:
                files[relative] = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            continue
    return _bounded_source(files, context)


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
    if "extra_parents" in context:
        parents = context["extra_parents"]
        if not isinstance(parents, list) or len(parents) > 8:
            raise ValueError("extra_parents must be a list of at most 8 parents")
        proposal_context["extra_parents"] = []
        for parent in parents:
            if not isinstance(parent, dict) or not isinstance(parent.get("candidate_id"), str):
                raise ValueError("extra parent requires candidate_id")
            selected = {key: parent[key] for key in ("candidate_id", "candidate_commit") if key in parent}
            for key in ("parent_files", "source"):
                if key in parent:
                    if not isinstance(parent[key], dict):
                        raise ValueError("extra parent source must be an object")
                    selected[key] = _bounded_source(parent[key], context)
            proposal_context["extra_parents"].append(selected)
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
