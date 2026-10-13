# ALFWorld flash replication: a gate-accepted skill improvement that transfers (2026-10-12)

> **2026-10-14 replication update — read this first.** A fresh rerun with 3 final-test
> repeats [did not replicate](../alfworld-flash-replication/README.md): the new search
> accepted nothing, and identical-skill conditions differed by one game (0.083 mean)
> across 3-repeat draws — the same magnitude as this study's two-game margin. Treat the
> result below as a single noisy draw, exactly as the selector-study protocol now
> prescribes; the platform-level findings (gated lifecycle on engine-scored tasks,
> harm-blocking, measured noise) stand.

Direct follow-up to the [GLM-5.3 ceiling null](../alfworld-phase2/README.md). Same platform,
same frozen test games (**identical 6 seen + 6 unseen panels** — test selection depends only
on `--test-per-split`), one deliberate change each: a **flash-tier agent** (more headroom than
the saturated GLM-5.3) and a **larger split** (`prepare.py --train 8 --validation 8`).

## Result: four proposals, one accepted, and it transfers

| Stage | Validation (8 games) |
| --- | --- |
| Baseline (initial skill) | 0.875 |
| Attempts 1 / 3 | 0.875 — ties, rejected |
| Attempt 2 | 0.625 — harmful, rejected |
| **Attempt 4** | **1.000 (+0.125) — accepted** |

Frozen final panel (12 games, 6 seen + 6 unseen):

| Condition | Score | Seen | Unseen |
| --- | ---: | ---: | ---: |
| Baseline (initial v0 skill) | 0.833 | 4/6 | 6/6 |
| No skills | 0.917 | 5/6 | 6/6 |
| **Candidate (evolved skill)** | **1.000** | **6/6** | **6/6** |

The evolved skill beat the initial-skill condition by two games and the bare agent by one,
and its episodes also finished cheaper (115 model calls vs 152/147 in the final panel).

## What the gate actually accepted

The accepted diff ([attempt4-proposal.diff](attempt4-proposal.diff),
[evolved-skill.md](evolved-skill.md)) was distilled from the one failed training episode —
a game lost by opening cabinet after cabinet until the step budget ran out:

- **mechanics**: closed receptacles hide contents; `go to` + `open` before anything appears;
- **location priors**: countertops, sink, table, fridge first; cabinets last;
- **step budgeting**: reserve the last two actions for delivery; change strategy after
  half the budget is spent searching;
- **no revisits** and **goal-type pipelines** (pick/place, heat/cool/clean, look-in-light).

This is the experience-to-guidance loop the literature (ExpeL, SkillWeaver) describes,
executed inside nanoRSI's frozen contract: one failed episode → proposed guidance →
strict-improvement gate on held-out validation → frozen unseen-panel transfer.

## Honest boundaries

- One seed, one repeat; the candidate-vs-no-skills gap (one game) sits inside the measured
  ±1-game panel noise band — the two-game gain over the initial skill and the +0.125 gated
  validation gain are the evidence; no general claim that evolved skills beat a bare agent.
- The initial v0 skill was itself mildly harmful versus no-skills (0.833 vs 0.917): its
  "explore one receptacle at a time" advice encourages exactly the exhaustive search that
  wastes the 24-step budget. Evolution recovered and exceeded the bare agent.
- Attempt 2 shows the gate blocking a harmful edit (−0.25) — the failure record is retained
  in full ([gate-summary.json](gate-summary.json), [evidence.md](evidence.md)).
- Cross-study comparison with the GLM-5.3 null is observational (different agent tier, same
  test games): headroom, not agent weakness alone, is what made the gain measurable.

Files: [summary.json](summary.json) · [final.json](final.json) · [audit.json](audit.json) ·
proposals [1](attempt1-proposal.diff) [2](attempt2-proposal.diff) [3](attempt3-proposal.diff)
[4](attempt4-proposal.diff) · [initial](initial-skill.md) vs [evolved](evolved-skill.md) skill.
