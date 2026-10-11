# ALFWorld phase 2: real agent tasks, honest null at the ceiling (2026-10-11)

The user-facing question behind this study: not toy puzzles — **real agent tasks**. This
port runs complete [ALFWorld](https://github.com/alfworld/alfworld) text games (MIT;
[NOTICE](../../alfworld_tasks/NOTICE)) on nanoRSI: the agent (GLM-5.3) explores rooms,
finds and manipulates objects across the six standard task families, and success is the
game engine's own `won` flag. The mutable surface is the operating skill; the game
runner, evaluator overlay and model bridge are frozen at baseline. Deterministic pack:
4 train / 6 validation games from the train split, 6 seen + 6 unseen layouts as the
frozen test panel. Pack and contract checks: [`examples/alfworld_tasks`](../../alfworld_tasks)
· [`tests/test_alfworld_pack.py`](../../../tests/test_alfworld_pack.py).

## Headline: the harness is real; the improvement is honestly null

| Stage | Result |
| --- | --- |
| Baseline (initial skill), validation | **0.833** (5/6 games) |
| Attempt 1 (placement-rule guidance) | 0.667 — **rejected by the gate as harmful** |
| Attempt 2 (task-type templates + location priors) | 0.833 — rejected, tie |
| Attempt 3 (guidance consolidation) | 0.833 — rejected, tie |
| Frozen final panel, 12 games (6 seen + 6 unseen) | **baseline 12/12 · no-skills 12/12 · candidate 12/12** |

Three proposals, zero accepted — the strict-improvement gate did its job (one harmful
edit blocked, two ties not promoted), and the final panel shows why no gain was
available: **GLM-5.3 solves this entire subset with or without the skill — a ceiling
effect.** Two baseline runs of the same six validation games differed by one game
(0.667 vs 0.833): the ±1-game noise band is larger than any single-edit guidance effect
at this agent strength. This null is about the small-pack + strong-agent regime, not
about skill editing in general.

## What this study actually establishes

1. **Real agent tasks run end to end on the platform**: engine-hosted episodes, frozen
   evaluator contract, per-episode transcripts and usage in the evidence ledger, audits
   clean (zero leakage, zero bypass; answers exist only as winning action sequences
   inside the engine), `verify` passes.
2. **A literature-aligned protocol is now cheap to run**: the seen/unseen split
   convention, engine-scored success, skill-as-mutable-surface (ExpeL/SkillWeaver
   style) — all wired into the ordinary nanoRSI CLI lifecycle.
3. **A measured negative with diagnosis**: guidance evolution needs headroom (weaker
   agent or harder games) and a noise-aware gate. Both follow-ups are already queued:
   the [RRSI noise-band protocol](../../../docs/research/industry-rsi/ADOPTION.md)
   (item 38) and a larger-split, flash-tier replication.

## Cost and record

Proposer: 3 calls / 10,673 input / 1,897 output tokens. Final test: 327 model calls
across 36 game-conditions. All failed proposals, panels and transcripts are retained
in [evidence](evidence.md); every rejected diff is archived
([1](attempt1-proposal.diff) · [2](attempt2-proposal.diff) · [3](attempt3-proposal.diff)).

Two workspace rebuilds were needed before the valid run: the first runner omitted the
propose mode (three attempts burned), the second had the alfworld skill unregistered in
`[agent] skills` and thinking left enabled (the bridge then received empty content).
Both defects are fixed in the generator and locked by tests — the honest cost of
finding them is part of this record.

Files: [summary.json](summary.json) · [final.json](final.json) · [audit.json](audit.json) ·
[evidence.md](evidence.md) · [initial-skill.md](initial-skill.md).
