# GLM-5.3 on real upstream RSI tasks (2026-09-17)

Two complete evaluation tasks reported by upstream papers and repositories, ported verbatim under Apache-2.0 attribution and run end to end on nanoRSI with **GLM-5.3 (full tier)**. Both produced clear, frozen-tested improvements; both audits are clean. Together with the earlier flash-tier function-minimization study, three upstream tasks have now run on this platform.

## Task 1 — ShinkaEvolve headless sine approximation (serial loop)

Source: [ShinkaEvolve](https://github.com/SakanaAI/ShinkaEvolve) (Apache-2.0, © Sakana AI 2025), `examples/sine_approx_headless`; the sine-approximation family is benchmarked in their paper (arXiv 2509.19349, ICLR 2026). Approximate `sin(x)` on [−π, π] without using any sine implementation; score `1/(1+4·RMSE+max_err)` over 161 wobbled points; direct-sine source snippets are blocked (their anti-cheating check, preserved).

| Stage | score | RMSE | max error |
| --- | ---: | ---: | ---: |
| initial (`return x`) | 0.1049 | 1.347 | 3.142 |
| accepted #1 (degree-9 fitted odd polynomial) | 0.8078 | | |
| **final (degree-13 Taylor)** | **0.999963** | **3.98e-06** | **2.11e-05** |

The final panel ran on a **denser 321-point grid containing inputs absent from the selection grid**. Five model calls (3,976 in / 2,982 out tokens); two unsalvageable diffs and one +0.000008-below-gate proposal honestly retained/rejected.

## Task 2 — OpenEvolve K-Module configuration (population search)

Source: [OpenEvolve](https://github.com/codelion/openevolve) (Apache-2.0, © Asankhaya Sharma 2025), `examples/k_module_problem`. Find the hidden 4-module configuration in a 5⁴ space where feedback reveals only **how many** modules are correct, never which — the task their README says defeats iterative refinement but suits evolution with crossover.

nanoRSI ran its **population search** (size 4, 2 generations, 2 workers, crossover enabled, count-only feedback preserved): 8 attempts, 8 model calls, 2 no-ops retained, one promotion.

| Condition | score | correct modules |
| --- | ---: | ---: |
| baseline (upstream initial guess) | 0.0 | 0/4 |
| **candidate** | **1.0** | **4/4** |

Honest note: the winning candidate was a first-generation **direct** proposal; crossover occurred within the population (17 journal events) but did not produce the winner. The mechanism was available, not load-bearing, in this run.

## Limits

Single runs, single seed, one model tier. The sine test grid is denser but shares the task's sampling formula; k-module's hidden target is deterministic, so the final test re-measures selection rather than generalization. Upstream author-reported numbers are not reproduced — these are independent nanoRSI runs of their tasks. A no-improvement outcome would have triggered re-reading the papers and optimizing the repository (the platform hardenings from the flash-tier study — action-JSON retry, fence stripping, diff-repair ladder — were exactly that loop).

Files: [summary.json](summary.json) · [sine/](sine) · [kmodule/](kmodule) · previous: [openevolve-fnmin](../openevolve-fnmin/README.md)
