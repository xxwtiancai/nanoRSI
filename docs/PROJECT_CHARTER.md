# nanoRSI Charter

nanoRSI is a small, hackable lab for improving executable artifacts, agent harnesses, reusable skills and model parameters under a fixed evaluation contract and a measurable budget.

## Goal

Make one complete experiment easy to read, run and inspect: execute training tasks, use their outcomes to propose a change, train parameters when appropriate, compare parent and candidate on validation tasks, retain a qualifying version, freeze choices and evaluate separate test tasks.

The primary audience is developers studying or improving their own programs and agents. Success means a correct, traceable experiment; negative, unchanged and inconclusive empirical results are valid.

## Questions that need separate comparisons

1. Does the selected artifact, harness or checkpoint improve on its initial version on frozen test tasks?
2. Do reusable skills help? Compare no-skills, initial-skills and selected-skills conditions.
3. Does recursive reuse contribute? Compare frozen and self-use proposers with matched initial states, tasks, inference and search budgets.
4. Does branching and population selection help at a matched budget? Compare it with serial search on the same task contract.

The implementation makes these comparisons possible. Loading a changed file, running more training rounds or passing mocked tests does not by itself establish recursive benefit. Heterogeneous demos must not be combined into one RSI score.

## Scope

- Schema-2 artifact, harness and model experiments with a shared baseline/search/freeze/final-test lifecycle.
- Live model proposals for executable programs and agent runners; coding and text-edit skills can contain both Markdown and callable Python scripts.
- Real CPU SFT, reward-sampled policy-gradient and LoRA examples with protected trainers, train-only payloads and committed checkpoints.
- Frozen and self-use proposer controls, including checkpoint-guided curriculum construction.
- A single-incumbent serial loop plus bounded population search, top-K branch retention, crossover context and local candidate concurrency.
- Optional authenticated HTTP evaluation adapters, demonstrated with two localhost worker processes.
- Exact Git snapshots, protected evaluation/configuration, explicit decisions, signed journal records and hashed evidence.
- Separate train/validation/final-test data; finite attempts, episodes, process time and output.
- A standard-library core of at most 5,000 lines, with modules at most 300 lines and functions at most 50 lines. Examples and exported runners remain visible outside that core inventory.

## Boundaries

The built-in execution model trusts local candidate code. Worktrees, process limits and receipts do not provide a hardened code sandbox or protect private labels from hostile same-user code. The HTTP example demonstrates localhost transport; multi-host operation and distributed training are unverified.

Universal Agent compatibility, hosted services, plugin registries, marketplaces and background daemons are outside this version. The tiny learner demonstrates actual parameter updates, not LLM fine-tuning. This project does not claim unrestricted self-modification, a general RSI solution or guaranteed gains.

## Rules

Candidates cannot change experiment scoring, task data, model endpoint settings or the protected trainer entry point. Test results never influence promotion. Final evaluation uses the frozen checkpoint without retraining. Failed/no-op attempts and unknown costs remain visible. Skills and source changes must implement general behavior rather than store benchmark answers.

Claims require real executions, versioned tasks, matching controls and disclosed budgets. Improvements on authored demos remain specific to those tasks. OpenRSI informs the interest in executable, bounded MLE meta-evolution; its results do not establish general RSI. nanoRSI independently implements its code and does not copy OpenRSI's CC-BY-NC source into this Apache-2.0 project.

Existing schema-1 workspaces remain compatible. The explicit `artifact-fixture`, `harness-fixture` and `model-contract` starters preserve the earlier demonstrations; their selection data is not relabelled as an independent final test.
