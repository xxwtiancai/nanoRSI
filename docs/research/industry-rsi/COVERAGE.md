# Coverage and date decisions / 检索覆盖与日期说明

[Research map](README.md) · [中文入口](README.zh-CN.md)

This initial audit was checked on **2026-09-13**, covering **2025-09-13–2026-09-13**. We searched company research pages, first-party repositories and paper publication histories, then opened the relevant primary documents. This is a selective engineering-oriented collection, not a systematic review or a ranking of labs. Newer paper versions may exist; a record pins the version supporting its result rather than silently changing its evidence.

本次首批资料核验于 **2026-09-13**，窗口为 **2025-09-13–2026-09-13**。检索覆盖公司研究页面、第一方仓库及论文发布记录，再打开相关原始材料核对。它面向工程实践，是精选集合，不是系统综述或机构排名；部分论文已有新版，条目固定引用提供该结果的版本，不悄悄替换证据。

## Included institutional coverage / 已收录机构

The university and collaborator relationships appear in each record. A company name below means a verified research or report connection, not sole ownership or proof of RSI. / 每条记录保留高校及合作方关系；下列公司名称表示已核验的研究或报告关联，不代表独占成果或已证明 RSI。

| Organization / 机构 | Representative entry / 代表条目 |
| --- | --- |
| OpenAI | [GPT-Red](parameter-learning.zh-CN.md#gpt-red), [Codex development assistance](research-workflows.zh-CN.md#codex-builds-codex) |
| Google DeepMind | [SIMA 2](parameter-learning.zh-CN.md#google-sima2-2025), [DiscoRL](parameter-learning.zh-CN.md#google-discorl-2025), [AlphaEvolve MARL](research-workflows.zh-CN.md#google-alphaevolve-marl-2026) |
| Anthropic / Fellows Program | [A3](parameter-learning.zh-CN.md#a3), [weak-to-strong researcher](research-workflows.zh-CN.md#automated-w2s), [alignment researchers](research-workflows.zh-CN.md#automated-alignment-researchers), [TASTE](research-workflows.zh-CN.md#taste) |
| Meta + universities | [Hyperagents](agent-code.zh-CN.md#meta-hyperagents-2026) |
| Microsoft + collaborators | [ACON](memory-context.zh-CN.md#microsoft-acon-2025), [LEGOMem](memory-context.zh-CN.md#microsoft-legomem-2025) |
| Sakana AI + collaborators | [ShinkaEvolve](agent-code.zh-CN.md#sakana-shinkaevolve), [TRINITY](parameter-learning.zh-CN.md#sakana-trinity), [Doc-to-LoRA](parameter-learning.zh-CN.md#sakana-doc-to-lora) |
| SambaNova + Stanford / Berkeley | [ACE](memory-context.zh-CN.md#sambanova-stanford-ace) |
| Salesforce Research + UNC / Stanford | [Agent0](parameter-learning.zh-CN.md#salesforce-unc-agent0) |
| Prime Intellect + collaborators | [Prime Agent](memory-context.zh-CN.md#prime-agent), [autonomous research evaluation](research-workflows.zh-CN.md#prime-measuring-autonomous-ai-research) |
| Cognition | [Devin builds Devin](research-workflows.zh-CN.md#cognition-devin-builds-devin) |
| Alibaba / Tongyi Lab | [AgentEvolver](parameter-learning.zh-CN.md#alibaba-agentevolver) |
| ByteDance Seed + collaborators | [HarnessDev](agent-code.zh-CN.md#bytedance-harnessdev), [S3Gym](memory-context.zh-CN.md#bytedance-s3gym), [Aspire](parameter-learning.zh-CN.md#bytedance-aspire) |
| Tencent AI Lab + BUPT | [MoE-CL](parameter-learning.zh-CN.md#tencent-moe-cl), classified as enabling / 持续学习支撑技术 |
| DeepSeek | [DeepSeekMath-V2](parameter-learning.zh-CN.md#deepseek-math-v2) |
| MiniMax | [M2.7 self-evolution report](agent-code.zh-CN.md#minimax-m27-self-evolution) |
| Frontis.AI / Horizon Research + Tsinghua | [Frontis-MA1 / OpenRSI](research-workflows.zh-CN.md#frontis-ma1-openmle) |

## Checked but not promoted to a dated main entry / 已检索但未强行收录

These are gaps in this audit, not evidence that an institution has no relevant work. / 以下是本轮核验缺口，不是“这些机构没有相关成果”的结论。

| Institution / lead | Decision and primary source / 决定与一手来源 |
| --- | --- |
| Nous Research / Hermes | [Hermes Agent](https://github.com/NousResearch/hermes-agent) documents persistent skills and memory. The [self-evolution repository](https://github.com/NousResearch/hermes-agent-self-evolution) marks skill evolution implemented, with code/system-prompt/continuous evolution still planned. A dated primary first-public announcement was not established; commit timestamps do not establish when a repository became public. / 已见持久技能和记忆；独立进化仓库仅确认技能进化，其他目标仍在计划中。尚未核实第一方公开首发日，不能用提交时间代替。 |
| Moonshot AI | [Kimi K2.5](https://www.kimi.com/en/blog/kimi-k2-5) describes PARL orchestrator training with frozen subagents. No separate persistent self-modification or successor-training demonstration was verified in this pass. / PARL 编排器训练与并行任务执行不自动等于持久自修改或后继模型训练，本轮未核实独立直接闭环成果。 |
| Zhipu / Z.AI | [GLM-5 documentation](https://docs.z.ai/guides/llm/glm-5) describes planning, tools and self-checks; retained improvement was not established from this source. / 规划、工具和自检本身不足以证明持续保留的自改进。早期 WebRL 另列下表。 |
| Mistral | [Remote agents / Medium 3.5](https://mistral.ai/news/vibe-remote-agents-mistral-medium-3-5/) describes agent execution and model capabilities; an autonomous persistent improvement mechanism was not verified. / 已检索产品能力，未核实自主持久改进机制。 |
| Reflection | [Company news](https://reflection.ai/news) provides organizational and infrastructure updates; no sufficiently specified mutation/feedback/reuse result was verified. / 已检索公司及基础设施动态，未核实足够明确的修改、反馈与复用实验。 |
| Alibaba CuES | [Paper](https://arxiv.org/abs/2512.01311) is a relevant follow-up lead; the full affiliation, mechanism and release audit is pending. / 是相关后续线索，完整机构、机制和资产核验待完成。 |

## Earlier foundations / 窗口之前的基础工作

These remain useful reading, but are excluded from the current new-work count. A later revision, conference appearance or announcement does not reset the original contribution's date. / 这些仍值得阅读，但不计入本窗口新工作数量；修订、参会或再次宣传不改变原始贡献的日期。

| Work | Original date | Why retain it / 保留原因 |
| --- | --- | --- |
| [AlphaEvolve introduction](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/) | 2025-05-14 | Program evolution foundation; the 2026 MARL paper is a separate application / 程序进化基础，2026 MARL 论文为不同成果 |
| [Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) | 2025-05-29 | Agent-code archive and stepping stones / Agent 代码档案及中间候选复用 |
| [Text-to-LoRA](https://arxiv.org/abs/2506.06105) | 2025-06-06 | Generated adapters; distinguish from 2026 Doc-to-LoRA / 生成适配器，区别于 2026 年 Doc-to-LoRA |
| [Agent Lightning](https://arxiv.org/abs/2508.03680) | 2025-08-05 | Agent-training infrastructure; later publicity does not redate it / Agent 训练基础设施，后续宣传不重置日期 |
| [WebEvolver](https://arxiv.org/abs/2504.21024) | 2025-04-23 | Earlier self-evolving web-agent work / 早期 Web Agent 自进化工作 |
| [WebRL](https://arxiv.org/abs/2411.02337) | 2024-11-04 | Earlier Tsinghua/Zhipu web-agent curriculum RL; [paper affiliations](https://openreview.net/pdf?id=oVKEAFjEqv) / 早期清华、智谱课程强化学习，机构关系见论文 |

## How to read the evidence / 如何理解证据

Publication access, implementation access and successful reproduction are separate. The catalogue contains no newly reproduced upstream result. Noncommercial code such as Hyperagents and OpenRSI must not be treated as an unrestricted dependency of nanoRSI; a paper license does not determine its code, model or dataset license.

论文可读、实现可下载和复现成功是三件不同的事。本资料库没有新增上游复现实验。Hyperagents、OpenRSI 等非商业许可代码不能当作 nanoRSI 可不受限引入的依赖；论文许可也不决定代码、模型或数据许可。

Further contributions should add a dated primary source, explain the persistent change and feedback, and retain failed attempts or missing controls. Unknown availability is a reason to investigate, not to invent a release or silently discard a useful result.

后续贡献应提供带日期的一手来源，说明持久改变和反馈，并保留失败尝试或缺失对照。未确认资产可用性意味着需要继续核查，不应据此虚构发布或直接忽略有价值的成果。
