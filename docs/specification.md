# nanoRSI Kernel Specification

This document describes v0.2. Python 3.11+, Git and the standard library are the core runtime. Local execution is trusted; this is not an OS sandbox.

## Scope and module ownership

One workspace has one accepted parent, one candidate at a time and a bounded sequence of proposal attempts. Schema 1 retains legacy artifact/harness/model command contracts. Schema 2 provides skills/harness experiments with train/validation/test separation and a frozen final panel.

| Module | Responsibility |
| --- | --- |
| `src/nanorsi/__init__.py` | Version |
| `src/nanorsi/cli.py` | Commands, snapshots and single-attempt orchestration |
| `src/nanorsi/loop.py` | Fixed contract, manifest checks, resource reservations, finite run, freeze and final-test |
| `src/nanorsi/config.py` | TOML contract and validated configuration |
| `src/nanorsi/paths.py` | Relative paths and containment |
| `src/nanorsi/hashing.py` | Stable content identity |
| `src/nanorsi/surface.py` | Patch mutation allow/deny policy |
| `src/nanorsi/gitops.py` | Exact Git snapshots, worktrees and refs |
| `src/nanorsi/proposer.py` | Context → external proposal → diff/hypothesis/usage |
| `src/nanorsi/evaluator.py` | External evaluation and versioned result validation |
| `src/nanorsi/gate.py` | Pure primary-metric and constraint comparison |
| `src/nanorsi/lineage.py` | Sequenced HMAC records and hashed artifact references |
| `src/nanorsi/process.py` | Filtered argv execution, finite timeout, raw output bound and POSIX process-group cleanup |
| `src/nanorsi/report.py` | Traceable search report and nullable cost coverage |
| `src/nanorsi/templates.py` | Exportable workspace starters |
| `src/nanorsi/doctor.py` | Local preflight, model configuration and manifest checks |
| `src/nanorsi/locking.py` | One mutation operation per workspace |

No module may exceed 300 lines, no function 50 lines, and core runtime source must remain at or below 2,500 lines. Tests enforce the module inventory and no runtime third-party imports. Supporting examples and exported Runner code are visible separately and do not become hidden core services.

## Configuration

`experiment.schema_version` defaults to 1. Version 2 requires harness mode and accepts `arm = "frozen" | "self-use"` and a nonnegative integer seed. `[agent]` pins the model bridge argv, model identity, inference limits and selected skill names; `[data].manifest` names the task file. Configuration and protected driver/data fingerprints are checked against baseline before subsequent operations.

The reference Runner supports at most eight model actions per task. `budget.max_steps` bounds all proposal attempts, not accepted generations. `max_episodes` bounds reserved search task executions; `max_output_bytes` caps captured raw bytes and result/proposal artifacts. UTF-8 replacement decoding may expand displayed bytes. Costs and token coverage are observations; absent values remain null, not zero. No dollar hard cap is advertised.

Credentials are optional and supplied through an explicit external key file. They are not ambient environment imports. Local custom code remains trusted. A provider alias cannot guarantee model-version immutability; users must pin snapshots when available and disclose drift otherwise.

## States and journal

```text
NEW → GEN0_SNAPSHOT → GEN0_EVALUATED
  → ATTEMPT_STARTED → TRAIN_EVALUATED → PROPOSAL_CREATED
  → PATCH_VALIDATED → CHILD_SNAPSHOT → CHILD_EVALUATED
  → GATED_ACCEPTED | GATED_REJECTED | INCONCLUSIVE | ATTEMPT_FAILED
  → LINEAGE_RECORDED → REPORT_WRITTEN
  → next bounded attempt, or FROZEN → FINAL_TEST → FINAL_REPORT
```

The append-only journal includes `baseline_started`, `evaluation_started/finished`, `attempt_started`, `proposal_started/finished`, `generation`, `attempt_failed`, `freeze`, `final_started/result`. A baseline-start record has no accepted generation. Every attempt start is durable before external proposal work; interrupted starts consume budget. `recover` records dangling attempts as interrupted and reconciles accepted tags.

Accepted generation counters are independent of attempts. Rejected records retain the current generation and identify their parent explicitly. Equality and empty v2 proposals do not promote. Legacy historical generation records lacking attempt IDs count toward the attempt allowance; previously unrecorded legacy failures cannot be reconstructed.

## Inputs, execution and evaluation

Task manifest: `{schema_version:1,tasks:[...]}`. Each task requires unique `task_id`, nonempty `group_id`, split train/validation/test, instruction and relative-path text mappings `input_files`/`expected_files`. Source groups cannot cross splits and each split is nonempty.

Schema-v2 baseline evaluates validation only. Each step samples up to four train tasks, passes their allowed evidence to the proposer, and compares the parent and candidate on matching validation panels. Search episodes are reserved before evaluation, including runs that later fail. Results must match the reserved task/repeat identities. Final-test episodes are accounted separately under the frozen panel.

The reference evaluator sends only public input to a new Runner process. The Runner loads actual skill bytes from its own snapshot, records their hashes, and performs list/read/write/final actions in a fresh temporary task directory. It receives no grader labels. Training records additionally include grader feedback for revision; validation/test records do not expose expected files. Local filesystem secrecy still requires a separate isolation service.

V2 evaluator results require finite aggregate metrics; nonempty unique task/repeat case records; finite score in [0,1]; a status; trace and skill hashes; nonnegative duration; nullable nonnegative usage. Case identities are checked against the task manifest. V1 aggregate/case shape remains compatible. Private task verdicts are supplied by fixed evaluator code, not by a candidate's claims about success.

## Proposer and recursive reuse

A fixed external proposer driver writes `proposal.diff`, `hypothesis.json`, `usage.json` and `trace.json`. Its explicit context contains current-parent files, train feedback and experiment metadata. V2 omits validation scores from this context. All outputs are bounded and retained as hashed artifacts where available, including failed attempts.

`frozen` uses the H0 Runner for each proposal. `self-use` uses the latest accepted Runner. Both edit the current parent source, and the actual source Runner loads its own skills. Rejected candidates never become future proposers. A recorded path alone is not proof of this property; tests inspect loaded skill hashes across generations.

## Frozen evaluation

`freeze --repeats N` pins initial and selected commits, model/task contract, comparison identity and repeats (1–10). Search is then prohibited. `final-test` evaluates baseline skills, no-skills baseline and selected candidate under the same task panel and inference settings. Test results never enter the gate. Successful panels are idempotent; unfinished panels are explicitly identified rather than silently rerun to select a favorable outcome.

The final report has schema 2, `manifest_hash`, `comparison_hash`, experiment/arm/seed, and per-condition/repeat case results. `manifest_hash` includes arm/seed configuration; `comparison_hash` excludes these experimental variables but binds task content, evaluator, inference configuration and initial target content. Cross-report aggregation requires a matching comparison identity, not merely matching task names.

`examples/compare.py` reports task-macro scores, paired deltas, equal-weight evolution-run summaries, per-arm results, per-episode timing and unknown cost coverage. Different numbers of repeated deployments must not overweight an evolution run. Reports do not assert statistical significance or real-model gains from test fixtures.

## Trust and compatibility invariants

1. Evaluation uses an exact recorded Git snapshot; evaluator/proposer/adapter/task/config changes cannot be accepted as target changes.
2. A failed or rejected attempt never changes the accepted parent.
3. All accepted generations retain the baseline evaluator and contract identity.
4. Receipts verify journal fields; artifact references verify persisted bytes. They do not protect against a malicious same-user process with access to the key.
5. No final-test result can promote a candidate or reopen a frozen search.
6. Legacy heldout remains selection data. V1 experiments are never relabelled as independent final tests; v2 starts from fresh workspaces.
7. The model template remains an external command contract, without model training in the core.
8. Provider failures and unknown cost stay visible. POSIX timeout cleanup covers process groups; external sandboxing, remote jobs and abrupt host death need their own operational controls.
