# Coverage and date decisions / 检索覆盖与日期说明

[Research map](README.md) · [中文入口](README.zh-CN.md)

This initial audit was checked on **2026-09-13**, covering **2025-09-13–2026-09-13**. We searched company research pages, first-party repositories and paper publication histories, then opened the relevant primary documents. This is a selective engineering-oriented collection, not a systematic review or a ranking of labs. Newer paper versions may exist; a record pins the version supporting its result rather than silently changing its evidence. Daily midnight sweeps since **2026-09-14** append verified records to the rolling window (see [RADAR.md](RADAR.md)); the tables below cover the initial audit plus institutions added by those sweeps. The analytical synthesis of all records lives in the [living survey](../RSI_SURVEY.md) / [活综述](../RSI_SURVEY.zh-CN.md). / 本次首批资料核验于 **2026-09-13**，窗口为 **2025-09-13–2026-09-13**。检索覆盖公司研究页面、第一方仓库及论文发布记录，再打开相关原始材料核对。它面向工程实践，是精选集合，不是系统综述或机构排名；部分论文已有新版，条目固定引用提供该结果的版本。自 **2026-09-14** 起每日零点检索会把核验过的记录追加进滚动窗口（见 [RADAR.md](RADAR.md)）；下表覆盖首批审计及后续每日新增机构。

## Included institutional coverage / 已收录机构

The university and collaborator relationships appear in each record. A company name below means a verified research or report connection, not sole ownership or proof of RSI. / 每条记录保留高校及合作方关系；下列公司名称表示已核验的研究或报告关联，不代表独占成果或已证明 RSI。

| Organization / 机构 | Representative entry / 代表条目 |
| --- | --- |
| OpenAI | [GPT-Red](parameter-learning.zh-CN.md#gpt-red), [Codex development assistance](research-workflows.zh-CN.md#codex-builds-codex), [research acceleration report](research-workflows.zh-CN.md#openai-research-acceleration-2026) |
| Google DeepMind / Google | [SIMA 2](parameter-learning.zh-CN.md#google-sima2-2025), [DiscoRL](parameter-learning.zh-CN.md#google-discorl-2025), [AlphaEvolve MARL](research-workflows.zh-CN.md#google-alphaevolve-marl-2026), [Procedural Graphs](memory-context.zh-CN.md#procedural-graphs-google) |
| Anthropic / Fellows Program | [A3](parameter-learning.zh-CN.md#a3), [weak-to-strong researcher](research-workflows.zh-CN.md#automated-w2s), [alignment researchers](research-workflows.zh-CN.md#automated-alignment-researchers), [TASTE](research-workflows.zh-CN.md#taste) |
| Meta + universities | [Hyperagents](agent-code.zh-CN.md#meta-hyperagents-2026) |
| Microsoft + collaborators | [ACON](memory-context.zh-CN.md#microsoft-acon-2025), [LEGOMem](memory-context.zh-CN.md#microsoft-legomem-2025), [SkillOpt](agent-code.zh-CN.md#microsoft-skillopt) |
| Sakana AI + collaborators | [ShinkaEvolve](agent-code.zh-CN.md#sakana-shinkaevolve), [TRINITY](parameter-learning.zh-CN.md#sakana-trinity), [Doc-to-LoRA](parameter-learning.zh-CN.md#sakana-doc-to-lora), [RSI Lab](research-workflows.zh-CN.md#sakana-rsi-lab) — dedicated recursive-self-improvement group announced 2026-06-05 |
| SambaNova + Stanford / Berkeley | [ACE](memory-context.zh-CN.md#sambanova-stanford-ace) |
| Salesforce (Research / AI Labs) + UNC / Stanford | [Agent0](parameter-learning.zh-CN.md#salesforce-unc-agent0), [self-improving agents story](research-workflows.zh-CN.md#salesforce-toward-self-improving-agents) |
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
| HK PolyU + Huawei + Renmin University | [Experience Funnel](parameter-learning.zh-CN.md#experience-funnel-state-policy) — state-policy alternating loop with transition-aware distillation |
| Fudan (+ independent researcher) | [SkillLift](agent-code.zh-CN.md#skilllift-dense-rubrics) — bilevel rubric surrogate decoupling skill search from oracle rollouts |
| Renmin University (GSAI/data lab) | [EvoOntology](memory-context.zh-CN.md#evoontology-self-evolving) — self-evolving MCP ontology layer behind a paired acceptance gate |
| METR + Stanford / CMU / Columbia / MIT / Yale economists | [Economics of RSI](research-workflows.zh-CN.md#economics-of-rsi-2026) — feedback-loop elasticity calibration (~9% observed vs ≥15% threshold) |
| Meta FAIR + UIUC / CMU / NUS | [Self-play SWE-RL](parameter-learning.zh-CN.md#meta-ssr-self-play), [SPICE](parameter-learning.zh-CN.md#meta-spice-self-play) — self-play task generation with self-emitted test artifacts; variance-shaped adversarial curriculum |
| Amazon (AWS Agentic AI) + UW-Madison | [Autonomous 30B post-training](research-workflows.zh-CN.md#amazon-autonomous-post-training), [SAGE](parameter-learning.zh-CN.md#sage-skill-augmented-grpo) — no-human multi-round post-training with policy-only promotion; skill-integrated GRPO |
| Apple | [Reinforced Agent](agent-code.zh-CN.md#apple-reinforced-agent) — pre-execution tool-call review with GEPA-optimized reviewer prompts |
| NVIDIA + CMU + Berkeley | [ENPIRE](research-workflows.zh-CN.md#nvidia-enpire-physical-autoresearch) — physical autoresearch on 8 robots with self-constructed verification environments |
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

## Checked but not promoted to a dated main entry / 已检索但未强行收录

These are gaps in this audit, not evidence that an institution has no relevant work. / 以下是本轮核验缺口，不是“这些机构没有相关成果”的结论。

| Institution / lead | Decision and primary source / 决定与一手来源 |
| --- | --- |
| Nous Research / Hermes | [Hermes Agent](https://github.com/NousResearch/hermes-agent) documents persistent skills and memory. The [self-evolution repository](https://github.com/NousResearch/hermes-agent-self-evolution) marks skill evolution implemented, with code/system-prompt/continuous evolution still planned. A dated primary first-public announcement was not established; commit timestamps do not establish when a repository became public. Re-checked 2026-09-14: v0.21.0–v0.21.2 releases (Aug 31–Sept 11) are session-store reliability work, not a new mechanism. Re-checked 2026-09-15: v0.21.3 (Sept 14) rolls up ~338 PRs, still remote-gateway/session reliability. / 已见持久技能和记忆；独立进化仓库仅确认技能进化，其他目标仍在计划中。尚未核实第一方公开首发日，不能用提交时间代替。2026-09-14 复查：v0.21.0–v0.21.2（8 月 31 日–9 月 11 日）为会话存储可靠性修复，非新机制。2026-09-15 复查：v0.21.3（9 月 14 日）合入约 338 个 PR，仍为远程网关/会话可靠性工作。 |
| Moonshot AI | [Kimi K2.5](https://www.kimi.com/en/blog/kimi-k2-5) describes PARL orchestrator training with frozen subagents. No separate persistent self-modification or successor-training demonstration was verified in this pass. / PARL 编排器训练与并行任务执行不自动等于持久自修改或后继模型训练，本轮未核实独立直接闭环成果。 |
| Zhipu / Z.AI | [GLM-5 documentation](https://docs.z.ai/guides/llm/glm-5) describes planning, tools and self-checks; retained improvement was not established from this source. / 规划、工具和自检本身不足以证明持续保留的自改进。早期 WebRL 另列下表。 |
| Mistral | [Remote agents / Medium 3.5](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/) describes agent execution and model capabilities; an autonomous persistent improvement mechanism was not verified. / 已检索产品能力，未核实自主持久改进机制。 |
| Reflection | [Company news](https://reflection.ai/news) provides organizational and infrastructure updates; no sufficiently specified mutation/feedback/reuse result was verified. / 已检索公司及基础设施动态，未核实足够明确的修改、反馈与复用实验。 |
| Alibaba CuES | [Paper](https://arxiv.org/abs/2512.01311) is a relevant follow-up lead; the full affiliation, mechanism and release audit is pending. / 是相关后续线索，完整机构、机制和资产核验待完成。 |
| ByteDance Seed-Evolving | Reported 2026-09-11 by [Tencent News](https://news.qq.com/rain/a/20260911A0F8DU00) as a self-evolving model; no official Seed page or paper existed when checked on 2026-09-14 (official list ends 2026.08.18). Re-checked 2026-09-15: the official list is unchanged. Re-checked 2026-09-16: still ends at Chain-of-Experience (2026.08.18). Media lead only; revisit when ByteDance publishes. / 腾讯新闻 2026-09-11 报道的自进化模型；2026-09-14 核验时 Seed 官方页无论文或公告（官方列表止于 2026.08.18）。2026-09-15 复查：官方列表无变化。2026-09-16 复查：仍止于 Chain-of-Experience（2026.08.18）。仅作媒体线索，官方发布后再议。 |

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
