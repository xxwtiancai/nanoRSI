"""Counterfactual challenger: the acceptance gate's second stage (ADOPTION item 28).

Generating validity-preserving variants is task-domain knowledge and stays with
the workspace: the evaluator exposes a ``counterfactual`` split alongside its
normal panels. This module owns the core-side adjudication. A candidate that
clears the primary strict-improvement gate is re-scored together with its
parent on the counterfactual panel under matched fresh measurement; a gain that
vanishes there is labelled ``shortcut`` and routed to the rejected-edit memory
instead of admission. Counterfactual evaluations are ordinary budgeted search
episodes, so the cost of the challenge is accounted like any other evaluation.
"""
from __future__ import annotations

from .gate import GateDecision, decide


def primary_decision(config, parent, measured_parent, gate, heldout):
    """First gate stage, factored out so only passing candidates pay for the challenge."""
    return decide(config.gate, parent=measured_parent.metrics if measured_parent else parent['gate_metrics'],
                  child={**gate.metrics, 'constraints': gate.constraints},
                  parent_heldout=parent.get('heldout_metrics'), child_heldout=heldout.metrics if heldout else None,
                  metric=config.evaluator.primary_metric, direction=config.evaluator.direction)


def pair_if_accepted(root, config, git, store, parent, checkout, run_dir, measured_parent, gate, heldout):
    """Evaluate parent and candidate counterfactual panels for gate-passing candidates only."""
    if not config.evaluator.counterfactual_enabled:
        return None
    if primary_decision(config, parent, measured_parent, gate, heldout).decision != 'accepted':
        return None
    from . import loop
    with git.worktree(parent['candidate_commit'], root / '.nanorsi/worktrees' / (run_dir.name + '-cf-parent')) as old:
        cf_parent = loop.evaluate(root, config, old, 'counterfactual', run_dir / 'cf-parent.json', store)
    cf_child = loop.evaluate(root, config, checkout, 'counterfactual', run_dir / 'cf-child.json', store)
    return cf_parent, cf_child


def adjudicate(config, parent, measured_parent, gate, heldout, pair):
    """Admit only gains that survive validity-preserving variants; relabel the rest shortcut."""
    primary = primary_decision(config, parent, measured_parent, gate, heldout)
    if pair is None:
        return primary
    cf_parent, cf_child = pair
    challenged = decide(config.gate, parent=cf_parent.metrics,
                        child={**cf_child.metrics, 'constraints': cf_child.constraints},
                        parent_heldout=None, child_heldout=None,
                        metric=config.evaluator.primary_metric, direction=config.evaluator.direction)
    if challenged.decision == 'accepted':
        return primary
    return GateDecision('shortcut', f'counterfactual gain vanished: {challenged.reason}', challenged.delta)
