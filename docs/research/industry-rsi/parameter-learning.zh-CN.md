# 参数与训练数据

[← 研究地图](README.zh-CN.md)

<a id="bytedance-aspire"></a>

## Aspire: Can Models Self-Evolve from Vague Goals?

**2026-08-31** · paper · 直接有界闭环

**日期说明** — arXiv v1：2026-08-31；共用项目公告：2026-09-01。

**机构关系** — 论文明列包括 ByteDance Seed 在内的四个研究机构。

**改变对象与反馈复用** — 智能体根据模糊目标选择数据、训练方法及父检查点，或修改框架。控制器核验谱系并冻结候选。在评分门控的权重流程中，仅保留实测正收益且合格的检查点，否则恢复输入状态；框架在冻结后评测，不代表递归交接。

**作者报告结果** — 隐藏评测包含六个目标下的 520 道专家题。固定 Qwen3.5-4B 为执行模型，最佳后继框架任务宏平均为 27.22，低于原始 Qwen-Agent 的 28.64；三个有效后继版本均落后于参考框架。

**证据边界** — 保留收益非负可能来自回滚选择，不代表每次修改都有效；模糊目标与代理评测可能导致退化。

**代码／权重／数据／许可** — 论文及项目页公开；论文为 CC BY-NC-ND 4.0。未核验到完整基准代码、隐藏数据、训练检查点及资产许可可公开下载。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI learner 报告：分开记录候选原始变化与保留状态变化，导出失败尝试，并对比模糊目标与明确目标。

![图 1：从明确任务优化走向模糊目标驱动的自进化。](assets/paper-figures/aspire-figure.png)

**原文图／官方图片** — 图 1：从明确任务优化走向模糊目标驱动的自进化。 · Figure 1, PDF p.2 · [source](https://arxiv.org/html/2608.31111v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2608.31111) · [Paper v1 retention protocol and Table 1](https://arxiv.org/html/2608.31111v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="gpt-red"></a>

## GPT-Red: Automated Red Teaming via Self-Play at Scale

**2026-07-15** · paper · 直接有界闭环

**日期说明** — 官方论文发布日。

**机构关系** — OpenAI 论文及公司报告。

**改变对象与反馈复用** — 自博弈 RL 依据攻击成功与抵抗成功的奖励更新攻击者和防守模型群体；更强防守者提供更难训练信号，再用训练后的红队生成 GPT-5.6 的对抗训练数据。

**作者报告结果** — 报告中，GPT-5.6 Sol 面对 GPT-Red 直接注入的成功攻击率为 0.05%，按保留环境内的攻击尝试取平均；不能解释为任意攻击都只有这一成功概率。

**证据边界** — 属于有界对抗共同训练，未证明自主设计下一代模型；内部模型及训练规模限制本地复现。

**代码／权重／数据／许可** — 论文公开；GPT-Red 仅供内部使用。所引来源未发布完整训练代码、权重与数据，未确认可复用代码许可。

**可用于 nanoRSI 的实验方向——本次未实现** — 可探索无害对抗样例，并分别衡量样例有效性、任务完成率和误拒率。

![图 1：随着测试时计算量增加，GPT-Red 的红队攻击表现变化。](assets/paper-figures/gpt-red-figure.png)

**原文图／官方图片** — 图 1：随着测试时计算量增加，GPT-Red 的红队攻击表现变化。 · Figure 1, PDF p.1 · [source](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Paper](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf) · [Official report](https://openai.com/index/unlocking-self-improvement-gpt-red/)

<a id="a3"></a>

## A3: An Automated Alignment Agent for Safety Finetuning

**2026-03-11** · report · 直接有界闭环

**日期说明** — 采用研究报告标注日期，不把仓库创建时间当作公开发布日。

**机构关系** — Jifan Zhang 属 Fellows Program；Henry Sleight 属 Constellation；Joe Benton 属 Anthropic。

**改变对象与反馈复用** — Agent 生成失败假设、划分数据，再依据实验日志与评测反馈调整 LoRA 超参数和数据权重；控制器改进的是目标模型，而非控制器自身权重。

**作者报告结果** — 在 Qwen-2.5-7B Instruct 上，外部迎合性评测从 68.0% 降至 42.0%，MMLU-Pro 从 52.9% 变为 52.4%（报告表 1）；迎合性越低越好。

**证据边界** — 仅覆盖三类目标失败；Llama 实验收益较弱并暴露遗忘问题。日志说明包含 OOD 反馈，不能把所有 OOD 划分都等同于完全未参与选择的最终测试。

**代码／权重／数据／许可** — Apache-2.0 代码、配置与数据目录公开；需模型/API 和 GPU 软件栈。未核实训练后检查点及完整数据是否齐备。

**可用于 nanoRSI 的实验方向——本次未实现** — 可为课程实验加入能力保持约束，并保留真正冻结的最终测试集。

![A3 流程：数据生成 Agent、微调 Agent 和实验日志围绕安全问题进行适应。](assets/paper-figures/a3.png)

**原文图／官方图片** — A3 流程：数据生成 Agent、微调 Agent 和实验日志围绕安全问题进行适应。 · A3 Pipeline figure · [source](https://alignment.anthropic.com/2026/automated-alignment-agent/)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Repository](https://github.com/safety-research/A3) · [Code license](https://github.com/safety-research/A3/blob/main/LICENSE)

**一手来源** — [Research report](https://alignment.anthropic.com/2026/automated-alignment-agent/) · [Repository](https://github.com/safety-research/A3) · [Code license](https://github.com/safety-research/A3/blob/main/LICENSE)

<a id="sakana-doc-to-lora"></a>

## Doc-to-LoRA: Learning to Instantly Internalize Contexts

**2026-02-13** · paper · 支撑技术／评测

**日期说明** — arXiv 首版为 2026 年 2 月 13 日。二月合并项目页也介绍 Text-to-LoRA，但后者 2025 年 6 月的原作仍在时间窗口之外。

**机构关系** — 官方项目页确认 Sakana 作者单位，Shinnosuke Uesaka 同时列出 Minerva University。

**改变对象与反馈复用** — 元训练后的超网络将文档激活映射为 LoRA 权重；师生蒸馏提供训练反馈，部署时复用适配器回答后续问题，无需重读文档或逐文档计算梯度。

**作者报告结果** — 在 2WikiMultihopQA 上，迭代式 D2L 报告归一化 ROUGE-L 为 0.844、额外更新显存 3.791 GB、延迟 0.551 秒；使用真实问题的理想上下文蒸馏分别为 0.901、7.820 GB、40.171 秒。归一化表现以携带上下文推理为参照。

**证据边界** — 这是摊销更新成本的适应机制，而非递归循环；部署不会改进超网络本身，准确率和适配器容量仍构成限制。

**代码／权重／数据／许可** — 官方代码为 MIT；已确认 Hugging Face 检查点文件，但模型卡缺少许可。存在数据生成及评测脚本，未完整审计数据集再分发。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：后续探索版本化文档适配器作为记忆后端，并与检索方案比较事实保留能力。

![Doc-to-LoRA 总览：超网络将文档激活映射到 LoRA 权重，实现快速内化。](assets/paper-figures/sakana-doc-to-lora.svg)

**原文图／官方图片** — Doc-to-LoRA 总览：超网络将文档激活映射到 LoRA 权重，实现快速内化。 · Overview figure · [source](https://arxiv.org/html/2602.15902v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official code](https://github.com/SakanaAI/doc-to-lora) · [Official checkpoint inventory](https://huggingface.co/SakanaAI/doc-to-lora/tree/main)

**一手来源** — [Original paper date](https://arxiv.org/abs/2602.15902) · [Paper Table 1](https://arxiv.org/html/2602.15902v1) · [Official project and affiliations](https://pub.sakana.ai/doc-to-lora/) · [Official code](https://github.com/SakanaAI/doc-to-lora) · [Official checkpoint inventory](https://huggingface.co/SakanaAI/doc-to-lora/tree/main)

<a id="sakana-trinity"></a>

## TRINITY: An Evolved LLM Coordinator

**2025-12-04** · paper · 支撑技术／评测

**日期说明** — arXiv 首版为 2025 年 12 月 4 日；Sakana 在 2026 年 4 月 26 日的公告属于后续传播。

**机构关系** — 多数作者单位为 Sakana；Qi Sun 同时列出东京科学大学。Peter Schwendeman 为密歇根大学，注明工作在 Sakana 实习期间完成。

**改变对象与反馈复用** — Sep-CMA-ES 扰动小型协调器头，以任务终局结果评分并重组候选参数；保留的协调器反复选择模型及思考者、执行者或验证者角色，底层基础模型权重保持固定。

**作者报告结果** — LiveCodeBench v6 上，取消输出长度限制且不重新训练协调器时，pass@1 为 86.2%，GPT-5 为 83.8%。另一个每次 4,096 token、最多五轮的对照设置下得分为 61%，不可混用两种条件。

**证据边界** — 这是在人类选择的基准上离线优化协调策略，未展示部署后的智能体修改自身学习算法。

**代码／权重／数据／许可** — 论文公开；未确认官方实现、协调器权重、再分发数据及其许可。第三方实现不能视为官方发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：在相同 token 预算下比较小型可进化角色/模型路由器与静态路由。

![图 1：循环协调架构，每轮由紧凑协调器选择模型和角色。](assets/paper-figures/sakana-trinity.svg)

**原文图／官方图片** — 图 1：循环协调架构，每轮由紧凑协调器选择模型和角色。 · Figure 1 · [source](https://arxiv.org/html/2512.04695v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Original paper date](https://arxiv.org/abs/2512.04695) · [Original paper methods and experimental conditions](https://arxiv.org/html/2512.04695v1) · [Official Sakana announcement](https://sakana.ai/trinity/)

<a id="deepseek-math-v2"></a>

## DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning

**2025-11-27** · paper · 直接有界闭环

**日期说明** — arXiv v1 与论文日期均为 2025-11-27。

**机构关系** — 论文明列 DeepSeek-AI，并注明实习期间完成的工作；发布由 DeepSeek 官方仓库承载。

**改变对象与反馈复用** — 验证器为生成器训练提供奖励；提高验证计算量，自动标注新生成的难验证证明，再训练验证器。专家标注启动的元验证器检查批评是否可信。推理时保留高分证明并据批评继续修改；这一层改变解答而非权重。

**作者报告结果** — 作者报告经专家评估后 Putnam 2024 得分 118/120。高计算量搜索从 64 份证明及每份 64 次分析开始，选取前 64 份证明，每份抽取 8 次分析，最多迭代 16 轮；并非单次生成成绩。

**证据边界** — 自然语言验证仍可能出错，并依赖专家初始监督；证明搜索成功本身不等于模型递归改进。

**代码／权重／数据／许可** — 推理代码、提示词/预测及 685B 权重公开；仓库与权重为 Apache-2.0。未核验到完整训练代码、人工标注或完整训练数据的发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI learner 适配器：分别版本化生成器、验证器、标签及专家审计，对比共同训练与冻结验证器。

![图 2：随着连续自验证改进次数上限增加，证明质量的变化。](assets/paper-figures/deepseek-math-v2.svg)

**原文图／官方图片** — 图 2：随着连续自验证改进次数上限增加，证明质量的变化。 · Figure 2 · [source](https://arxiv.org/html/2511.22570v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official DeepSeek-Math-V2 repository](https://github.com/deepseek-ai/DeepSeek-Math-V2) · [Official weights and Apache-2.0 statement](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2)

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2511.22570) · [Paper v1 methods and high-compute evaluation](https://arxiv.org/html/2511.22570v1) · [Official DeepSeek-Math-V2 repository](https://github.com/deepseek-ai/DeepSeek-Math-V2) · [Official weights and Apache-2.0 statement](https://huggingface.co/deepseek-ai/DeepSeek-Math-V2)

<a id="salesforce-unc-agent0"></a>

## Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning

**2025-11-20** · paper · 直接有界闭环

**日期说明** — arXiv 首版为 2025 年 11 月 20 日，官方代码发布于 11 月 29 日；与 2025 年 7 月同名推荐系统论文不同。

**机构关系** — 作者名单由 UNC 团队主导；Can Qin、Caiming Xiong 单位为 Salesforce Research，Fang Wu 为斯坦福。

**改变对象与反馈复用** — 课程策略面向使用工具的执行器生成任务；十次执行器回答估计不确定性并产生伪标签，筛选任务用于训练执行器，新能力再改变下一轮课程，两种策略迭代更新。

**作者报告结果** — Qwen3-8B 数学平均分从 49.2 升至 58.2（增加 9.0 个百分点，约相对提高 18%），仅加工具为 53.2。七个数学基准除 AMC/AIME 使用 mean@32 外均为贪心 pass@1；表 1 报告训练过程峰值。

**证据边界** — 零数据指不使用人工整理的训练集，并不代表没有预训练知识；自一致性可能强化错误，结果不证明无界改进。

**代码／权重／数据／许可** — 已确认官方课程及执行器训练代码，Apache-2.0 许可；未确认训练后权重及完整生成数据集的发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：先用不可修改的答案验证器检验难度自适应任务生成，再考虑昂贵的策略训练。

![图 2：Agent0 在课程生成与执行器训练之间的共同进化闭环。](assets/paper-figures/salesforce-unc-agent0.png)

**原文图／官方图片** — 图 2：Agent0 在课程生成与执行器训练之间的共同进化闭环。 · Figure 2 · [source](https://arxiv.org/html/2511.16043v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official series repository and release date](https://github.com/aiming-lab/Agent0) · [Agent0 training implementation](https://github.com/aiming-lab/Agent0/blob/main/Agent0/README.md)

**一手来源** — [Paper dates](https://arxiv.org/abs/2511.16043) · [Original paper and numerical tables](https://arxiv.org/html/2511.16043v1) · [Official series repository and release date](https://github.com/aiming-lab/Agent0) · [Agent0 training implementation](https://github.com/aiming-lab/Agent0/blob/main/Agent0/README.md)

<a id="google-sima2-2025"></a>

## SIMA 2: A Generalist Embodied Agent for Virtual Worlds

**2025-11-13** · report · 直接有界闭环

**日期说明** — 官方研究发布于2025-11-13；论文首发于2025-12-04。结果采用论文v1。

**机构关系** — Google DeepMind的SIMA团队官方发布确认机构归属。

**改变对象与反馈复用** — Gemini生成任务并评价轨迹；积累的经验用于训练后续SIMA世代，新策略继续采集经验。初始智能体由人类示范启动。

**作者报告结果** — 在固定ASKA任务中，初始不足四分之一的任务超过Gemini奖励阈值（>50），后续世代全部超过阈值。这是模型评分下的任务覆盖率，不能当作独立验证的回合成功率；该组固定任务来自人类。

**证据边界** — 证据限于游戏实验、模型评价器和较短记忆；未展示Gemini或学习算法本身的改进。

**代码／权重／数据／许可** — 已确认公开论文和演示；已打开的官方来源未发现训练代码、权重、经验数据及其许可；仍依赖专有Gemini。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：分别记录学习器世代和评分轨迹，并用独立保留任务集验证迁移。

![图 16：自进化设置包含任务设置器、奖励模型、经验数据集和重新训练的 SIMA 2 Agent。](assets/paper-figures/google-sima2-2025.png)

**原文图／官方图片** — 图 16：自进化设置包含任务设置器、奖励模型、经验数据集和重新训练的 SIMA 2 Agent。 · Figure 16 · [source](https://arxiv.org/html/2512.04797v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Google DeepMind announcement](https://deepmind.google/blog/sima-2-an-agent-that-plays-reasons-and-learns-with-you-in-virtual-3d-worlds/) · [Paper version history](https://arxiv.org/abs/2512.04797) · [Paper v1, section 4.5](https://arxiv.org/html/2512.04797v1)

<a id="alibaba-agentevolver"></a>

## AgentEvolver: Towards Efficient Self-Evolving Agent System

**2025-11-13** · paper · 直接有界闭环

**日期说明** — arXiv v1 首次提交于 2025-11-13；采用论文首发事件，不使用仓库后续更新日期。

**机构关系** — 论文明确署名阿里巴巴集团通义实验室。

**改变对象与反馈复用** — 通过自主生成的环境任务更新智能体策略参数：自我提问生成并筛选任务，自我导航检索历史经验指导轨迹，自我归因结合结果奖励分配细粒度信用。强化学习后的策略和经验池用于后续探索。

**作者报告结果** — 作者表 1：Qwen2.5-7B 在 AppWorld 与 BFCL-v3 上的平均 avg@8 从 15.8% 升至 45.2%，差值为 29.4 个百分点。这是基础模型与完整训练系统的比较，并非单独归因机制的效果。

**证据边界** — 闭环受任务生成、裁判质量及环境覆盖范围约束；证据针对智能体训练，不证明无限自主重构或通用 RSI。

**代码／权重／数据／许可** — 代码：ModelScope 公开仓库，Apache-2.0。权重：未核验到论文独立检查点。数据：可见生成及集成代码，完整训练集及其许可未核验。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI learner 实验：为每个策略检查点记录生成任务清单版本，并以固定数据对照组评估经验复用。

![图 2：AgentEvolver 结合自我提问、自我导航和自我归因机制。](assets/paper-figures/alibaba-agentevolver.png)

**原文图／官方图片** — 图 2：AgentEvolver 结合自我提问、自我导航和自我归因机制。 · Figure 2 · [source](https://arxiv.org/html/2511.10395v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official AgentEvolver repository](https://github.com/modelscope/AgentEvolver)

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2511.10395) · [Paper v1: affiliation, methods, Table 1](https://arxiv.org/html/2511.10395v1) · [Official AgentEvolver repository](https://github.com/modelscope/AgentEvolver)

<a id="google-discorl-2025"></a>

## Discovering state-of-the-art reinforcement learning algorithms

**2025-10-22** · paper · 支撑技术／评测

**日期说明** — 线上首发为2025-10-22，12月为后续卷期日期。2024年12月收稿不等于公开发表。

**机构关系** — 原始论文将全部作者机构列为Google DeepMind。

**改变对象与反馈复用** — 元网络提供策略和预测的更新目标；元梯度优化智能体总体回报，更新后的规则用于后续智能体；发现的规则冻结后迁移到新环境。

**作者报告结果** — 扩展数据图4报告：在57个Atari游戏、2亿环境步的比较下，以约少40%的评价阶段TPU计算达到MuZero最终表现；该数字不包含额外的算法发现成本。

**证据边界** — 人类设计的元目标和框架固定，证据限于学习规则发现，不能证明通用智能递归修改自身。

**代码／权重／数据／许可** — 已确认官方元训练、评价代码及Disco103元参数。软件采用Apache-2.0，仓库其他材料采用CC BY 4.0；环境和数据另有条款。完整规模复现需要大量计算。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：区分学习器权重与更新规则参数，先在小型环境中验证外层目标，再扩大规模。

![DiscoRL 官方项目方法图：元网络从 Agent 群体经验中学习更新目标。](assets/paper-figures/google-discorl-2025.png)

**原文图／官方图片** — DiscoRL 官方项目方法图：元网络从 Agent 群体经验中学习更新目标。 · Official project method figure · [source](https://google-deepmind.github.io/disco_rl/)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official code and licence statements](https://github.com/google-deepmind/disco_rl)

**一手来源** — [Primary Nature article at PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12695655/) · [Publication metadata](https://pubmed.ncbi.nlm.nih.gov/41125136/) · [Author project and artifact availability](https://google-deepmind.github.io/disco_rl/) · [Official code and licence statements](https://github.com/google-deepmind/disco_rl)

<a id="tencent-moe-cl"></a>

## Self-Evolving LLMs via Continual Instruction Tuning

**2025-09-14** · paper · 支撑技术／评测

**日期说明** — arXiv v1：2025-09-14；记录的最新修订为 2025-10-15（v4）。按首发日期纳入。

**机构关系** — 论文 v1 明确注明作者分属北邮与腾讯 AI Lab；腾讯既是合作研究机构，也是应用场景。

**改变对象与反馈复用** — 连续指令微调更新任务专属与共享 LoRA 专家，任务感知对抗判别器帮助区分可迁移知识及任务特有信息；保留的专家将旧知识带入后续任务。未建立自主任务生成、评测及改进者再训练闭环，因此归为持续学习支撑技术。

**作者报告结果** — 论文评估连续学习及腾讯内容审核应用。此处不保留数值结论：摘要将指标表述为审核成本下降，实验部分则描述离线免审率提升；引用业务效果前需统一口径。

**证据边界** — 在外部提供的任务流上保留知识，不证明自主递归改进；工业数据访问限制复现。

**代码／权重／数据／许可** — 已核验 BAI-LAB/MoE-CL 公开实现。权重及工业数据未核验为公开；打开的仓库页未找到代码许可，不应假定可自由复用。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI learner 对照：固定外部任务流，保留各任务退化分数，区分持续学习与直接自我改进。

![图 1：MoE-CL 结合任务专属 LoRA 专家、共享专家和任务感知判别器。](assets/paper-figures/tencent-moe-cl.png)

**原文图／官方图片** — 图 1：MoE-CL 结合任务专属 LoRA 专家、共享专家和任务感知判别器。 · Figure 1 · [source](https://arxiv.org/html/2509.18133v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Author implementation](https://github.com/BAI-LAB/MoE-CL)

**一手来源** — [arXiv submission and revision history](https://arxiv.org/abs/2509.18133) · [Paper v1 affiliations and experiments](https://arxiv.org/html/2509.18133v1) · [Author implementation](https://github.com/BAI-LAB/MoE-CL)
