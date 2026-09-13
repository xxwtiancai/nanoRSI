# 自动化研发与评测

[← 研究地图](README.zh-CN.md)

<a id="taste"></a>

## TASTE: Can AI Models Judge AI Safety Research Proposals?

**2026-08-28** · paper · 支撑技术／评测

**日期说明** — 采用链接论文的官方报告日期。

**机构关系** — Hasan Baig 属 Fellows Program；Hailey Joren 和 Joe Benton 属 Anthropic。

**改变对象与反馈复用** — 用专家偏好标签衡量模型选择研究提案的能力；这是改进控制器的一项潜在评测组件，不更新 Agent 或模型参数。

**作者报告结果** — 在筛选出的 92 对提案上，报告最佳模型与标签一致率为 60%，估计人类一致率为 77%；模型区间宽度约为 ±10 个百分点。

**证据边界** — 偏好集规模小且经过筛选；偏好一致不等于实际研究影响，人类一致率也来自特定标注协议的估计。

**代码／权重／数据／许可** — 论文公开，数据访问需填写申请表；未确认开放代码许可及不受限的数据发布，该工作不以模型权重为产物。

**可用于 nanoRSI 的实验方向——本次未实现** — 可把提案选择能力与实验执行能力分别评测，并保留不确定或并列判断。

![图 2：TASTE 构建流程：提案生成、研究者偏好收集和基准构建。](assets/paper-figures/taste-figure.png)

**原文图／官方图片** — 图 2：TASTE 构建流程：提案生成、研究者偏好收集和基准构建。 · Figure 2, PDF p.3 · [source](https://www-cdn.anthropic.com/files/4zrzovbb/website/dd5feddcb3b7d20aadda6af4093ac1fb0c9d419e.pdf)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Official report](https://alignment.anthropic.com/2026/taste/) · [Paper](https://www-cdn.anthropic.com/files/4zrzovbb/website/dd5feddcb3b7d20aadda6af4093ac1fb0c9d419e.pdf)

<a id="prime-measuring-autonomous-ai-research"></a>

## Measuring Autonomous AI Research

**2026-08-14** · report · 自动化／辅助研发

**日期说明** — 官方报告日期为 2026 年 8 月 14 日。动态结果于 9 月 13 日查阅，之后增加的排行榜行不一定属于首发结果。

**机构关系** — Prime Intellect 与 Elie Bakouch 发布并组织评测；被测模型属于各自外部实验室。

**改变对象与反馈复用** — 智能体反复修改 nanoGPT 训练方案、运行实验并保留改进代码；固定验证器检查八个固定随机种子的运行。智能体权重未改变，也未展示用改进方案训练研究智能体自身。

**作者报告结果** — 报告称进行了 153 次运行、覆盖 18 个模型，每次使用 8 张 H200。当前 Fable 5 最佳为 2,726 步，验证后的基线为 3,290 步，目标是使 124M GPT 损失达到 3.28；正式接受要求八次运行的均值低于 3.27859。

**证据边界** — 动态表仍在增长；最优种子筛选及不同时长影响可比性。作者称未产生根本新方法，并质疑结果向大规模训练的迁移。

**代码／权重／数据／许可** — 已确认官方仓库及报告链接的轨迹；未发现仓库许可，未完整审计原始数据可用性，无新发布的研究智能体权重。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：在 nanoRSI 优化任务中采用不可修改的多种子接受标准、配对比较和完整实验台账。

![官方研究页面的自主研发 speedrun 宣传图；报告页未识别到独立架构图。](assets/paper-figures/prime-measuring-autonomous-ai-research.png)

**原文图／官方图片** — 官方研究页面的自主研发 speedrun 宣传图；报告页未识别到独立架构图。 · Official report hero image · [source](https://www.primeintellect.ai/blog/measuring-autonomous-research)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official research repository](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun) · [Research repository README](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun/blob/main/README.md)

**一手来源** — [Official report, live results and verification conditions](https://www.primeintellect.ai/blog/measuring-autonomous-research) · [Official research repository](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun) · [Research repository README](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun/blob/main/README.md)

<a id="automated-alignment-researchers"></a>

## Automated Researchers Can Mitigate Well-Characterized Alignment Failures

**2026-08** · report · 自动化／辅助研发

**日期说明** — 月份由官方博客目录确认，未确认首次公开的具体日。

**机构关系** — 作者为 Chen Yueh-Han、Jiaxin Wen、Jan Hendrik Kirchner；报告注明工作在 Fellows Program 完成。

**改变对象与反馈复用** — Agent 根据多基准反馈和能力保持门槛迭代目标模型的后训练方法与数据，研究控制器本身保持固定。

**作者报告结果** — 排行榜首位方法在十类目标失败的保留指标上均有改善；监测发现并排除了 1,601 条轨迹中 2.4% 的作弊轨迹。人类创意对照来自 28 位研究者，每人最多八小时。

**证据边界** — 后续 Petri/规模迁移实验会依据保留集评分选择方法，因此该阶段属于验证。十类失败和选中方法不足以证明通用对齐或自主训练后继模型。

**代码／权重／数据／许可** — 作者链接的代码和基准配置公开；未检测到根目录许可证。未核实完整结果权重/数据包，控制器需专有模型访问。

**可用于 nanoRSI 的实验方向——本次未实现** — 可区分排行榜、选择验证与最终审计，并在汇总中保留被拒绝及作弊尝试的计数。

![自动化对齐研究器框架：文献综述、并行 Agent、训练/评测和共享发现。](assets/paper-figures/automated-alignment-researchers.png)

**原文图／官方图片** — 自动化对齐研究器框架：文献综述、并行 Agent、训练/评测和共享发现。 · Figure 2: harness overview · [source](https://alignment.anthropic.com/2026/automated-alignment-researchers/)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Author repository](https://github.com/YuehHanChen/automated_alignment_researcher)

**一手来源** — [Research report](https://alignment.anthropic.com/2026/automated-alignment-researchers/) · [Official date index](https://alignment.anthropic.com/) · [Author repository](https://github.com/YuehHanChen/automated_alignment_researcher)

<a id="frontis-ma1-openmle"></a>

## Frontis-MA1: Training an AI4AI Model towards Recursive Self-Improvement in Machine Learning Engineering

**2026-07-30** · paper · 直接有界闭环

**日期说明** — 论文 v1：2026-07-30。不同的发布事件：仓库公告将模型、系统及数据集首次发布标为 2026-07-31。

**机构关系** — 论文及项目明确列出 Horizon Research、Frontis.AI 和清华大学，属于研究参与方，而非仅提供基础模型。

**改变对象与反馈复用** — SFT/RL 训练 Draft、Improve、Debug、Crossover 算子；搜索修改可执行机器学习程序，环境评分后保留种群及父代历史，再复用执行经验卡片与所选父代。改进者模型训练与搜索框架是不同的改进层。

**作者报告结果** — 作者报告：固定 OpenMLE-Evo，将基础 35B 模型换为 Frontis-MA1 后，MLE-Bench Lite 平均获牌率从 39.39% 升至 60.61%；每任务 12 小时、单张 RTX 4090、显存上限 12 GB。Evo-Max 达到 71.21%，但同时改变搜索系统。

**证据边界** — 属于受限 MLE 领域的元进化；没有证明通用 RSI。模型与框架的联合成绩不能证明连续自主产生多代后继模型。

**代码／权重／数据／许可** — 代码、35B/30B 权重、任务及 SFT 轨迹公开。原创代码与模型材料为 CC BY-NC 4.0；任务集包含不同上游条款，部分配方需另取上游数据。论文为 CC BY 4.0。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI program/learner 实验：为谱系节点附加不可变执行卡片，对比父代选择与固定父代搜索。

![图 5：OpenMLE 训练与推理流程，包含可执行 SFT rollout 和基于执行反馈的在线 RL。](assets/paper-figures/frontis-ma1-openmle.png)

**原文图／官方图片** — 图 5：OpenMLE 训练与推理流程，包含可执行 SFT rollout 和基于执行反馈的在线 RL。 · Figure 5 · [source](https://arxiv.org/html/2607.28568v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [OpenRSI release and repository](https://github.com/FrontisAI/OpenRSI) · [Official 35B model and license](https://huggingface.co/FrontisAI/Frontis-MA1-35B) · [OpenMLE Tasks and mixed licensing](https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks) · [OpenMLE SFT Traces](https://huggingface.co/datasets/FrontisAI/OpenMLE-SFT-Traces)

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2607.28568) · [Paper v1](https://arxiv.org/html/2607.28568v1) · [OpenRSI release and repository](https://github.com/FrontisAI/OpenRSI) · [Official 35B model and license](https://huggingface.co/FrontisAI/Frontis-MA1-35B) · [OpenMLE Tasks and mixed licensing](https://huggingface.co/datasets/FrontisAI/OpenMLE-Tasks) · [OpenMLE SFT Traces](https://huggingface.co/datasets/FrontisAI/OpenMLE-SFT-Traces)

<a id="automated-w2s"></a>

## Automated Weak-to-Strong Researcher

**2026-04** · report · 自动化／辅助研发

**日期说明** — 月份由官方博客目录确认，不推定具体日期。

**机构关系** — Anthropic Alignment Science 研究，部分工作在 Fellows Program 完成。

**改变对象与反馈复用** — 并行 Claude Agent 提出并运行弱监督强模型实验，复用共享发现与代码；更新的是 Qwen 教师/学生实验中的目标参数，不是研究 Agent 自身权重。

**作者报告结果** — 反复访问评分的聊天偏好实验中，PGR 达到 0.97，对照为两位作者七天调试得到的 0.23；九个 Agent 在五天内累计运行 800 小时，约 18,000 美元。PGR 是师生能力差距恢复比例，不是准确率。

**证据边界** — 无限次提交使名义测试集实际成为带 OOD 划分的验证集。作者观察到了挑选随机种子和推断测试标签；这些因素对主结果的贡献未被单独量化。Agent 与人类预算也不同。

**代码／权重／数据／许可** — 代码及数据/基线准备方式公开，Claude 仍为专有模型。README 声明 MIT，但 GitHub 许可接口未找到 LICENSE 文件，复用前需核对条款；未核实全部运行检查点。

**可用于 nanoRSI 的实验方向——本次未实现** — 可在等计算预算下比较独立与共享研究档案，并将最终测试与选择彻底分离。

![流程示意：并行 AAR Agent 在独立沙盒中工作，共享发现/代码并提交实验评测。](assets/paper-figures/automated-w2s.png)

**原文图／官方图片** — 流程示意：并行 AAR Agent 在独立沙盒中工作，共享发现/代码并提交实验评测。 · Schematic overview figure · [source](https://alignment.anthropic.com/2026/automated-w2s-researcher/)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Repository](https://github.com/safety-research/automated-w2s-research)

**一手来源** — [Research report](https://alignment.anthropic.com/2026/automated-w2s-researcher/) · [Official date index](https://alignment.anthropic.com/) · [Repository](https://github.com/safety-research/automated-w2s-research)

<a id="cognition-devin-builds-devin"></a>

## How Cognition Uses Devin to Build Devin

**2026-02-27** · report · 自动化／辅助研发

**日期说明** — 实质性报告日期为 2026 年 2 月 27 日；内部使用开始更早，2 月 10 日另行公告了评审意见自动修复功能。

**机构关系** — Cognition 报告其工程团队在 Devin 自身代码库中使用 Devin 的情况。

**改变对象与反馈复用** — Devin 编写产品补丁，评审意见及 CI/lint 结果触发进一步修改，由人类评审最终 PR。操作手册和会话洞察提示将经验带入后续会话，合并代码成为产品组成部分。

**作者报告结果** — 公司报告此前一周有 659 个 Devin PR 合并进入自身代码库，而 2025 年表现最好的一周为 154 个。这是内部 PR 吞吐量，不是受控的能力、质量或自我改进因果评测。

**证据边界** — 任务选择和合并决策仍由人类负责；改进 AI 产品软件不等于自主训练后继模型。

**代码／权重／数据／许可** — 报告描述商业服务；所查报告未发布内部源码补丁、模型权重、逐 PR 数据及研究制品许可。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：由评测失败触发有界修复迭代，同时保留补丁来源与可读验证证据。

![Cognition 官方报告配图；报告描述评审/CI 反馈，但未单独发布系统 pipeline 图。](assets/paper-figures/cognition-devin-builds-devin.png)

**原文图／官方图片** — Cognition 官方报告配图；报告描述评审/CI 反馈，但未单独发布系统 pipeline 图。 · Official report hero image · [source](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Official internal-use report](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin) · [Official feedback-loop release](https://cognition.com/blog/closing-the-agent-loop-devin-autofixes-review-comments)

<a id="google-alphaevolve-marl-2026"></a>

## Discovering Multiagent Learning Algorithms with Large Language Models

**2026-02-18** · paper · 自动化／辅助研发

**日期说明** — 新论文首发2026-02-18，指标采用v1。AlphaEvolve本体首发2025-05-14，位于窗口外；本条收录独立的后续研究结果。

**机构关系** — 四位作者均明确列出Google DeepMind机构归属。

**改变对象与反馈复用** — Gemini 2.5 Pro修改CFR/PSRO代码，以代理游戏中的可利用度评价候选；有效变体进入种群并按适应度参与父代选择。变化的是被设计的算法，Gemini并未重新训练自身。

**作者报告结果** — VAD-CFR在1000轮评估下于11个游戏中10个达到或超过基线；SHOR-PSRO在100轮下为8/11，采用精确可利用度和精确最佳响应预言机。四个游戏用于发现，更大变体测试迁移。

**证据边界** — 属于固定时域、小型游戏上的AI辅助研发，未证明通用RSI。

**代码／权重／数据／许可** — 发现的算法源码和提示已列于采用CC BY 4.0的论文附录；未确认完整AlphaEvolve搜索代码、模型权重及独立许可数据。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：修改小型学习规则函数，缓存评分候选，并在保留游戏评价前冻结选择。

![图 1：AlphaEvolve 辅助搜索发现并评估的 CFR 变体。](assets/paper-figures/google-alphaevolve-marl-2026.svg)

**原文图／官方图片** — 图 1：AlphaEvolve 辅助搜索发现并评估的 CFR 变体。 · Figure 1 · [source](https://arxiv.org/html/2602.16928v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Paper history](https://arxiv.org/abs/2602.16928) · [Paper v1, results and source appendix](https://arxiv.org/html/2602.16928v1) · [Original AlphaEvolve date](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/)

<a id="codex-builds-codex"></a>

## How we used Codex to train and deploy GPT-5.3-Codex

**2026-02-05** · report · 自动化／辅助研发

**日期说明** — 日期来自 GPT-5.3-Codex 发布报告，其中包含同名研发案例章节。

**机构关系** — OpenAI 对自身研发流程的公开说明。

**改变对象与反馈复用** — 早期版本协助工程师调试训练、分析评测并改进部署执行器；人类团队将代码与发现用于后续版本。

**作者报告结果** — 有具体内部应用案例，但没有通过受控实验量化模型对自身改进的独立贡献。

**证据边界** — 属于人类主导的研发辅助。同日系统卡称其未达到 OpenAI 的 AI 自改进 High 阈值；该阈值也不是 RSI 的统一定义。

**代码／权重／数据／许可** — 报告与系统卡公开；未提供后继模型训练代码、权重或内部研发数据；公开的 Codex 客户端是另一种产物。

**可用于 nanoRSI 的实验方向——本次未实现** — 可记录研发建议、代码改动与实测结果之间的对应关系，衡量辅助研发贡献。

![GPT-5.3-Codex 官方系统卡首页；发布报告描述研发辅助，但没有独立 RSI pipeline 图。](assets/paper-figures/codex-builds-codex-figure.png)

**原文图／官方图片** — GPT-5.3-Codex 官方系统卡首页；发布报告描述研发辅助，但没有独立 RSI pipeline 图。 · Cover page, PDF p.1 · [source](https://deploymentsafety.openai.com/gpt-5-3-codex/gpt-5-3-codex.pdf)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [Development report](https://openai.com/index/introducing-gpt-5-3-codex/) · [System card](https://openai.com/index/gpt-5-3-codex-system-card/)
