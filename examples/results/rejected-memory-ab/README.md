# Rejected-edit memory A/B on a live model (2026-09-19)

The live half of [ADOPTION item 14](../../../../docs/research/industry-rsi/ADOPTION.md): does the rejected-edit memory (`rejected_recent` in the proposal context) stop repeat proposals from a real model? Fixture plumbing was validated on 2026-09-17 (memoryless scripted proposer 2/2 identical repeats vs memory-aware 0/2).

**Finding: a clean null result.** On the OpenEvolve function-minimization task (Apache-2.0 port) with GLM-5.3-Flash, seed 0 and five attempts per arm, **neither arm produced a single identical or near-identical (Jaccard ≥ 0.6) repeat proposal** — the hypothesized failure mode did not occur, so the memory's trigger never fired. Both arms still evolved successfully; the memory observed no cost.

| Arm | Attempts (decision, Δvalidation) | Identical repeats | Final baseline → candidate | Model calls |
| --- | --- | ---: | ---: | ---: |
| memory on (default) | accepted +0.077, failed, rejected −0.047, rejected −0.087, failed | 0/5 | 0.9418 → 0.9944 | 5 |
| memory off | failed, rejected −0.011, rejected −0.010, accepted +0.080, failed | 0/5 | 0.9418 → 0.9997 | 9 |

Interpretation stays narrow: at n=1 task × 1 model × 1 seed × 5 attempts, zero observed repeats means there is no power to detect a reduction — this is an absence-of-precondition observation, not evidence the memory cannot help elsewhere (weaker models, tighter budgets, or longer horizons may repeat more). The memory therefore remains on by default as a zero-observed-cost safeguard, and a per-workspace switch `[proposer] rejected_memory = false` ships for controlled replication.

Limits: single task/model/seed; rejections in both arms were genuine diverse attempts (negative deltas), not repeats; call-count differences (5 vs 9) reflect invalid-JSON retries under the bridge, not the memory.

Files: [summary.json](summary.json) · [memon/](memon) · [memoff/](memoff)
