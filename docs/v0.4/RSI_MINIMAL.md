# The minimal mechanism set of RSI

New to recursive self-improvement? This page defines RSI in its bounded, measurable form, lists the smallest set of mechanisms any such system needs, maps each one to this repository, and shows what our reference projects contribute. Five minutes to read; one command to run.

**[中文版](RSI_MINIMAL.zh-CN.md)** · [Run the smoke experiment](#run-it-now)

## What RSI means here

A system performs *recursive self-improvement* when it improves the machinery that produces its own improvements — its program, agent harness, skills or parameters — and every change is measured rather than assumed. nanoRSI implements the bounded, verifiable version of that idea: **a model proposes, deterministic code adjudicates, and only strictly better candidates survive.** Nothing in this repository claims general RSI is solved.

## The minimal set

| # | Mechanism | Why it is necessary | Where it lives here |
| --- | --- | --- | --- |
| 1 | **Verifiable task contract** | Without fixed, machine-checkable tasks there is no improvement to measure | `tasks/manifest.json`, `loop.tasks`, `evaluator.py` |
| 2 | **A mutable surface** | The system must declare what may change and protect everything else | `surface.py` (`SurfacePolicy`, protected paths) |
| 3 | **A proposer** | Something must generate candidate changes — model or script, always as diffs | `proposer.py`, starter templates |
| 4 | **A gate** | Candidates survive only on strict measured improvement with constraints satisfied; ties are rejected | `gate.py` (`decide`) |
| 5 | **A lineage** | Exact parent/candidate snapshots and a tamper-evident journal make claims auditable | `lineage.py`, `gitops.py`, `reports/evidence.jsonl` |
| 6 | **Freeze + unseen final test** | Selection feedback and honest evaluation must never mix | `loop.freeze`, `loop.final_test` |
| 7 | **Controls** | "Did evolution help?" and "did recursive reuse help?" are separate questions needing separate arms | `arm = frozen / self-use`, `no-skills` condition, uniform/random curricula |

Remove any one row and the loop stops being measurable: without the gate you keep regressions; without the freeze the test set leaks into selection; without the surface policy the candidate can rewrite its own scorer.

## What the reference projects contribute

We study real open implementations and borrow **ideas only** — their licenses forbid or do not authorize code reuse here.

- **[OpenRSI](https://github.com/FrontisAI/OpenRSI)** (Frontis.AI, code CC BY-NC 4.0): decomposes RSI into a verifiable task gym (`OpenMLE-Gym`), operator training (`OpenMLE-ERL`) and long-horizon search (`OpenMLE-Evo`). Its four atomic operators — **Draft, Improve, Debug, Crossover** — are the operator vocabulary our skills proposer already uses. Its validation discipline separates model gains from harness gains (their MLE-Bench Lite 39.39% → 60.61% model-only, 71.21% with search) and ships a `--smoke` one-command mode; notably it has **no unit tests**, which is exactly the gap nanoRSI fills with its regression suite.
- **[MetaRSI / RSI-Harness](https://github.com/CosmosMind-ai/RSI-Harness)** (CosmosMind; the harness repository publishes **no license**, so we treat it as all-rights-reserved): frames the system as a triple *(data D, model θ, harness H)* run through one kernel — **Observe → Diagnose → Propose → Validate → Execute → Select → Export** — with "model proposes, deterministic code adjudicates" as the authority boundary (the same rule our gate enforces). Its harness is a five-slot scaffold: system prompt, memory, built-in tools, skills, MCP tools. Two engineering habits worth stealing: an *identity invariant* ("with no Genome loaded, behave exactly like the upstream agent") and a *coverage invariant* ("every upstream settings key must be routed") — these became [`tests/test_invariants.py`](../tests/test_invariants.py). Its paper's control battery — identical budgets, sealed held-out splits, five seeds, no-improvement and single-operator baselines — is the standard our studies report against.
- Sakana's ShinkaEvolve, SEAL, DGM, OpenEvolve and the rest of the tracked projects are catalogued in the [industry research map](research/industry-rsi/README.md) with per-entry evidence limits.

All cited numbers are author-reported. Nothing on this page is a local reproduction of any upstream system.

## Run it now

```bash
python examples/smoke/run_smoke.py
```

That command builds a throwaway CPU workspace, trains a real checkpoint three times under the gate, freezes the choices, tests on the unseen split (baseline 0.0 vs candidate 0.75), runs the leakage/silent-bypass audit and writes the evidence ledger — offline, no API key. For the live-model path, continue with the [quickstart](QUICKSTART.md).

## What RSI is not

A passing panel is not per-case correctness (our published counterexample: a 4/4 parser that still fails `(12.5)`); a demo that improves is not a benchmark; heterogeneous demos must not be combined into one "RSI score"; and a self-use arm tying a frozen arm is a valid, publishable result — ours did, twice.
