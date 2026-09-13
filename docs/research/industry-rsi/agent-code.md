# Agents and code

[← Research map](README.md)

<a id="bytedance-harnessdev"></a>

## HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?

**2026-09-01** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-01; shared Self-Developing Agents project page also dated September 1.

**Institutional relationship** — All listed affiliations appear explicitly in the paper, with ByteDance Seed as a research participant.

**What changes and how feedback is reused** — Creation builds a runnable harness from a weak seed; Evolution repeatedly edits that persistent harness using downstream execution feedback. Official versions are frozen and later evaluated on hidden tasks, measuring reuse across tasks rather than single-output repair. Runtime-model controls test portability.

**Author-reported result** — Across nine single evolution trajectories, visible and held-out score directions agree on 34/64 adjacent version switches (53.1%); only 2/9 declared final versions are held-out best. Creation covers six creators, four domains and 2,207 downstream instances.

**Evidence limits** — A benchmark of bounded direct loops, not proof of stable compounding. Selected final artifacts can regress, and gains depend on the executor.

**Code / weights / data / license** — Paper and project page public; paper CC BY-NC-ND 4.0. A downloadable benchmark code/data repository, derived weights and their licenses were not verified. Do not label the project as an open-code release.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI coding study: freeze every candidate, retain the complete score trajectory, and measure development/held-out direction agreement under a fixed executor.

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2609.01437) · [Paper v1](https://arxiv.org/html/2609.01437v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="meta-hyperagents-2026"></a>

## Hyperagents

**2026-03-19** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-03-19; Meta publication page: 2026-03-24.

**Institutional relationship** — Paper lists FAIR at Meta and Meta Superintelligence Labs affiliations, alongside academic collaborators.

**What changes and how feedback is reused** — An editable meta agent modifies itself and the task agent. Evaluated valid variants enter an archive and supply later parents and feedback; admission need not require immediate improvement.

**Author-reported result** — After 100 iterations, held-out paper-review accuracy was 0.710 (CI 0.590–0.750), versus static baseline 0.630 and customized DGM 0.590. The customized-DGM difference was not significant; initial 0.0 reflected output-format failure.

**Evidence limits** — Fixed foundation models/evaluators and bounded runs do not demonstrate indefinite self-acceleration.

**Code / weights / data / license** — Official code and linked experiment logs verified; foundation-model weights are not supplied. Code licence is CC BY-NC-SA 4.0, not permissive commercial open source. Linked log payloads/separate data licence were not inspected.

**Possible nanoRSI experiment — not implemented here** — Proposed: separately version task/meta code, preserve evaluated stepping stones, and keep immutable evaluation records.

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Primary sources** — [Paper history](https://arxiv.org/abs/2603.19461) · [Paper v1, authors and section 5.1](https://arxiv.org/html/2603.19461v1) · [Meta publication](https://ai.meta.com/research/publications/hyperagents/) · [Official code](https://github.com/facebookresearch/HyperAgents) · [Code licence](https://github.com/facebookresearch/HyperAgents/blob/main/LICENSE.md)

<a id="minimax-m27-self-evolution"></a>

## MiniMax M2.7: Early Echoes of Self-Evolution

**2026-03-18** · report · Direct bounded loop

**Publication date** — Official report dated 2026-03-18. Related M2-series technical paper first appeared 2026-05-26; its July revision is not the original M2.7 event.

**Institutional relationship** — First-party MiniMax report; the related technical paper is the MiniMax-M2 series report.

**What changes and how feedback is reused** — An internal M2.7 agent reads failure trajectories, proposes edits to scaffold code and sampling settings, evaluates them, and keeps or reverts changes for subsequent rounds. A separate research workflow updates memory/skills while helping researchers run RL experiments; that workflow retains human direction and critical decisions.

**Author-reported result** — MiniMax reports over 100 autonomous scaffold iterations and a 30% improvement on internal programming evaluations. Absolute baseline, evaluation-set identity and uncertainty are undisclosed, so the number is not independently comparable.

**Evidence limits** — First-party internal experiment, not a reproduced result. Assisted model R&D and scaffold self-editing do not establish fully autonomous successor-model training.

**Code / weights / data / license** — M2.7 weights are public. Current model LICENSE is custom non-commercial; commercial use requires written authorization. The internal self-evolution harness, evaluation data and complete training pipeline were not verified as public.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI coding experiment: constrain mutations to scaffold files, freeze the executor, and audit keep/revert decisions on a hidden test split.

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Primary sources** — [Official M2.7 report](https://www.minimax.io/news/minimax-m27-en) · [Related M2-series technical paper dates](https://arxiv.org/abs/2605.26494) · [Related M2-series paper v1](https://arxiv.org/html/2605.26494v1) · [Official M2.7 model](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) · [Current M2.7 non-commercial license](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)

<a id="sakana-shinkaevolve"></a>

## ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution

**2025-09-17** · paper · Direct bounded loop

**Publication date** — arXiv v1: September 17, 2025; Sakana announcement: September 25. Later repository updates are not the original date.

**Institutional relationship** — Sakana AI develops and releases the framework; its company announcement links the paper and official repository.

**What changes and how feedback is reused** — LLMs mutate archived programs; verifier fitness selects reusable parents. Novelty rejection and bandit-based model selection improve search. Targets include AIME agent scaffolds and MoE load-balancing losses.

**Author-reported result** — Authors report a 26-circle packing solution exceeding AlphaEvolve's solution after 150 samples. MoE loss search used 30 generations; versus Global LBL, the announcement reports 5.81% less inefficient routing and 1.73% higher average performance across seven benchmarks.

**Evidence limits** — Bounded, human-defined objectives and external LLMs; this does not demonstrate an autonomously improving mutation engine or unlimited RSI.

**Code / weights / data / license** — Official code/examples: verified; Apache-2.0. No new foundation weights required. Complete experimental data availability was not audited.

**Possible nanoRSI experiment — not implemented here** — Proposed: add an archive-based scaffold-search example with fixed held-out tests and cost-aware parent selection.

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Primary sources** — [arXiv original date](https://arxiv.org/abs/2509.19349) · [Sakana announcement and results](https://sakana.ai/shinka-evolve/) · [Official code and license](https://github.com/SakanaAI/ShinkaEvolve)
