# Selector-study protocol (ADOPTION items 38/39/45 acceptance bar)

**Status: design document.** This file defines the matched study any selector-style
mechanism must pass before it can ship as anything but an opt-in arm — the RRSI-style
regularized selection (item 38), the judge-ranked pre-gate (item 39) and
failure-composition routing (item 45). It is a protocol, not a result: nothing here
claims a measured benefit, and no selector becomes default without a study that follows it.

## Why this protocol exists (measured, not assumed)

Three live studies measured how large evaluation noise is relative to single-edit effects
on this platform:

- ALFWorld (GLM-5.3): two same-config baseline runs differed by one game (±0.17 on 6 games);
  every final condition saturated 12/12.
- ALFWorld (flash): the gate's fresh parent re-measurement moved 0.875 → 1.000 between
  runs; identical-skill final draws differed by one game.
- HumanEval (flash): the parent re-measured 0.88 → 1.00 on a 25-problem panel; with
  3 final repeats, identical-skill conditions differed by 0.019 mean (≈ one problem per
  repeat).

Any acceptance claim smaller than these bands is unfalsifiable at these panel sizes. The
noise-band tooling (`reports/noise-band.json`, `[gate] noise_band`) landed 2026-10-13
(commit 67a1cc5) exists precisely to measure the band before interpreting a delta.

## Preconditions (all studies)

1. **Noise band first.** Run `nanorsi report` after baseline and read
   `reports/noise-band.json` (parent-remeasure spread + final-repeat flip rates). A
   claimed effect must exceed the measured band, or the panel must be enlarged until it does.
2. **Headroom check.** Measure the no-skills condition on the validation split before
   searching. If the base agent is within the noise band of the ceiling (as in the two
   ceiling studies above), the study is redesigned — harder tasks, larger splits, or a
   weaker agent — not re-run until a lucky draw.
3. **Frozen contract as usual.** Evaluator/proposer/adapters/tasks frozen at baseline;
   freeze-then-final-test; `verify` passing; audits clean.

## Matched design

- **Arms:** strict-improvement gate (control) vs the selector arm under test, plus the
  no-skills condition as the primary behavioral comparison. Optional: a sham control
  (item 34) when the selector consumes guidance-like artifacts.
- **Grid:** ≥ 3 seeds × ≥ 3 budget points. Budgets match **total evaluation cost**
  (episodes + model calls + tokens), not attempt counts — a selector that spends budget
  judging must show what that budget would have earned as full evaluations.
- **Panels:** frozen splits with ≥ 30 test tasks per final panel and **≥ 3 final-test
  repeats**; per-repeat scores are reported individually, never only their mean.
- **Selector-specific accounting:** judge/pre-rank calls and tokens (item 39), routing
  labels and per-class rerouting counts (item 45), band re-estimation cost (item 38).

## Required reported fields

evolve-set gain; held-out transfer (seen/unseen or equivalent split); tokens and model
calls per arm; accepted/rejected edit counts with reasons; **false-blocks** (candidates
the selector blocked that the control gate accepted — requires offline double-scoring of
blocked candidates) and **false-admits**; the measured noise band and the threshold used;
all seeds, failures and no-ops retained in the evidence ledger.

## Honesty rules

No selector ships as a default or is claimed beneficial before a study following this
protocol; author-reported numbers from the source papers are never described as local
results; a null or negative outcome is published with the same completeness as a positive
one (the three ceiling/null studies above are the standing examples); auto-calibrating
the gate from evaluation evidence remains rejected until a study says otherwise.

## What is already available

Task packs: BBH (program track), ALFWorld (agent track; split sizes parameterized,
frozen test panels comparable across studies), HumanEval (coding track; 3-repeat final
testing demonstrated). Tooling: noise-band report, evidence ledger with gate summary,
audit, counterfactual challenger, multi-seed orchestration, and the read-only offline
double-scoring harness at `examples/double_scoring/run.py`. The harness recomputes
control decisions from recorded metrics and can re-evaluate archived pre-evaluation-
blocked diffs in isolated worktrees; it does not select, promote or mutate the source
study. Before any selector arm changes behavior, the first study must still freeze the
exact three-seed × three-budget plan, matched total evaluation budgets, repeated-frozen
parent rescoring, held-out panel and failure accounting.
