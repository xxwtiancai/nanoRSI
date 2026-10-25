"""Workspace configuration: one TOML file, validated once, frozen by the ledger."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class ModelConfig:
    model: str = "configure-your-model"
    base_url: str = ""
    api_key_file: str = ""
    max_tokens: int = 8192
    timeout_s: float = 600.0
    thinking: str = "disabled"


@dataclass(frozen=True)
class RunnerConfig:
    kind: str = "loopback"
    command: list[str] = field(default_factory=list)
    timeout_s: int = 3600


@dataclass(frozen=True)
class BudgetConfig:
    max_proposer_calls: int = 40
    max_rollouts: int = 40
    max_output_bytes: int = 2_000_000


@dataclass(frozen=True)
class Config:
    experiment_id: str
    goal: str
    mode: str  # agg | seq — the paper's parallel / sequential recursion
    k: int
    seed: int
    model: ModelConfig
    runner: RunnerConfig
    budget: BudgetConfig
    harness_root: str = "harness"
    tasks_manifest: str = "tasks/manifest.json"
    judge_command: list[str] = field(default_factory=list)
    judge_model: str = ""


def _section(data: dict, name: str) -> dict:
    value = data.get(name, {})
    if not isinstance(value, dict):
        raise ConfigError(f"[{name}] must be a table")
    return value


def _command(section: dict, key: str) -> list[str]:
    value = section.get(key, [])
    if not isinstance(value, list) or any(not isinstance(part, str) for part in value):
        raise ConfigError(f"{key} must be an array of strings")
    return list(value)


def load_config(path: Path) -> Config:
    try:
        data = tomllib.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"cannot read {path}: {error}") from error
    exp = _section(data, "experiment")
    goal = str(exp.get("goal", "")).strip()
    mode = str(exp.get("mode", "agg"))
    if not goal:
        raise ConfigError("[experiment] goal is required")
    if mode not in {"agg", "seq"}:
        raise ConfigError("[experiment] mode must be agg or seq")
    k = int(exp.get("k", 1))
    if not 1 <= k <= 8:
        raise ConfigError("[experiment] k must be between 1 and 8")
    model = ModelConfig(
        model=str(_section(data, "model").get("model", "configure-your-model")),
        base_url=str(_section(data, "model").get("base_url", "")),
        api_key_file=str(_section(data, "model").get("api_key_file", "")),
        max_tokens=int(_section(data, "model").get("max_tokens", 8192)),
        timeout_s=float(_section(data, "model").get("timeout_s", 600)),
        thinking=str(_section(data, "model").get("thinking", "disabled")),
    )
    if model.thinking not in {"enabled", "disabled"}:
        raise ConfigError("[model] thinking must be enabled or disabled")
    runner = RunnerConfig(
        kind=str(_section(data, "runner").get("kind", "loopback")),
        command=_command(_section(data, "runner"), "command"),
        timeout_s=int(_section(data, "runner").get("timeout_s", 3600)),
    )
    if runner.kind not in {"loopback", "command"}:
        raise ConfigError("[runner] kind must be loopback or command")
    if runner.kind == "command" and not runner.command:
        raise ConfigError("[runner] command is required when kind is command")
    budget = BudgetConfig(
        max_proposer_calls=int(_section(data, "budget").get("max_proposer_calls", 40)),
        max_rollouts=int(_section(data, "budget").get("max_rollouts", 40)),
        max_output_bytes=int(_section(data, "budget").get("max_output_bytes", 2_000_000)),
    )
    if budget.max_proposer_calls < 1 or budget.max_rollouts < 1:
        raise ConfigError("[budget] limits must be positive")
    return Config(
        experiment_id=str(exp.get("id", Path(path).parent.name)),
        goal=goal, mode=mode, k=k, seed=int(exp.get("seed", 0)),
        model=model, runner=runner, budget=budget,
        harness_root=str(_section(data, "harness").get("root", "harness")),
        tasks_manifest=str(_section(data, "tasks").get("manifest", "tasks/manifest.json")),
        judge_command=_command(_section(data, "judge"), "command"),
        judge_model=str(_section(data, "judge").get("model", "")),
    )
