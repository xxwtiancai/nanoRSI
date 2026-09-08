from __future__ import annotations

import math
import tomllib
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(ValueError):
    pass


SECTIONS = {
    "experiment", "surface", "proposer", "evaluator", "gate",
    "budget", "training", "safety",
    "agent", "data",
}


@dataclass(frozen=True)
class ExperimentConfig:
    id: str
    goal: str
    mode: str
    schema_version: int = 1
    seed: int = 0
    arm: str = "frozen"


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
    max_episodes: int = 400


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
    agent: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)


def _mapping(value, section: str) -> dict:
    if not isinstance(value, dict):
        raise ConfigError(f"[{section}] must be a table")
    return value


def _command(value, section: str, default_timeout: int = 60) -> CommandConfig:
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x for x in value):
        raise ConfigError(f"{section}.command must be a non-empty argv array")
    return CommandConfig([*value], default_timeout)


def _integer(value, name: str, minimum: int = 1) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ConfigError(f"{name} must be an integer >= {minimum}")
    return value


def _number(value, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ConfigError(f"{name} must be finite and non-negative")
    return float(value)


def _v2(raw: dict, experiment: dict) -> tuple[dict, dict]:
    agent = dict(_mapping(raw.get("agent", {}), "agent"))
    data = _mapping(raw.get("data", {}), "data")
    if experiment.get("schema_version", 1) == 1:
        return agent, data
    from .paths import normalize_relative_path
    if experiment.get("mode") != "harness":
        raise ConfigError("schema_version 2 requires harness mode")
    if experiment.get("arm", "frozen") not in {"frozen", "self-use"}:
        raise ConfigError("experiment.arm must be frozen or self-use")
    _command(agent.get("model_command"), "agent.model_command")
    if not isinstance(agent.get("model"), str) or not agent["model"]:
        raise ConfigError("agent.model must be configured")
    for key, default in [("max_turns", 8), ("max_tokens", 2048), ("timeout_s", 60)]:
        agent[key] = _integer(agent.get(key, default), f"agent.{key}")
    if agent["max_turns"] > 8:
        raise ConfigError("reference agent.max_turns must be <= 8")
    skills = agent.get("skills", [])
    if not isinstance(skills, list) or any(not isinstance(s, str) or not s or "/" in s or "\\" in s or s in {".", ".."} for s in skills):
        raise ConfigError("agent.skills must be an array of simple names")
    if len(set(skills)) != len(skills):
        raise ConfigError("agent.skills contains duplicates")
    if agent.get("api_key_file") and not Path(agent["api_key_file"]).is_absolute():
        raise ConfigError("agent.api_key_file must be an absolute external path")
    if raw.get("evaluator", {}).get("heldout_enabled", False):
        raise ConfigError("schema 2 uses validation and frozen final-test, not legacy heldout")
    try:
        normalize_relative_path(data.get("manifest", ""))
    except (ValueError, TypeError) as error:
        raise ConfigError("data.manifest must be a contained relative path") from error
    return agent, data


def _read(path: Path) -> dict:
    try:
        raw = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ConfigError(f"cannot read config: {error}") from error
    unknown = sorted(set(raw) - SECTIONS)
    if unknown:
        raise ConfigError(f"Unknown config sections: {', '.join(unknown)}")
    return raw


def load_config(path: Path) -> Config:
    raw = _read(path)
    experiment = _mapping(raw.get("experiment", {}), "experiment")
    surface = _mapping(raw.get("surface", {}), "surface")
    proposer = _mapping(raw.get("proposer", {}), "proposer")
    evaluator = _mapping(raw.get("evaluator", {}), "evaluator")
    gate = _mapping(raw.get("gate", {}), "gate")
    budget = _mapping(raw.get("budget", {}), "budget")
    version = experiment.get("schema_version", 1)
    if type(version) is not int or version not in {1, 2}:
        raise ConfigError("experiment.schema_version must be 1 or 2")
    agent, data = _v2(raw, experiment)
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
    return _build(path, experiment, surface, proposer, evaluator, gate, budget, training, raw, agent, data)


def _build(path, experiment, surface, proposer, evaluator, gate, budget, training, raw, agent, data):
    mode = experiment["mode"]
    allow = surface["allow"]
    return Config(
        ExperimentConfig(str(experiment.get("id", path.parent.name)), str(experiment.get("goal", "")), mode,
                         experiment.get("schema_version", 1), _integer(experiment.get("seed", 0), "seed", 0), experiment.get("arm", "frozen")),
        SurfaceConfig([str(x) for x in allow], [str(x) for x in surface.get("deny", [])]),
        _command(proposer.get("command"), "proposer", _integer(proposer.get("timeout_s", 60), "proposer.timeout_s")),
        EvaluatorConfig(
            _command(evaluator.get("command"), "evaluator", int(evaluator.get("timeout_s", 60))).command,
            _integer(evaluator.get("timeout_s", 60), "evaluator.timeout_s"),
            str(evaluator.get("primary_metric", "score")),
            evaluator.get("direction", "maximize"),
            bool(evaluator.get("heldout_enabled", False)),
        ),
        GateConfig(
            _number(gate.get("minimum_improvement", 0.0), "gate.minimum_improvement"),
            [str(x) for x in gate.get("required_constraints", [])],
            _number(gate.get("max_heldout_regression", 0.0), "gate.max_heldout_regression"),
        ),
        BudgetConfig(_integer(budget.get("max_steps", 1), "budget.max_steps"),
                     _integer(budget.get("max_output_bytes", 1_000_000), "budget.max_output_bytes"),
                     _integer(budget.get("max_episodes", 400), "budget.max_episodes")),
        training,
        _mapping(raw.get("safety", {}), "safety"),
        agent, data,
    )
