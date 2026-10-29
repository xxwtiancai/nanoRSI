# ALFWorld flash replication: not replicated, noise measured at 3 repeats (2026-10-14)

A fresh end-to-end rerun of the [alfworld-flash study](../alfworld-flash/README.md) under
the revised standard: identical deterministic pack and frozen 6-seen + 6-unseen test games,
GLM-5.3-Flash, same goal and attempts — with **3 final-test repeats** from the start (the
original workspace cannot raise repeats: the frozen protocol is immutable by design, which
is correct behavior worth recording).

## Outcome

- **Search: zero acceptances.** Baseline validation 0.875 (identical to the original run);
  attempts 1–3 all ties (0.875 → 0.875), attempt 4 a no-op. The original's accepted +0.125
  edit did not reappear.
- **Final panel (12 games × 3 repeats):**

| Condition | Repeat scores | Mean |
| --- | --- | ---: |
| Baseline (initial skill) | 0.917 / 1.000 / 0.917 | 0.944 |
| No skills | 1.000 / 0.833 / 0.917 | 0.917 |
| Candidate (= initial skill; nothing accepted) | 0.917 / 0.750 / 0.917 | 0.861 |

- **Same-skill noise, directly measured:** baseline and candidate carry identical skills
  yet differ by 0.083 mean (one game); every condition swings within [0.75, 1.0] across
  repeats. All unseen layouts were solved 6/6 in every condition and repeat — the variation
  concentrates on seen layouts.

## Verdict and what it changes

**The original flash improvement is not replicated.** Its two-game frozen-panel margin over
the initial-skill condition sits inside the same-skill band measured here, and this run's
search accepted nothing. The original study's README already flagged the one-game
candidate-vs-no-skills margin as within noise; the two-game margin must now be read the
same way, and its ADOPTION annotation has been amended accordingly.

What survives unchanged: the platform capability (real engine-scored agent tasks through
the full gated lifecycle), the gate's harm-blocking (three ties honestly rejected here),
and the central measured lesson — **single-run gate acceptances on panels this size are
noise-dominated**, which is precisely why the [selector-study protocol](../../../docs/v0.4/SELECTOR_STUDY_PROTOCOL.md)
requires noise-band measurement and multi-seed designs before any selector claim.

A non-replication at n=2 does not prove the original effect was pure noise — both searches
are draws from the same noisy process — but reproducible evidence requires exactly the
protocol this study now exemplifies.

Files: [summary.json](summary.json) · [final.json](final.json) · [audit.json](audit.json) ·
[noise-band.json](noise-band.json) · [gate-summary.json](gate-summary.json) ·
[evidence.md](evidence.md) · proposals [1](attempt1-proposal.diff) [2](attempt2-proposal.diff)
[3](attempt3-proposal.diff). Proposer: 4 calls / 16,819 input / 2,166 output tokens; final
test 1,259 calls.
