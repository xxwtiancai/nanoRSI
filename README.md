<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI — Small code. Measurable change." width="100%">
</p>

<p align="center"><strong>Make coding agents learn from test failures.</strong><br>Evolve reusable skills. Check the improvement on unseen tasks.</p>

<p align="center">
  <a href="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml"><img src="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.11+"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/runtime_dependencies-0-f4512c" alt="Zero third-party runtime dependencies"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.3.1-f4512c" alt="Version 0.3.1"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-171717" alt="Apache-2.0 license"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#bring-your-model">Bring your model</a> ·
  <a href="#research-with-it">Research</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

---

You changed a skill. Did the agent actually get better?

**nanoRSI** turns that question into a small experiment. Run tasks, collect feedback, propose a skill patch, and compare the candidate with the current version. Keep the change only when it passes the gate. Then freeze your choices and test on unseen tasks.

The model weights stay fixed. The skills and harness are what you study.

| Small enough to read | Complete enough to run | Built for inspection |
| :---: | :---: | :---: |
| **<2.5k lines** of Python core | **One** parent, candidate and loop | **Every attempt** leaves evidence |
| Standard library + Git | Training → validation → final test | Patches, traces, decisions and costs |

## Why nanoRSI

- **Executable Python tasks.** Twelve repair tasks with public tests for debugging and separate private tests for behavioral grading. A configurable model bridge and three procedural skills are included.
- **A loop you can understand.** Sequential attempts, ordinary files, exact Git snapshots and a single readable [loop module](src/nanorsi/loop.py).
- **Useful comparisons.** Compare initial skills, no skills and evolved skills. Switch between a frozen and a self-use proposer harness.
- **A report you can share.** Standalone HTML and Markdown show final comparisons, search decisions, failed attempts and known/unknown costs.

The coding suite is an independently authored starter pack, not a published general-purpose benchmark. The existing 90 text-edit tasks remain protocol fixtures. Engineering tests and reference solutions establish correctness of the lab; model gains require actual model experiments.

## Quick start

Clone and install with Python 3.11+ and Git:

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Try the **scripted offline demo** first. It makes no model API calls:

```bash
nanorsi new artifact ./artifact-demo
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi report --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

<p align="center"><img src="docs/assets/readme/terminal-demo.svg" alt="A recorded offline fixture run creates a candidate, accepts it, writes a report and verifies the lineage." width="100%"></p>

<sub>Terminal visualization of an actual scripted fixture run. <a href="docs/assets/readme/demo-transcript.txt">Read the transcript</a> · <a href="docs/assets/readme/demo-evidence.json">Inspect the captured output</a>. Fixture scores demonstrate protocol behavior.</sub>

## Run a coding experiment

**Configure API access before running.** A chat-app login or `export OPENAI_API_KEY=...` alone does not configure nanoRSI. Create an API key in your provider's console, then replace `YOUR_MODEL_ID` with an exact API model ID available to your account. This example uses the [OpenAI API-key console](https://platform.openai.com/api-keys); [other providers and local servers](docs/QUICKSTART.md#2-get-api-access-and-choose-an-endpoint) are supported through compatible chat-completions endpoints.

```bash
nanorsi new coding ./coding-lab --goal "Learn reliable Python repair skills"
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
nanorsi doctor --workspace ./coding-lab --check-model
nanorsi baseline --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

`--prompt-key` reads a hidden terminal input and stores the key outside the workspace; TOML contains only its file path. Alternatively, use `--api-key-file /absolute/external/path` or `--no-api-key` for an unauthenticated local server. Plain `doctor` is offline; `--check-model` makes one bounded model request, which may incur a charge outside experiment accounting. Configure is offline and must run before the experiment journal starts.

Open `coding-lab/reports/report.html`. Compare **initial skills**, **no skills** and **selected skills** on the same frozen task/repeat pairs. During each task, the model repairs a fresh Python file and can run public tests. Across attempts, only persistent Markdown skills evolve; model weights, task data and the evaluator stay fixed. Task-code repairs and skill patches are separate outputs. A rejected patch or no final gain is a valid result.

This one-attempt preset uses up to **16 search episodes + 12 final-test episodes**, with up to eight model calls per episode and one additional proposal call. Final testing is outside the search cap; episode limits are not a dollar cap. No model yet? Run `python examples/coding_tasks/prepare.py --check` to validate the authored task pack offline.

**[Complete first-run tutorial: API key → connection check → RSI loop → report](docs/QUICKSTART.md)** · [中文入门](docs/QUICKSTART.zh-CN.md) · [Task format](docs/CODING_LAB.md)

## How it works

<p align="center"><img src="docs/assets/readme/experiment-loop.svg" alt="Train: run tasks and propose a skill patch. Validate: compare parent and candidate, then keep or reject. After search: freeze and test unseen tasks without feedback to selection." width="100%"></p>

Training feedback helps write the next patch. Validation chooses which version survives. Final-test results stay out of that selection loop.

Failed, rejected and unchanged proposals still consume the attempt budget. Every accepted version has an exact parent and candidate commit, so the experiment remains traceable.

## Bring your model

The coding starter above is the smallest complete path. Follow the [provider/key setup guide](docs/QUICKSTART.md#2-get-api-access-and-choose-an-endpoint) to use OpenAI, OpenRouter, DeepSeek or a local compatible server. The bundled bridge uses `/chat/completions`; native Anthropic Messages and OpenAI Responses require a custom adapter. It does not automatically read API-key environment variables or `.env` files.

For text-edit protocol research, create `nanorsi new skills ./skills-lab`, then use the same `configure` → `doctor --check-model` → `baseline` → `run` → `freeze` → `final-test` → `report` → `verify` sequence with that workspace. Its 90-task manifest is larger: five attempts can use 350 search episodes, and a three-repeat final panel adds 270. [Choose a budget before running](docs/QUICKSTART.md#choose-a-budget-before-running).

Generated model/proposer/evaluator commands use the Python interpreter that created the workspace. Preserve those commands. All settings become fixed once the experiment journal starts; to change the model or endpoint after that, create a fresh workspace.

<details>
<summary><strong>What is inside the workspace?</strong></summary>

```text
skills-lab/
├── target/agent/
│   ├── run.py                 # Small task/propose runner
│   └── skills/
│       ├── inspect/SKILL.md
│       ├── edit/SKILL.md
│       └── verify/SKILL.md
├── proposer/propose.py        # Fixed proposal driver
├── evaluator/evaluate.py      # Fixed task grader
├── adapters/model.py          # Configurable model bridge
├── tasks/manifest.json        # Grouped train/validation/test fixtures
├── nanorsi.toml               # Experiment settings
└── reports/                   # Search evidence and final comparisons
```

Only `target/agent/skills/**` is mutable by default. The reference runner loads Markdown skills and uses list/read/write/final actions in fresh task directories. Script execution and vector retrieval are outside this starter.

[Full walkthrough](docs/QUICKSTART.md) · [All contracts and states](docs/specification.md)

</details>

## Research with it

Three questions deserve three separate comparisons:

| Question | Comparison |
| --- | --- |
| Do these skills help? | No skills vs. initial skills |
| Did evolution help on new tasks? | Initial vs. selected skills on the frozen test set |
| Does recursive reuse add anything? | Frozen proposer vs. self-use proposer, with matched settings and budgets |

`arm = "frozen"` always proposes through the initial harness. `arm = "self-use"` proposes through the latest accepted harness. Both modify the current parent. Use separate workspaces and freeze all arms before examining final results.

The comparison tool reports paired task-macro deltas, per-arm results, episode timing and cost coverage. Independent evolution runs and repeated deployments are kept distinct. A negative result is still useful evidence.

Our [evaluation research notes](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md) cover DGM, SICA, GEPA, ACE, Memento-Skills and recent skills benchmarks. The small, readable project philosophy draws inspiration from [nanoGPT](https://github.com/karpathy/nanoGPT) and [nanochat](https://github.com/karpathy/nanochat).

## Where to look next

| I want to… | Start here |
| --- | --- |
| Run my own experiment | [Quickstart and budgets](docs/QUICKSTART.md) |
| Read the implementation | [The loop](src/nanorsi/loop.py) · [Reference runner](src/nanorsi/templates/skills/target/agent/run.py) |
| Understand the design | [Project charter](docs/PROJECT_CHARTER.md) · [v0.2 design](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md) |
| Prepare tasks or compare runs | [Examples](examples/README.md) |
| Check changes and contribute | [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) |

**Execution boundary:** the built-in mode is trusted local execution. Worktrees and receipts provide version checks; private-label isolation for untrusted code requires an external container, VM or service. [Read the security model](SECURITY.md).

<details>
<summary><strong>Development checks and legacy templates</strong></summary>

```bash
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

CI checks Python 3.11/3.12 on Linux and macOS. Architecture tests enforce a 2,500-line core ceiling, 300-line files, 50-line functions and no runtime third-party imports.

Legacy artifact/harness templates remain scripted offline demos. Model mode remains an external training contract. Legacy heldout data participates in selection; v2 experiments start in fresh workspaces with an independent final-test phase.

</details>

---

<p align="center"><img src="docs/assets/brand/nanorsi-mascot.png" alt="The nanoRSI terminal robot holding an iteration card" width="110"></p>
<p align="center"><strong>Bring a task. Run an experiment. Share what happened.</strong><br>
If this is the kind of agent research you want more of, <a href="https://github.com/xxwtiancai/nanoRSI">give nanoRSI a star</a>.<br>
<a href="https://github.com/xxwtiancai/nanoRSI/issues">Share an experiment or report a bug</a> · <a href="CONTRIBUTING.md">Contribute</a></p>

<p align="center">Apache-2.0 · <a href="LICENSE">License</a></p>
