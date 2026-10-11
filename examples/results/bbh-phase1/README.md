# BBH phase 1: program evolution on public benchmark tasks (2026-10-11)

First effect-evidence study on a **public benchmark** rather than self-authored panels
([ADOPTION item 37](../../../docs/research/industry-rsi/ADOPTION.md), phase 1). Two
[BIG-Bench-Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) tasks (MIT, data vendored
verbatim — [NOTICE](../../bbh_tasks/NOTICE)) were ported as program-evolution targets by the
deterministic pack generator [`examples/bbh_tasks/prepare.py`](../../bbh_tasks/prepare.py):
250 examples each, deterministic 50 train / 50 validation / 150 test split, one task per
example, exact-match grading by the **stock program evaluator** (no custom scoring code).
The initial solvers are authored weak classical heuristics (BBH ships data, not programs):
dyck closes brackets in a fixed type order ignoring nesting; bool evaluates left to right
ignoring precedence.

**Headline (frozen final panels, 150 unseen examples each):**

| Task | Initial solver (validation / test) | Evolved candidate (test) | Accepted change |
| --- | ---: | ---: | --- |
| `dyck_languages` | 0.78 / 0.6933 | **1.0000** | closes in nesting order via `reversed(stack)` — a textbook stack match |
| `boolean_expressions` | 0.90 / 0.7333 | **0.9800** | recursive-descent parser with not/and/or precedence |

Ten proposer calls total (8,276 input / 19,734 output tokens, GLM-5.3-Flash, seed 0,
frozen arm, five attempts per task); two `doctor` probes excluded per convention.

## The runs, honestly

- **dyck** accepted on attempt 1 (+0.22 validation → 1.00); attempts 2–5 were provider
  failures (3× `model_timeout`, 1× `model_invalid_response`) retained in the evidence
  ledger. With validation already at 1.00, the strict-improvement gate would have
  rejected any further change anyway.
- **bool** failed twice on provider errors, then accepted attempt 3 (+0.02 → 0.92); a
  tie proposal was rejected (gate minimum), and attempt 5 proposed no file change. The
  frozen test panel rewards precedence more than validation does (longer expressions
  sort later): **0.7333 → 0.98**.
- **The bool candidate is not the oracle.** The remaining 3/150 misses share one
  diagnosed pattern: the evolved parser combines sub-parses with Python short-circuit
  `or`/`and`, so a truthy left side skips calling the continuation parser and leaves
  tokens unconsumed (verified leftover `['False', ')', 'or', 'True']` on
  `not ( True or False ) or True`). An eager precedence parser reaches 1.0 on all 250
  examples — asserted in [`tests/test_bbh_tasks.py`](../../../tests/test_bbh_tasks.py).
  The gate accepted on the +0.02 validation gain it could see; the residual bug is part
  of the honest record, not a hidden failure.
- Audits: zero expected-answer leakage, zero silent bypass; `verify: lineage ok` in both
  workspaces. Short answers ("True", "] ]") sit below the 8-character leakage threshold,
  so the pack-level screen is the generator + hardcoding test plus the known
  workspace trust boundary (documented in the pack README).

## Limits

Single runs, single seed, one flash-tier model, one accepted generation per task. Gains
are measured over the authored weak initial solvers, not over BBH leaderboard systems;
upstream author-reported BBH numbers are **not** reproduced — these are independent
nanoRSI runs of public benchmark tasks. Validation granularity is 0.02 (50 examples).
The generalization claim is narrow: the evolved programs transfer from a 100-example
train+validation prefix to the 150-example test split of the same task family.

Files: [summary.json](summary.json) · [dyck/](dyck) · [bool/](bool) (initial and evolved
programs, final panels, audits, evidence ledgers).
