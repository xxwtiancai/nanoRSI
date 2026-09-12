from __future__ import annotations

import math
import tomllib
from urllib.parse import urlsplit
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(ValueError):
    pass


def validate_endpoint(value: str) -> str:
    try:
        if not isinstance(value, str) or any(c.isspace() or ord(c) < 32 or 127 <= ord(c) <= 159 for c in value) or '?' in value or '#' in value:
            raise ValueError
        parsed = urlsplit(value)
        if parsed.scheme not in {'http', 'https'} or not parsed.hostname or parsed.username is not None or parsed.password is not None or parsed.netloc.endswith(':'):
            raise ValueError
        if parsed.port is not None and not 1 <= parsed.port <= 65535:
            raise ValueError
    except ValueError as error:
        raise ConfigError('agent.base_url must be an HTTP(S) URL without credentials, query or fragment') from error
    return value.rstrip('/')


def credential_path(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or not Path(value).is_absolute():
        raise ConfigError('agent.api_key_file must be an absolute external path')
    path = Path(value).resolve()
    if path.is_relative_to(root.resolve()):
        raise ConfigError('agent.api_key_file must be outside the experiment workspace')
    return path


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
    final_conditions: list[str] = field(default_factory=lambda: ["baseline", "candidate"])


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
    train_limit: int = 4


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
    if experiment.get("arm", "frozen") not in {"frozen", "self-use"}:
        raise ConfigError("experiment.arm must be frozen or self-use")
    if agent or experiment.get("mode") == "harness":
        _validate_agent(agent)
    if raw.get("evaluator", {}).get("heldout_enabled", False):
        raise ConfigError("schema 2 uses validation and frozen final-test, not legacy heldout")
    try:
        normalize_relative_path(data.get("manifest", ""))
    except (ValueError, TypeError) as error:
        raise ConfigError("data.manifest must be a contained relative path") from error
    return agent, data


def _validate_agent(agent):
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
    if any(key in agent for key in ['api_key', 'apikey', 'authorization']):
        raise ConfigError('inline credentials are not supported; use agent.api_key_file')
    if 'base_url' in agent:
        validate_endpoint(agent['base_url'])
    if agent.get('token_parameter', 'max_tokens') not in {'max_tokens', 'max_completion_tokens'}:
        raise ConfigError('agent.token_parameter must be max_tokens or max_completion_tokens')
    if agent.get('thinking', 'enabled') not in {'enabled', 'disabled'}:
        raise ConfigError('agent.thinking must be enabled or disabled')


def _final_conditions(experiment):
    default = ["baseline", "no-skills", "candidate"] if experiment.get("mode") == "harness" else ["baseline", "candidate"]
    value = experiment.get("final_conditions", default)
    if (not isinstance(value, list) or any(not isinstance(x, str) for x in value)
            or len(value) != len(set(value)) or not {"baseline", "candidate"} <= set(value)
            or not set(value) <= {"baseline", "no-skills", "candidate"}):
        raise ConfigError("experiment.final_conditions must be a unique subset of baseline/no-skills/candidate containing baseline and candidate")
    return list(value)


def _fixed_training_command(root, command, surface):
    from .contracts import training_entrypoints
    from .surface import check_paths
    root = root.resolve()
    try:
        sources = training_entrypoints(root, command)
    except (IndexError, ValueError) as error:
        raise ConfigError(f"invalid training.command wrapper: {error}") from error
    for path in sources:
        for source in [path, path.resolve()]:
            if source.is_relative_to(root) and not check_paths([source.relative_to(root).as_posix()], surface["allow"], surface.get("deny", [])):
                raise ConfigError("training.command references a mutable local trainer; place it under protected trainer/")


def _training(raw, mode, version, surface, root):
    value = raw.get("training")
    if mode == "model" and (not isinstance(value, dict) or not value.get("command")):
        raise ConfigError("model mode requires training.command to be configured")
    if value is None or version == 1:
        return value
    from .paths import normalize_relative_path
    from .surface import SurfacePolicy
    value = dict(_mapping(value, "training"))
    value["command"] = _command(value.get("command"), "training").command
    _fixed_training_command(root, value["command"], surface)
    value["compute_budget_s"] = _number(value.get("compute_budget_s", 60), "training.compute_budget_s")
    if value["compute_budget_s"] <= 0:
        raise ConfigError("training.compute_budget_s must be positive")
    value["max_checkpoint_bytes"] = _integer(value.get("max_checkpoint_bytes", 10_000_000), "training.max_checkpoint_bytes")
    try:
        value["checkpoint"] = normalize_relative_path(value.get("checkpoint", "target/model.json"))
        SurfacePolicy(surface["allow"], surface.get("deny", [])).validate_paths([value["checkpoint"]])
    except (ValueError, TypeError) as error:
        raise ConfigError(f"training.checkpoint must be a mutable contained file: {error}") from error
    return value


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
    if 'api_key_file' in agent:
        credential_path(path.parent, agent['api_key_file'])
    mode = experiment.get("mode", "")
    if mode not in {"artifact", "harness", "model"}:
        raise ConfigError("experiment.mode must be artifact, harness, or model")
    allow = surface.get("allow", [])
    if not isinstance(allow, list) or not allow:
        raise ConfigError("surface.allow must be a non-empty path-pattern array")
    direction = evaluator.get("direction", "maximize")
    if direction not in {"maximize", "minimize"}:
        raise ConfigError("evaluator.direction must be maximize or minimize")
    training = _training(raw, mode, version, surface, path.parent)
    return _build(path, experiment, surface, proposer, evaluator, gate, budget, training, raw, agent, data)


def _build(path, experiment, surface, proposer, evaluator, gate, budget, training, raw, agent, data):
    mode = experiment["mode"]
    allow = surface["allow"]
    return Config(
        ExperimentConfig(str(experiment.get("id", path.parent.name)), str(experiment.get("goal", "")), mode,
                         experiment.get("schema_version", 1), _integer(experiment.get("seed", 0), "seed", 0), experiment.get("arm", "frozen"), _final_conditions(experiment)),
        SurfaceConfig([str(x) for x in allow], [str(x) for x in surface.get("deny", [])]),
        _command(proposer.get("command"), "proposer", _integer(proposer.get("timeout_s", 60), "proposer.timeout_s")),
        EvaluatorConfig(
            _command(evaluator.get("command"), "evaluator", int(evaluator.get("timeout_s", 60))).command,
            _integer(evaluator.get("timeout_s", 60), "evaluator.timeout_s"),
            str(evaluator.get("primary_metric", "score")),
            evaluator.get("direction", "maximize"),
            bool(evaluator.get("heldout_enabled", False)),
            _integer(evaluator.get("train_limit", 4), "evaluator.train_limit"),
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
