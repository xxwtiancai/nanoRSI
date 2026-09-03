# nanoRSI Charter

nanoRSI is a nano-scale, evidence-gated kernel for Recursive Self-Improvement (RSI)
experiments. It is intentionally not an agent platform, model-training framework,
benchmark service, or distributed evolution system.

## Scope

nanoRSI v0.1 implements one complete, auditable improvement generation:

```text
goal intake
  -> target surface
  -> baseline snapshot and evaluation
  -> one external proposal
  -> patch validation
  -> child snapshot
  -> canonical evaluation
  -> accept/reject/inconclusive gate
  -> append-only lineage
  -> rollback/report/verify
```

The core uses one authoritative parent, one child candidate at a time, one external
proposer command, one canonical evaluator command, and single-parent hill climbing.

## Non-goals

- populations, islands, MAP-Elites, or multi-parent archives;
- distributed evaluation;
- plugin systems or dynamic operator registries;
- hosted services, dashboards, or marketplaces;
- vendor-specific model adapters in core;
- model-weight training in core;
- concurrent candidates in one experiment;
- indefinite background evolution.

## Foundation rules

1. Candidate code never mutates the evaluator, configuration, or lineage.
2. Evaluation runs against an exact Git tree.
3. Scores enter lineage only through the nanoRSI mechanism.
4. A rejected or inconclusive candidate never becomes the parent.
5. Model-layer training is always an explicitly configured external command.
6. The core remains small, standard-library-only, and test-enforced.
