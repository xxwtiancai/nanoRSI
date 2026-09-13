# Agent 与代码

[← 研究地图](README.zh-CN.md)

<a id="bytedance-harnessdev"></a>

## HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?

**2026-09-01** · paper · 直接有界闭环

**日期说明** — arXiv v1：2026-09-01；共用的 Self-Developing Agents 项目页同样标为九月一日。

**机构关系** — 所列机构均由论文明列，字节跳动 Seed 为研究参与方。

**改变对象与反馈复用** — Creation 从弱种子构建可运行框架；Evolution 根据下游执行反馈反复修改持久框架。正式版本冻结后在隐藏任务上评测，衡量跨任务复用而非单份输出修补；固定运行模型的对照评估可迁移性。

**作者报告结果** — 九条单次进化轨迹中，可见分数与隐藏分数的变化方向仅在 34/64 次相邻版本切换中一致（53.1%）；仅 2/9 个声明最终版本在隐藏集上最优。Creation 覆盖六个创建模型、四个领域和 2,207 个下游实例。

**证据边界** — 这是受限直接闭环的基准研究，不证明稳定累积改进；最终选定产物可能退化，收益依赖执行模型。

**代码／权重／数据／许可** — 论文与项目页公开，论文为 CC BY-NC-ND 4.0；未核验到可下载的基准代码/数据仓库、衍生权重或对应许可，不应标为已开放代码。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI coding 实验：冻结每个候选版本，保留完整评分轨迹，在固定执行模型下衡量开发集与隐藏集提升方向的一致性。

![图 1：从弱种子创建可运行框架，再用执行反馈持续演化持久化框架。](assets/paper-figures/harnessdev-figure.png)

**原文图／官方图片** — 图 1：从弱种子创建可运行框架，再用执行反馈持续演化持久化框架。 · Figure 1, PDF p.2 · [source](https://arxiv.org/html/2609.01437v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — 核验来源中没有确认的公开代码／资产链接。

**一手来源** — [arXiv first submission](https://arxiv.org/abs/2609.01437) · [Paper v1](https://arxiv.org/html/2609.01437v1) · [Official Self-Developing Agents project](https://self-developing-agents.github.io/)

<a id="qwen38-max-self-evolving-harness"></a>

## Qwen3.8-Max: A New Bar for Coding and Cowork (self-evolving harness demonstrations)

**2026-08-03** · report · 直接有界闭环

**日期说明** — Qwen 团队官方博客，页面标注 2026/08/03，发布 Qwen3.8-Max（2.4T 参数、激活 95B）；页面承诺次周开放权重。

**机构关系** — 阿里 Qwen 团队对自家旗舰模型与演示过程的第一方报告；所有数字均为官方博客自报。

**改变对象与反馈复用** — 三个长程演示，模型通过反馈回路修改自身工作基础设施：(1) 从空文件夹起用 10+ 天自主运行构建 oh-my-cli 项目，配合 issue 状态机、调度器、监控与看门狗——"需求归一化为 issue，由 agent 自动认领执行，经代码、测试、预览与日志持续迭代"；(2) 从零复现论文《Unified Data Selection for LLM Reasoning》（约 125 小时、约 7,600 行代码、33 轮 GPU 训练），再以"假设→写码→上 GPU→分析"的自改进环在四轮中自提 18 个改进想法；(3) 竞赛榜单迭代。

**作者报告结果** — 自报结果：oh-my-cli 自主运行约 16 天累计 265 次提交、127 个 PR、151 个 issue（截至 2026 年 7 月 30 日）；研究复现环节先复现论文六项主要发现（其选择法在 AIME24 上超随机 +7.7%），再演化出在 AIME24 上超过原方法 +2.7 分的新方法。

**证据边界** — 属演示而非受控实验：harness 运行没有公开基线 harness、固定种子对照或成本控制；AIME24 +2.7 分为单模型自报结果，无方差与独立核验。审计时点的开放权重状态：页面承诺公开，但本次运行未核验到已发布。

**代码／权重／数据／许可** — 官方博客；演示仓库 github.com/qwen-code-dev-bot/oh-my-cli 公开（Apache-2.0，2026-07-13 创建）并保留完整轨迹；模型权重已宣布开放，但本次审计未核验到发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：搭建最小 issue 环路 harness，让 nanoRSI 的改进器认领、实现并验证自己仓库的 issue，在同一 issue 流上与固定计划对照比较有效 diff 产出率与回归率。

![博客中描述 10+ 天自主运行的章节："通过反馈回路自我演化"，含 oh-my-cli 的 issue 认领环路（状态机、调度器、监控、看门狗）与自测细节。](assets/paper-figures/qwen38-max-self-evolving-harness.png)

**原文图／官方图片** — 博客中描述 10+ 天自主运行的章节："通过反馈回路自我演化"，含 oh-my-cli 的 issue 认领环路（状态机、调度器、监控、看门狗）与自测细节。 · Section '10+ Days of Autonomous Coding: Building a Self-Evolving Harness' · [source](https://qwen.ai/blog?id=qwen3.8)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-14.

**开源代码／权重／数据链接** — [Demonstration repository with full trace (Apache-2.0)](https://github.com/qwen-code-dev-bot/oh-my-cli)

**一手来源** — [Official Qwen blog post (opened via browser)](https://qwen.ai/blog?id=qwen3.8) · [Demonstration repository with full trace (Apache-2.0)](https://github.com/qwen-code-dev-bot/oh-my-cli)

<a id="microsoft-skillopt"></a>

## SkillOpt: Executive Strategy for Self-Evolving Agent Skills

**2026-06-30** · report · 直接有界闭环

**日期说明** — 微软研究院官方博客，日期 2026 年 6 月 30 日；随附的论文页与开源仓库在同一季度公开（仓库创建于 2026-05-08）。

**机构关系** — 微软研究院（MSRA）作者团队（Yifan Yang、Xuemei Gao、Qi Dai、Bei Liu、Kai Qiu、Dongdong Chen、Chong Luo）报告自有方法；博客数字为作者自报，论文自同一页面链接。

**改变对象与反馈复用** — 把 agent 的技能文件当作文本空间中的可训练参数：优化器模型在前向–反向–更新循环中提出有界编辑，候选技能"只有在留出验证集上严格优于当前技能时才被采纳"；被拒编辑进入缓冲区作为负反馈，其上还有按 epoch 的慢速/元更新。

**作者报告结果** — 作者报告：在全部 52 个评测单元（6 基准 × 7 模型 × 3 执行模式）中相对人工技能、单次 LLM 技能、Trace2Skill、TextGrad、GEPA、EvoSkill 取得最优或并列最优；GPT-5.5 直聊下六基准平均从 58.8 升至 82.3（绝对 +23.5 分）；SpreadsheetBench 41.8→80.7；在 Codex 中训练的表格技能把 Claude Code 从 22.1 提到 81.8（+59.7）；最终技能中位约 920 token、仅 1–4 次被采纳编辑；去掉元技能/慢更新后 SpreadsheetBench 从 77.5 跌至 55.0。

**证据边界** — 技能优化由固定基准内的留出验证监督——闭环是在已知测试分布上优化，未证明分布外或套件外任务的收益；跨 harness 迁移只展示了一个技能族；执行模式依赖未固定版本的商业 harness。

**代码／权重／数据／许可** — 官方实现已核验：github.com/microsoft/SkillOpt（MIT 许可，2026-05-08 创建，约 1.7 万星）；论文页自博客链接；无新权重（冻结第三方模型）；基准数据适用各基准自身条款。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：在 nanoRSI 的技能面上增加"留出闸门"技能编辑器——只在严格验证提升时采纳有界 diff 提案——与无闸门自编辑及冻结技能在相同任务流上对比，记录编辑采纳率与回归。

![图 1：技能空间优化类比——带留出选择闸门的有界编辑沿验证误差面下降，而无约束的临时更新会跳变；右侧表格把经典训练超参数映射到文本空间对应物。](assets/paper-figures/microsoft-skillopt.png)

**原文图／官方图片** — 图 1：技能空间优化类比——带留出选择闸门的有界编辑沿验证误差面下降，而无约束的临时更新会跳变；右侧表格把经典训练超参数映射到文本空间对应物。 · Blog Figure 1 · [source](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-14.

**开源代码／权重／数据链接** — [Official implementation (MIT)](https://github.com/microsoft/SkillOpt)

**一手来源** — [Official MSR blog post (opened)](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/) · [Official implementation (MIT)](https://github.com/microsoft/SkillOpt) · [Publication page](https://www.microsoft.com/en-us/research/publication/skillopt-executive-strategy-for-self-evolving-agent-skills/)

<a id="tencent-skillhone"></a>

## SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History

**2026-06-07** · paper · 直接有界闭环

**日期说明** — arXiv v1 首次提交于 2026-06-07；后续修订不重置纳入日期。论文标注 WeChat、Tencent Inc. 机构，并将 SkillHone 描述为持续研究框架。

**机构关系** — 论文将腾讯作者标为 WeChat、Tencent Inc.，并说明一位作者曾在 Tencent Inc. 的 WeChat AI 实习。高校合作方不被写成腾讯独占成果。

**改变对象与反馈复用** — 持久决策历史保存诊断、候选技能修订、脱敏评测证据和结果。优化 Agent 与评测 Agent 分别操作技能仓库和评测仓库；被接受的修订进入后续会话，因此技能产物在迭代间被修改并复用。

**作者报告结果** — 在 Qwen3.6-35B-A3B 的开放网页设置中，SkillHone 报告 GAIA 平均 64.6，对比精心构建的深度研究 Agent 48.8（+15.8）；WebWalkerQA-EN 为 66.4，对比 63.2（+3.2）。内部工具场景报告平均提升 +18.8；这些是作者报告的、任务特定的结果。

**证据边界** — 论文主要评测英文基准，并一次隔离一个技能；尚未展示多技能联合进化。原始企业内部框架不等同于公开仓库，因此不应把开源包写成腾讯内部基础设施的完整发布。

**代码／权重／数据／许可** — 已核验 Tencent/SkillHone 公开仓库。README 与 LICENSE 声明 MIT，但 GitHub API 元数据为 NOASSERTION。论文中的内部框架、内部数据和模型权重未随该仓库发布。

**可用于 nanoRSI 的实验方向——本次未实现** — 为 nanoRSI 增加版本化技能目录：保存决策记录、候选 diff、评测证据和回滚决定，再在隐藏任务上比较固定技能与接受修订后的复用。

![图 2：SkillHone 将持久决策历史、技能优化和技能评测分开，使通过的修订可在后续迭代复用。](assets/paper-figures/tencent-skillhone.png)

**原文图／官方图片** — 图 2：SkillHone 将持久决策历史、技能优化和技能评测分开，使通过的修订可在后续迭代复用。 · Figure 2, framework.png · [source](https://ar5iv.labs.arxiv.org/html/2606.08671/assets/framework.png)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Tencent SkillHone repository](https://github.com/Tencent/SkillHone) · [SkillHone MIT license](https://github.com/Tencent/SkillHone/blob/main/LICENSE)

**一手来源** — [arXiv first submission and history](https://arxiv.org/abs/2606.08671) · [Paper v1 and framework figure](https://arxiv.org/html/2606.08671v1) · [Tencent SkillHone repository](https://github.com/Tencent/SkillHone) · [SkillHone MIT license](https://github.com/Tencent/SkillHone/blob/main/LICENSE)

<a id="meta-hyperagents-2026"></a>

## Hyperagents

**2026-03-19** · paper · 直接有界闭环

**日期说明** — arXiv v1发布于2026-03-19；Meta论文页面日期为2026-03-24。

**机构关系** — 论文列有FAIR at Meta、Meta Superintelligence Labs及学术合作机构。

**改变对象与反馈复用** — 可编辑的元智能体修改自身及任务智能体；经评价的有效变体进入档案，作为后续父代和反馈来源，入库不要求立即提高分数。

**作者报告结果** — 100轮后，论文评审保留集准确率为0.710（置信区间0.590–0.750），静态基线为0.630、定制DGM为0.590。与定制DGM的差异不显著；初始0.0源于输出格式失败。

**证据边界** — 基础模型和评价器固定，有限轮次实验不能证明无限自我加速。

**代码／权重／数据／许可** — 已确认官方代码及实验日志链接；未提供基础模型权重。代码采用CC BY-NC-SA 4.0，不能称为允许商业使用的宽松开源。未检查日志内容及独立数据许可。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议实验：分别管理任务代码和元代码版本，保留已评价的中间变体及不可变评价记录。

![图 1：DGM-Hyperagents 将可修改的任务 Agent 与元 Agent 结合，并用 stepping-stone 档案持续搜索。](assets/paper-figures/meta-hyperagents-2026.png)

**原文图／官方图片** — 图 1：DGM-Hyperagents 将可修改的任务 Agent 与元 Agent 结合，并用 stepping-stone 档案持续搜索。 · Figure 1 · [source](https://arxiv.org/html/2603.19461v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official code](https://github.com/facebookresearch/HyperAgents) · [Code licence](https://github.com/facebookresearch/HyperAgents/blob/main/LICENSE.md)

**一手来源** — [Paper history](https://arxiv.org/abs/2603.19461) · [Paper v1, authors and section 5.1](https://arxiv.org/html/2603.19461v1) · [Meta publication](https://ai.meta.com/research/publications/hyperagents/) · [Official code](https://github.com/facebookresearch/HyperAgents) · [Code licence](https://github.com/facebookresearch/HyperAgents/blob/main/LICENSE.md)

<a id="minimax-m27-self-evolution"></a>

## MiniMax M2.7: Early Echoes of Self-Evolution

**2026-03-18** · report · 直接有界闭环

**日期说明** — 官方报告日期为 2026-03-18。相关 M2 系列技术论文首发于 2026-05-26，不能以七月修订日期替代 M2.7 最早事件。

**机构关系** — MiniMax 第一方报告，并有 MiniMax-M2 系列技术论文作为后续材料。

**改变对象与反馈复用** — 内部 M2.7 智能体分析失败轨迹，修改 scaffold 代码及采样配置，评测后保留或回滚，并用于下一轮。另一个研发流程更新记忆/技能、辅助研究员开展 RL 实验，但仍由人提供方向并作关键决策。

**作者报告结果** — MiniMax 报告进行了超过 100 轮自主 scaffold 迭代，内部编程评测提升 30%；未披露绝对基线、评测集身份及不确定性，因此不能独立横向比较。

**证据边界** — 这是第一方内部实验，尚非复现结果；辅助模型研发与 scaffold 自改不证明完全自主的后继模型训练。

**代码／权重／数据／许可** — M2.7 权重公开。当前模型 LICENSE 为自定义非商业许可，商业使用需书面授权；未核验到内部自进化框架、评测数据及完整训练流程公开。

**可用于 nanoRSI 的实验方向——本次未实现** — 拟议 nanoRSI coding 实验：将修改限制在 scaffold 文件，冻结执行模型，在隐藏测试集上审计保留/回滚决策。

![图 8：M2.7 自进化使用的模型迭代系统与双循环流程。](assets/paper-figures/minimax-m27-self-evolution.svg)

**原文图／官方图片** — 图 8：M2.7 自进化使用的模型迭代系统与双循环流程。 · Figure 8 · [source](https://arxiv.org/html/2605.26494v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official M2.7 model](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) · [Current M2.7 non-commercial license](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)

**一手来源** — [Official M2.7 report](https://www.minimax.io/news/minimax-m27-en) · [Related M2-series technical paper dates](https://arxiv.org/abs/2605.26494) · [Related M2-series paper v1](https://arxiv.org/html/2605.26494v1) · [Official M2.7 model](https://huggingface.co/MiniMaxAI/MiniMax-M2.7) · [Current M2.7 non-commercial license](https://huggingface.co/MiniMaxAI/MiniMax-M2.7/blob/main/LICENSE)

<a id="tencent-webaggregator"></a>

## WebAggregator: Enhancing Compositional Reasoning Capabilities of Deep Research Agent Foundation Models

**2025-10-16** · paper · 直接有界闭环

**日期说明** — arXiv v1 于 2025-10-16 以 Explore-to-Evolve 工作标题提交；后续改名为 WebAggregator 不改变原始日期。

**机构关系** — 论文明确列出腾讯 AI Lab 与香港中文大学作者；代码及数据构建仓库由腾讯账号发布。

**改变对象与反馈复用** — 在线探索器访问网页，组合逻辑提案器选择、组合并细化高层聚合操作。质量控制将可执行聚合程序转成覆盖 5 万网站、11 个领域的 1 万条可验证 QA；轨迹与答案再用于 WebAggregator 模型的 SFT。

**作者报告结果** — 论文报告 WebAggregator-8B 达到 GPT-4.1 水平，32B 在 GAIA-text 上超过 GPT-4.1 十个百分点以上并接近 Claude-3.7。人工标注的 WebAggregatorQA 测试中，Claude-3.7 的 pass@1 为 28.0%，GPT-4.1 为 25.8%；模型比较使用固定裁判和有界重试。

**证据边界** — 被进化的对象是网页聚合程序及其生成训练数据；下游基础模型经过 SFT 后评测，并未递归部署来改进自身提案器。网站可用性、裁判质量和生成数据泄漏都会影响结果。

**代码／权重／数据／许可** — Tencent/WebAggregator 发布 QA 构建引擎、查询、轨迹、模型和运行脚本。LICENSE.txt 为 WebAggregator 自定义条款，并写明不适用于欧盟境内；GitHub API 元数据为 NOASSERTION。数据、模型和第三方条款仍需分别核验。

**可用于 nanoRSI 的实验方向——本次未实现** — 使用小型封闭网页任务集测试 nanoRSI 程序进化：保存每个提案程序、来源 URL、验证器输出和生成样本，再比较固定数据 SFT 与刷新数据的迭代。

![图 2：Explore-to-Evolve 将网页探索与可执行聚合逻辑转成可验证 QA 和模型训练数据。](assets/paper-figures/tencent-webaggregator.png)

**原文图／官方图片** — 图 2：Explore-to-Evolve 将网页探索与可执行聚合逻辑转成可验证 QA 和模型训练数据。 · Figure 2, illus.png · [source](https://ar5iv.labs.arxiv.org/html/2510.14438/assets/illus.png)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Tencent WebAggregator repository](https://github.com/Tencent/WebAggregator) · [WebAggregator custom license terms](https://github.com/Tencent/WebAggregator/blob/main/LICENSE.txt)

**一手来源** — [arXiv first submission and history](https://arxiv.org/abs/2510.14438) · [Paper v1 and Explore-to-Evolve figure](https://arxiv.org/html/2510.14438v1) · [Tencent WebAggregator repository](https://github.com/Tencent/WebAggregator) · [WebAggregator custom license terms](https://github.com/Tencent/WebAggregator/blob/main/LICENSE.txt)

<a id="sakana-shinkaevolve"></a>

## ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution

**2025-09-17** · paper · 直接有界闭环

**日期说明** — arXiv 首版为 2025 年 9 月 17 日，Sakana 公告为 9 月 25 日；不以之后的仓库更新重新确定首发日期。

**机构关系** — Sakana AI 开发并发布该框架，公司公告直接链接论文及官方仓库。

**改变对象与反馈复用** — LLM 修改档案中的程序，以验证器适应度选择下一轮可复用的父代；新颖性筛选与多臂赌博机模型选择提高搜索效率。目标包括 AIME 智能体框架和 MoE 负载均衡损失。

**作者报告结果** — 作者报告以 150 个样本找到优于 AlphaEvolve 的 26 圆装填解。MoE 损失搜索使用 30 代；公告称相对 Global LBL，无效路由减少 5.81%，七个基准的平均表现提高 1.73%。

**证据边界** — 目标由人类限定，并依赖外部 LLM；并未证明变异引擎自身持续改进或无界递归自我改进。

**代码／权重／数据／许可** — 已确认官方代码与示例，许可为 Apache-2.0；不要求发布新的基础模型权重。未完整审计实验数据开放情况。

**可用于 nanoRSI 的实验方向——本次未实现** — 建议：增加基于档案的智能体框架搜索示例，固定留出测试，并在父代选择中计入成本。

![图 1：ShinkaEvolve 的档案、拒绝采样、程序变异和适应度评估闭环。](assets/paper-figures/sakana-shinkaevolve.png)

**原文图／官方图片** — 图 1：ShinkaEvolve 的档案、拒绝采样、程序变异和适应度评估闭环。 · Figure 1 · [source](https://arxiv.org/html/2509.19349v1)

**nanoRSI 复现状态** — not-run. 来源最近核验：2026-09-13.

**开源代码／权重／数据链接** — [Official code and license](https://github.com/SakanaAI/ShinkaEvolve)

**一手来源** — [arXiv original date](https://arxiv.org/abs/2509.19349) · [Sakana announcement and results](https://sakana.ai/shinka-evolve/) · [Official code and license](https://github.com/SakanaAI/ShinkaEvolve)
