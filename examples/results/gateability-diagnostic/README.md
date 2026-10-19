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
