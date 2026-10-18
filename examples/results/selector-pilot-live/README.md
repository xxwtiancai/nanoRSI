# Live selector pilot: protocol machinery on real noise, degenerate comparison (2026-10-19)

First **live** run of the [selector-study protocol](../../../docs/SELECTOR_STUDY_PROTOCOL.md),
redesigned after the [2026-10-18 headroom stop](../../results): validation raised to 8 games
(baseline 0.875 on both arms — one game of headroom, the protocol's floor), one seed, two
attempts, two arms — strict control vs **noise_band 0.13** (the measured one-game swing).

| Arm | Validation attempts | Accepted | Final (baseline / no-skills / candidate) | false-blocks |
| --- | --- | ---: | --- | ---: |
| Strict | 1 (tie) | 0 | 1.000 / 0.833 / 1.000 | 0 |
| Noise-band 0.13 | 2 (ties) | 0 | 0.750 / 0.917 / 0.833 | 0 |

**Degenerate comparison, honestly null.** No proposal cleared even the strict gate on
either arm, so the band never bound — double-scoring shows full agreement with zero
false-blocks because there was nothing to block. At this proposer tier and panel size the
binding constraint is proposal quality, not noise sensitivity. The cross-arm final panels
differ by up to two games with identical initial skills — the familiar single-draw noise.

The pilot's deliverable is the machinery: headroom precondition → two live arms → full
lifecycle → freeze/final → verify → double-scoring accounting, all executed on real noisy
episodes with per-arm usage. The full three-seed study now has a costed template; its
prerequisite, per this null, is an arm where acceptance is achievable at all (more
attempts, a stronger proposer tier, or tasks where single edits move multiple games).

Files: [summary.json](summary.json) · [strict](strict-final.json) · [band](band-final.json)
· noise-band reports [strict](strict-noise-band.json) · [band](band-noise-band.json) ·
gate summaries [strict](strict-gate-summary.json) · [band](band-gate-summary.json).
Proposer: 2 calls per arm (8.1k/8.4k input tokens); final tests 419/456 calls.
