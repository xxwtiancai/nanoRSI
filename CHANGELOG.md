# Changelog

## 0.3.0 — 2026-09-12

- Add a coding starter with twelve independently authored Python repair tasks and behavioral unittest grading.
- Let coding agents run fixed public tests for debugging while private tests and reference solutions stay outside model requests.
- Reuse the bounded skills loop, frozen final-test comparisons and versioned evaluation contract.
- Generate standalone HTML and richer Markdown reports from verified lineage, with paired final comparisons, search decisions and cost coverage.
- Document the executable-task and reproducible-evidence ideas learned from OpenRSI; independently implement them without importing upstream code.
- Correct process termination tests to distinguish a running descendant from a terminated zombie awaiting reaping.

The starter suite and offline checks do not establish real-model gains or reproduce OpenRSI benchmark results. Code execution is trusted local execution, not a hardened sandbox.

## 0.2.0 — 2026-09-09

- Focus the repository on measured skills and Agent Harness improvement under a fixed model.
- Add a schema-v2 skills starter with a reference Runner, real configurable model-command/HTTP bridge, train feedback and 90 grouped local protocol fixtures.
- Add bounded multi-attempt runs, explicit attempt/episode reservations, frozen final testing and fixed/self-use proposer harness selection.
- Record per-task outcomes, actual loaded skill hashes, artifacts, usage coverage and rejected/failed/no-op attempts.
- Add task-macro, per-arm, paired comparison tools; keep deployment repeats separate from independent evolution runs.
- Fix missing evaluator fingerprint across accepted generations and non-score metric handling.
- Harden subprocess output/timeout behavior and versioned evaluator result validation.
- Preserve legacy artifact/harness demos and external model-training contracts. Their heldout scores remain selection data.

Validation uses offline fake-model and local HTTP fixtures. No paid model gains, benchmark reproduction, statistical significance or hardened sandbox capability is claimed. Independent live runs, external benchmark transfer and an isolated evaluator adapter remain research/deployment follow-ups.
