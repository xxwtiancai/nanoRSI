# HumanEval coding study: a well-measured null at the ceiling (2026-10-13)

The most recognizable benchmark in code generation, run on the **stock coding template**
([pack](../../humaneval_tasks/README.md): 161 usable MIT problems, deterministic 20/25/36
split, reference solutions never enter the workspace), under the **revised study standard**:
36-problem frozen panel, **3 final-test repeats**, no-skills as the primary comparison.
GLM-5.3-Flash, seed 0, thinking disabled.

## Result: flash is at the ceiling; the noise is now measured properly

| Condition | Repeat scores (36 problems) | Mean |
| --- | --- | ---: |
| Baseline (initial skills) | 0.944 / 0.972 / 0.972 | 0.963 |
| **No skills (primary control)** | 0.972 / 0.972 / 0.972 | **0.972** |
| Candidate (same initial skills — nothing accepted) | 0.917 / 0.944 / 0.972 | 0.944 |

Zero of three proposals passed the gate, each for an informative reason:

- **Attempt 1 (tie):** the proposed edit reached 25/25 validation — but the gate re-measured
  the *parent* fresh, and the same baseline skills that scored 22/25 at the baseline event
  now scored 25/25. A ±3-problem swing on the 25-problem validation: the noise band, live.
- **Attempt 2 (harmful):** −0.16, blocked.
- **Attempt 3:** the episode budget ran out — attempts actually consume
  train(20) + parent re-measure(25) + candidate(25) = 70 episodes each; the workspace was
  budgeted at 45. A sizing bug, recorded as such.

The decisive measurement: **baseline and candidate carry identical skills** (nothing was
accepted), yet their independent final draws differ by 0.019 mean — condition-level noise is
about one problem per repeat. Single-edit skill effects at this tier sit far below that
band. No-skills is the strongest condition at 35–36/36 per repeat.

## What this study adds

1. **The pack** ([humaneval_tasks](../../humaneval_tasks)) — the field's standard code
   benchmark on the platform with zero custom evaluator code, transparent exclusion of the
   three upstream-defect problems, and a wrapper whose validity was proven in **both**
   directions (161/161 canonical solutions pass, 0/161 pass-stubs pass — after catching the
   vacuous "164/164" that a missing `check()` call initially produced).
2. **The first properly-powered panel** in the repo: 3 repeats × 3 conditions, quantifying
   per-repeat and condition-level noise on identical skills — the concrete evidence behind
   the noise-band gate queued in ADOPTION item 38.
3. **An honest ceiling null**: ~96–97% pass at flash tier leaves no measurable headroom for
   guidance evolution; harder code suites (or weaker agents) on the same protocol are the
   path to effect evidence on this track.

Files: [summary.json](summary.json) · [final.json](final.json) · [audit.json](audit.json) ·
[gate-summary.json](gate-summary.json) · [evidence.md](evidence.md) ·
proposals [1](attempt1-proposal.diff) · [2](attempt2-proposal.diff) ·
initial skills [inspect](initial-skill-inspect.md) · [edit](initial-skill-edit.md) ·
[verify](initial-skill-verify.md).
