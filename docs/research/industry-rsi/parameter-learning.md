# Parameters and training data

[← Research map](README.md)

<a id="tokenrhythm-neohorse-1"></a>

## NeoHorse-1: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness

**2026-09-08** · paper · Direct bounded loop

**Publication date** — arXiv v1: September 8, 2026, submitted by the NeoHorse Team. Models were released on Hugging Face around the same date; the GitHub repository was created September 4, 2026.

**Institutional relationship** — Corporate–university joint team: TokenRhythm Technologies and Infinigence AI lead, with Tsinghua, Peking University, CUHK and Alibaba Group authors; two investment firms (Visionplus Capital, WX Capital) also appear in the affiliation list.

**What changes and how feedback is reused** — A routing harness backed by a heterogeneous model pool logs capability-demand signals from real agentic traffic. Those records become training examples (structural validation, six-dimension semantic scoring, subscene labeling), routing scores order a three-stage SFT curriculum and routing-guided on-policy distillation, and a capability-guided allocation step turns evaluation feedback into the next training mixture; updated checkpoints return to the harness, 'closing an evaluation–selection–update loop'.

**Author-reported result** — Post-training lifts the macro-average over ten benchmarks (six agentic, two coding, two instruction-following) from 58.94 to 64.87 at 4B and from 65.60 to 69.04 at 9B, with Qwen3.5-4B/9B bases; the post-trained 4B narrows the gap to the untrained 9B base. Comparators per track include Gemma-4, Granite-4.2, Spark-X2.5 and others.

**Evidence limits** — The authors state this is 'an initial attempt at recursive self-improvement rather than a definitive demonstration': results cover one pass of the evaluation–selection–update loop, so accumulation across successive iterations is untested; validation is limited to agentic/coding/tool-use/instruction-following capabilities.

**Code / weights / data / license** — Code verified at github.com/TokenRhythm/NeoHorse (Apache-2.0, created 2026-09-04) and model weights on the Hugging Face TokenRhythm NeoHorse-1 collection; training data sources and their redistribution terms are not documented in the audited sources.

**Possible nanoRSI experiment — not implemented here** — Proposed: on a fixed task stream, compare capability-guided training-data allocation against uniform sampling and a frozen data mixture with matched token budgets, logging whether the allocator's choices transfer to held-out tasks.

![Figure 2: the routing-guided agentic training loop — diverse tasks run through a routing harness over a model pool, interaction records become a training mixture, capability feedback steers the next distribution, and updated models return to the harness.](assets/paper-figures/tokenrhythm-neohorse-1.svg)

**Source figure / official image** — Figure 2: the routing-guided agentic training loop — diverse tasks run through a routing harness over a model pool, interaction records become a training mixture, capability feedback steers the next distribution, and updated models return to the harness. · Figure 2 · [source](https://arxiv.org/html/2609.08183v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-14.

**Open code / weights / data links** — [Official implementation (Apache-2.0)](https://github.com/TokenRhythm/NeoHorse)

**Primary sources** — [arXiv abstract (v1 date)](https://arxiv.org/abs/2609.08183) · [Paper HTML (loop description, scores, limitations)](https://arxiv.org/html/2609.08183v1) · [Official implementation (Apache-2.0)](https://github.com/TokenRhythm/NeoHorse)

<a id="experience-funnel-state-policy"></a>

## Experience Funnel: A State-Policy Alternating Loop for Self-Evolving Agents

**2026-09-08** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-09-08. No later revision recorded at verification time. Surfaced as a lead on 2026-09-15 (abstract lacked affiliation and numbers); verified against the HTML full text on 2026-09-16.

**Institutional relationship** — Paper v1: Wenbo Gao and James Chung-wai Cheung are at The Hong Kong Polytechnic University; the Huawei group includes Zhaomou Song, Renxi Liu, Xing Li, Xianzhi Yu, Xiaoguang Li, Weizhe Lin (corresponding), Yaoyuan Wang; Zhiyuan Ji is affiliated with both Huawei and Renmin University of China.

**What changes and how feedback is reused** — A two-timescale loop over a deployed (textual state, policy) pair. Fast: trajectories are aggregated into a task-specific textual state summarizing recurring procedures, failure modes and corrective strategies, and candidate state edits must pass validation on held-out interactions before acceptance. Slow: Transition-Aware Skill Distillation compares rollouts under no state, the previous state and the updated state, labeling each experience newly-useful (0,1), persistently-useful (1,1), regressive (1,0) or inactive (0,0); token-level Jensen-Shannon divergence localizes state-responsive decisions, and a state-conditioned teacher distills only the useful rollouts into the state-free student policy, combined with a state-free RL reward. The updated pair redeploys for the next round.

**Author-reported result** — Three benchmarks (SearchQA, ALFWorld, WebShop) with a Qwen3.5-4B student and frozen Qwen3.5-27B teacher on Ascend 910B3 NPUs: average 57.6% vs SkillRL 56.2, OPID 55.4, SkillOpt 53.9 and base 33.7. The state-free policy itself rises 58.1% -> 61.3% on SearchQA over five rounds (residual state contributes nothing after consolidation: 61.3 with full state vs 61.3 with residual). Ablation: state-only 61.1, policy-only 62.8, full loop 63.6; experience selection (0,1)+(1,1) reaches 63.0 vs 58.9 unfiltered. Honest no-op accounting: of five evolution rounds only rounds 1 and 4 were accepted; rounds 2, 3 and 5 were rejected.

**Evidence limits** — No code release; the margin over SkillRL is +1.4 points; per-benchmark numbers show SearchQA carries most of the gain (WebShop 42.4 remains low). Rejected rounds are reported but not analyzed in depth.

**Code / weights / data / license** — No code, weights or data release located; paper only. Experiments run on Huawei Ascend 910B3 NPUs with Qwen3.5-4B/27B checkpoints.

**Possible nanoRSI experiment — not implemented here** — For nanoRSI's parameter track: adopt the counterfactual state comparison (rollouts under no-state vs previous-state vs updated-state) as the acceptance test for whether a context change deserves distillation, keeping weight updates gated the same way skill commits are.

![Figure 1: the state-policy consolidation loop - Phase I aggregates trajectories into a validated textual state; Phase II labels matched rollouts by transition type and distills state-responsive behavior into the state-free policy.](assets/paper-figures/experience-funnel-state-policy.svg)

**Source figure / official image** — Figure 1: the state-policy consolidation loop - Phase I aggregates trajectories into a validated textual state; Phase II labels matched rollouts by transition type and distills state-responsive behavior into the state-free policy. · Figure 1 · [source](https://arxiv.org/html/2609.08919v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-16.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv abstract](https://arxiv.org/abs/2609.08919) · [Paper v1 (affiliations, Figure 1, Tables, ablations)](https://arxiv.org/html/2609.08919v1)

<a id="bytedance-aspire"></a>

## Aspire: Can Models Self-Evolve from Vague Goals?

**2026-08-31** · paper · Direct bounded loop

**Publication date** — arXiv v1: 2026-08-31. Shared project announcement: 2026-09-01.

**Institutional relationship** — The paper explicitly lists the four research affiliations, including ByteDance Seed.

**What changes and how feedback is reused** — Given a vague goal, an agent chooses data, training methods and parent checkpoints, or edits a harness. The controller verifies lineage and freezes candidates. Score-gated weight campaigns retain an eligible checkpoint only if its measured gain is positive, otherwise restoring the incoming state; harness evaluation is post-freeze and does not imply recursive handoff.

**Author-reported result** — Hidden evaluation contains 520 expert-authored items across six goals. With Qwen3.5-4B fixed as runtime, the best successor harness scores 27.22 task-macro versus 28.64 for original Qwen-Agent; all three valid successors trail the reference.

**Evidence limits** — Nonnegative retained gains can be created by rollback selection; they do not mean every attempted update helped. Vague goals and proxy validation can induce regressions.

**Code / weights / data / license** — Paper/project public; paper CC BY-NC-ND 4.0. Complete benchmark code, hidden data, trained checkpoints and asset licenses were not verified as publicly downloadable.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI learner reporting: separate raw candidate delta from retained-state delta, export failed attempts, and test vague versus explicit goals.

![Figure 1: From explicit-task optimization to vague-goal-driven self-evolution.](assets/paper-figures/aspire-figure.png)

**Source figure / official image** — Figure 1: From explicit-task optimization to vague-goal-driven self-evolution. · Figure 1, PDF p.2 · [source](https://arxiv.org/html/2608.31111v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2608.31111) · [Paper v1 retention protocol and Table 1](https://arxiv.org/html/2608.31111v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="gpt-red"></a>

## GPT-Red: Automated Red Teaming via Self-Play at Scale

**2026-07-15** · paper · Direct bounded loop

**Publication date** — Official paper announcement date.

**Institutional relationship** — OpenAI paper and company report.

**What changes and how feedback is reused** — Self-play RL updates an attacker and defender population from failure/resistance rewards. Stronger defenders create harder attacker training; the trained red-teamer then supplies adversarial data for GPT-5.6.

**Author-reported result** — The report gives 0.05% GPT-Red direct-injection success against GPT-5.6 Sol, averaged over attempts on held-out environments. This is one threat model, not a universal attack-failure probability.

**Evidence limits** — Bounded adversarial co-training; no autonomous successor-design proof. Internal models and training scale prevent direct local replication.

**Code / weights / data / license** — Paper public; GPT-Red internal-only. Training code, weights and full data are not released in these sources; no reusable code license established.

**Possible nanoRSI experiment — not implemented here** — Explore benign adversarial fixtures with separate attack-validity, task-success and over-refusal scores.

![Figure 1: GPT-Red red-teaming performance as test-time compute increases.](assets/paper-figures/gpt-red-figure.png)

**Source figure / official image** — Figure 1: GPT-Red red-teaming performance as test-time compute increases. · Figure 1, PDF p.1 · [source](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [Paper](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf) · [Official report](https://openai.com/index/unlocking-self-improvement-gpt-red/)

<a id="a3"></a>

## A3: An Automated Alignment Agent for Safety Finetuning

**2026-03-11** · report · Direct bounded loop

**Publication date** — Dated research report; repository creation is not treated as a public release date.

**Institutional relationship** — Jifan Zhang: Fellows Program; Henry Sleight: Constellation; Joe Benton: Anthropic.

**What changes and how feedback is reused** — Agents generate failure hypotheses, split data, then adapt LoRA hyperparameters and data weights using an experiment log and evaluation feedback. The controller improves a target model, not its own weights.

**Author-reported result** — For Qwen-2.5-7B Instruct, external sycophancy evaluation falls from 68.0% to 42.0%; MMLU-Pro changes from 52.9% to 52.4% (report Table 1). Lower sycophancy is better.

**Evidence limits** — Three targeted failures; weaker Llama results expose forgetting. The log description includes OOD feedback, so do not equate every reported OOD split with an untouched final test.

**Code / weights / data / license** — Apache-2.0 code, configs and data directory public. Requires model/API access and a GPU stack; trained checkpoints and full data completeness not verified.

**Possible nanoRSI experiment — not implemented here** — Extend curriculum experiments with capability-retention constraints and a truly frozen final panel.

![A3 pipeline: data-generation agent, fine-tuning agent and experiment log adapt to safety failures.](assets/paper-figures/a3.png)

**Source figure / official image** — A3 pipeline: data-generation agent, fine-tuning agent and experiment log adapt to safety failures. · A3 Pipeline figure · [source](https://alignment.anthropic.com/2026/automated-alignment-agent/)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Repository](https://github.com/safety-research/A3) · [Code license](https://github.com/safety-research/A3/blob/main/LICENSE)

**Primary sources** — [Research report](https://alignment.anthropic.com/2026/automated-alignment-agent/) · [Repository](https://github.com/safety-research/A3) · [Code license](https://github.com/safety-research/A3/blob/main/LICENSE)

<a id="sakana-doc-to-lora"></a>

## Doc-to-LoRA: Learning to Instantly Internalize Contexts

**2026-02-13** · paper · Enabling technique / evaluation

**Publication date** — arXiv v1: February 13, 2026. The combined February project page also discusses Text-to-LoRA, whose June 2025 original remains outside the window.

**Institutional relationship** — The official project page identifies Sakana authors; Shinnosuke Uesaka additionally lists Minerva University.

**What changes and how feedback is reused** — A meta-trained hypernetwork maps document activations to LoRA weights. Teacher/student distillation supplies training feedback; deployment reuses generated adapters for later queries without rereading the document or per-document gradients.

**Author-reported result** — On 2WikiMultihopQA, iterative D2L reports 0.844 normalized ROUGE-L, 3.791 GB additional update memory and 0.551 s latency. Oracle context distillation reports 0.901, 7.820 GB and 40.171 s; normalized performance is relative to contextual inference.

**Evidence limits** — An amortized adaptation mechanism, not a recursive loop: deployment does not improve the hypernetwork. Accuracy and adapter capacity remain constraints.

**Code / weights / data / license** — Official code: MIT. Hugging Face checkpoint files verified; model-card license absent. Data-generation/evaluation scripts exist; complete dataset redistribution not audited.

**Possible nanoRSI experiment — not implemented here** — Proposed: explore versioned document adapters as a later memory backend, benchmarking factual retention against retrieval.

![Overview of Doc-to-LoRA: a hypernetwork maps document activations to LoRA weights for fast internalization.](assets/paper-figures/sakana-doc-to-lora.svg)

**Source figure / official image** — Overview of Doc-to-LoRA: a hypernetwork maps document activations to LoRA weights for fast internalization. · Overview figure · [source](https://arxiv.org/html/2602.15902v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official code](https://github.com/SakanaAI/doc-to-lora) · [Official checkpoint inventory](https://huggingface.co/SakanaAI/doc-to-lora/tree/main)

**Primary sources** — [Original paper date](https://arxiv.org/abs/2602.15902) · [Paper Table 1](https://arxiv.org/html/2602.15902v1) · [Official project and affiliations](https://pub.sakana.ai/doc-to-lora/) · [Official code](https://github.com/SakanaAI/doc-to-lora) · [Official checkpoint inventory](https://huggingface.co/SakanaAI/doc-to-lora/tree/main)

<a id="sakana-trinity"></a>

## TRINITY: An Evolved LLM Coordinator

**2025-12-04** · paper · Enabling technique / evaluation

**Publication date** — arXiv v1: December 4, 2025; Sakana's April 26, 2026 announcement is later dissemination.

**Institutional relationship** — Most authors list Sakana; Qi Sun also lists Science Tokyo. Peter Schwendeman lists Michigan and work during a Sakana internship.

**What changes and how feedback is reused** — Sep-CMA-ES perturbs a small coordinator head, scores terminal task outcomes and recombines candidate parameters. The retained coordinator repeatedly selects a model and Thinker/Worker/Verifier role; underlying foundation-model weights stay fixed.

**Author-reported result** — LiveCodeBench v6: 86.2% pass@1 versus GPT-5 83.8%, using uncapped outputs and no coordinator retraining. Under the separate 4,096-token, five-turn comparison, TRINITY scores 61%; do not conflate these settings.

**Evidence limits** — An offline optimizer learns coordination on human-selected benchmarks; the deployed agent is not shown modifying its own learning algorithm.

**Code / weights / data / license** — Paper public. Official implementation, coordinator weights, redistributed data and their licenses not verified; third-party implementations are not official releases.

**Possible nanoRSI experiment — not implemented here** — Proposed: evaluate a tiny evolvable role/model router against static routing at equal token budgets.

![Figure 1: Cyclical coordination architecture with a compact coordinator selecting model and role each turn.](assets/paper-figures/sakana-trinity.svg)

**Source figure / official image** — Figure 1: Cyclical coordination architecture with a compact coordinator selecting model and role each turn. · Figure 1 · [source](https://arxiv.org/html/2512.04695v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [Original paper date](https://arxiv.org/abs/2512.04695) · [Original paper methods and experimental conditions](https://arxiv.org/html/2512.04695v1) · [Official Sakana announcement](https://sakana.ai/trinity/)

<a id="deepseek-math-v2"></a>

## DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning

**2025-11-27** · paper · Direct bounded loop

**Publication date** — arXiv v1 and the paper's date are 2025-11-27.

**Institutional relationship** — The paper explicitly lists DeepSeek-AI and identifies internship work; the official DeepSeek repository hosts the release.

**What changes and how feedback is reused** — A verifier rewards generator training; harder generated proofs are automatically labeled with increased verification compute to further train the verifier. An expert-seeded meta-verifier checks critique faithfulness. At inference, scored candidate proofs are retained and refined using their critiques; this second loop changes solutions, not weights.

**Author-reported result** — Authors report 118/120 on Putnam 2024 after expert assessment. High-compute search starts with 64 proofs and 64 analyses each, selects 64 top proofs, samples 8 analyses per proof, and runs up to 16 refinement iterations. This is not one-shot performance.

**Evidence limits** — Natural-language verification is fallible and uses expert bootstrap supervision. Proof-search success alone is not recursive improvement of the model.

**Code / weights / data / license** — Public inference code, prompts/predictions, and 685B weights; repository and weights are Apache-2.0. Full training code, human annotations and complete training data were not verified as released.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI learner adapter: version generator, verifier, labels and expert audit separately; compare verifier co-training against a frozen verifier.

![Figure 2: Proof quality improves as the maximum number of sequential self-verification refinements increases.](assets/paper-figures/deepseek-math-v2.svg)

**Source figure / official image** — Figure 2: Proof quality improves as the maximum number of sequential self-verification refinements increases. · Figure 2 · [source](https://arxiv.org/html/2511.22570v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official DeepSeek-Math-V2 repository](https://github.com/deepseek-ai/DeepSeek-Math-V2) · [Official weights and Apache-2.0 statement](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2)

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2511.22570) · [Paper v1 methods and high-compute evaluation](https://arxiv.org/html/2511.22570v1) · [Official DeepSeek-Math-V2 repository](https://github.com/deepseek-ai/DeepSeek-Math-V2) · [Official weights and Apache-2.0 statement](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2)

<a id="salesforce-unc-agent0"></a>

## Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning

**2025-11-20** · paper · Direct bounded loop

**Publication date** — arXiv v1: November 20, 2025; official code release: November 29. Distinct from the unrelated July 2025 recommendation paper named Agent0.

**Institutional relationship** — UNC leads the author list; Can Qin and Caiming Xiong list Salesforce Research, and Fang Wu lists Stanford.

**What changes and how feedback is reused** — A curriculum policy generates tasks against a tool-using executor. Ten executor responses estimate uncertainty and pseudo-labels; filtered tasks train the executor, whose new capability changes the next curriculum. Both policies receive iterative training updates.

**Author-reported result** — Qwen3-8B math average rises 49.2→58.2 (+9.0 points; about 18% relative), versus tool-only 53.2. Seven math benchmarks use greedy pass@1 except AMC/AIME mean@32; Table 1 reports peak training performance.

**Evidence limits** — Zero data means no human-curated training set, not no pretrained knowledge. Self-consistency can reinforce errors; results do not establish unbounded improvement.

**Code / weights / data / license** — Official curriculum/executor training code verified; Apache-2.0. Released trained weights and complete generated datasets not verified.

**Possible nanoRSI experiment — not implemented here** — Proposed: test difficulty-adaptive task generation with immutable answer verifiers before attempting costly policy training.

![Figure 2: Agent0 co-evolutionary loop between curriculum generation and executor training.](assets/paper-figures/salesforce-unc-agent0.png)

**Source figure / official image** — Figure 2: Agent0 co-evolutionary loop between curriculum generation and executor training. · Figure 2 · [source](https://arxiv.org/html/2511.16043v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official series repository and release date](https://github.com/aiming-lab/Agent0) · [Agent0 training implementation](https://github.com/aiming-lab/Agent0/blob/main/Agent0/README.md)

**Primary sources** — [Paper dates](https://arxiv.org/abs/2511.16043) · [Original paper and numerical tables](https://arxiv.org/html/2511.16043v1) · [Official series repository and release date](https://github.com/aiming-lab/Agent0) · [Agent0 training implementation](https://github.com/aiming-lab/Agent0/blob/main/Agent0/README.md)

<a id="google-sima2-2025"></a>

## SIMA 2: A Generalist Embodied Agent for Virtual Worlds

**2025-11-13** · report · Direct bounded loop

**Publication date** — Official research announcement: 2025-11-13; first paper: 2025-12-04. Results use paper v1.

**Institutional relationship** — Google DeepMind's official SIMA-team announcement establishes affiliation.

**What changes and how feedback is reused** — Gemini sets tasks and scores trajectories. Experience trains subsequent SIMA generations, whose new policies collect further experience; demonstrations bootstrap the initial agent.

**Author-reported result** — On fixed ASKA tasks, fewer than one quarter initially exceeded the Gemini reward threshold (>50); later generations exceeded it on every task. This measures model-scored task coverage, not independently verified episode success. These fixed tasks were human-supplied.

**Evidence limits** — Bounded game experiments, model-based evaluation and short memory; no demonstrated improvement of Gemini or the learning algorithm itself.

**Code / weights / data / license** — Paper/demos verified. Training code, weights, experience data and their licences were not identified in opened official sources; proprietary Gemini remains required.

**Possible nanoRSI experiment — not implemented here** — Proposed: version learner generations and scored trajectories; evaluate transfer with an independent held-out task set.

![Figure 16: Self-improvement setup with task setter, reward model, experience dataset and retrained SIMA 2 agent.](assets/paper-figures/google-sima2-2025.png)

**Source figure / official image** — Figure 16: Self-improvement setup with task setter, reward model, experience dataset and retrained SIMA 2 agent. · Figure 16 · [source](https://arxiv.org/html/2512.04797v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — No verified public code/asset link in the audited sources.

**Primary sources** — [Google DeepMind announcement](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) · [Paper version history](https://arxiv.org/abs/2512.04797) · [Paper v1, section 4.5](https://arxiv.org/html/2512.04797v1)

<a id="alibaba-agentevolver"></a>

## AgentEvolver: Towards Efficient Self-Evolving Agent System

**2025-11-13** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2025-11-13; this is the original paper event, not a later repository update.

**Institutional relationship** — The paper explicitly identifies Tongyi Lab, Alibaba Group as its affiliation.

**What changes and how feedback is reused** — Mutates agent policy parameters using self-generated environment tasks. Self-questioning synthesizes and filters tasks; self-navigation retrieves prior experience to guide rollouts; self-attribution supplies differentiated credit alongside outcome rewards. RL updates become the next policy, while the experience pool supports subsequent exploration.

**Author-reported result** — Author Table 1: Qwen2.5-7B average avg@8 across AppWorld and BFCL-v3 rises from 15.8% to 45.2%, a 29.4 percentage-point difference. This compares the base model with the full trained system, not an isolated credit-assignment ablation.

**Evidence limits** — Task/judge quality and environment coverage bound the loop. Evidence concerns agent training, not unlimited autonomous redesign or general RSI.

**Code / weights / data / license** — Code: public ModelScope repository, Apache-2.0. Weights: no standalone paper checkpoint verified. Data: generation/integration code visible; complete training corpus and its license not verified.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI learner experiment: version generated task manifests with each policy checkpoint and compare experience reuse against a frozen-data control.

![Figure 2: AgentEvolver combines self-questioning, self-navigating and self-attributing mechanisms.](assets/paper-figures/alibaba-agentevolver.png)

**Source figure / official image** — Figure 2: AgentEvolver combines self-questioning, self-navigating and self-attributing mechanisms. · Figure 2 · [source](https://arxiv.org/html/2511.10395v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official AgentEvolver repository](https://github.com/modelscope/AgentEvolver)

**Primary sources** — [arXiv first submission](https://arxiv.org/abs/2511.10395) · [Paper v1: affiliation, methods, Table 1](https://arxiv.org/html/2511.10395v1) · [Official AgentEvolver repository](https://github.com/modelscope/AgentEvolver)

<a id="google-discorl-2025"></a>

## Discovering state-of-the-art reinforcement learning algorithms

**2025-10-22** · paper · Enabling technique / evaluation

**Publication date** — Online publication: 2025-10-22; December issue date is later. Manuscript receipt in December 2024 is not public publication.

**Institutional relationship** — Primary article lists all authors at Google DeepMind.

**What changes and how feedback is reused** — A meta-network supplies policy/prediction update targets. Meta-gradients maximize agents' collective return; updated rules train subsequent agents. The frozen discovered rule transfers to new environments.

**Author-reported result** — Extended Data Fig. 4 reports reaching MuZero's final Atari performance with approximately 40% less evaluation TPU computation: 57 games, 200M environment steps. This excludes the separate discovery cost.

**Evidence limits** — Bounded learning-rule discovery under a fixed human-designed meta-objective/framework; not evidence of general recursively self-modifying intelligence.

**Code / weights / data / license** — Official meta-training/evaluation code and Disco103 meta-parameters verified. Software: Apache-2.0; other repository materials: CC BY 4.0. Environment/data terms are separate. Full-scale reproduction is computationally substantial.

**Possible nanoRSI experiment — not implemented here** — Proposed: separate learner weights from update-rule parameters and test an outer objective in tiny environments before scaling.

![Official DiscoRL method diagram: a meta-network learns update targets from population experience.](assets/paper-figures/google-discorl-2025.png)

**Source figure / official image** — Official DiscoRL method diagram: a meta-network learns update targets from population experience. · Official project method figure · [source](https://google-deepmind.github.io/disco_rl/)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Official code and licence statements](https://github.com/google-deepmind/disco_rl)

**Primary sources** — [Primary Nature article at PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12695655/) · [Publication metadata](https://pubmed.ncbi.nlm.nih.gov/41125136/) · [Author project and artifact availability](https://google-deepmind.github.io/disco_rl/) · [Official code and licence statements](https://github.com/google-deepmind/disco_rl)

<a id="tencent-spear"></a>

## Learn the Ropes, Then Trust the Wins: Self-imitation with Progressive Exploration for Agentic Reinforcement Learning

**2025-09-26** · paper · Direct bounded loop

**Publication date** — arXiv v1 submitted 2025-09-26; the public repository was released around the same research release. Inclusion uses the first paper submission.

**Institutional relationship** — The paper lists Tencent Youtu Lab and four university collaborators. Tencent Youtu Lab is the industrial research lead; collaborators and ownership are kept explicit.

**What changes and how feedback is reused** — SPEAR combines a curriculum that schedules intrinsic tool-use rewards for progressive exploration with self-imitation replay for exploitation. Advantage recalibration corrects replay drift, while covariance-based clipping and entropy control stabilize updates. The replay buffer is reused across policy updates, creating a bounded policy-training loop.

**Author-reported result** — The abstract reports up to +16.1/+5.1/+8.6% on ALFWorld and +20.7/+11.8/+13.9% on WebShop over GRPO/GiGPO/Dr.BoT. In a controlled 32K Qwen2.5-32B-Instruct row, AIME24 rises from 67.2 with Dr.BoT to 71.0 (+3.8), and AIME25 from 55.1 to 61.0 (+5.9).

**Evidence limits** — Gains vary by model, task and ablation: self-imitation alone can reduce AIME24 in some rows. The task stream, verifier and reward design remain externally supplied, so this is policy self-improvement under a fixed training harness rather than an autonomous improver redesigning itself.

**Code / weights / data / license** — TencentYoutuResearch/SPEAR code is public and includes SPEAR_LICENSE.txt. The custom terms state that SPEAR is not intended for use within the European Union; GitHub API metadata reports NOASSERTION. Check third-party component terms before reuse; no released checkpoint is assumed beyond what the repository explicitly documents.

**Possible nanoRSI experiment — not implemented here** — Expose replay provenance in nanoRSI learner experiments: compare uniform, frozen-replay and recursively refreshed replay with matched rollout budgets, and report both held-out gains and replay-induced regressions.

![Figure 2: SPEAR couples progressive exploration with self-imitation replay and stabilized policy updates.](assets/paper-figures/tencent-spear.png)

**Source figure / official image** — Figure 2: SPEAR couples progressive exploration with self-imitation replay and stabilized policy updates. · Figure 2, overview.png · [source](https://ar5iv.labs.arxiv.org/html/2509.22601/assets/figures/overview.png)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Tencent YoutuResearch SPEAR repository](https://github.com/TencentYoutuResearch/SPEAR) · [SPEAR custom license terms](https://github.com/TencentYoutuResearch/SPEAR/blob/main/SPEAR_LICENSE.txt)

**Primary sources** — [arXiv first submission and history](https://arxiv.org/abs/2509.22601) · [Paper v1 and overview figure](https://arxiv.org/html/2509.22601v1) · [Tencent YoutuResearch SPEAR repository](https://github.com/TencentYoutuResearch/SPEAR) · [SPEAR custom license terms](https://github.com/TencentYoutuResearch/SPEAR/blob/main/SPEAR_LICENSE.txt)

<a id="tencent-moe-cl"></a>

## Self-Evolving LLMs via Continual Instruction Tuning

**2025-09-14** · paper · Enabling technique / evaluation

**Publication date** — arXiv v1: 2025-09-14; latest recorded revision 2025-10-15 (v4). Original submission is used for inclusion.

**Institutional relationship** — Paper v1 explicitly assigns authors to BUPT and Tencent AI Lab. Tencent is a collaborating institution and application setting.

**What changes and how feedback is reused** — Sequential instruction tuning updates task-specific and shared LoRA experts. A task-aware adversarial discriminator helps separate transferable knowledge from task-specific information; retained experts carry earlier knowledge into subsequent tasks. No autonomous task-generation/evaluation/improver-retraining loop is established, so classify this as enabling continual learning.

**Author-reported result** — The paper evaluates sequential learning and Tencent content-review applications. No numerical claim is retained here: its abstract describes review-cost reduction while the experimental discussion describes offline stripping-rate improvements, which need harmonization before quoting a business effect.

**Evidence limits** — Preserving knowledge under externally supplied task streams is not evidence of autonomous recursive self-improvement. Industrial data access limits reproducibility.

**Code / weights / data / license** — Public BAI-LAB/MoE-CL implementation verified. Weights and industrial data: not verified public. No code license was located on the opened repository page; do not assume reuse permission.

**Possible nanoRSI experiment — not implemented here** — Proposed nanoRSI learner control: evaluate a fixed externally supplied task stream, retaining per-task regression scores to distinguish continual learning from direct self-improvement.

![Figure 1: MoE-CL combines task-specific LoRA experts, a shared expert and a task-aware discriminator.](assets/paper-figures/tencent-moe-cl.png)

**Source figure / official image** — Figure 1: MoE-CL combines task-specific LoRA experts, a shared expert and a task-aware discriminator. · Figure 1 · [source](https://arxiv.org/html/2509.18133v1)

**nanoRSI reproduction** — not-run. Last source check: 2026-09-13.

**Open code / weights / data links** — [Author implementation](https://github.com/BAI-LAB/MoE-CL)

**Primary sources** — [arXiv submission and revision history](https://arxiv.org/abs/2509.18133) · [Paper v1 affiliations and experiments](https://arxiv.org/html/2509.18133v1) · [Author implementation](https://github.com/BAI-LAB/MoE-CL)
