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

![Figure 1: Creation builds a runnable harness from a weak seed, then Evolution repeatedly edits the persistent harness with execution feedback.](assets/paper-figures/harnessdev-figure.png)

**Source figure / official image** — Figure 1: Creation builds a runnable harness from a weak seed, then Evolution repeatedly edits the persistent harness with execution feedback. · Figure 1, PDF p.2 · [source](https://arxiv.org/html/2609.01437v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2609.01437) · [Paper v1](https://arxiv.org/html/2609.01437v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="qwen38-max-self-evolving-harness"></a>

## Qwen3.8-Max: A New Bar for Coding and Cowork (self-evolving harness demonstrations)

**2026-08-03** · report · Direct bounded loop

**Publication date** — Official Qwen team blog post dated 2026/08/03 announcing Qwen3.8-Max (2.4T parameters, 95B active); open weights were promised the following week on this page.

**Institutional relationship** — Alibaba's Qwen team reporting on its own flagship model and demonstration runs; all numbers are self-reported on the official blog.

**What changes and how feedback is reused** — Three long-horizon demonstrations in which the model modifies its own working infrastructure through feedback loops: (1) building the oh-my-cli project from an empty folder over a 10+ day autonomous run with an issue state machine, dispatcher, monitor and watchdog — 'requirements are normalized into issues, automatically claimed and executed by agents, and continuously iterated through code, tests, previews, and logs'; (2) reproducing the paper 'Unified Data Selection for LLM Reasoning' from scratch (~125 hours, ~7,600 lines, 33 GPU training rounds) and then running a hypothesis→code→GPU→analysis self-improvement loop over 18 self-generated ideas in four rounds; (3) competition leaderboard iteration.

**Author-reported result** — Self-reported: the autonomous oh-my-cli run accumulated 265 commits, 127 PRs and 151 issues over ~16 days (as of July 30, 2026); the research-reproduction loop first reproduced the paper's six findings (its selection method beats random +7.7% on AIME24) and then evolved a method beating the paper's own approach by +2.7 points on AIME24.

**Evidence limits** — Demonstrations, not controlled experiments: no baseline harness, fixed-seed comparator or cost control is published for the harness run, and the +2.7 AIME24 gain is a single-model self-reported result without variance or independent verification. Open-weight status at audit time: weights were promised publicly but release was not yet verified in this run.

**Code / weights / data / license** — Official blog post; the demonstration repository github.com/qwen-code-dev-bot/oh-my-cli is public (Apache-2.0, created 2026-07-13) with the full trace; model weights release was announced but not yet verified in this audit.

**Possible nanoRSI experiment — not implemented here** — Proposed: a minimal issue-loop harness in which nanoRSI's improver claims, implements and verifies its own repository issues, comparing accepted-diff yield and regression rate against a fixed-plan control on the same issue stream.

![The blog section describing the 10+ day autonomous run: 'it self-evolves through feedback loops', with the oh-my-cli issue-claiming loop (state machine, dispatcher, monitor, watchdog) and self-testing details.](assets/paper-figures/qwen38-max-self-evolving-harness.png)

**Source figure / official image** — The blog section describing the 10+ day autonomous run: 'it self-evolves through feedback loops', with the oh-my-cli issue-claiming loop (state machine, dispatcher, monitor, watchdog) and self-testing details. · Section '10+ Days of Autonomous Coding: Building a Self-Evolving Harness' · [source](https://qwen.ai/blog?id=qwen3.8)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-14.

**Open code / weights / data links** — [Demonstration repository with full trace (Apache-2.0)](https://github.com/qwen-code-dev-bot/oh-my-cli)

**Primary sources** — [Official Qwen blog post (opened via browser)](https://qwen.ai/blog?id=qwen3.8) · [Demonstration repository with full trace (Apache-2.0)](https://github.com/qwen-code-dev-bot/oh-my-cli)

<a id="microsoft-skillopt"></a>

## SkillOpt: Executive Strategy for Self-Evolving Agent Skills

**2026-06-30** · report · Direct bounded loop

**Publication date** — Microsoft Research blog post dated June 30, 2026; the accompanying publication page and open-source repository were created the same quarter (repository created 2026-05-08).

**Institutional relationship** — Microsoft Research / MSRA authors (Yifan Yang, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Dongdong Chen, Chong Luo) reporting their own method; blog numbers are author-reported with the paper linked from the same page.

**What changes and how feedback is reused** — Treats an agent's skill file as a trainable parameter in text space: an optimizer model proposes bounded edits in a forward–backward–update cycle, and a candidate is adopted 'only if it scores strictly higher than the current skill on the held-out validation split'; rejected edits are buffered as negative feedback, with epoch-wise slow/meta updates on top.

**Author-reported result** — Author-reported: best or tied-best in all 52 evaluation cells (6 benchmarks × 7 models × 3 execution modes) against human-written skills, one-shot LLM skills, Trace2Skill, TextGrad, GEPA and EvoSkill; with GPT-5.5 in direct chat the six-benchmark average rises from 58.8 to 82.3 (+23.5 points absolute); SpreadsheetBench 41.8→80.7; a spreadsheet skill trained in Codex lifts Claude Code from 22.1 to 81.8 (+59.7); median final skill ~920 tokens with only 1–4 accepted edits; removing meta-skill/slow-update drops SpreadsheetBench from 77.5 to 55.0.

**Evidence limits** — Skill optimization is supervised by held-out validation within fixed benchmarks — the loop optimizes against known test distributions, so gains on shifted or out-of-suite tasks are not demonstrated; cross-harness transfer is shown for one skill family only; execution modes rely on commercial harnesses whose versions are not pinned.

**Code / weights / data / license** — Official implementation verified at github.com/microsoft/SkillOpt (MIT license, created 2026-05-08, ~17k stars); paper page linked from the blog; no new weights (frozen third-party models); benchmark data subject to the original benchmark terms.

**Possible nanoRSI experiment — not implemented here** — Proposed: add a held-out-gate skill editor to nanoRSI's skills surface — bounded diff proposals accepted only on strict validation improvement — compared against ungated self-editing and frozen skills on identical task streams, tracking edit acceptance rates and regressions.

![Figure 1: skill-space optimization analogy — bounded edits with a held-out selection gate descend the validation-error surface where ad-hoc unguarded updates jump; the table maps classic training hyperparameters to their text-space counterparts.](assets/paper-figures/microsoft-skillopt.png)

**Source figure / official image** — Figure 1: skill-space optimization analogy — bounded edits with a held-out selection gate descend the validation-error surface where ad-hoc unguarded updates jump; the table maps classic training hyperparameters to their text-space counterparts. · Blog Figure 1 · [source](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-14.

**Open code / weights / data links** — [Official implementation (MIT)](https://github.com/microsoft/SkillOpt)

**Primary sources** — [Official MSR blog post (opened)](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/) · [Official implementation (MIT)](https://github.com/microsoft/SkillOpt) · [Publication page](https://www.microsoft.com/en-us/research/publication/skillopt-executive-strategy-for-self-evolving-agent-skills/)

<a id="tencent-skillhone"></a>

## SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History

**2026-06-07** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2026-06-07; later revisions are not used to reset the inclusion date. The paper identifies WeChat, Tencent Inc. affiliations and describes SkillHone as an ongoing research harness.

**Institutional relationship** — The paper lists WeChat, Tencent Inc. for the Tencent authors; one author is described as having worked at WeChat AI, Tencent Inc. during an internship. University affiliations are not treated as Tencent ownership.

**What changes and how feedback is reused** — A persistent decision history stores diagnoses, candidate skill revisions, redacted evaluation evidence and outcomes. Separate optimizer and evaluator agents work against separate skill and evaluation repositories; accepted revisions feed later sessions, so the skill artifact itself is edited and reused across iterations.

**Author-reported result** — On the raw open-web setting with Qwen3.6-35B-A3B, SkillHone reports 64.6 GAIA average versus 48.8 for a curated deep-research agent (+15.8) and 66.4 WebWalkerQA-EN versus 63.2 (+3.2). Internal tool-mediated scenarios report an average +18.8 improvement; these are author-reported, task-specific results.

**Evidence limits** — The paper evaluates English benchmarks and isolates one skill at a time; joint multi-skill evolution is not demonstrated. The original enterprise harness is not the public repository, so the open bundle should not be presented as a full release of Tencent internal infrastructure.

**Code / weights / data / license** — Public Tencent/SkillHone repository verified. Its README and LICENSE state MIT; the GitHub API metadata reports NOASSERTION. The paper harness, internal data and model weights are not released in this repository.

**Possible nanoRSI experiment — not implemented here** — Add a versioned skill directory to nanoRSI: keep decision records, candidate diffs, evaluator evidence and rollback decisions, then compare fixed skills with accepted-revision reuse on held-out tasks.

![Figure 2: SkillHone separates persistent decision history, skill optimization and skill evaluation so accepted revisions can be reused.](assets/paper-figures/tencent-skillhone.png)

**Source figure / official image** — Figure 2: SkillHone separates persistent decision history, skill optimization and skill evaluation so accepted revisions can be reused. · Figure 2, framework.png · [source](https://ar5iv.labs.arxiv.org/html/2606.08671/assets/framework.png)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Tencent SkillHone repository](https://github.com/Tencent/SkillHone) · [SkillHone MIT license](https://github.com/Tencent/SkillHone/blob/main/LICENSE)

**Primary sources** — [arXiv first submission and history](https://arxiv.org/abs/2606.08671) · [Paper v1 and framework figure](https://arxiv.org/html/2606.08671v1) · [Tencent SkillHone repository](https://github.com/Tencent/SkillHone) · [SkillHone MIT license](https://github.com/Tencent/SkillHone/blob/main/LICENSE)

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

![Figure 1: DGM-Hyperagents combines a modifiable task agent and meta agent with an archive of stepping stones.](assets/paper-figures/meta-hyperagents-2026.png)

**Source figure / official image** — Figure 1: DGM-Hyperagents combines a modifiable task agent and meta agent with an archive of stepping stones. · Figure 1 · [source](https://arxiv.org/html/2603.19461v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official code](https://github.com/facebookresearch/HyperAgents) · [Code licence](https://github.com/facebookresearch/HyperAgents/blob/main/LICENSE.md)

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

![Figure 8: Model Iteration System and the dual-loop workflow used in M2.7 self-evolution.](assets/paper-figures/minimax-m27-self-evolution.svg)

**Source figure / official image** — Figure 8: Model Iteration System and the dual-loop workflow used in M2.7 self-evolution. · Figure 8 · [source](https://arxiv.org/html/2605.26494v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official M2.7 model](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) · [Current M2.7 non-commercial license](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)

**Primary sources** — [Official M2.7 report](https://www.minimax.io/news/minimax-m27-en) · [Related M2-series technical paper dates](https://arxiv.org/abs/2605.26494) · [Related M2-series paper v1](https://arxiv.org/html/2605.26494v1) · [Official M2.7 model](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) · [Current M2.7 non-commercial license](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)

<a id="tencent-webaggregator"></a>

## WebAggregator: Enhancing Compositional Reasoning Capabilities of Deep Research Agent Foundation Models

**2025-10-16** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2025-10-16 under the Explore-to-Evolve working title; the later title WebAggregator does not change the original date.

**Institutional relationship** — The paper explicitly lists Tencent AI Lab authors alongside The Chinese University of Hong Kong authors. The code and data-construction repository is published under Tencent.

**What changes and how feedback is reused** — An online explorer visits websites and a Compositional Logic Proposer selects, composes and refines high-level aggregation operations. Quality control turns executable aggregation programs into 10K verifiable QA items across 50K websites and 11 domains; the resulting traces and answers then support SFT of WebAggregator models.

**Author-reported result** — The paper reports WebAggregator-8B matching GPT-4.1 and WebAggregator-32B exceeding GPT-4.1 by more than 10% on GAIA-text while approaching Claude-3.7. On its human-annotated WebAggregatorQA test, reported pass@1 is 28.0% for Claude-3.7 and 25.8% for GPT-4.1; the model comparisons use a fixed judge and bounded retries.

**Evidence limits** — The evolving object is a web aggregation program and its generated training data; the downstream foundation model is SFT-trained and then evaluated, not recursively redeployed to improve its own proposer. Website availability, judge quality and generated-data leakage can affect the result.

**Code / weights / data / license** — Tencent/WebAggregator publishes the QA construction engine, queries, trajectories, models and run scripts. LICENSE.txt contains custom WebAggregator terms and states the project is not intended for use within the European Union; GitHub API metadata reports NOASSERTION. Verify data, model and third-party terms separately.

**Possible nanoRSI experiment — not implemented here** — Use a small closed web task set to test nanoRSI program evolution: retain each proposer program, source URLs, verifier outputs and generated examples, then compare fixed-data SFT with refreshed-data iterations.

![Figure 2: Explore-to-Evolve turns web exploration and executable aggregation logic into verified QA and model-training data.](assets/paper-figures/tencent-webaggregator.png)

**Source figure / official image** — Figure 2: Explore-to-Evolve turns web exploration and executable aggregation logic into verified QA and model-training data. · Figure 2, illus.png · [source](https://ar5iv.labs.arxiv.org/html/2510.14438/assets/illus.png)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Tencent WebAggregator repository](https://github.com/Tencent/WebAggregator) · [WebAggregator custom license terms](https://github.com/Tencent/WebAggregator/blob/main/LICENSE.txt)

**Primary sources** — [arXiv first submission and history](https://arxiv.org/abs/2510.14438) · [Paper v1 and Explore-to-Evolve figure](https://arxiv.org/html/2510.14438v1) · [Tencent WebAggregator repository](https://github.com/Tencent/WebAggregator) · [WebAggregator custom license terms](https://github.com/Tencent/WebAggregator/blob/main/LICENSE.txt)

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

![Figure 1: ShinkaEvolve archive, rejection sampling, program mutation and fitness evaluation loop.](assets/paper-figures/sakana-shinkaevolve.png)

**Source figure / official image** — Figure 1: ShinkaEvolve archive, rejection sampling, program mutation and fitness evaluation loop. · Figure 1 · [source](https://arxiv.org/html/2509.19349v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official code and license](https://github.com/SakanaAI/ShinkaEvolve)

**Primary sources** — [arXiv original date](https://arxiv.org/abs/2509.19349) · [Sakana announcement and results](https://sakana.ai/shinka-evolve/) · [Official code and license](https://github.com/SakanaAI/ShinkaEvolve)
