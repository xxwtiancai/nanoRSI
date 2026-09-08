from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GateConfig:
    minimum_improvement: float = 0.0
    required_constraints: list[str] | None = None
    max_heldout_regression: float = 0.0


@dataclass(frozen=True)
class GateDecision:
    decision: str
    reason: str
    delta: float


def _metric(values: dict, metric: str) -> float:
    return float(values[metric])


def _better(direction: str, child: float, parent: float) -> bool:
    return child > parent if direction == "maximize" else child < parent


def decide(
    config: GateConfig,
    *,
    parent: dict,
    child: dict,
    parent_heldout: dict | None,
    child_heldout: dict | None,
    metric: str = "score",
    direction: str = "maximize",
) -> GateDecision:
    child_constraints = child.get("constraints", child)
    parent_score = _metric(parent, metric)
    child_score = _metric(child, metric)
    delta = child_score - parent_score
    improvement = delta if direction == "maximize" else -delta
    missing = [name for name in config.required_constraints or [] if not child_constraints.get(name)]
    if missing:
        return GateDecision("inconclusive", "failed constraints: " + ", ".join(missing), delta)
    if improvement <= 0 or improvement < config.minimum_improvement:
        return GateDecision("rejected", f"improvement below minimum: {improvement:.6f}", delta)
    if parent_heldout is not None and child_heldout is not None:
        old = _metric(parent_heldout, metric)
        new = _metric(child_heldout, metric)
        regression = old - new if direction == "maximize" else new - old
        if regression > config.max_heldout_regression:
            return GateDecision("rejected", f"heldout regression {regression:.6f}", delta)
    return GateDecision("accepted", f"improvement {improvement:.6f}", delta)
