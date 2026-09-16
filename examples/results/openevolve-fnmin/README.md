# Running a real upstream RSI task on nanoRSI: OpenEvolve function minimization (2026-09-16)

nanoRSI running a **complete evaluation task taken verbatim from another open RSI repository** — [OpenEvolve](https://github.com/codelion/openevolve) (Apache-2.0, © Asankhaya Sharma 2025; see [NOTICE](NOTICE)) — with a live model, and producing a genuine, frozen-tested improvement.

**Headline: on the frozen test panel with unseen trial seeds, the evolved program scored 0.9960 vs the upstream initial program's 0.9418; the average distance to the known global minimum fell from 0.175 to 0.013 and the average function value reached −1.5184 against the true optimum −1.519.** The accepted change replaced pure random search with batched global exploration plus adaptive pattern-search local refinement. Five model calls, 11,067 tokens.

## What was ported

| File | Origin | Adaptation |
| --- | --- | --- |
| `initial-program.py` | `examples/function_minimization/initial_program.py` | verbatim under an attribution header |
| evaluator (in `summary.json` settings) | `examples/function_minimization/evaluator.py` | scoring formula preserved (value/distance/reliability scores, solution-quality multipliers, 10 trials); trials run as bounded subprocesses; per-trial numpy RNG seeding; combined score (≤1.5) normalized to [0,1] |

The task: minimize `f(x,y) = sin(x)cos(y) + sin(xy) + (x²+y²)/20` on [−5,5]², known optimum ≈ (−1.704, 0.678, −1.519). The initial algorithm is a 1000-iteration random search; only `search_algorithm` is evolvable (`EVOLVE-BLOCK` markers), `evaluate_function` stays fixed.

## The run (GLM-5.3-Flash, seed 0, frozen arm, 3 attempts→5 attempts budget)

| Attempt | Decision | Detail |
| ---: | --- | --- |
| 1 | failed | provider rate limit (429) — retained |
| 2 | **accepted** | validation 0.9194 → 0.9975 (+0.0776) |
| 3 | failed | structurally corrupt diff — retained |
| 4 | rejected | +0.0005 below the 0.01 gate minimum |
| 5 | rejected | +0.0026 below the gate minimum |

Freeze with one test repeat; final panel on the test split (trial seeds disjoint from validation):

| Condition | score | avg distance | avg value | reliability |
| --- | ---: | ---: | ---: | ---: |
| baseline (upstream initial program) | 0.9418 | 0.1749 | −1.4912 | 1.0 |
| candidate (evolved) | **0.9960** | **0.0126** | **−1.5184** | 1.0 |

The evolved algorithm: `evolved-program.py` (90 lines). The audit found zero expected-answer leakage and zero silent bypass; the evidence ledger retains all five attempts including failures; `verify` passes.

## Platform hardening this real run forced

Running real models on real tasks exposed three failure classes, each fixed in the platform with tests (they benefit every starter):

1. **Invalid action JSON** (GLM-flash emits lone backslashes when embedding whole files in JSON): the skills/program runner now retries a model call once on unparseable action content, and strips a single outer markdown fence before strict parsing ([`tests/test_live_templates.py`](../../../tests/test_live_templates.py)). Task-side mitigation: the workspace goal steers the proposer toward the diff format, which has a far smaller escaping surface.
2. **Miscounted/drifted unified-diff hunks** (the classic model-diff defect): `git apply` now runs a bounded repair ladder — `--recount`, then `--recount -C1` — and still rejects hallucinated context ([`tests/test_gitops.py`](../../../tests/test_gitops.py)).
3. **Header-less diffs**: `changed_paths_from_unified_diff` falls back to `+++ b/` lines when no `diff --git` header exists.

## Related-repo survey (bundled real tasks and licenses)

| Repository | License | Runnable tasks bundled | Used here |
| --- | --- | --- | --- |
| [OpenEvolve](https://github.com/codelion/openevolve) | Apache-2.0 | yes (initial program + evaluator + metric per example) | **yes — this study** |
| [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) | Apache-2.0 | yes (`examples/` with `initial.py` + `evaluate.py`: circle packing, 2048, sine approximation…) | queued follow-up |
| [OpenRSI](https://github.com/FrontisAI/OpenRSI) | CC BY-NC (tasks mixed upstream terms) | yes (OpenMLE-Tasks on HF) | no — license |
| [RSI-Harness](https://github.com/CosmosMind-ai/RSI-Harness) | none stated | no benchmark code | no — license |

## Limits

One seed, one repeat, one flash-tier model, one upstream task. This measures optimization quality on a fixed objective, not generalization. Upstream author-reported OpenEvolve results (e.g., their MLE-Bench Lite numbers) are **not** reproduced here — this is nanoRSI independently running their task. The rejected micro-improvements (attempts 4–5) suggest the gate's 0.01 minimum, not the search, was the binding constraint near the optimum.

Files: [summary.json](summary.json) · [initial-program.py](initial-program.py) · [evolved-program.py](evolved-program.py) · [final.json](final.json) · [evidence.jsonl](evidence.jsonl) · [audit.json](audit.json) · [NOTICE](NOTICE)
