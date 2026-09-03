from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path


class ConfigError(ValueError):
    pass


SECTIONS = {
    "experiment", "surface", "proposer", "evaluator", "gate",
    "budget", "training", "safety",
}


@dataclass(frozen=True)
class ExperimentConfig:
    id: str
    goal: str
    mode: str


@dataclass(frozen=True)
class SurfaceConfig:
    allow: list[str]
    deny: list[str]


@dataclass(frozen=True)
class CommandConfig:
    command: list[str]
    timeout_s: int


@dataclass(frozen=True)
class EvaluatorConfig:
    command: list[str]
    timeout_s: int
    primary_metric: str
    direction: str
    heldout_enabled: bool


@dataclass(frozen=True)
class GateConfig:
    minimum_improvement: float
    required_constraints: list[str]
    max_heldout_regression: float


@dataclass(frozen=True)
class BudgetConfig:
    max_steps: int
    max_output_bytes: int


@dataclass(frozen=True)
class Config:
    experiment: ExperimentConfig
    surface: SurfaceConfig
    proposer: CommandConfig
    evaluator: EvaluatorConfig
    gate: GateConfig
    budget: BudgetConfig
    training: dict | None
    safety: dict


def _mapping(value, section: str) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"[{section}] must be a table")
    return value


def _command(value, section: str, default_timeout: int = 60) -> CommandConfig:
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
        raise ConfigError(f"{section}.command must be a non-empty argv array")
    return CommandConfig([*value], default_timeout)


def load_config(path: Path) -> Config:
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"cannot read config: {error}") from error
    unknown = sorted(set(raw) - SECTIONS)
    if unknown:
        raise ConfigError(f"Unknown config sections: {', '.join(unknown)}")
    experiment = _mapping(raw.get("experiment", {}), "experiment")
    surface = _mapping(raw.get("surface", {}), "surface")
    proposer = _mapping(raw.get("proposer", {}), "proposer")
    evaluator = _mapping(raw.get("evaluator", {}), "evaluator")
    gate = _mapping(raw.get("gate", {}), "gate")
    budget = _mapping(raw.get("budget", {}), "budget")
    mode = experiment.get("mode", "")
    if mode not in {"artifact", "harness", "model"}:
        raise ConfigError("experiment.mode must be artifact, harness, or model")
    allow = surface.get("allow", [])
    if not isinstance(allow, list) or not allow:
        raise ConfigError("surface.allow must be a non-empty path-pattern array")
    direction = evaluator.get("direction", "maximize")
    if direction not in {"maximize", "minimize"}:
        raise ConfigError("evaluator.direction must be maximize or minimize")
    training = raw.get("training")
    if mode == "model" and (not isinstance(training, dict) or not training.get("command")):
        raise ConfigError("model mode requires training.command to be configured")
    return Config(
        ExperimentConfig(str(experiment.get("id", path.parent.name)), str(experiment.get("goal", "")), mode),
        SurfaceConfig([str(x) for x in allow], [str(x) for x in surface.get("deny", [])]),
        _command(proposer.get("command"), "proposer", int(proposer.get("timeout_s", 60))),
        EvaluatorConfig(
            _command(evaluator.get("command"), "evaluator", int(evaluator.get("timeout_s", 60))).command,
            int(evaluator.get("timeout_s", 60)),
            str(evaluator.get("primary_metric", "score")),
            direction,
            bool(evaluator.get("heldout_enabled", False)),
        ),
        GateConfig(
            float(gate.get("minimum_improvement", 0.0)),
            [str(x) for x in gate.get("required_constraints", [])],
            float(gate.get("max_heldout_regression", 0.0)),
        ),
        BudgetConfig(int(budget.get("max_steps", 1)), int(budget.get("max_output_bytes", 1_000_000))),
        training,
        _mapping(raw.get("safety", {}), "safety"),
    )
