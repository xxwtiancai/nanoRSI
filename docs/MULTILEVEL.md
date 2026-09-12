# Executable improvement at several levels

[简体中文](MULTILEVEL.zh-CN.md) · [First run and API keys](QUICKSTART.md) · [Kernel contract](specification.md)

nanoRSI v0.4 runs bounded improvement experiments on programs, agent runners, skills and model parameters. Each experiment records what changed, whether validation accepted it, and what the frozen version did on separate test tasks. Recursive reuse and population search are additional experiment choices; neither establishes general recursive self-improvement by itself.

## Choose what changes

| Starter | Kernel mode | Mutable target | What executes |
| --- | --- | --- | --- |
| `artifact` / `program` | `artifact`, schema 2 | `target/program.py` | Python reads JSON records and produces a summary; a configured LLM proposes source changes |
| `harness` / `agent` | `harness`, schema 2 | `target/agent/run.py` | A local agent schedules dependent tools; an LLM proposes changes to its runner |
| `skills` | `harness`, schema 2 | `target/agent/skills/**` | An LLM edits files using Markdown guidance and any declared executable skills |
| `coding` | `harness`, schema 2 | `target/agent/skills/**` | An LLM repairs Python utilities and runs public tests; private tests grade behavior |
| `model` / `learner` | `model`, schema 2 | `target/**`, including a saved checkpoint and training recipe | A protected trainer updates a tiny classifier on CPU; no model API is needed |

The canonical starters are `artifact`, `harness` and `model`; `program`, `agent` and `learner` are aliases. The explicit `artifact-fixture`, `harness-fixture` and `model-contract` names preserve schema-1 examples and command contracts. Existing schema-1 workspaces still run.

## Run one complete experiment

With Python 3.11+, Git and nanoRSI installed, a CPU learning experiment needs no credentials:

```bash
nanorsi new model ./learner-lab
nanorsi baseline --workspace ./learner-lab
nanorsi run --workspace ./learner-lab
nanorsi freeze --workspace ./learner-lab --repeats 1
nanorsi final-test --workspace ./learner-lab
nanorsi report --workspace ./learner-lab --format html
nanorsi verify --workspace ./learner-lab
```

For a live program experiment, create `nanorsi new artifact ./program-lab`, configure the provider before baseline, and use the same remaining commands with that workspace. The agent starter works the same way. [The first-run guide](QUICKSTART.md) explains API access, external credential files, connection checks and budgets. A chat-product subscription or login does not configure an API endpoint automatically.

For an account that has access to Z.ai's Coding Plan endpoint, configuration can be:

```bash
nanorsi configure --workspace ./program-lab \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key --thinking disabled \
  --max-steps 2 --max-episodes 200
nanorsi doctor --workspace ./program-lab --check-model
```

Use your own external key-file path and an exact model ID available to your account. A successful connection probe establishes access, not improvement. The probe makes one bounded provider request outside experiment accounting. Configuration is offline and becomes immutable when the experiment journal starts.

## What the learning demo actually trains

The learner is a four-feature, three-class softmax classifier on overlapping synthetic numeric clusters. Its JSON checkpoint contains real numerical parameters. Each attempt starts from the accepted checkpoint, applies the proposed recipe, runs `trainer/train.py`, and commits the resulting checkpoint before validation. Rejected training runs keep their evidence and do not replace the accepted model.

| Method | Actual update |
| --- | --- |
| `sft` | Minibatch cross-entropy gradients update the full weight matrix |
| `rl` | Sampled actions receive an environment reward; REINFORCE with a running baseline updates the policy |
| `lora` | Cross-entropy gradients update rank-two factors A and B while the base weight matrix stays frozen |

This is a teaching-scale parameter-learning experiment, not LLM fine-tuning. The tiny LoRA factors contain 16 parameters versus 15 in the base matrix, so this example demonstrates the update mechanism and makes no parameter-efficiency claim.

Run the default 18-trial panel—three methods × three seeds × frozen/self-use proposer controls—through the ordinary CLI:

```bash
python examples/parameter_learning/run.py ./parameter-results
```

The output directory must be new. The driver retains every command outcome, workspace, accepted/rejected attempt and final report, then writes `summary.json`. In the verified 18-run panel, all runs completed: 54 training rounds produced 20 accepted and 34 rejected candidates. Audits checked parent-checkpoint links, train-data hashes, frozen LoRA base weights and final checkpoint identity. No API calls were made; monetary cost was not measured.

| Method | Initial test accuracy | Selected, frozen proposer | Selected, self-use proposer |
| --- | ---: | ---: | ---: |
| SFT | 46.11% | 85.83% | 85.83% |
| REINFORCE | 46.11% | 85.56% | 86.39% |
| LoRA | 46.11% | 85.00% | 84.44% |

These are means across three independent evolution seeds per cell on this synthetic task. Accuracy differences are percentage points, not relative percent improvement. The nine matched self-use comparisons yielded one positive difference, one negative difference and seven ties. Parameter learning improved this small task; a consistent recursive advantage was not demonstrated.

## Recursive reuse must do work

Set `experiment.arm` before baseline. `frozen` uses the initial proposer harness; `self-use` uses the latest accepted harness. Both produce changes against the current parent. A source hash proves which file loaded, but does not prove that the changed behavior affected the proposal.

In the harness, `plan_steps` is shared by task execution and proposal-time analysis of training workflows. `run_propose` executes the selected harness's planner and adds step order, dependency checks and blocked steps to the feedback sent to the LLM. A `proposal_planner_used` trace records the actual output. An improved planner can therefore change the next proposal's input, rather than merely produce a new source hash.

In the learner, the chosen proposer checkpoint computes losses on the allowed training-feedback examples. Those losses choose difficult examples to receive three times the sampling weight in the next training recipe. Frozen and self-use therefore differ in the checkpoint used to construct a curriculum; both still train from the current accepted checkpoint. This isolates checkpoint-guided curriculum reuse from ordinary repeated gradient training.

Use separate workspaces for control arms, match tasks, initial state, inference and search budgets, and freeze all arms before inspecting final results. A self-use run alone cannot establish that recursive reuse helped.

## Executable skills

A declared skill can contain both `SKILL.md` and `run.py`. Its instructions explain the arguments; the runner exposes a `skill` action only when that declared script exists. The model calls, for example:

```json
{"tool":"skill","name":"edit","arguments":{"old":"old_name","new":"new_name"}}
```

The fixed script path is `target/agent/skills/edit/run.py`. It receives JSON stdin containing an absolute episode `workspace` and the `arguments` object, and returns one JSON object. The runtime records the invoked source hash and enforces a two-second process limit and 1 MB output limit. Arguments are defined by the skill; the example above requires a script implementing that interface. Model actions cannot choose arbitrary command lines. Candidate scripts remain trusted local code.

The live skills demo asks the model to create a reusable batch-edit script under a four-action task budget. Its evidence can show whether the learned script was actually invoked and whether it generalized to separate edits. Merely creating a Markdown file or a script is not a measured capability gain.

## Population search and HTTP workers

To search branches instead of one serial candidate chain:

```bash
nanorsi population --workspace ./program-lab --size 3 --generations 2 --workers 2
```

Run this before freeze, after configuring sufficient attempt and episode budgets. The coordinator reserves budget before launching local candidate workers, retains the validation-ranked top K and can propose draft, improve, debug and crossover candidates. Crossover receives bounded mutable source from another parent; the recorded candidate DAG identifies both parents. The Git commit still has one source parent. Only the coordinator appends the root HMAC journal and promotes an incumbent. `recover` records interrupted work and reconciles reservations; interruption does not grant free retries.

Population concurrency uses local threads and isolated candidate worktrees. The separate [HTTP worker example](../examples/remote_workers/README.md) demonstrates authenticated evaluation with two real localhost worker processes. It has request/source/manifest/evaluator identity checks and can be used by the ordinary CLI. Multi-host deployment, distributed training and containment of hostile code have not been validated.

## Reproduce the live demonstrations

```bash
python examples/demos/run.py ./live-results \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key --max-requests 60
```

The default kinds are `program`, `agent`, `recursive`, `skills`, `population` and `remote`; use `--kinds` to select a subset. The remote demo automatically starts and stops two localhost worker processes. The driver uses live model proposals, caps provider request starts, serializes provider access through a shared ledger, freezes searches before final evaluation, and retains failed, unchanged and negative outcomes. A request cap is not a dollar cap. The output includes `plan.json`, `requests.jsonl`, per-workspace reports and `summary.json`.

Program and agent task execution is local Python; the LLM supplies improvement proposals. The skills demo also calls the LLM during task execution. These tasks measure different things: do not average them into one “RSI score.” Use their own frozen baseline/candidate panels and preserve metric direction. Proportion scores can be reported in percentage points; losses retain native units.

## Read the result before making the claim

Schema-2 artifact, harness and model starters compare `baseline` and `candidate`; skills/coding also include `no-skills`. Freeze binds the conditions, selected commits, metric direction and repeat count. Final evaluation reads the saved checkpoints without retraining and cannot influence selection. A better validation score is a search result until the frozen test panel completes.

These small authored demonstrations establish executable mechanisms and task-specific observations. They do not establish broad benchmark superiority, statistical significance, unrestricted self-modification or solved general RSI. Reports should include the task, seeds, controls, budget, failures and evidence that supports the measured result.

The project independently implements ideas from executable research systems, including OpenRSI's bounded MLE meta-evolution setting. OpenRSI is not evidence that unrestricted general RSI is solved. No OpenRSI source code is copied into this Apache-2.0 project; its CC-BY-NC licensing is not treated as an Apache-compatible code license.
