# Coverage and date decisions / 检索覆盖与日期说明

[Research map](README.md) · [中文入口](README.zh-CN.md)

This initial audit was checked on **2026-09-13**, covering **2025-09-13–2026-09-13**. We searched company research pages, first-party repositories and paper publication histories, then opened the relevant primary documents. This is a selective engineering-oriented collection, not a systematic review or a ranking of labs. Newer paper versions may exist; a record pins the version supporting its result rather than silently changing its evidence. Daily midnight sweeps since **2026-09-14** append verified records to the rolling window (see [RADAR.md](RADAR.md)); the tables below cover the initial audit plus institutions added by those sweeps. The analytical synthesis of all records lives in the [living survey](../RSI_SURVEY.md) / [活综述](../RSI_SURVEY.zh-CN.md). / 本次首批资料核验于 **2026-09-13**，窗口为 **2025-09-13–2026-09-13**。检索覆盖公司研究页面、第一方仓库及论文发布记录，再打开相关原始材料核对。它面向工程实践，是精选集合，不是系统综述或机构排名；部分论文已有新版，条目固定引用提供该结果的版本。自 **2026-09-14** 起每日零点检索会把核验过的记录追加进滚动窗口（见 [RADAR.md](RADAR.md)）；下表覆盖首批审计及后续每日新增机构。

## Included institutional coverage / 已收录机构

The university and collaborator relationships appear in each record. A company name below means a verified research or report connection, not sole ownership or proof of RSI. / 每条记录保留高校及合作方关系；下列公司名称表示已核验的研究或报告关联，不代表独占成果或已证明 RSI。

| Organization / 机构 | Representative entry / 代表条目 |
| --- | --- |
| OpenAI | [GPT-Red](parameter-learning.zh-CN.md#gpt-red), [Codex development assistance](research-workflows.zh-CN.md#codex-builds-codex), [research acceleration report](research-workflows.zh-CN.md#openai-research-acceleration-2026) |
| Google DeepMind / Google | [SIMA 2](parameter-learning.zh-CN.md#google-sima2-2025), [DiscoRL](parameter-learning.zh-CN.md#google-discorl-2025), [AlphaEvolve MARL](research-workflows.zh-CN.md#google-alphaevolve-marl-2026), [Procedural Graphs](memory-context.zh-CN.md#procedural-graphs-google) |
| Anthropic / Fellows Program / Institute | [A3](parameter-learning.zh-CN.md#a3), [weak-to-strong researcher](research-workflows.zh-CN.md#automated-w2s), [alignment researchers](research-workflows.zh-CN.md#automated-alignment-researchers), [TASTE](research-workflows.zh-CN.md#taste), [When AI builds itself](research-workflows.zh-CN.md#anthropic-when-ai-builds-itself) — 2026-06 institute essay with internal RSI telemetry; [pace measurements](research-workflows.zh-CN.md#anthropic-measuring-pace) — 2026-09-17 R&D Automation Index (Claude leads 26%), oversight and safety-compute telemetry |
| Meta + universities | [Hyperagents](agent-code.zh-CN.md#meta-hyperagents-2026) |
| Microsoft + collaborators | [ACON](memory-context.zh-CN.md#microsoft-acon-2025), [LEGOMem](memory-context.zh-CN.md#microsoft-legomem-2025), [SkillOpt](agent-code.zh-CN.md#microsoft-skillopt) |
| Sakana AI + collaborators | [ShinkaEvolve](agent-code.zh-CN.md#sakana-shinkaevolve), [TRINITY](parameter-learning.zh-CN.md#sakana-trinity), [Doc-to-LoRA](parameter-learning.zh-CN.md#sakana-doc-to-lora), [RSI Lab](research-workflows.zh-CN.md#sakana-rsi-lab) — dedicated recursive-self-improvement group announced 2026-06-05 |
| SambaNova + Stanford / Berkeley | [ACE](memory-context.zh-CN.md#sambanova-stanford-ace) |
| Salesforce (Research / AI Labs) + UNC / Stanford | [Agent0](parameter-learning.zh-CN.md#salesforce-unc-agent0), [self-improving agents story](research-workflows.zh-CN.md#salesforce-toward-self-improving-agents), [EvoHarnessBench](research-workflows.zh-CN.md#evoharnessbench-harness-evolution) — harness-evolution benchmark quantifying harness-induced forgetting (with UNC/UW–Madison, 2026-09) |
| Prime Intellect + collaborators | [Prime Agent](memory-context.zh-CN.md#prime-agent), [autonomous research evaluation](research-workflows.zh-CN.md#prime-measuring-autonomous-ai-research) |
| Cognition | [Devin builds Devin](research-workflows.zh-CN.md#cognition-devin-builds-devin) |
| Alibaba / Tongyi / Qwen | [AgentEvolver](parameter-learning.zh-CN.md#alibaba-agentevolver), [Qwen3.8-Max self-evolving harness](agent-code.zh-CN.md#qwen38-max-self-evolving-harness) |
| ByteDance Seed + collaborators | [HarnessDev](agent-code.zh-CN.md#bytedance-harnessdev), [S3Gym](memory-context.zh-CN.md#bytedance-s3gym), [Aspire](parameter-learning.zh-CN.md#bytedance-aspire), [Chain-of-Experience with UCSC](memory-context.zh-CN.md#bytedance-chain-of-experience) |
| Tencent / WeChat AI | [SkillHone](agent-code.zh-CN.md#tencent-skillhone) — persistent decision history and skill revision loop; the paper's enterprise harness and the public implementation are recorded separately |
| Tencent Youtu Lab + collaborators | [SPEAR](parameter-learning.zh-CN.md#tencent-spear) — self-imitation replay and progressive exploration; [Training-Free GRPO](memory-context.zh-CN.md#tencent-training-free-grpo) — frozen-model experience evolution |
| Tencent AI Lab + CUHK | [WebAggregator / Explore-to-Evolve](agent-code.zh-CN.md#tencent-webaggregator) — executable web aggregation programs and verified training data |
| Tencent AI Lab + BUPT | [MoE-CL](parameter-learning.zh-CN.md#tencent-moe-cl), classified as enabling / 持续学习支撑技术 |
| DeepSeek | [DeepSeekMath-V2](parameter-learning.zh-CN.md#deepseek-math-v2) |
| MiniMax | [M2.7 self-evolution report](agent-code.zh-CN.md#minimax-m27-self-evolution) |
| Frontis.AI / Horizon Research + Tsinghua | [Frontis-MA1 / OpenRSI](research-workflows.zh-CN.md#frontis-ma1-openmle) |
| TokenRhythm + Infinigence + Tsinghua / PKU / CUHK / Alibaba | [NeoHorse-1](parameter-learning.zh-CN.md#tokenrhythm-neohorse-1) |
| SJTU Theseus Labs + Tsinghua / ByteDance / Shanghai AI Lab et al. | [genuine RSI roadmap](research-workflows.zh-CN.md#genuine-rsi-roadmap-2026) |
| NUS + IAIC (Singapore) | [SkillGLoW](agent-code.zh-CN.md#skillglow-procedural-families) — procedural-family skill consolidation behind a verifier-grounded commit gate |
| Tsinghua + Beijing Jiaotong | [SkillEvolver](agent-code.zh-CN.md#skillevolver-meta-skill) — skill learning as a portable meta-skill with a fresh-session auditor |
| UESTC + Zhejiang | [Persistent skills on OSWorld](agent-code.zh-CN.md#persistent-skills-osworld) — online evolution of a versioned GUI skill library |
| PKU + Edinburgh + Northwestern (+ Tencent / Tsinghua) | [SE-GoS](memory-context.zh-CN.md#se-gos-skill-graph) — training-free self-evolution of a skill-retrieval graph |
| Jilin + Tongji | [SimSkill](agent-code.zh-CN.md#simskill-traffic) — gap-driven self-evolving agent for SUMO traffic simulation |
| HUST + USTC + Microsoft Research + AIR Tsinghua + Nanjing | [EmbodiSkill](agent-code.zh-CN.md#embodiskill-skill-aware-reflection) — skill-aware reflection splitting defect edits from lapse re-emphasis |
| Aether AI + UCSD + UIC | [RSIAgent](memory-context.zh-CN.md#rsiagent-autonomous-exploration) — broad-then-deep autonomous exploration freezing a causal memory |
| Weco AI | [AIDE²](agent-code.zh-CN.md#weco-aide2-first-evidence) — the AIDE lineage's bi-level self-rewriting loop with a fixed-budget reject ladder; the 2026-09-22 technical report is now the primary evidence, but its implementation, weights and data remain unreleased; [AutoData](parameter-learning.zh-CN.md#autodata-pretraining-search) — with UvA, agentic search over pre-training data-selection programs (2026-09-17) |
| Nous Research / Hermes | [Hermes self-refactor](agent-code.zh-CN.md#nous-hermes-selfrefactor) — the agent reworks its own ~1M-line codebase with 1,393 worktree-isolated subagents and auto-saved skills (2026-09-15); promoted from the tracked-leads table once the dated first-party post appeared |
| Intrepid Labs (Toronto) | [Andromeda 2](research-workflows.zh-CN.md#andromeda2-evidence-grounded-lab) — evidence-grounded autonomous formulation lab |
| UC San Diego + Johns Hopkins | [PrimeScientist](research-workflows.zh-CN.md#primescientist-effort-allocation) — strategic effort allocation for autonomous research |
| University of Washington + Georgetown | [Trusting Trust, revisited](agent-code.zh-CN.md#trusting-trust-self-modifying) — poisoned benchmarks contaminating self-modifying agents |
| University of Washington + AI2 + UPenn | [EvoLM](parameter-learning.zh-CN.md#evolm-coevolved-rubrics) — co-evolved discriminative rubrics via temporal contrast, ICLR-2026 RSI-workshop spotlight |
| HK PolyU + Huawei + Renmin University | [Experience Funnel](parameter-learning.zh-CN.md#experience-funnel-state-policy) — state-policy alternating loop with transition-aware distillation |
| Fudan (+ independent researcher) | [SkillLift](agent-code.zh-CN.md#skilllift-dense-rubrics) — bilevel rubric surrogate decoupling skill search from oracle rollouts |
| Renmin University (GSAI/data lab) | [EvoOntology](memory-context.zh-CN.md#evoontology-self-evolving) — self-evolving MCP ontology layer behind a paired acceptance gate |
| METR + Stanford / CMU / Columbia / MIT / Yale economists | [Economics of RSI](research-workflows.zh-CN.md#economics-of-rsi-2026) — feedback-loop elasticity calibration (~9% observed vs ≥15% threshold) |
| Meta FAIR + UIUC / CMU / NUS | [Self-play SWE-RL](parameter-learning.zh-CN.md#meta-ssr-self-play), [SPICE](parameter-learning.zh-CN.md#meta-spice-self-play) — self-play task generation with self-emitted test artifacts; variance-shaped adversarial curriculum |
| Amazon (AWS Agentic AI) + UW-Madison | [Autonomous 30B post-training](research-workflows.zh-CN.md#amazon-autonomous-post-training), [SAGE](parameter-learning.zh-CN.md#sage-skill-augmented-grpo) — no-human multi-round post-training with policy-only promotion; skill-integrated GRPO |
| Apple | [Reinforced Agent](agent-code.zh-CN.md#apple-reinforced-agent) — pre-execution tool-call review with GEPA-optimized reviewer prompts |
| NVIDIA (+ CMU + Berkeley) | [ENPIRE](research-workflows.zh-CN.md#nvidia-enpire-physical-autoresearch) — physical autoresearch on 8 robots with self-constructed verification environments; [Agora](research-workflows.zh-CN.md#agora-git-shared-memory) — Git-DAG shared memory for collective AutoResearch (all-NVIDIA authorship) |
| Huawei + VU Amsterdam | [EvoScientist](research-workflows.zh-CN.md#evoscientist-self-evolving) — ideation/experimentation memory evolution; ICAIS 2025 Best Paper |
| Inherent Laboratories | [Faraday / Replica](research-workflows.zh-CN.md#faraday-replica-ai-scientist) — training AI scientists to replicate research under auto-generated rubric judges |
| Stanford (Finn group / IRIS) + MIT + KRAFTON | [Feedback Descent](agent-code.zh-CN.md#stanford-feedback-descent), [Meta-Harness](agent-code.zh-CN.md#stanford-meta-harness) — preference rationales as text gradients; harness search over full-trace filesystems |
| Princeton PLI (Arora) | [Contextual Drag](research-workflows.zh-CN.md#princeton-contextual-drag) — erroneous in-context drafts drag SOTA reasoners 10-20% |
| CMU (Wu & Raghunathan) | [STV](parameter-learning.zh-CN.md#cmu-stv-self-trained-verification) — self-trained verification for training- and test-time improvement |
| UNC (aiming-lab) + NEC + UC system | [SkillRL](parameter-learning.zh-CN.md#skillrl-skill-augmented-rl) — skill-bank ↔ policy co-evolution |
| Fudan + Nankai + Hello Group | [EvoRS](parameter-learning.zh-CN.md#evors-reward-evolution) — the reward system itself evolves as an executable DAG |
| Tsinghua + Eigen AI | [EigenData](parameter-learning.zh-CN.md#eigendata-self-evolving-synthesis) — self-evolving synthetic-data pipeline with per-instance checkers |
| CAS (UCAS + Inst. of Automation) + PKU + Mininglamp + THU + Qilu | [SESA](parameter-learning.zh-CN.md#sesa-self-play-skills) — asymmetric self-play with solver-only skill retrieval |
| TU/e + Liverpool + MIT-IBM Watson | [Q-Evolve](parameter-learning.zh-CN.md#qevolve-in-distribution) — in-distribution critic co-evolution |
| Duke + Adobe + PSU + NUS + OSU + Amazon | [RLSVR / SpyRL](parameter-learning.zh-CN.md#spyrl-self-verifiable-rewards) — task transformation induces mechanically checkable rewards |
| Shanghai AI Lab + ZJU/ECNU/Fudan/SJTU/USTC | [EvolveR](parameter-learning.zh-CN.md#evolver-experience-lifecycle) — offline self-distillation alternated with policy RL |
| UIUC (Ji / Hakkani-Tür / Tur) | [TT-SI](parameter-learning.zh-CN.md#ttsi-test-time-self-improvement) — test-time self-improvement via temporary LoRA |
| Google Research + Harvard / Virginia Tech | [WikiSkill](agent-code.zh-CN.md#wikiskill-experience-wiki), [Generalization Gap](research-workflows.zh-CN.md#gengap-self-evolution) — wiki-audited skill evolution; sharpening-vs-learning controls |
| NTU Singapore + UIUC + UIC + THU | [MemSkill](memory-context.zh-CN.md#memskill-memory-skills) — memory operations as evolvable skills |
| Minnesota + SNU | [Meta^n](agent-code.zh-CN.md#metan-emergent-depth) — measured meta-depth 3-6 vs ~2.5 prior cap |
| UESTC + LMU Munich + MCML | [MGM](agent-code.zh-CN.md#mgm-mendel-godel-machine) — Mendelian comparative evolution of coding agents |
| Alibaba Amap (DreamX) | [SkillClaw](agent-code.zh-CN.md#skillclaw-collective-evolution) — collective skill evolution across a user fleet |
| A3 Lab (Shenzhen Aquaintelling + Fudan) | [GenericAgent](agent-code.zh-CN.md#genericagent-skill-tree) — 3.3K-line seed growing a skill tree |
| U Maryland + Google DeepMind + UVA | [Dream-RSI](agent-code.zh-CN.md#dream-rsi-replay-simulator) — offline policy improvement by replaying the discovery tree |
| Tübingen (ELLIS/MPI/AI Center) + Thoughtful Lab | [PostTrainBench](research-workflows.zh-CN.md#posttrainbench-autonomous-post-training) — benchmarking autonomous post-training with a cheating ledger |
| Jilin + KAUST + Alberta + IDSIA (Schmidhuber) | [Self-Improving Agents survey](research-workflows.zh-CN.md#self-improving-agents-survey) — the self-induced update-operator formalism |
| AI-scientist audit (Tianyu Ding et al.) | [Verification gap](research-workflows.zh-CN.md#ai-scientist-verification-gap) — 0/9 LLM-era closed-loop systems externally validated |
| Sakana AI + U Michigan + Science Tokyo | [Conductor / Fugu](parameter-learning.zh-CN.md#sakana-conductor-fugu) — RL-trained orchestrator designing recursive topologies (RSI-Lab lineage) |
| HKUST + ZJU + HUST | [XSkill](memory-context.zh-CN.md#xskill-dual-stream) — dual-stream visually-grounded skills and experiences for multimodal agents |
| ANU + Linköping + MBZUAI + Aalto | [EvoLMM](parameter-learning.zh-CN.md#evolmm-proposer-solver) — label-free multimodal self-evolution with continuous rewards |
| Arc Intelligence | [ATLAS](memory-context.zh-CN.md#atlas-pamphlets) — teacher/student pamphlets for gradient-free continual adaptation |
| UIUC + Google DeepMind | [Evo-Memory](memory-context.zh-CN.md#evo-memory-remem) — streaming benchmark for self-evolving memory; hard-to-easy ordering wins |
| Lehigh + UIC + UBC/Vector + Salesforce + MGH/Harvard | [OpenSkill](agent-code.zh-CN.md#openskill-open-world) — skills and verification anchors from open-world sources |
| UW + Stanford + CMU + MIT + NUS + SNU + Stevens + NEU + UChicago | [SPADE](parameter-learning.zh-CN.md#spade-adaptive-environments) — self-play in corpus-grounded executable environments |
| USTC + CUHK + Macau + Tsinghua + ZJU + Soochow + Brown + SJTU | [EvoPolicyGym](agent-code.zh-CN.md#evopolicygym-benchmark) — benchmarking executable-policy evolution |
| NUS + Stanford + Oxford + Princeton | [Recuris](memory-context.zh-CN.md#recuris-memory-evolution) — recursive experiential-working memory evolution |
| DeepGrounding / AlphaAvatar / IIT | [RSI survey](research-workflows.zh-CN.md#rsi-survey-1250) — 1,250 papers, two-axis taxonomy, verification hierarchy |
| StepFun + academic partners | [SE-Agent](memory-context.zh-CN.md#se-agent-trajectory) — trajectory-level self-evolution (archival, v1 predates window) |
| K-Dense AI | [Scientific Agent Skills](agent-code.zh-CN.md#scientific-agent-skills-library) — 163-skill curated library, 45K stars |
| Beihang + Manchester + IQuest Research + M-A-P + Langboat + Hohai | [ModularRSI](agent-code.zh-CN.md#modularrsi-modular-harness) — scoped module evolution with conflict-resolving integration on benchmark-disjoint tasks |
| PhAI Labs + Fudan Zhongshan Hospital + Shanghai Academy of Natural Sciences + Shunwei Capital + Oxford + Stanford + Princeton | [ScienceBuddy](research-workflows.zh-CN.md#sciencebuddy-recursive-in-recursive) — recursive-in-recursive: paired-dev harness edits alternate with GRPO model training |
| Johns Hopkins + Amazon AGI | [EchoPath](memory-context.zh-CN.md#echopath-replayable-memory) — execution-level replayable memory with validation provenance and lifecycle states |
| CityU HK + Huawei Noah's Ark + A*STAR (with Adelaide on the safety audit) | [AlgoEvo](agent-code.zh-CN.md#algoevo-agentic-search), [Skill Misevolution](agent-code.zh-CN.md#skill-misevolution-safety) — self-evolving agentic algorithm search; skill-evolution safety audit |
| CosmosMind | [MetaRSI / RSI2](research-workflows.zh-CN.md#metarsi-composition) — Data/Harness/Model-RSI operators under a learned schedule; artifact repository ships no license file (reference only) |
| Zhipu (HKEX 2513) | [GLM fully-self-training filing](research-workflows.zh-CN.md#zhipu-glm-selftraining-filing) — recursive self-improvement closed loop written into the funded use-of-proceeds disclosure of 2026-09-13 |
| UIC + MBZUAI/McGill + Columbia + ZJU + UBC | [CoEvoSkills](agent-code.zh-CN.md#coevoskills-coevolutionary-verification) — skill generator and surrogate verifier co-evolve behind an information-isolated oracle (COLM 2026) |
| Tübingen ELLIS/MPI cluster | [GASP](parameter-learning.zh-CN.md#gasp-guided-asymmetric-selfplay) — goalpost-anchored asymmetric self-play, ICLR-2026 RSI-workshop spotlight |
| Fudan (School of Data Science) | [ACE adversarial tests](parameter-learning.zh-CN.md#ace-fudan-adversarial-tests) — one LLM alternating Solver/Adversary roles trains itself without ground truth (in addition to the earlier SkillLift row) |
| NVIDIA + NTU + MIT | [SoL-Pi](agent-code.zh-CN.md#solpi-recursive-autoresearch-loops) — recursively scaling auto-research loops over the agent harness with a never-touched held-out benchmark |
| Microsoft Research Asia + CityU HK | [RHO](agent-code.zh-CN.md#rho-retrospective-harness) — label-free full-stack harness optimization from past trajectories via self-preference (June miss caught 2026-09-19) |
| Nanjing University (NKLST) | [SkillAA](agent-code.zh-CN.md#skillaa-attribution-rollback) — attribution-guided skill-graph repairs behind Local/Big gates with rollback |
| SimpleWay.AI + McGill/Toronto/UCLA/CUHK/Mila + 6 more | [FinSkillOps](agent-code.zh-CN.md#finskillops-sec-filing-qa) — gated skill lifecycle for SEC-filing QA with a 6/33 honest promotion rate |
| University of Birmingham | [STRETCH](parameter-learning.zh-CN.md#stretch-unified-self-taught) — unified scaffolder/learner self-play with 50%-success difficulty alignment |
| Tsinghua IIIS + SJTU + Shanghai Qi Zhi | [CERA-MoA](parameter-learning.zh-CN.md#cera-moa-coevolving-routing) — familiarity-driven routing co-evolving with continually learning agents |
| Boltzbit + Cambridge | [Infinite-Parameter LLMs](parameter-learning.zh-CN.md#infinite-parameter-weights-from-live-data) — weights generated from live data via online Bayesian belief (CC BY-NC-ND — reference only) |
| KAIST + DeepAuto.ai | [EvolveTrade](agent-code.zh-CN.md#evolvetrade-experience-driven-policy) — experience-driven prompt-policy refinement for trading agents with honest per-window losses |
| XPENG Robotics | [XPACE](parameter-learning.zh-CN.md#xpace-world-model-selfimprovement) — world-model-driven self-improvement loop on real robots |
| UNC-Chapel Hill + Berkeley + UCSC | [SimpleMem](memory-context.zh-CN.md#simplemem-lifelong-memory) — compression-then-consolidation lifelong memory, ICLR-2026 RSI-workshop |
| Zhejiang University + Alibaba | [RetireOPD](parameter-learning.zh-CN.md#retireopd-self-retiring-distillation) — skill internalization with divergence-triggered teacher retirement |
| Anthropic (CEO essay) | [We Must Pace the Frontier](research-workflows.zh-CN.md#amodei-pace-the-frontier) — first-party statement that RSI is starting across the industry including at Anthropic, with a proposed RSI speed-limit level (2026-09-12) |
| Tencent Hunyuan | [Hyra](research-workflows.zh-CN.md#tencent-hyra-research-agent) — the Hunyuan Research Agent with an Experience Bank loop and eval-solution co-evolution (2026-07-21) |
| ByteDance Seed | [Seed-for-Seed](research-workflows.zh-CN.md#bytedance-seed-for-seed) — the model participating in its own development pipeline (evaluation, data, training, research, infrastructure), disclosed 2026-06-23 |
| IBM Research | [Evolution or Illusion](research-workflows.zh-CN.md#evolution-or-illusion-budget) — seeds-by-iterations evaluation protocol showing budget-dependent rankings in evolutionary search (2026-09-17) |
| The Walt Disney Company | [AURA](agent-code.zh-CN.md#aura-recommender-refinement) — production recommender diagnosis-to-code-refinement pipeline with honest null results (2026-09-15) |
| AgentDescent (independent) | [AgentDescent](agent-code.zh-CN.md#agentdescent-agent-gradient) — MIT-licensed multi-worker engine with reflective merge for shared-artifact evolution (2026-07-26) |
| Prism Shadow | [PenguinHarness](agent-code.zh-CN.md#penguin-harness-self-evolution) — Apache-2.0 auto-dev platform with a benchmark→fix→ship self-evolution engine; marketing-grade claims, benchmarks not yet public (2026-07-19) |
| Pengcheng Laboratory + HIT Shenzhen (+ China Unicom GBA Institute) | [ThinkFlow](memory-context.zh-CN.md#thinkflow-latent-memory), [Interactive Memory Learning](memory-context.zh-CN.md#interactive-memory-learning) — sibling latent-memory and memory-policy papers from one group (2026-09-15) |
| CUHK-Shenzhen + Edinburgh | [harness-value](research-workflows.zh-CN.md#harness-value-sham-control) — placebo-controlled decomposition of agent-harness value (2026-09-17) |
| NYU + Princeton | [Compiled Agency](agent-code.zh-CN.md#compiled-agency-gauntlet) — coding agents compile standalone game controllers from bare interaction (2026-09-17) |
| Zhejiang University + HKU + HKUST | [Reflective Recovery](parameter-learning.zh-CN.md#reflective-recovery) — self-supervised recovery training from failed trajectories (2026-09-18) |

## Checked but not promoted to a dated main entry / 已检索但未强行收录

These are gaps in this audit, not evidence that an institution has no relevant work. / 以下是本轮核验缺口，不是“这些机构没有相关成果”的结论。

| Institution / lead | Decision and primary source / 决定与一手来源 |
| --- | --- |
| Nous Research repositories | The [Hermes Agent](https://github.com/NousResearch/hermes-agent) and [self-evolution](https://github.com/NousResearch/hermes-agent-self-evolution) repositories themselves still lack a dated primary mechanism announcement; the 2026-09-15 refactor post (now a main entry above) is the first dated first-party artifact. Re-checked 2026-09-18: v0.21.3 (Sept 14) remains the last release; Sept-17 commits add a capability fail-closed gate as a breaking change, v0.21.4 imminent. / 两个仓库仍缺带日期的第一方机制公告；2026-09-15 重构博文（已升为主条目）是首个带日期一手产物。2026-09-18 复查：v0.21.3（9 月 14 日）仍为最新发布；9 月 17 日提交以破坏性变更加入能力 fail-closed 闸门，v0.21.4 将近。 |
| Moonshot AI | [Kimi K2.5](https://www.kimi.com/en/blog/kimi-k2-5) describes PARL orchestrator training with frozen subagents. No separate persistent self-modification or successor-training demonstration was verified in this pass. / PARL 编排器训练与并行任务执行不自动等于持久自修改或后继模型训练，本轮未核实独立直接闭环成果。 |
| Zhipu / Z.AI | GLM-5 documentation (planning, tools, self-checks) was insufficient for a mechanism entry, and the official docs portal listed nothing new when checked 2026-09-17; the 2026-09-13 HKEX filing is now covered as a dated main entry above. / GLM-5 文档（规划、工具、自检）不足以立机制条目，2026-09-17 核验官方文档站亦无新条目；2026-09-13 港交所公告已作为带日期主条目收录（见上表）。 |
| Mistral | [Remote agents / Medium 3.5](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/) describes agent execution and model capabilities; an autonomous persistent improvement mechanism was not verified. / 已检索产品能力，未核实自主持久改进机制。 |
| Reflection | [Company news](https://reflection.ai/news) provides organizational and infrastructure updates; no sufficiently specified mutation/feedback/reuse result was verified. / 已检索公司及基础设施动态，未核实足够明确的修改、反馈与复用实验。 |
| Alibaba CuES | [Paper](https://arxiv.org/abs/2512.01311) is a relevant follow-up lead; the full affiliation, mechanism and release audit is pending. / 是相关后续线索，完整机构、机制和资产核验待完成。 |
| ByteDance Seed-Evolving | Reported 2026-09-11 by [Tencent News](https://news.qq.com/rain/a/20260911A0F8DU00) as a self-evolving model; no official Seed page or paper existed when checked on 2026-09-14 (official list ends 2026.08.18). Re-checked 2026-09-15: the official list is unchanged. Re-checked 2026-09-16: still ends at Chain-of-Experience (2026.08.18). Re-checked 2026-09-17: unchanged; HarnessDev (2026-09-01, catalogued) is not listed there either. Re-checked 2026-09-18: the old publications URL now 404s — the site restructured into a 'Blog & Publication' page whose newest entry is SeedRealtime (2026-08-05); still no Seed-Evolving trace. Re-checked 2026-09-19 by opening the Seed2.1 release post (2026-06-23) in both EN and ZH: neither version mentions a seed-evolving endpoint or weekly rolling upgrades — the claim stays media-only; the verifiable first-party anchor in that post is the Seed-for-Seed initiative, now a main entry above. / 腾讯新闻 2026-09-11 报道的自进化模型；2026-09-14 起连续复查官方均无对应页面。2026-09-19 以内置浏览器打开 Seed2.1 发布博文（2026-06-23）中英文版逐段核验：两版均无 seed-evolving 端点或每周滚动升级表述——该说法维持仅媒体；博文中可核验的一手锚点是 Seed-for-Seed 计划，已作为主条目收录（见上表）。 |

## Earlier foundations / 窗口之前的基础工作

These remain useful reading, but are excluded from the current new-work count. A later revision, conference appearance or announcement does not reset the original contribution's date. / 这些仍值得阅读，但不计入本窗口新工作数量；修订、参会或再次宣传不改变原始贡献的日期。

| Work | Original date | Why retain it / 保留原因 |
| --- | --- | --- |
| [AlphaEvolve introduction](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | 2025-05-14 | Program evolution foundation; the 2026 MARL paper is a separate application / 程序进化基础，2026 MARL 论文为不同成果 |
| [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) | 2025-05-29 | Agent-code archive and stepping stones / Agent 代码档案及中间候选复用 |
| [Text-to-LoRA](https://arxiv.org/abs/2506.06105) | 2025-06-06 | Generated adapters; distinguish from 2026 Doc-to-LoRA / 生成适配器，区别于 2026 年 Doc-to-LoRA |
| [Agent Lightning](https://arxiv.org/abs/2508.03680) | 2025-08-05 | Agent-training infrastructure; later publicity does not redate it / Agent 训练基础设施，后续宣传不重置日期 |
| [WebEvolver](https://arxiv.org/abs/2504.21024) | 2025-04-23 | Earlier self-evolving web-agent work / 早期 Web Agent 自进化工作 |
| [WebCoT](https://arxiv.org/abs/2505.15478) | 2025-05-26 | Tencent SelfEvolvingAgent archive entry; outside the current one-year window / Tencent SelfEvolvingAgent 档案中的条目，超出当前一年窗口 |
| [Cognitive Kernel-Pro](https://arxiv.org/abs/2508.00414) | 2025-08-01 | Tencent research lead and public repository, but outside the current window / 腾讯研究与公开仓库，首发日期超出当前窗口 |
| [WebRL](https://arxiv.org/abs/2411.02337) | 2024-11-04 | Earlier Tsinghua/Zhipu web-agent curriculum RL; [paper affiliations](https://openreview.net/pdf?id=oVKEAFjEqv) / 早期清华、智谱课程强化学习，机构关系见论文 |

## How to read the evidence / 如何理解证据

Publication access, implementation access and successful reproduction are separate. The catalogue contains no newly reproduced upstream result. Noncommercial code such as Hyperagents and OpenRSI must not be treated as an unrestricted dependency of nanoRSI; a paper license does not determine its code, model or dataset license.

论文可读、实现可下载和复现成功是三件不同的事。本资料库没有新增上游复现实验。Hyperagents、OpenRSI 等非商业许可代码不能当作 nanoRSI 可不受限引入的依赖；论文许可也不决定代码、模型或数据许可。

Further contributions should add a dated primary source, explain the persistent change and feedback, and retain failed attempts or missing controls. Unknown availability is a reason to investigate, not to invent a release or silently discard a useful result.

后续贡献应提供带日期的一手来源，说明持久改变和反馈，并保留失败尝试或缺失对照。未确认资产可用性意味着需要继续核查，不应据此虚构发布或直接忽略有价值的成果。
