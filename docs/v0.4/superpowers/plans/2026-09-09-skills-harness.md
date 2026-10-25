# Skills / Harness v0.2 implementation plan

**Goal:** Implement the accepted skills-first design as a working, bounded experiment: train feedback → propose → validation → freeze → test, with a reference skills runner and a frozen/self-use proposer comparison.

**Architecture:** Keep the existing standard-library package and Git worktrees. Add only `loop.py` to the core module inventory. Preserve legacy artifact/harness/model templates; introduce `new skills` as the schema-v2 real-model starter, so scripted legacy demos remain available for offline compatibility tests. Experiments use one accepted parent and one candidate at a time.

**Tech stack:** Python 3.11+, Git, standard-library unittest; optional external model command. No new runtime dependencies.

**Worktree:** `/Users/xiongweixiao/main/OpenSource/.worktrees/nanorsi-harness-v0.2` on `feat/skills-harness-v0.2`. All commands below run there with `PYTHONPATH=src PATH=/opt/miniconda3/bin:$PATH /opt/miniconda3/bin/python3.13` in this development environment.

**Delegation:** Every child uses `gpt-5.6-luna` with `xhigh`, fresh bounded context, explicit file ownership, and no recursive delegation or commits. Independent ownership lanes run in parallel; the parent owns integration decisions and commits. Parent reviews requirements first, followed by independent quality review.

## Scope and fixed contracts

### Configuration

Legacy `[experiment] schema_version` defaults to 1. V2 sets `schema_version=2`, `mode="harness"`, `seed=0`, `arm="frozen"` or `"self-use"`. Keep current fields.

New optional sections:

```toml
[agent]
model_command = ["python3", "adapters/model.py"]
model = "configure-your-model"
max_turns = 8
skills = ["inspect", "edit", "verify"]

[data]
manifest = "tasks/manifest.json"

[budget]
max_steps = 5 # v2 proposal attempts, including failures
max_episodes = 400
max_output_bytes = 1000000
```

Agent config may include `base_url`, `api_key_file`, `max_tokens`, and `timeout_s`; these are frozen experiment inputs, not mutable target files. Dollar totals are reported with unknown coverage; no unprovable dollar-hard-cap claim. Turn, output, timeout, attempt and episode caps are enforced.

### Task manifest

One JSON object with `schema_version: 1` and `tasks: [...]`. Each task has unique `task_id`, `group_id`, `split` (train/validation/test), `instruction`, `input_files` (relative path → content), `expected_files` (relative path → expected content). Groups must not cross splits. Every split is nonempty. Default fixture tasks are deterministic local document edits, 30 per split, disjoint groups. Grader compares exact final files and rejects unexpected changes to initial files.

### Model bridge (custom JSON protocol)

stdin JSON: `{messages: [{role, content}], model, max_tokens, base_url?, api_key_file?, timeout_s?}`. stdout JSON: `{content: STRING, usage: {model_calls, input_tokens, output_tokens, cost_usd}}`. `content` encodes one action as JSON. A real OpenAI-compatible HTTP example translates this custom protocol; tests use a clearly labelled fixture command. Unknown usage values remain null. Candidate does not define authoritative resource counters.

### Reference Runner

`python target/agent/run.py` reads one JSON request from stdin and writes one JSON result. Frozen evaluator/proposer supply `agent` config in the request.

Task request: `{mode:"task", task:{task_id,instruction,input_files}, agent:{...}}`.

Task actions: `{"tool":"list"}`, `{"tool":"read","path":"..."}`, `{"tool":"write","path":"...","content":"..."}`, `{"tool":"final"}`. Execute in a new TemporaryDirectory per request; path containment and symlink rejection apply. No shell tool. Return `{status, output_files, trace, skill_hashes, usage, duration_ms}`. Skills are loaded from the runner's own `skills/<name>/SKILL.md`; trace proves actual loaded bytes. No expected_files or test identities are passed to the model.

Propose request: `{mode:"propose", context:{...}, agent:{...}}`. Same runner, same loaded skills; one model call asking for JSON `{diff,hypothesis}`. Return `{diff,hypothesis,trace,skill_hashes,usage,duration_ms}`. `context` contains explicit current-parent target file contents plus training feedback; runner identity may be H0 (frozen) or parent (self-use). It never writes to the parent checkout.

### Evaluation and proposal bridges

Evaluator environment: existing `NANORSI_SPLIT`, `NANORSI_RESULT_PATH`; add `NANORSI_AGENT_CONFIG` JSON, `NANORSI_TASK_MANIFEST` absolute path, `NANORSI_REPEAT_ID`, `NANORSI_TRAIN_LIMIT` (4 for train), `NANORSI_SEED`.

Evaluator reads task manifest; only task input reaches Runner. V2 result has `schema_version:2,status:"ok",metrics:{score:...},constraints:{tests_passed:true},case_results:[...],cost_usd,duration_ms,usage`. Each case contains `task_id,group_id,repeat_id,score,status,trace,skill_hashes,usage,duration_ms`; all cases, including failures, are retained. Mean is task-macro (one repeat per evaluator invocation). Valid v1 result parsing remains compatible.

Proposer reads existing context/env paths and `NANORSI_PROPOSER_HARNESS` (absolute directory holding the selected `target/agent/run.py`). Parent checkout is cwd, so current target files come from cwd, not necessarily the proposer harness. Context contains `agent`, `train_results` and `parent_commit`, `proposer_harness_commit`, `goal`, `surface`; no validation/test outcomes. Writes existing `proposal.diff`, `hypothesis.json`, plus `usage.json` and `trace.json`. Core persists complete output hashes, including metadata for failed proposals where available.

### Search state

Baseline pins config, manifest and protected driver bytes to an immutable manifest hash. Every operation checks live protected inputs against baseline. V2 train/validation/test invocation uses snapshot-bound commands and manifest, not mutable cwd data.

Each proposal attempt gets an ID regardless of decision; acceptance increments generation only. Record attempt start before external execution; record result afterward; dangling starts from killed runs count against budget and are converted to interrupted on recovery. Nonaccepted candidates never become parent or proposer. Score equality/no-op retains parent.

Events reference artifacts as `{path,sha256}` relative to workspace; lineage verify checks them. All score decisions use configured primary metric without renaming it to score. Evaluator fingerprint is attached to every generation.

V2 `baseline`: validation only. V2 `step`: train, proposal, parent/child paired validation; no final test. `run`: bounded repeated step calls until attempts or episode allowance exhausted (failures consume allowance). `freeze`: records H0 and selected candidate plus manifest, blocks further search. `final-test --repeats 3`: only after freeze, evaluates H0, no-skills H0 and final candidate with fresh episodes; output separate final report, never promotion. Finished results are idempotent; partial runs are identifiable and resumable without hiding costs. Legacy heldout remains explicitly legacy selection data.

## Task 1 — process and evaluator contracts (child A)

Ownership: `src/nanorsi/process.py`, `src/nanorsi/evaluator.py`, `tests/test_process.py`, `tests/test_episode_contract.py` only.

- [x] Write tests showing output limits, process-tree timeout cleanup and invalid finite/nonnegative usage fail.
- [x] Extend `ProcessResult` with `output_limited: bool=False`, `duration_ms:int=0`; preserve existing positional construction.
- [x] Extend `run_argv(..., max_output_bytes=1_000_000, input_text=None)`; bounded stdout/stderr streaming, terminate process group on timeout/overflow (POSIX, Windows fallback), safe environment unchanged. Do not wait forever for descendants holding pipes.
- [x] Extend `EvaluationResult` with `usage:dict` and preserve six original fields and v1 parser.
- [x] Strictly validate v2 case/usage fields and unique task/repeat IDs, finite scores and nonnegative costs. Cases required/nonempty for v2. Do not treat null usage as zero.
- [x] Extend `run_evaluation(..., extra_env=None)` and pass config budget output cap to process; do not change config.
- [x] Run targeted tests and report red/green evidence.

Contract smoke test shape:

```python
result = run_argv([sys.executable, "-c", "print('x'*1000000)"],
                  cwd=root, timeout_s=2, max_output_bytes=100)
self.assertTrue(result.output_limited)
self.assertLessEqual(len(result.stdout.encode()) + len(result.stderr.encode()), 100)
```

## Task 2 — reference skills Runner and bridges (child B)

Ownership: new `src/nanorsi/templates/skills/target/**`, `.../proposer/**`, `.../evaluator/**`, `.../adapters/**`, `tests/test_skills_runner.py` only. Parent creates config, manifest and package registration.

- [x] Write fake-model subprocess tests for actual skill loading, multi-action read/write, traversal rejection, clean episodes, model timeout/invalid output, propose output.
- [x] Implement the fixed custom protocol above, standard library only, no shared core imports required inside exported workspace.
- [x] Implement evaluator with private labels withheld from Runner, exact-file grader and all case traces/usage included.
- [x] Implement proposer fixed driver selecting Runner from `NANORSI_PROPOSER_HARNESS` while editing current parent contents.
- [x] Implement real HTTP bridge, explicitly configured model endpoint/key file. Do not make actual network calls in tests.
- [x] Include concise inspect/edit/verify skills; no answer tables or pre-baked correct task output in default proposer.
- [x] Run targeted tests and report red/green evidence. No template registry/config edits.

## Task 3 — task generator and comparison (child C)

Ownership: `examples/local_tasks/prepare.py`, `examples/compare.py`, `examples/README.md`, `tests/test_comparison.py` only.

- [x] Write tests for deterministic generation, unique tasks/groups and disjoint splits; compare tests for task-macro aggregation, pairing and unknown cost coverage.
- [x] `prepare.py OUTPUT` writes the fixed manifest contract above, 30 tasks/split, varied exact textual replacements and evidence-driven instruction, no third-party dependency. Deterministic stable source groups; no identical source fixture across splits.
- [x] `compare.py REPORT...` reads final-report JSON format `{schema_version:2,manifest_hash,experiment_id,arm,seed,results:[{condition:"baseline"|"no-skills"|"candidate",repeat_id,case_results,cost_usd,duration_ms}]}`; verify compatible task sets for paired endpoints. Summarize task-macro condition score and delta_pp, all observed cost and coverage, individual seeds. Reject missing/duplicate condition task/repeat pairs.
- [x] Keep bootstrap optional simple group-paired resampling with deterministic seed if implemented; never claim significance from three seeds. No plots/UI/dependencies.
- [x] Document that fixture tasks are protocol exercises, not a public benchmark result.

## Task 4 — integration and lifecycle (parent)

Ownership: `config.py`, `cli.py`, `loop.py`, `proposer.py`, `gate.py`, `lineage.py`, `report.py`, `templates.py`, `doctor.py`, skills template TOML/manifest/gitignore/README, lifecycle tests and integration changes.

- [x] Baseline current 31 tests, then regressions for accepted→rejected→accepted and non-score metric.
- [x] Implement strict config v2, immutable identity and attempts/episodes bookkeeping, correct v1 multi-round fingerprint and primary metric handling.
- [x] Keep bounded loop explicit, output references verifiable, crashed attempts recorded, freeze/test selection boundaries enforced.
- [x] Register new template and package all JSON/Markdown/script files. Preserve scripted legacy demos.
- [x] Test training-only context, snapshot-bound model identity, budget reservation before calls, frozen versus self-use Runner hashes, freeze rejection of continued search, test results never promoting.
- [x] Integrate child outputs, inspect each diff, run protocol and end-to-end tests.

## Task 5 — maintenance and final verification

- [x] Update charter, specification, READMEs, SECURITY, changelog and CI for implemented behavior; distinguish local trust from true isolation and fixture from live-model validation.
- [x] Independent spec review, then quality/security review with bounded child tasks; fix confirmed issues before final checks.
- [x] Full unittest; AST compile/static architecture checks; `git diff --check`; package wheel/install smoke using available build tools, without adding dependencies.
- [x] Run offline v2 five-attempt lifecycle including freeze/test and compare, plus legacy commands. A real model bridge remains ready for configured endpoint; no fabricated live gains.
- [x] Commit coherent Lore decision records; leave clean feature branch and switch original checkout to it after removing clean temporary worktree.

## Acceptance evidence

Completion means working v2 protocol and reference executable integration, regression coverage, honest limitations and coherent repository state. Measured improvement on a paid model, three independent live evolution runs, a public benchmark reproduction and a hardened container adapter are follow-up experiments, not results to invent or silently claim.

## Progress

- Planning: complete; initial design committed as `a7a7e98`.
- Baseline: 31 existing tests passed before implementation.
- Child lanes: execution/evaluation, reference Runner/bridges, task generation/comparison completed with `gpt-5.6-luna`, `xhigh` and isolated prompts.
- Reviews: independent process, Runner, comparison and lifecycle spec/quality passes completed. Confirmed findings received regression tests and fixes.
- Final verification: 81 tests passed; AST compilation, architecture limits and whitespace passed; built and independently installed the v0.2 wheel; five-attempt fixture run, freeze, three-condition final-test, verify, comparison and legacy artifact smoke passed.
- Core size: 1,771 lines across 17 modules; no added runtime dependencies.
- Maintenance: release docs, CI starter checks and v0.2 version metadata synchronized. Implementation is committed locally and moved back to the original checkout as part of handoff; no remote push is performed.

## Implementation clarifications

- `new skills` is the new reference template. The previous scripted harness remains a compatibility demo.
- The fixed comparison identity is separate from the full manifest hash because arm and seed legitimately differ across comparison runs.
- Train sampling is deterministic for the configured seed; actual reserved task identities are checked exactly.
- Interrupted search attempts require recovery before freeze. An incomplete final panel remains an explicit failure rather than being silently retried to improve its score; successful final panels are idempotent.
- The reference model adapter supports keyless compatible local endpoints or an explicitly configured external credential file. It uses JSON actions over ordinary chat messages, with a tested local HTTP roundtrip.
- Runtime script execution, vector retrieval, a hardened container adapter, paid-model performance claims and multi-seed public-benchmark reproduction remain out of this implemented release. There are no fabricated gains; fake-model tests are labelled as protocol fixtures.
