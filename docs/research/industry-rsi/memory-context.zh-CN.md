# 记忆与上下文

[← 研究地图](README.zh-CN.md)

<a id="bytedance-s3gym"></a>

## S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?

**2026-08-31** · paper · 直接有界闭环

**日期说明** — arXiv v1 提交于 2026-08-31，项目公告为 2026-09-01；标题采用 arXiv 可检索的 S3Gym 拼写。

**机构关系** — 论文明列 ByteDance Seed、M-A-P 和 TokenWave.AI。

**改变对象与反馈复用** — 智能体探索游戏并自评决策，在后续回合复用原始历史、按分数整理的记忆摘要或经验训练后的参数。主要探索阶段的可执行验证器奖励留在基准侧，通过更严格且隔离的评测检查继承状态是否改善行为；没有通用的收益准入门。

**作者报告结果** — 七个游戏中，自评质量与下一次严格评测提升的分块相关系数接近零：事件一致性为 −0.010，负校准误差为 −0.018。这些是相关系数而非提升百分比。不同任务适合不同上下文路径，参数训练可能产生负迁移。

**证据边界** — 证据限于特定游戏；识别成功不保证形成有效记忆或可迁移策略。

**代码／权重／数据／许可** — 论文及项目页公开；论文为 CC BY 4.0。未核验到独立基准代码、数据、训练检查点及对应资产许可的发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI skills 消融：比较原始历史、摘要记忆与冻结状态，构建记忆时隐藏验证器分数。

![图 2：S3Gym 通过历史 ICL、摘要记忆和参数训练展示经验驱动的改进路径。](assets/paper-figures/s3gym-figure.png)

**原文图／官方图片** — 图 2：S3Gym 通过历史 ICL、摘要记忆和参数训练展示经验驱动的改进路径。 · Figure 2, PDF p.7 · [source](https://arxiv.org/html/2608.31100v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2608.31100) · [Paper v1 methods and Table 6](https://arxiv.org/html/2608.31100v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="bytedance-chain-of-experience"></a>

## Chain-of-Experience for Continual LLM Improvement

**2026-08-18** · paper · 直接有界闭环

**日期说明** — arXiv v1 为 2026 年 8 月 18 日；字节跳动 Seed 官方论文页以 2026.08.18 收录同一论文。

**机构关系** — 作者来自 UC Santa Cruz 与字节跳动 Seed（Haoqin Tu 与 Yunhao Fang 为同等贡献；资深作者 Cihang Xie、Shen Yan）。

**改变对象与反馈复用** — 测试时经验学习：模型不再单轮推理，而是在迭代解题中累积自身经验轨迹（提问、尝试、正确性或测试通过反馈），这些轨迹供后续尝试使用，形成经验链（CoE）。研究比较了反馈来源（自我反馈与环境反馈）、通道组合以及保留策略，包括刻意保留"混乱"的失败轨迹。

**作者报告结果** — 在八个 LLM（含 GPT-5、Gemini-2.5 Pro、Claude-4.5 Sonnet）的数学/代码/知识任务上，迭代经验相对无反馈基线整体提升 5.6%，同时 API 成本降低 19%；组合互补反馈通道带来额外收益，单位 token 准确率优于其他测试时方法，且对弱反馈或噪声反馈稳健。

**证据边界** — 收益属于固定模型上的有界测试时适应：无权重更新，且按字节官方页的定位是"超越零样本推理的持续改进"，而非可学习更新器的跨任务迁移。百分比为作者在自选基准集上的汇总。

**代码／权重／数据／许可** — arXiv（CC BY 4.0）；收录于字节 Seed 官方论文页。已核验来源中没有代码或数据发布链接；基准提示与轨迹未见公开。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：在 nanoRSI 的数字/编程任务上，在固定 token 预算下比较单通道执行反馈与自我+环境反馈组合，并检验保留失败轨迹（而非只留成功）是否改变隐藏集准确率。

![图 2：研究的问题设定演进——从依赖世界反馈的迭代改进，到迭代演化，再到以累积经验为核心的闭环（环境提供多样化反馈，模型从经验中学习）。](assets/paper-figures/bytedance-chain-of-experience.png)

**原文图／官方图片** — 图 2：研究的问题设定演进——从依赖世界反馈的迭代改进，到迭代演化，再到以累积经验为核心的闭环（环境提供多样化反馈，模型从经验中学习）。 · Figure 2 · [source](https://arxiv.org/html/2608.18027v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-14.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [arXiv abstract (v1 date, license)](https://arxiv.org/abs/2608.18027) · [Paper HTML (loop figures, results)](https://arxiv.org/html/2608.18027v1) · [ByteDance Seed official publications page (2026.08.18)](https://seed.bytedance.com/zh/public_papers)

<a id="prime-agent"></a>

## Prime Agent: A Self-Improving RLM Harness

**2026-08-05** · paper · 直接有界闭环

**日期说明** — 论文明确标注首次发布于 2026 年 8 月 5 日，arXiv 首版提交于 8 月 24 日；上线博客亦确认为 8 月 5 日。

**机构关系** — Prime Intellect 发布该框架；论文列出 Prime Intellect、普林斯顿及 MIT 作者单位。

**改变对象与反馈复用** — 轨迹触发的改进修改持久化补充提示、技能、记忆和子智能体配置。磁盘持久化与回滚历史支持跨轨迹复用，基础系统提示保持不可修改。

**作者报告结果** — Sonnet 5 的七天 Factorio 运行完成了 196 项技术中的 24 项，使用 2,340 万输出 token；该案例没有匹配的关闭改进机制对照。其他框架基准收益不能全部归因于自我改进。

**证据边界** — 另一条 Factorio 轨迹将直接生成资源的作弊方式保存为技能。持久化修改可能放大规则漏洞，两类案例均未证明学习算法自身改进。

**代码／权重／数据／许可** — 已确认官方代码，MIT 许可；不需要新的模型权重，未完整审计评测轨迹、数据及各自许可。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：将不可修改的评测器及基础策略，与版本化记忆更新分离，并记录来源及支持回滚。

![图 1：Prime Agent 将持久根会话、子智能体会话连接到守护进程和持续改进闭环。](assets/paper-figures/prime-agent-figure.png)

**原文图／官方图片** — 图 1：Prime Agent 将持久根会话、子智能体会话连接到守护进程和持续改进闭环。 · Figure 1, PDF p.3 · [source](https://arxiv.org/html/2608.23552v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official code and license](https://github.com/PrimeIntellect-ai/prime-agent)

**一手来源** — [arXiv record](https://arxiv.org/abs/2608.23552) · [Paper first-publication statement and Factorio evidence](https://arxiv.org/html/2608.23552v1) · [Official launch and update mechanism](https://www.primeintellect.ai/blog/prime-agent) · [Official code and license](https://github.com/PrimeIntellect-ai/prime-agent)

<a id="tencent-training-free-grpo"></a>

## Training-Free Group Relative Policy Optimization

**2025-10-09** · paper · 直接有界闭环

**日期说明** — arXiv v1 首次提交于 2025-10-09。对应 Youtu-Agent 分支于 2025 年 10 月公布，之后合入主仓库；按论文日期纳入。

**机构关系** — 论文列出腾讯 Youtu Lab、复旦大学和厦门大学；官方实现发布在 TencentCloudADP/youtu-agent。

**改变对象与反馈复用** — 冻结的基础模型生成分组 rollout，将语义优势蒸馏到会演化的经验库和 token 先验中，再通过上下文回馈而非梯度更新。多个 epoch 共享累积经验，参数保持不变但后续输出分布发生变化。

**作者报告结果** — 在 DeepSeek-V3.1-Terminus 上，直接提示的 AIME24 从 68.6 提升到 72.6（+4.0），AIME25 从 52.9 到 54.0（+1.1）；ReAct+CI 的 AIME24 为 80.0→82.7（+2.7），AIME25 为 67.9→73.3（+5.4），论文报告成本为 18 美元。论文设置下 WebWalkerQA 为 63.2→67.8（+4.6）。

**证据边界** — 这是上下文空间的经验进化，不是参数训练：基础模型冻结，变化的是经验库。结果依赖有界分组、重试和任务特定提示；论文未展示改进器自主重设计自身算法。

**代码／权重／数据／许可** — TencentCloudADP/youtu-agent 发布 training_free_GRPO 分支和示例；LICENSE 声明 MIT，但 GitHub API 元数据为 NOASSERTION。论文使用的基础模型和基准数据仍受各自条款约束；不能因发布代码推断发生了参数更新。

**可用于 nanoRSI 的实验方向——本次未实现** — 为 nanoRSI 记忆实验增加冻结模型对照：在相同分组数量下比较无经验库、固定经验库和递归刷新经验，并记录 token 成本、过时建议和隐藏集迁移。

![图 2：Training-Free GRPO 在冻结基础模型的同时，用分组 rollout 更新经验库。](assets/paper-figures/tencent-training-free-grpo.png)

**原文图／官方图片** — 图 2：Training-Free GRPO 在冻结基础模型的同时，用分组 rollout 更新经验库。 · Figure 2, training-free_GRPO.png · [source](https://ar5iv.labs.arxiv.org/html/2510.08191/assets/figures/training-free_GRPO.png)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official Youtu-Agent implementation](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · [Youtu-Agent MIT license](https://github.com/TencentCloudADP/youtu-agent/blob/main/LICENSE)

**一手来源** — [arXiv first submission and history](https://arxiv.org/abs/2510.08191) · [Paper v1 and Training-Free GRPO figure](https://arxiv.org/html/2510.08191v1) · [Official Youtu-Agent implementation](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · [Youtu-Agent MIT license](https://github.com/TencentCloudADP/youtu-agent/blob/main/LICENSE)

<a id="sambanova-stanford-ace"></a>

## Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models

**2025-10-06** · paper · 直接有界闭环

**日期说明** — arXiv 首版为 2025 年 10 月 6 日；仓库公告标记为 2025 年 11 月，论文修订延续至 2026 年 3 月。

**机构关系** — 论文明确列出斯坦福、SambaNova 和伯克利作者单位，属于联合研究，不能全部归功于 SambaNova。

**改变对象与反馈复用** — 生成器轨迹与执行反馈交给反思器，整理器产出局部策略手册增量；通过有益/有害计数及去重，跨任务保留可复用策略，无需更新权重。

**作者报告结果** — 所有角色均使用非思考模式 DeepSeek-V3.1 时，无标准答案的在线 ACE 在 AppWorld 四项 TGC/SGC 指标上平均为 59.5，ReAct 为 42.4，Dynamic Cheatsheet 为 51.9；差值应表述为百分点，而非相对百分比。

**证据边界** — 在线评测按顺序先预测、再用该测试任务更新。证据支持有界适应，不涉及权重学习，也不证明更新器自身改进。

**代码／权重／数据／许可** — 已确认官方实现及评测代码，Apache-2.0 许可；无新模型权重，第三方数据集仍适用各自条款，未完整审计数据再分发。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：在固定任务流上比较版本化增量记忆与整文件重写。

![图 4：ACE 由 Generator、Reflector 和 Curator 组成，用于演化上下文 playbook。](assets/paper-figures/sambanova-stanford-ace.png)

**原文图／官方图片** — 图 4：ACE 由 Generator、Reflector 和 Curator 组成，用于演化上下文 playbook。 · Figure 4 · [source](https://arxiv.org/html/2510.04618v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official implementation](https://github.com/ace-agent/ace)

**一手来源** — [arXiv dates](https://arxiv.org/abs/2510.04618) · [Original paper affiliations, protocol and Table 1](https://arxiv.org/html/2510.04618v1) · [Official implementation](https://github.com/ace-agent/ace)

<a id="microsoft-legomem-2025"></a>

## LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation

**2025-10-06** · paper · 支撑技术／评测

**日期说明** — arXiv论文首发为2025-10-06；Microsoft页面列出的AAMAS 2026/2026年1月晚于首发。

**机构关系** — Microsoft Research官方论文页面确认机构归属。

**改变对象与反馈复用** — 成功日志转为完整任务规划记忆和角色专用子任务记忆，后续任务检索复用。实验先离线建库再评价推理，并未测试持续在线记忆演化。

**作者报告结果** — OfficeBench采用148个训练任务、152个测试任务和三个随机种子：GPT-4o成功率58.44%，无记忆为45.83%；GPT-4o-mini为38.16%，无记忆为24.78%。Synapse配GPT-4o达58.11%，因此该设置中相对强基线的优势很小。

**证据边界** — 支持程序性记忆复用，未展示多轮递归自我改进；记忆筛选和外部模型依赖会影响结论。

**代码／权重／数据／许可** — 已确认公开论文；已打开来源及定向搜索未发现专用官方代码、权重、记忆库数据及其许可，相关可用性仍未核实。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：比较经成功筛选的程序记忆与无记忆基线，区分规划和子任务检索，并冻结测试记忆库。

![图 1：LEGOMem 的协调器、任务 Agent 和模块化程序记忆。](assets/paper-figures/microsoft-legomem-2025.png)

**原文图／官方图片** — 图 1：LEGOMem 的协调器、任务 Agent 和模块化程序记忆。 · Figure 1 · [source](https://arxiv.org/html/2510.04851v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Paper history](https://arxiv.org/abs/2510.04851) · [Paper v1, method and Table 1](https://arxiv.org/html/2510.04851v1) · [Microsoft Research publication](https://www.microsoft.com/en-us/research/publication/legomem-modular-procedural-memory-for-multi-agent-llm-systems-for-workflow-automation/)

<a id="microsoft-acon-2025"></a>

## ACON: Optimizing Context Compression for Long-horizon LLM Agents

**2025-10-01** · paper · 直接有界闭环

**日期说明** — 论文首发2025-10-01，后于2025-10-17和2026-06-01修订；指标采用v1。

**机构关系** — 论文明确标注第一作者在Microsoft实习完成工作，以及Microsoft、KAIST和剑桥机构归属。

**改变对象与反馈复用** — LLM比较完整上下文成功、压缩上下文失败的配对轨迹，修改压缩指南并评价候选指南；选择结果用于后续优化轮次，基础智能体权重保持固定。

**作者报告结果** — OfficeBench采用GPT-4.1作为智能体和压缩器：效用优化的历史压缩取得74.74%准确率和4.93k峰值令牌；无压缩为76.84%/7.27k，简单提示压缩为71.58%/4.40k（v1表2）。

**证据边界** — 属于有限的离线模块优化；准确率与令牌开销的取舍不等于普遍提高准确率，也不是优化器重写自身。

**代码／权重／数据／许可** — 已确认官方代码、MIT许可及蒸馏流程；未确认公开蒸馏权重、专用数据集及其许可；外部基准和模型适用各自条款。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：根据配对失败优化压缩提示，保留独立验证集，同时记录成功率和上下文峰值。

![图 3：压缩指导优化使用成功与失败轨迹的对比反馈。](assets/paper-figures/microsoft-acon-2025.png)

**原文图／官方图片** — 图 3：压缩指导优化使用成功与失败轨迹的对比反馈。 · Figure 3 · [source](https://arxiv.org/html/2510.00615v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official Microsoft code](https://github.com/microsoft/acon) · [MIT licence](https://github.com/microsoft/acon/blob/main/LICENSE)

**一手来源** — [Paper history](https://arxiv.org/abs/2510.00615) · [Paper v1](https://arxiv.org/html/2510.00615v1) · [Official Microsoft code](https://github.com/microsoft/acon) · [MIT licence](https://github.com/microsoft/acon/blob/main/LICENSE)
