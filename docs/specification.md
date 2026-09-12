# nanoRSI Kernel Specification

This document describes v0.4. Python 3.11+, Git and the standard library are the core runtime. Local execution is trusted; this is not an OS sandbox.

## Scope and module ownership

One workspace has one accepted incumbent and a bounded proposal budget. Serial search evaluates one candidate at a time; population search retains branches and evaluates bounded batches concurrently. Schema 2 supports artifact, harness and model experiments with train/validation/test separation and a frozen final panel. The canonical `artifact`, `harness` and `model` starters are executable schema-2 experiments; `program`, `agent` and `learner` are aliases. `artifact-fixture`, `harness-fixture` and `model-contract` retain schema-1 demonstrations, and existing schema-1 workspaces remain compatible.

| Module | Responsibility |
| --- | --- |
| `src/nanorsi/__init__.py` | Version |
| `src/nanorsi/cli.py` | Commands, snapshots and single-attempt orchestration |
| `src/nanorsi/loop.py` | Fixed contract, manifest checks, resource reservations, finite run, freeze and final-test |
| `src/nanorsi/config.py` | TOML contract and validated configuration |
| `src/nanorsi/configure.py` | Offline, atomic model/credential configuration before baseline |
| `src/nanorsi/contracts.py` | Frozen machinery and comparison identities; trainer entry-point discovery |
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
| `src/nanorsi/training.py` | Bounded training dispatch, train-only payloads and checkpoint evidence |
| `src/nanorsi/population.py` | Candidate branches, top-K retention, crossover, local workers and coordinator promotion |

No module may exceed 300 lines, no function 50 lines, and core runtime source must remain at or below 5,000 lines. Tests enforce the module inventory and no runtime third-party imports. Supporting examples and exported Runner code are visible separately and do not become hidden core services.

## Configuration

`experiment.schema_version` defaults to 1. Version 2 accepts artifact, harness and model modes, `arm = "frozen" | "self-use"`, and a nonnegative integer seed. `[agent]`, when present, pins the model bridge argv, model identity, inference limits and selected skill names; it is required for harness mode. `[data].manifest` names the task file. Configuration and protected driver/data/trainer fingerprints are checked against baseline before subsequent operations.

`experiment.final_conditions` must contain `baseline` and `candidate`, may include `no-skills`, and cannot contain duplicates. Harness mode defaults to all three conditions; the executable harness starter explicitly selects baseline/candidate. Artifact and model modes default to baseline/candidate. Skills/coding retain all three. `[evaluator].direction` is `maximize` or `minimize` and remains part of the frozen evaluation contract.

The reference Runner supports at most eight model actions per task. `budget.max_steps` bounds all proposal attempts, not accepted generations. `max_episodes` bounds reserved search task executions; `max_output_bytes` caps captured raw bytes and result/proposal artifacts. UTF-8 replacement decoding may expand displayed bytes. Costs and token coverage are observations; absent values remain null, not zero. No dollar hard cap is advertised.

Credentials are optional and supplied through an explicit external key file. They are not ambient environment imports. Local custom code remains trusted. A provider alias cannot guarantee model-version immutability; users must pin snapshots when available and disclose drift otherwise.

## States and journal

```text
NEW → GEN0_SNAPSHOT → GEN0_EVALUATED
  → ATTEMPT_STARTED → TRAIN_EVALUATED → PROPOSAL_CREATED
  → PATCH_VALIDATED → [MODEL_TRAINING] → CHILD_SNAPSHOT → CHILD_EVALUATED
  → GATED_ACCEPTED | GATED_REJECTED | INCONCLUSIVE | ATTEMPT_FAILED
  → LINEAGE_RECORDED → REPORT_WRITTEN
  → next bounded attempt, or FROZEN → FINAL_TEST → FINAL_REPORT
```

The append-only journal includes `baseline_started`, `evaluation_started/finished`, `attempt_started`, `proposal_started/finished`, `generation`, `attempt_failed`, `freeze`, `final_started/result`. Training evidence is stored with its attempt and retained as hashed artifacts. Population searches also record candidates, reservations, retained branches and coordinator decisions. A baseline-start record has no accepted generation. Every attempt start is durable before external proposal work; interrupted starts consume budget. `recover` records dangling attempts as interrupted, settles outstanding reservations and reconciles accepted tags.

Accepted generation counters are independent of attempts. Rejected records retain the current generation and identify their parent explicitly. Equal metric outcomes do not promote. A v2 attempt that changes no files after proposal and optional training is rejected; an empty model proposal may still produce a changed trained checkpoint. Legacy historical generation records lacking attempt IDs count toward the attempt allowance; previously unrecorded legacy failures cannot be reconstructed.

## Inputs, execution and evaluation

Task manifest: `{schema_version:1,tasks:[...]}`. Each task requires unique `task_id`, nonempty `group_id`, split train/validation/test, instruction and relative-path text mappings `input_files`/`expected_files`. Source groups cannot cross splits and each split is nonempty.

Schema-v2 baseline evaluates validation only. Each step samples up to four train tasks, passes their allowed evidence to the proposer, and compares the parent and candidate on matching validation panels. Search episodes are reserved before evaluation, including runs that later fail. Results must match the reserved task/repeat identities. Final-test episodes are accounted separately under the frozen panel.

The reference evaluator sends only public input to a new Runner process. The Runner loads actual skill bytes from its own snapshot, records their hashes, and performs list/read/write/final actions in a fresh temporary task directory. Declared skills may also expose a fixed `skills/<name>/run.py` through the `skill` action; coding provides a fixed public-test action. The task runner receives no grader labels. Training records additionally include grader feedback for revision; validation/test records do not expose expected files. Local filesystem secrecy still requires a separate isolation service.

V2 evaluator results require finite aggregate metrics; nonempty unique task/repeat case records; finite score in [0,1]; a status; trace and skill hashes; nonnegative duration; nullable nonnegative usage. Case identities are checked against the task manifest. V1 aggregate/case shape remains compatible. Private task verdicts are supplied by fixed evaluator code, not by a candidate's claims about success.

## Proposer and recursive reuse

A fixed external proposer driver writes `proposal.diff`, `hypothesis.json`, `usage.json` and `trace.json`. Its explicit context contains current-parent files, train feedback and experiment metadata. V2 omits validation scores from this context. All outputs are bounded and retained as hashed artifacts where available, including failed attempts.

`frozen` uses the H0 Runner for each proposal. `self-use` uses the latest accepted Runner. Both edit the current parent source, and the actual source Runner loads its own skills. Rejected candidates never become future proposers. A recorded path alone is not proof of this property; tests inspect loaded skill hashes across generations. The executable harness runs its shared `plan_steps` during both task execution and proposal-time training-workflow analysis; `proposal_planner_used` records its actual scheduling diagnostics before they enter the model request. The model learner consumes the chosen checkpoint to compute a curriculum, rather than merely recording its identity.

## Frozen evaluation

`freeze --repeats N` pins initial and selected commits, model/task contract, comparison identity, mode-specific conditions, metric direction and repeats (1–10). Search is then prohibited. `final-test` evaluates the declared conditions under the same task panel and inference settings. In model mode it reads the saved checkpoint from each frozen commit without running the trainer, and verifies that evaluation did not mutate checkpoint bytes. Test results never enter the gate. Successful panels are idempotent; unfinished panels are explicitly identified rather than silently rerun to select a favorable outcome.

The final report has schema 2, `manifest_hash`, `comparison_hash`, experiment/arm/seed, mode, conditions, metric name/direction, and per-condition/repeat case results. `manifest_hash` includes arm/seed configuration; `comparison_hash` excludes those experimental variables and credential locations but binds task content, fixed machinery including the trainer, inference settings, initial target/checkpoint, training settings, mutation surface and budgets. Cross-report aggregation requires a matching comparison identity, not merely matching task names.

`examples/compare.py` reports task-macro scores, paired deltas, equal-weight evolution-run summaries, per-arm results, per-episode timing and unknown cost coverage. Different numbers of repeated deployments must not overweight an evolution run. Reports do not assert statistical significance or real-model gains from test fixtures.

## Trust and compatibility invariants

1. Evaluation uses an exact recorded Git snapshot; evaluator/proposer/adapter/task/config changes cannot be accepted as target changes.
2. A failed or rejected attempt never changes the accepted parent.
3. All accepted generations retain the baseline evaluator and contract identity.
4. Receipts verify journal fields; artifact references verify persisted bytes. They do not protect against a malicious same-user process with access to the key.
5. No final-test result can promote a candidate or reopen a frozen search.
6. Legacy heldout remains selection data. V1 experiments are never relabelled as independent final tests; v2 starts from fresh workspaces.
7. Model training runs through a protected external command under kernel time/output limits; resulting checkpoint bytes are checked, committed and evaluated. The kernel does not implement a general training framework.
8. Provider failures and unknown cost stay visible. POSIX timeout cleanup covers process groups; external sandboxing, remote jobs and abrupt host death need their own operational controls.

## Training and checkpoint contract (v0.4)

Model mode requires `[training].command`. Schema 2 also validates a positive `compute_budget_s`, a positive `max_checkpoint_bytes` and a contained mutable `checkpoint` path. Direct local trainer entry points must be outside the mutable surface; place them under protected `trainer/`. Trainer discovery recognizes direct scripts and common Python/shell/env wrappers, not arbitrary transitive imports. Fixed contract hashing includes `trainer/`, and post-training checks reject changes outside the declared surface.

The kernel writes a schema-1 payload containing only manifest rows whose split is `train`. It passes `NANORSI_TRAINING_DATA_PATH`, `NANORSI_TRAINING_RESULT_PATH` and `NANORSI_CHECKPOINT_PATH` to the trainer inside the candidate worktree. It measures input/checkpoint hashes, trainer and target source identities, process status and duration. Payload hashes must remain unchanged; the checkpoint must be a nonempty bounded regular file with no symlink ancestors.

The trainer writes a schema-1 JSON result with `status = "completed"`, a nonempty `method`, nonnegative integer `steps` and `duration_ms`, and the exact configured `checkpoint_path`. Supplied data, initial-checkpoint and final-checkpoint hashes must match measured bytes. The candidate snapshot is created after training. A valid empty proposal may still train and change the checkpoint. Failed training cannot promote; rejected checkpoints and training evidence remain associated with their attempt.

The CPU learner performs SFT cross-entropy updates, REINFORCE with sampled rewards, or rank-two LoRA updates with a frozen base matrix. Its proposer uses the selected frozen/self-use checkpoint to compute train-example losses and adjust curriculum sampling weights. This is actual parameter training and checkpoint reuse on a tiny synthetic classifier, not LLM fine-tuning or proof that recursive reuse helps. See the bilingual [multilevel guide](MULTILEVEL.md) for the measured panel and reproduction commands.

## Population and optional HTTP execution (v0.4)

`population --size K --generations N --workers W` runs schema-2 searches with at most 32 candidates per round, 32 rounds and eight local worker threads, within the workspace's attempt/episode budgets. It retains validation-ranked unique commits satisfying required constraints, respecting metric direction. Candidate workers use separate worktrees and unsigned local evidence journals. Only the locked coordinator appends root HMAC records and promotes a qualifying champion through the ordinary gate.

Attempt starts and episode reservations precede worker execution. Completed worker evidence is collected serially, reservations are settled, and evaluated branches receive stable candidate refs. Parent IDs and crossover source-parent commits form a candidate DAG; Git candidates retain a single source parent, checked during collection. Crossover context contains bounded, allowed mutable source, not protected data or credentials. Recovery preserves interrupted attempts and conservatively accounts for reserved work rather than granting a fresh budget.

`examples/remote_workers/` is an optional standard-library HTTP evaluator adapter using bearer authentication and checked request, source, task-manifest and evaluator identities. Two independent localhost worker processes execute the fixed program evaluator. The wire protocol does not accept arbitrary argv or client-provided grader labels. This is transport validation only: no multi-host validation, distributed training or hardened isolation is claimed. The local worker coordinator and root lineage remain the source of experiment decisions.

## Executable skills and reports (v0.4)

The `skill` action accepts a declared name and an arguments object. The runner invokes only that skill's fixed `run.py` with JSON stdin containing the episode workspace and arguments, and requires a JSON-object response. It records the script hash and uses a two-second timeout and 1 MB output cap. Candidate scripts remain trusted code; these process limits are not a filesystem/network sandbox.

Final report rendering follows the frozen condition list and primary-metric direction. Proportion-score differences use percentage points; other metrics retain native units. Incomplete panels cannot generate an improvement claim. `examples/demos/run.py` retains live request receipts and failed runs under a cumulative request cap; this is not a dollar cap. Its heterogeneous authored tasks must not be combined into a general RSI score.

## Coding starter and evidence reports (v0.3)

`nanorsi new coding PATH` layers the coding task pack, grader and procedural skills over the skills starter. It uses the existing schema-v2 lifecycle. Task manifests retain identity, split, `input_files` and `expected_files`; in coding tasks `expected_files` contains reference source for suite verification, not exact-match grading. `grading.kind` is `python-unittest`, with separate `public_tests`, `private_tests` and `timeout_s`. Public tests are supplied through the coding evaluator to the fixed `test` action. Private tests and references are excluded from model requests and training feedback. Candidate behavior is graded in bounded fresh subprocesses.

The shared test helper lives under protected `adapters/`, included in the frozen experiment identity. The default mutable surface stays `target/agent/skills/**`. Source groups, comparison identity, final-test freezing and lineage requirements are unchanged. Local executable code remains trusted; this is not a hardened sandbox.

`nanorsi report --format html` writes standalone `reports/report.html` alongside Markdown and raw lineage JSON. Final summaries require all frozen conditions and repeats, identical task/repeat pairs and finite bounded scores. Repeats are averaged within tasks, then tasks equally weighted. Incomplete final panels show pending evaluation instead of an improvement claim. All dynamic HTML is escaped. Search/test costs disclose coverage and preserve unknown values.

## Model onboarding and credential contract (v0.3.1)

`src/nanorsi/configure.py` implements offline, locked, atomic pre-baseline configuration. `nanorsi configure` takes model and endpoint plus exactly one explicit authentication choice: hidden terminal input, an existing external credential file, or no key. Prompted keys are stored in unique owner-only files outside the experiment; only their paths enter TOML. Failed updates retain the previous configuration and remove newly created unused credential files. Any nonempty journal prevents reconfiguration; create a new workspace to change a started experiment. Unrelated TOML settings remain intact.

`src/nanorsi/config.py` rejects inline credential fields, credential paths resolving inside the workspace, invalid HTTP(S) endpoints and unsupported `token_parameter` values. `max_tokens` remains the bridge default; `max_completion_tokens` can be selected explicitly for compatible model APIs. New coding/skills templates use the creating interpreter path for agent, proposer and evaluator commands.

Plain `doctor` performs offline model/credential/task checks. `doctor --check-model` makes one bounded bridge request and validates a JSON final action, without creating baseline, lineage or final-test state. The probe can incur provider charges outside experiment cost accounting. HTTP errors use stable redacted categories, unknown bridge errors remain generic, and response bodies and credential values are never printed as diagnostic messages. The bundled bridge refuses redirects and reads only the explicitly configured external key file; ambient API-key variables and .env files are not consumed.

### Darwin process-group termination

The process runner retains the group leader until after escalation. On macOS, a group containing only zombies can return `EPERM` when signaled ([Apple XNU signal implementation](https://github.com/apple-oss-distributions/xnu/blob/main/bsd/kern/kern_sig.c)). Only on Darwin, the runner checks group IDs/states with the system `/bin/ps` under a one-second timeout. It accepts that permission error only when every remaining group member is a zombie or the group is absent. Failed inspections and live members preserve the original permission error. The leader is reaped after signaling. This is lifecycle handling, not a privilege bypass.
