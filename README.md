<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI — Small code. Measurable change." width="100%">
</p>

<p align="center"><strong>A minimal, auditable recursive harness-improvement loop.</strong><br>
A frozen model. An editable harness around it. A recursion that proposes, probes, contrasts and composes — and only judges after a freeze.</p>

<p align="center">
  <a href="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml"><img src="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.11+"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/runtime_dependencies-0-f4512c" alt="Zero third-party runtime dependencies"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.5.0-f4512c" alt="Version 0.5.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-171717" alt="Apache-2.0 license"></a>
</p>

<p align="center">
  <a href="#quick-start">Quick start</a> ·
  <a href="#the-loop">The loop</a> ·
  <a href="#attach-a-real-executor">Real executor</a> ·
  <a href="#results">Results</a> ·
  <a href="docs/research/RSI_NOTES.md">Research notes</a> ·
  <a href="README.zh-CN.md">简体中文</a>
</p>

---

nanoRSI v0.5 is a from-scratch, standard-library implementation of the recursion in
**Harness²** (Google Cloud AI Research, [arXiv 2610.14224](https://arxiv.org/abs/2610.14224)):
keep the model frozen, make the *harness* around it editable, and improve the harness
from execution evidence without a verifier in the loop. The whole core is sixteen
modules and about 1,400 lines; every rollout, proposal, contrast, composition and
judgement is a hash-chained ledger event.

| What is editable | How edits are admitted | What stays honest |
| --- | --- | --- |
| system prompt · guardrails · memory · tool guidance · skills · scripts | matched-configuration probe → `mitigates` / `neutral` / `regresses` contrast, no ground truth | scores exist only after `freeze`; budgets charged per call; ledger `verify` fails on any rewrite |

Two tracks live under this name. The **engineering track** is this loop. The
**research track** is a daily living document of RSI papers, classified on the two axes
of the 1,250-paper RSI survey: [docs/research/RSI_NOTES.md](docs/research/RSI_NOTES.md).

## Quick start

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git && cd nanoRSI
python3 -m venv .venv && source .venv/bin/activate && pip install -e .

nanorsi new ./lab --goal "Improve the harness for document work"
nanorsi configure --workspace ./lab --model YOUR_MODEL --base-url https://api.example.com/v1 \
  --api-key-file ~/.nanorsi/keys/provider.key        # the key stays outside the workspace
nanorsi doctor --workspace ./lab --check-model

nanorsi evolve --workspace ./lab      # base → INV/DOM proposals → probes → contrasts → compose → final, per task
nanorsi freeze --workspace ./lab      # pin the chosen harness per task; evolve is refused afterwards
nanorsi judge  --workspace ./lab      # score base and final deliverables with the workspace judge
nanorsi report --workspace ./lab && nanorsi verify --workspace ./lab
```

The starter ships a four-file base harness, two offline document tasks the built-in
agent can execute, and a keyword judge — so the full lifecycle runs on any
OpenAI-compatible endpoint with no benchmark installed.

## The loop

```text
per task                                       mode agg (parallel, width)      mode seq (sequential, depth)
  base1  ── reference rollout                  k pairs probed vs the base,     k rounds; each composition
  INV    ── one cross-domain edit  ─┐          then k compositions             becomes the next base
  DOM    ── one domain edit        ─┤ probe each under matched config
  contrast ─ mitigates/neutral/regresses per probe (no scores)
  compose  ─ adopt / merge / keep, every decision tied to an observation
  final    ─ rollout of the composed harness (a keep reuses the reference)
  select   ─ blind choice over anonymised deliverables when finals > 1
  lesson   ─ one evidence-backed entry into the workspace library
```

Everything above is a ledger event with its token usage; `reports/report.md` is a derived
view. The paper's two remaining components, subagents and plugins, need a host runtime
nano does not ship — [the specification](docs/specification.md) lists every boundary.

## Attach a real executor

The core never learns what runs a task. Set `runner.kind = "command"` and point
`runner.command` at a script that reads `NANORSI_REQUEST` (task, harness directory,
rendered always-on text) and writes `NANORSI_RESULT` (trajectory, deliverables, usage).
The judge is the same shape (`NANORSI_JUDGE_REQUEST` → `n_passed / n_criteria`). The
[LAB + OpenCode adapter](examples/lab_opencode/README.md) runs the paper's own legal
benchmark through the paper's own executor substrate this way.

## Results

| Study | Setup | Base → final partial |
| --- | --- | --- |
| [nanoRSI v0.5 on LAB](examples/results/harness2-lab-nanorsi/README.md) | this loop, OpenCode executor, GLM-5.3 as executor/improver/judge | 0.859 → 0.838 (−2.1 pp, 3W/3T/2L) — two `mitigates` adopts collapsed at the final draw |
| [Original Harness² code on LAB](examples/results/harness2-lab-opencode/README.md) | `google-research/harness2`, same models | 0.872 → 0.892 (+2.0 pp, 5W/1T/2L) |
| Paper (GLM-5 / OpenCode) | authors' report | 0.596 → 0.714 (+11.8 pp) |

Earlier studies on the v0.4 core (BBH, ALFWorld, HumanEval, OpenEvolve and ShinkaEvolve
tasks, parameter learning) remain published unchanged under
[examples/results/](examples/results/) as historical evidence; their task packs and
runners live in [examples/v0.4/](examples/v0.4/) and no longer run on the current core.

## Honesty rules

Author results are not local reproductions. Negative and null results are kept. No
claim that general recursive self-improvement is solved. Scores never influence
selection. Budgets, failed calls and unknown costs stay visible.

## License

Apache-2.0. Harness² (Apache-2.0) informed the mechanism shape; no upstream code is
copied. LAB tasks (harveyai/harvey-labs, MIT) are used as an installed dependency.
