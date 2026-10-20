# Gate-ability diagnostic: the known-good edit the gate cannot see (2026-10-20)

The degenerate [selector pilot](../selector-pilot-live/README.md) left two hypotheses:
acceptance blocked by proposal quality, or by the gate/panel. This diagnostic removes
proposal quality entirely — a **scripted proposer replays the archived known-good skill
edit** ([alfworld-flash attempt 4](../alfworld-flash/attempt4-proposal.diff), the only
edit that ever passed this gate) on the same 8/8 config. Zero model calls for proposing.

## Result: good edit, invisible validation, gate refuses

| Panel | Outcome |
| --- | --- |
| Validation (8 train-split games) | parent re-measure 0.875, candidate 0.875 — **tie, rejected**; per-task vectors **identical** (zero wins, zero losses) |
| Frozen test panel (6 seen + 6 unseen) | **candidate 1.000** (6/6 + 6/6) vs baseline 0.833 (4/6 + 6/6) and no-skills 0.833 (5/6 + 5/6) |

The edit is worth **+2 games over both controls on the very panel where the gate refused
it** — but this validation draw (train-split games) carried no signal: same mean, same
per-task outcomes. Not mean-tie arithmetic and not paired-task arithmetic could have
accepted it. The 2026-10-12 acceptance was a lucky validation draw; the 2026-10-19 nulls
were unlucky draws of the same coin.

## Diagnosis and implications

**Validation representativeness is the binding constraint.** The pack's validation games
come from the train split, while the edit's value lives on seen/unseen test layouts.
Implications:

1. The ALFWorld pack needs validation drawn from the seen/unseen distribution (a pack
   design change), or a larger validation panel — not a smarter gate formula.
2. A paired per-task gate was considered and **rejected for now**: on this real draw it
   would also have rejected (zero task flips) — the honest instrument said nothing.
3. The selector-pilot verdict stands with a sharper cause: acceptance was impossible on
   that validation draw regardless of gate strictness.

Files: [summary.json](summary.json) · [final.json](final.json) ·
[attempt panels](attempt-parent-panel.json) · [audit.json](audit.json) ·
[noise-band.json](noise-band.json). Final test: 440 model calls; proposer: zero (scripted).


## Recheck 2026-10-21: representative validation, same lottery

After the [pack redesign](../../alfworld_tasks/README.md) (validation now drawn 4+4 from the
seen/unseen pools, disjoint from test), the same archived edit was replayed once more:
**still a tie with identical per-task vectors** — and this draw the baseline condition also
saturated the test panel (12/12), so the edit showed no test advantage either. Across three
replays the effect is small and draw-dependent everywhere; representative validation was
necessary but not sufficient. The empirically demonstrated acceptance path is **persistence**:
the original study accepted on attempt 4 of 4 — every attempt is a fresh draw. Pilots ran 1-2
attempts. Study-design implication: ≥4 attempts for small-effect edits, or larger panels, both
costed by the (1+attempts)×(train+2×validation) budget rule. Files:
[recheck-final.json](recheck-final.json) · [recheck panels](recheck-parent-panel.json).
