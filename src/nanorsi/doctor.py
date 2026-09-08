from __future__ import annotations

import shutil
from pathlib import Path

from .config import Config, load_config
from .gitops import Git


def _command_status(root: Path, command: list[str]) -> str:
    if not command:
        return "missing"
    first = command[0]
    if "/" in first:
        return "ok" if (root / first).exists() else "missing"
    return "ok" if shutil.which(first) else "missing"


def doctor(root: Path) -> tuple[bool, str]:
    try:
        config = load_config(root / "nanorsi.toml")
    except Exception as error:
        return False, f"config: invalid ({error})\n"
    lines = [
        f"config: ok ({config.experiment.mode})",
        f"git: {'ok' if _git_ok(root) else 'missing'}",
        f"proposer command: {' '.join(config.proposer.command)} ({_command_status(root, config.proposer.command)})",
        f"evaluator command: {' '.join(config.evaluator.command)} ({_command_status(root, config.evaluator.command)})",
        f"execution: local subprocess; sandbox is caller responsibility",
    ]
    if config.experiment.mode == "model":
        lines.extend(
            [
                "model: external training contract",
                f"training command: {' '.join(config.training['command'])}",
                f"compute budget: {config.training.get('compute_budget_s', 'unbounded')} seconds",
            ]
        )
    ready = _git_ok(root) and all(_command_status(root, command) == "ok" for command in [config.proposer.command, config.evaluator.command])
    if config.experiment.schema_version == 2:
        from .loop import tasks
        try:
            rows = tasks(root, config)
            lines.append(f"task manifest: ok ({len(rows)} tasks; disjoint source groups)")
        except (OSError, ValueError, KeyError) as error:
            lines.append(f"task manifest: invalid ({error})")
            ready = False
        model_ready = config.agent["model"] != "configure-your-model"
        lines.extend([f"model: {config.agent['model']} ({'configured' if model_ready else 'configure agent.model first'})",
                      f"proposer harness: {config.experiment.arm}",
                      "budget: attempts/episodes/time/output bounded; dollar usage reported, not a hard cap"])
        ready = ready and model_ready and _command_status(root, config.agent["model_command"]) == "ok"
    return ready, "\n".join(lines) + "\n"


def _git_ok(root: Path) -> bool:
    try:
        Git(root).ensure_repository()
        return True
    except Exception:
        return False
