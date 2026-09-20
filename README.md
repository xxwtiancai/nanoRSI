<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI — Small code. Measurable change." width="100%">
</p>

<p align="center"><strong>A minimal recursive self-improvement (RSI) lab you can read.</strong><br>Run the change. Measure it on unseen tasks.<br>Paired with a daily RSI research radar.</p>

<p align="center">
  <a href="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml"><img src="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.11+"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/runtime_dependencies-0-f4512c" alt="Zero third-party runtime dependencies"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.4.1-f4512c" alt="Version 0.4.1"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-171717" alt="Apache-2.0 license"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#real-tasks-ported-from-upstream-rsi-projects">Real tasks</a> ·
  <a href="#how-it-works">How it works</a> ·
  <a href="#bring-your-model">Bring your model</a> ·
  <a href="#research-with-it">Research</a> ·
  <a href="docs/research/industry-rsi/RADAR.md">Daily radar</a> ·
  <a href="docs/research/industry-rsi/README.md">Research map</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

---

You changed the program, the agent, or its weights. Did it actually get better?

**nanoRSI** turns that question into a small executable experiment. Run tasks, collect feedback, propose a change, and compare the candidate with its parent. In model mode, actually train and save the parameters. Keep qualifying changes, then freeze your choices and test on separate tasks.

| Small enough to read | Several things to improve | Built for inspection |
| :---: | :---: | :---: |
| **5,000-line core ceiling** | **Artifacts · harnesses · parameters** | **Every attempt** leaves evidence |
| Standard library + Git | Serial or population search | Patches, checkpoints, traces and costs |

## Mission

nanoRSI is two things under one name:

1. **A minimal, runnable RSI implementation.** Improve a program, an agent harness, reusable skills or model parameters, then validate every change on minimal tasks against frozen, uniform and random controls. The framework must stay runnable end to end and stay aligned with the mechanisms current enterprise and university RSI frameworks actually use — high-star open projects such as OpenRSI, SEAL, DGM and OpenEvolve are tracked as references, with licenses checked before anything is borrowed.
2. **A daily RSI research radar.** Every day at midnight an automated sweep verifies and files new RSI results from authoritative sources worldwide — arXiv, company research pages, domestic and international university labs, conference and journal outputs, and high-star GitHub projects — into one unified catalogue format, logged in the [daily radar](docs/research/industry-rsi/RADAR.md).

[Radar findings become prioritized experiments](docs/research/industry-rsi/ADOPTION.md); experiment results feed back into what the radar watches. Neither track claims general RSI is solved; evidence limits stay part of every record.

New to RSI? [The minimal mechanism set](docs/RSI_MINIMAL.md) explains the concept in five minutes, and `python examples/smoke/run_smoke.py` runs the entire loop offline — no API key.

## What can improve?

| Start with | What actually changes | Try it |
| --- | --- | --- |
| **Artifact** | An executable Python program; a live LLM proposes source improvements | `nanorsi new artifact ./program-lab` |
| **Harness** | An agent's executable workflow planner and runner | `nanorsi new harness ./agent-lab` |
| **Model** | Real numerical parameters trained with SFT, REINFORCE or LoRA on CPU | `nanorsi new model ./learner-lab` |
| **Skills / coding** | Reusable Markdown guidance and declared `run.py` skills used by an LLM agent | `nanorsi new coding ./coding-lab` |

`program`, `agent` and `learner` are aliases for artifact, harness and model. All use the same baseline → search → freeze → final-test lifecycle. Frozen/self-use proposer controls and bounded population search let you study how improvements are produced. [The multilevel guide](docs/MULTILEVEL.md) explains the actual execution, comparisons and limits · [中文](docs/MULTILEVEL.zh-CN.md).

The bundled tasks are small authored demonstrations, not broad capability benchmarks. The parameter example is a tiny classifier, not LLM fine-tuning. Executable recursive mechanisms do not by themselves prove a recursive advantage or solve general RSI.

## Quick start

Clone and install with Python 3.11+ and Git:

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Start with **real CPU parameter learning**. It makes no model API calls:

```bash
nanorsi new model ./learner-lab
nanorsi baseline --workspace ./learner-lab
nanorsi run --workspace ./learner-lab
nanorsi freeze --workspace ./learner-lab --repeats 1
nanorsi final-test --workspace ./learner-lab
nanorsi report --workspace ./learner-lab --format html
nanorsi verify --workspace ./learner-lab
```

Open `learner-lab/reports/report.html`. It compares the initial and selected saved checkpoints on frozen test cases; final evaluation does not retrain them. For API-driven artifact, harness or coding experiments, configure the model before baseline using the first-run path below.

**[First model run: API key → connection check → experiment → report](docs/QUICKSTART.md)** · [中文入门](docs/QUICKSTART.zh-CN.md)

## Real tasks ported from upstream RSI projects

nanoRSI does not only run its own authored demos. Complete evaluation tasks from high-star open RSI projects were ported — licenses checked, initial programs preserved verbatim under attribution headers — and executed end to end on this platform with real model calls, real gate decisions and frozen final panels:

| Ported task | From | Model | Calls | Initial → selected | Evidence |
| --- | --- | --- | ---: | ---: | --- |
| Function minimization | [OpenEvolve](https://github.com/codelion/openevolve) (Apache-2.0) | GLM-5.3-Flash | 5 | 0.9418 → 0.9960 | [Study](examples/results/openevolve-fnmin/README.md) |
| Sine approximation | [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) (Apache-2.0 · arXiv 2509.19349) | GLM-5.3 | 5 | 0.1049 → 0.999963 (RMSE 4.0e-06) | [Study](examples/results/glm53-real-tasks/README.md) |
| K-module configuration | [OpenEvolve](https://github.com/codelion/openevolve) (Apache-2.0) | GLM-5.3 | 8 | 0/4 → 4/4 modules | [Study](examples/results/glm53-real-tasks/README.md) |

<p align="center"><img src="docs/assets/readme/real-tasks-results.svg" alt="Paired bars: on every ported task, the evolved candidate's bar reaches far beyond the initial program's; frozen final-test scores." width="100%"></p>

Every accepted candidate passed the strict-improvement gate against its parent on validation, then faced a frozen unseen final panel. Failed and rejected attempts stay in the published record: the sine run needed two repairs of corrupt model diffs before its Taylor-series candidate, the k-module winner was a first-generation direct candidate (population crossover produced no winner). A separate [rejected-memory A/B study](examples/results/rejected-memory-ab/README.md) honestly reports a null result.

These are independent nanoRSI runs of upstream tasks, **not** reproductions of upstream author-reported results; each study page lists its seeds, budgets, audits and limits. [Regenerate the chart](docs/assets/readme/render-real-tasks.py) · [All published studies](examples/results/).

## Evaluation standard and internal studies

Showcased experiments follow the evaluation protocols of the RSI literature: tasks and metrics come from established upstream suites (or community-standard benchmarks), scores are reported on frozen held-out panels, and every failure stays in the record. New experiments target common validation sets — the candidates and protocol notes live in [ADOPTION.md](docs/research/industry-rsi/ADOPTION.md).

Earlier platform work predates this standard and is **not benchmark evidence**: the [v0.4.0 live study](examples/results/v0.4.0/README.md) (self-authored four-case smoke panels and a known parser counterexample), the [handwritten-digits study](examples/results/recursive-digits-v0.4.1/README.md) (a custom, non-official split of the UCI digits subset with matched controls), the [skills transfer study](examples/results/live-skills-frozen-selfuse/README.md) (authored tasks; self-use tied the frozen proposer) and the [v0.4.0 CPU panel](examples/results/v0.4.0/README.md#cpu-parameter-learning) (synthetic clusters) remain published unchanged as platform-validation and controlled-ablation records — retained for honesty, not presented as effect claims.

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

Open `coding-lab/reports/report.html`. Compare **initial skills**, **no skills** and **selected skills** on the same frozen task/repeat pairs. During each task, the model repairs a fresh Python file and can run public tests. Across coding attempts, persistent skill files evolve, including declared executable scripts when proposed; model weights, task data and the evaluator stay fixed. Task-code repairs and skill patches are separate outputs. A rejected patch or no final gain is a valid result.

This one-attempt preset uses up to **16 search episodes + 12 final-test episodes**, with up to eight model calls per episode and one additional proposal call. Final testing is outside the search cap; episode limits are not a dollar cap. No model yet? Run `python examples/coding_tasks/prepare.py --check` to validate the authored task pack offline.

**[Complete first-run tutorial: API key → connection check → RSI loop → report](docs/QUICKSTART.md)** · [中文入门](docs/QUICKSTART.zh-CN.md) · [Task format](docs/CODING_LAB.md)

## How it works

<p align="center"><img src="docs/assets/readme/experiment-loop.svg" alt="Train: run tasks and propose a skill patch. Validate: compare parent and candidate, then keep or reject. After search: freeze and test unseen tasks without feedback to selection." width="100%"></p>

Training feedback helps write the next change; model mode also runs the protected trainer before evaluation. Validation chooses which version survives. Final-test results stay out of that selection loop.

Failed, rejected and unchanged proposals still consume the attempt budget. Every accepted version has an exact parent and candidate commit, so the experiment remains traceable.

## Bring your model

The coding starter above is one complete model-backed path. Use `artifact` to improve a program or `harness` to improve its agent runner with the same configuration flow. Follow the [provider/key setup guide](docs/QUICKSTART.md#2-get-api-access-and-choose-an-endpoint) to use OpenAI, OpenRouter, DeepSeek or a local compatible server. The bundled bridge uses `/chat/completions`; native Anthropic Messages and OpenAI Responses require a custom adapter. It does not automatically read API-key environment variables or `.env` files.

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

In skills/coding workspaces, `target/agent/skills/**` is mutable. The runner loads Markdown guidance and uses list/read/write/final actions in fresh task directories. Declared skills may include `run.py`; a bounded `skill` action invokes that exact script and records its source hash. Other starters declare their own narrow mutation surface.

[Full walkthrough](docs/QUICKSTART.md) · [All contracts and states](docs/specification.md)

</details>

## Research with it

Different questions need separate comparisons:

| Question | Comparison |
| --- | --- |
| Do these skills help? | No skills vs. initial skills |
| Did evolution help on new tasks? | Initial vs. selected program, harness, skills or checkpoint on the frozen test set |
| Does recursive reuse add anything? | Frozen proposer vs. self-use proposer, with matched settings and budgets |
| Does population search help? | Serial vs. population search on the same task with matched budgets |

`arm = "frozen"` always proposes through the initial harness. `arm = "self-use"` proposes through the latest accepted harness. Both modify the current parent. The harness planner also preprocesses training feedback during proposal generation; the learner checkpoint computes a curriculum for subsequent training. Use separate workspaces and freeze all arms before examining final results.

The skills comparison tool reports paired task-macro deltas, per-arm results, episode timing and cost coverage. Each other mode has its own frozen report; heterogeneous demos are not one RSI score. Independent evolution runs and repeated deployments are kept distinct. A negative result is still useful evidence.

Our [evaluation research notes](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md) cover DGM, SICA, GEPA, ACE, Memento-Skills and recent skills benchmarks. The small, readable project philosophy draws inspiration from [nanoGPT](https://github.com/karpathy/nanoGPT) and [nanochat](https://github.com/karpathy/nanochat).

## RSI research radar (updated daily)

**[Read the daily radar log](docs/research/industry-rsi/RADAR.md)** · [Browse the research map](docs/research/industry-rsi/README.md) · [中文](docs/research/industry-rsi/README.zh-CN.md)

Each day at midnight an automated sweep covers arXiv preprints (cs.AI/cs.LG/cs.CL/cs.MA), official results from OpenAI, Google DeepMind, Anthropic, Meta, Microsoft, Salesforce, Sakana AI, Alibaba, ByteDance, Tencent, DeepSeek, Frontis/Tsinghua and other companies, labs at Tsinghua, Peking, SJTU, Zhejiang, USTC, HKUST, MIT, Stanford, CMU and Berkeley, NeurIPS/ICML/ICLR/ACL/CVPR and other venues, high-star GitHub RSI projects, and authoritative media reports used strictly as leads that must trace back to an original source. Verified findings enter the catalogue in one unified format; the day's sweep and its coverage gaps are logged in the radar log, including honest "no qualified new findings" days.

The collection separates parameter/data learning, agent/code evolution, memory/context updates and automated research. Each entry explains the feedback loop, author-reported results, comparison conditions, code/weights/data licenses and evidence limits, with a locally stored source figure, official research image or source-page screenshot and direct links to verified open materials where available.

Direct bounded loops, enabling techniques and assisted R&D are labeled separately. The catalogue preserves original publication dates and negative findings; it does not represent local reproduction or a combined RSI leaderboard. Use the [five-minute research quickstart](docs/research/industry-rsi/QUICKSTART.md), [landscape and taxonomy](docs/research/industry-rsi/LANDSCAPE.md), and [open-materials index](docs/research/industry-rsi/OPEN_MATERIALS.md) before diving into the case pages. [Research-informed experiment priorities](docs/research/industry-rsi/ADOPTION.md) connect the findings to concrete nanoRSI work.

## Where to look next

| I want to… | Start here |
| --- | --- |
| Understand RSI fast | [Minimal mechanism set](docs/RSI_MINIMAL.md) · [Offline smoke](examples/smoke/run_smoke.py) |
| Run my own experiment | [Quickstart and API keys](docs/QUICKSTART.md) · [Multilevel experiments](docs/MULTILEVEL.md) |
| Read the implementation | [The loop](src/nanorsi/loop.py) · [Reference runner](src/nanorsi/templates/skills/target/agent/run.py) |
| Understand the design | [Project charter](docs/PROJECT_CHARTER.md) · [v0.2 design](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md) |
| Prepare tasks or compare runs | [Examples](examples/README.md) |
| Check changes and contribute | [Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) |

**Execution boundary:** the built-in mode is trusted local execution. Optional HTTP evaluation has been demonstrated with two localhost worker processes; multi-host operation remains unverified. Worktrees and receipts provide version checks; private-label isolation for untrusted code requires an external container, VM or service. [Read the security model](SECURITY.md).

<details>
<summary><strong>Development checks and legacy templates</strong></summary>

Install the checkout in your virtual environment first so evaluator subprocesses can import nanoRSI from temporary workspaces.

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

CI checks Python 3.11/3.12 on Linux and macOS. Architecture tests enforce a 5,000-line core ceiling, 300-line files, 50-line functions and no runtime third-party imports.

Use `artifact-fixture` or `harness-fixture` for the legacy scripted offline demos, and `model-contract` for the legacy external-training contract. Existing schema-1 workspaces still run; their heldout data participates in selection. New artifact/harness/model workspaces use schema 2 and an independent final-test phase.

</details>

---

<p align="center"><img src="docs/assets/brand/nanorsi-mascot.png" alt="The nanoRSI terminal robot holding an iteration card" width="110"></p>
<p align="center"><strong>Bring a task. Run an experiment. Share what happened.</strong><br>
If this is the kind of agent research you want more of, <a href="https://github.com/xxwtiancai/nanoRSI">give nanoRSI a star</a>.<br>
<a href="https://github.com/xxwtiancai/nanoRSI/issues">Share an experiment or report a bug</a> · <a href="CONTRIBUTING.md">Contribute</a></p>

<p align="center">Apache-2.0 · <a href="LICENSE">License</a></p>
