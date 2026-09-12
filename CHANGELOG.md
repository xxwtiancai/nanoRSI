# Changelog

## 0.4.1 — 2026-09-13

- Serialize Git worktree administration across population threads while keeping candidate evaluation concurrent; avoid a create/remove metadata race observed on Linux CI.
- Make the TRAIN feedback limit configurable while preserving the default-four comparison identity and correctly reserving larger population panels.
- Add an optional NumPy handwritten-digit experiment with frozen/self-use, uniform and random-priority controls, full TRAIN feedback, per-attempt random streams and real SFT/REINFORCE/LoRA checkpoint updates.
- Separate study-wide search/freeze from final testing, bind the complete study plan into immutable workspace contracts, and verify paired designs before testing.
- Distinguish completed final outcomes from complete training budgets, retain failed-attempt work and report both all-measured and matched-budget paired effects with descriptive and family-adjusted uncertainty.
- Publish the complete handwritten-digit confirmation panel: 120 runs, 720 completed training rounds, 676 accepted and 44 rejected candidates, no failed attempts, and verified matched actual budgets. Include all four controls, validation-only pilot records, per-case outcomes, curricula, training receipts and checkpoints in an unsigned public extract without HMAC keys.
- Add bilingual study guides and paired results to both READMEs while preserving the v0.4.0 CPU and live-model history.

On the custom UCI/scikit-learn digits split, mean self-use minus frozen test accuracy was +3.654 pp for SFT (10/10 seeds positive), +8.187 pp for REINFORCE (9/10), and +2.527 pp for LoRA (8/10). Only REINFORCE met the predeclared observed-mean ≥5 pp target with a positive nominal Bonferroni-adjusted bootstrap lower bound; SFT and LoRA did not. This does not establish a true gain ≥5 pp. REINFORCE nevertheless trailed uniform sampling by 8.764 pp, and LoRA by 0.824 pp. SFT's test error fell from 10.16% to 6.51%, a 35.95% relative error reduction, equivalent to +3.65 pp accuracy. These results concern one fixed split and small linear models, not official benchmark performance or LLM fine-tuning. See the [complete results and evidence limits](examples/results/recursive-digits-v0.4.1/README.md).

## 0.4.0 — 2026-09-12

- Run schema-2 artifact, harness and model experiments through the same baseline, bounded search, freeze, final-test, report and verify commands. `program`, `agent` and `learner` remain descriptive aliases; legacy starters are available as `artifact-fixture`, `harness-fixture` and `model-contract`.
- Add live model proposals for an executable JSON-processing program and an agent workflow runner; retain coding and skills experiments and allow declared skills to execute `run.py` with bounded JSON input/output.
- Dispatch actual training before candidate evaluation, protect trainer entry points, pass train-only data, validate checkpoint bytes and commit trained checkpoints. Final evaluation reads the frozen checkpoint without retraining.
- Add inspectable CPU SFT, REINFORCE and LoRA implementations for a tiny softmax classifier, with checkpoint-guided curriculum and frozen/self-use controls.
- Support mode-specific final conditions and preserve primary-metric direction in frozen reports and comparison identities.
- Add bounded population search with top-K branch retention, crossover ancestry, local concurrent candidate worktrees, serialized root journal writes and durable budget reservations/recovery.
- Add optional authenticated HTTP evaluation workers and a two-process localhost demonstration; multi-host operation and hostile-code containment remain unverified.
- Add reproducible CPU and request-capped live-demo drivers that retain unsuccessful outcomes. Document the measured CPU panel, API onboarding and the limits of each experiment.
- Publish all six live GLM experiments and 18 CPU trials with frozen results, source/checkpoint snapshots, failed and rejected attempts, and a descriptive result figure. Exported summaries are rebuilt from verified outcomes; provider receipts remain separately labelled unsigned records.
- Exercise real parameter training and all canonical starter rendering from the installed wheel in CI.
- Start numeric loopback HTTP workers without reverse DNS, preventing resolver stalls observed on macOS CI.
- Expand the core ceiling to 5,000 lines while retaining the 300-line module and 50-line function limits and zero third-party core runtime dependencies.

The verified CPU panel completed 18 runs and 54 training rounds, with 20 accepted and 34 rejected candidates. Held-out mean accuracy rose from 46.11% to 84.44–86.39% across method/control groups on overlapping synthetic clusters. Self-use comparisons were mixed: one positive, one negative and seven ties. These teaching-scale results are not LLM fine-tuning, general benchmark performance or proof of general recursive self-improvement.

The live study used 43 GLM-5.3-Flash requests and 87,812 tokens. Five four-case demonstrations went from 1/4 to 4/4; the single batch-skill task went from 0/1 to 1/1. Recursive and frozen proposers tied on the final panel. A known parsing defect remains in the remote demo's measured generated candidate; see the [complete evidence and counterexample](examples/results/v0.4.0/README.md).

## 0.3.1 — 2026-09-12

- Handle macOS zombie-only process-group permission errors without losing timeout outcomes; verify terminal group state and preserve genuine permission failures.

- Add `configure` with masked terminal key input, external credential files, explicit no-key mode and a small-run budget preset via flags.
- Validate endpoint and credential settings before experiments; preserve unrelated TOML and reject reconfiguration after a journal starts.
- Add optional `doctor --check-model` to validate one authenticated JSON model action before baseline, with actionable redacted failures.
- Support selectable completion-token field names, reject HTTP redirects, and prevent raw provider errors from leaking credentials.
- Pin the creating Python interpreter in new coding/skills workspaces.
- Rewrite bilingual first-run guides around API keys, model selection, budget, full RSI lifecycle and troubleshooting.
- Test the complete authenticated HTTP path with a local fixture; no paid-provider or real-model performance claim.

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
