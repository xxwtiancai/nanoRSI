# Changelog

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
