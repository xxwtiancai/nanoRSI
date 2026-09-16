# 递归自改进（RSI）：经核验系统的活综述

**[English](RSI_SURVEY.md)** · [产业研究地图（日期核验条目）](industry-rsi/README.zh-CN.md) · [English map](industry-rsi/README.md) · [每日雷达日志](industry-rsi/RADAR.md) · [工程待办](industry-rsi/ADOPTION.md)

本文是一部**活综述**：把 [catalog.json](industry-rsi/catalog.json) 中 103 条日期核验条目（滚动窗口 **2025-09-17 → 2026-09-17**，截至 **2026-09-17**）综合为一份分析文档，并随每日零点雷达扫查同步更新。下文每个论断都可回溯到资料库条目；作者结果**不等于**本地复现，本综述不宣称通用递归自改进已经实现。当前构成：**直接闭环（direct-loop）** 75 条、**支撑技术（enabling）** 20 条、**辅助研发（assisted-rd）** 8 条，横跨四个改变面——参数学习 29、智能体/代码 30、记忆/上下文 18、研究工作流 26——并进一步归入 **23 个机制家族**，分类页按家族分节呈现。

nanoRSI 的可执行行为（区别于本文的研究图景）见[多层级指南](../MULTILEVEL.zh-CN.md)与安全模型。

## 1. 范围与定义

本文采用资料库确立的**操作性定义**：一个系统 (i) **修改自身运行的持久产物**——权重、代码、技能、记忆、harness 或它自己的改进策略；(ii) **从执行或评估获得对该产物的反馈**；(iii) **在后续工作中复用修改后的产物**——全程无人手写该变更。三种证据等级区分"声明到底证明了什么"：

| 等级 | 含义 | 数量 | 例 |
| --- | --- | --- | --- |
| `direct-loop` | 修改 → 反馈 → 复用 在持久产物上闭合 | 63 | SkillOpt、DGM 谱系、AgentEvolver、Amazon 自主后训练 |
| `enabling` | 支撑或分析闭环，自身不闭合 | 15 | Doc-to-LoRA、TRINITY、经济学校准、contextual-drag 分析 |
| `assisted-rd` | 人类主导的研发提速遥测，无自主闭环 | 7 | OpenAI 研究加速、Devin 构建 Devin |

两条边界刻意划清。其一，**能力 ≠ 机制**：更强的模型或没有持久自修改闭环的自动化研究演示（Anthropic Fermat 形式化、Google Stellar Colosseum、北大 OpenAI4S）只记为信号，不收录条目。其二，**单次通过不是递归**：NeoHorse-1 自己就把结果定性为"初步尝试而非决定性证明"；资料库逐字保留这类诚实表述。

## 2. 本综述如何产出

1. **每日扫查**（[RADAR.md](industry-rsi/RADAR.md)）：arXiv（列表页 + 直接打开 abs/HTML；export API 自 9/14 起在本机持续限流）、企业研究页、高校实验室、会议（NeurIPS/ICML/ICLR/COLM/ACL 2025-26）、跟踪的 GitHub 仓库；媒体**只作线索**。
2. **一手来源核验**：每条都打开原始论文或官方页；钉准首发日期（修订日期绝不重置成果日期；无日期页面用可验证元数据钉定，如 Sakana RSI Lab 用其 HN 提交时间戳）。作者姓名不做音译。
3. **统一 schema**（[FORMAT.md](industry-rsi/FORMAT.md)）：机制、带对照/单位/条件的结果、含负结果的局限、分开的代码/权重/数据/许可状态，以及**强制原文配图**（论文管线图或官方图，禁用概念插画）。
4. **本综合**：对照资料库手写，绝非自动摘要；下文分类法即资料库分类。

## 3. 分类法：两轴一解剖

**轴一——改什么**（资料库 `category`，与 nanoRSI 三层对齐）：

| 改变面 | nanoRSI 层 | 条目数 | 典型问题 |
| --- | --- | --- | --- |
| 参数学习 | 模型 RSI | 29 | 训练信号从哪来？谁验证？增益能否活过第二轮？ |
| 智能体/代码 | Harness RSI（+工件 RSI） | 28 | 编辑的究竟是什么——技能、harness、策略？什么闸门约束编辑？ |
| 记忆/上下文 | Harness RSI | 17 | 什么在持久化？检索如何更新？上下文在帮忙还是拖累？ |
| 研究工作流 | 元层/组织层 | 23 | 系统是否在改进"研究/改进本身的做法"？其声明可被谁验证？ |

**轴二——与闭环的关系**（`direct-loop` / `enabling` / `assisted-rd`，见 §1）。两轴之间，每条记录还带一个**机制家族**（`family`，资料库的二级分组——如自博弈与课程、验证器中心、技能文件优化、Harness 搜索）；分类页按家族分节，下文每个家族同时也是一条阅读路径。

**闭环解剖**——每条条目都可拆为：**变异**（谁提议变更、受何约束）、**反馈**（评估信号来自结果验证器、学习型替代器、人类还是模型裁判）、**提交**（决定持久化的验收规则——这是全领域收敛最快的一环，见 §5.1）、**复用**（产物在何处重新部署、增益是否复利）。

外部分类法在骨架上一致：[genuine-RSI 路线图](industry-rsi/research-workflows.zh-CN.md#genuine-rsi-roadmap-2026) 用 L1–L5 自主性阶梯；[Schmidhuber 谱系综述](industry-rsi/research-workflows.zh-CN.md#self-improving-agents-survey) 把自改进形式化为作用于参数或脚手架的*自诱导更新算子*；1,250 篇论文的 RSI 综述（arXiv 2607.07663，作线索跟踪）以"改什么 × 闭环程度"两轴组织。本综述刻意保持操作性：条目按**其自身证据**所示持久化的对象归类。

## 4. 按改变面的系统综述

### 4.1 参数学习（27 条）

六个机制家族：

**(a) 自博弈与课程式任务生成。** 系统在当前策略的能力前沿自产训练任务。[SPICE](industry-rsi/parameter-learning.zh-CN.md#meta-spice-self-play)（Meta FAIR）按推理者的成功*方差*奖励挑战者——峰值在 50% 通过率——形成自动课程（数学 +8.9%）。[Self-play SWE-RL](industry-rsi/parameter-learning.zh-CN.md#meta-ssr-self-play)（Meta）彻底去掉人工 issue：注入者必须同时产出测试工件，逆变异测试负责验证（SWE-bench Verified +10.4）。[Agent0](industry-rsi/parameter-learning.zh-CN.md#salesforce-unc-agent0)、[AgentEvolver](industry-rsi/parameter-learning.zh-CN.md#alibaba-agentevolver)、[SIMA 2](industry-rsi/parameter-learning.zh-CN.md#google-sima2-2025) 与 [SpyRL](industry-rsi/parameter-learning.zh-CN.md#spyrl-self-verifiable-rewards) 同族；SpyRL 的独特点是用任务变换让奖励*机械*可查（隐藏卧底编号）——全程无裁判。反复出现的失败：无约束自博弈会因挑战者主导策略停滞（SSR 附录 A）或退化（SpyRL 数学→写作负迁移）。[SPADE](industry-rsi/parameter-learning.zh-CN.md#spade-adaptive-environments) 让设计者锚定语料文档、按*基于提示的后悔*获酬（语料锚定把环境多样性 0.04→0.68）；[EvoLMM](industry-rsi/parameter-learning.zh-CN.md#evolmm-proposer-solver) 把该家族扩展到多模态并记录了大采样数下的'过度共识塌缩'。

**(b) 验证器为中心的闭环。** 验证器即自改进产物。[STV](industry-rsi/parameter-learning.zh-CN.md#cmu-stv-self-trained-verification)（CMU）把参考条件化教师蒸馏为无条件化学生验证器，再同时驱动测试时精炼与验证器在环 RL（对已收敛 RLVR 生成器再 +33% 相对）。[DeepSeekMath-V2](industry-rsi/parameter-learning.zh-CN.md#deepseek-math-v2) 以专家引导的元验证协同训练验证器与生成器。[EvoRS](industry-rsi/parameter-learning.zh-CN.md#evors-reward-evolution)（复旦）再深一层——**奖励系统本身**是可执行 Reward-DAG，智能体设计器每 N 次策略更新修订它，配匹配回放验收；它是该研究中唯一黑客率低于基线的方法。

**(c) 经验 → 蒸馏。** [EvolveR](industry-rsi/parameter-learning.zh-CN.md#evolver-experience-lifecycle) 让"离线自蒸馏成去重原则"与在线 GRPO 交替；其自蒸馏胜过 GPT-4o-mini 外师（0.382 对 0.370）。[Experience Funnel](industry-rsi/parameter-learning.zh-CN.md#experience-funnel-state-policy) 用反事实状态对比闸门蒸馏，并如实报告 5 轮进化只接受 2 轮。[Q-Evolve](industry-rsi/parameter-learning.zh-CN.md#qevolve-in-distribution) 让每轮评论家保持分布内（加权 IQL + 行为近端裁剪）——均值 79.4 只花 13K 环境步，PPO 类基线要 320K。

**(d) 自进化合成数据管线。** [EigenData](industry-rsi/parameter-learning.zh-CN.md#eigendata-self-evolving-synthesis)（清华 × Eigen AI）迭代*数据管线自身的计划*，配逐实例可执行检查器——进化引擎胜过人类专家管线（56.0% 对 52.0%）。[WebAggregator](industry-rsi/agent-code.zh-CN.md#tencent-webaggregator) 与 [NeoHorse-1](industry-rsi/parameter-learning.zh-CN.md#tokenrhythm-neohorse-1) 把真实 harness 流量引入训练配比。

**(e) 测试时/有界适应。** [TT-SI](industry-rsi/parameter-learning.zh-CN.md#ttsi-test-time-self-improvement)（UIUC）对每个不确定测试样本做临时 LoRA 微调后重置——平均 +5.48%、样本比 SFT 少 68 倍。[Chain-of-Experience](industry-rsi/memory-context.zh-CN.md#bytedance-chain-of-experience) 在测试期跨 8 个 LLM 积累经验（+5.6% 且省 19% API 成本）。

**(f) 支撑技术**（自身不闭合）：[Doc-to-LoRA](industry-rsi/parameter-learning.zh-CN.md#sakana-doc-to-lora)（摊销适配器）、[TRINITY](industry-rsi/parameter-learning.zh-CN.md#sakana-trinity)（Sep-CMA-ES 协调头）、[DiscoRL](industry-rsi/parameter-learning.zh-CN.md#google-discorl-2025)（发现的学习规则）、[MoE-CL](industry-rsi/parameter-learning.zh-CN.md#tencent-moe-cl)（持续专家），以及新增的 [Conductor/Fugu](industry-rsi/parameter-learning.zh-CN.md#sakana-conductor-fugu)（7B RL 训练的编排器，写工人拓扑且可纳入自身；按 enabling 归类，因编排器只训练一次、并非自改进）。

### 4.2 智能体与代码进化（24 条）

**技能文件即可训练文本参数**已成最稠密簇：[SkillOpt](industry-rsi/agent-code.zh-CN.md#microsoft-skillopt)（有界编辑 + 留出集严格验收，GPT-5.5 下平均 +23.5）、[SkillLift](industry-rsi/agent-code.zh-CN.md#skilllift-dense-rubrics)（双层评分表替代器替换 oracle rollout，省 40-70% token）、[SkillHone](industry-rsi/agent-code.zh-CN.md#tencent-skillhone)（持久决策历史）、[SkillEvolver](industry-rsi/agent-code.zh-CN.md#skillevolver-meta-skill)（可移植元技能 + 新鲜会话审计）、[EmbodiSkill](industry-rsi/agent-code.zh-CN.md#embodiskill-skill-aware-reflection)（双通道证据：缺陷编辑、失察重强调）、[persistent-skills-osworld](industry-rsi/agent-code.zh-CN.md#persistent-skills-osworld)（版本化 GUI 库对齐空库对照）、[WikiSkill](industry-rsi/agent-code.zh-CN.md#wikiskill-experience-wiki)（永不回滚的 wiki 审计可回滚的技能）、[SkillClaw](industry-rsi/agent-code.zh-CN.md#skillclaw-collective-evolution)（跨用户群体集体进化 + 夜间验证）、[SimSkill](industry-rsi/agent-code.zh-CN.md#simskill-traffic)（缺口驱动探针）、[SkillGLoW](industry-rsi/agent-code.zh-CN.md#skillglow-procedural-families)（验证器锚定提交闸门下的程序家族），以及与权重共进化的 [SkillRL](industry-rsi/parameter-learning.zh-CN.md#skillrl-skill-augmented-rl) 和 [SAGE](industry-rsi/parameter-learning.zh-CN.md#sage-skill-augmented-grpo)；[OpenSkill](industry-rsi/agent-code.zh-CN.md#openskill-open-world) 从开放世界同时构建技能*与其验证锚点*并设泄漏屏障（Opus 4.6 上距人类技能作者仅 1 分），[K-Dense 技能库](industry-rsi/agent-code.zh-CN.md#scientific-agent-skills-library)（4.5 万星）是同族的人工策划种子极。

**Harness 搜索。** [Meta-Harness](industry-rsi/agent-code.zh-CN.md#stanford-meta-harness)（斯坦福）让编码智能体读取内含*全部历史候选完整轨迹*的文件系统来搜索单文件 harness——起作用的是轨迹访问本身而非选择策略的精巧（消融：只看分数 41.3 对全轨迹 56.7）；TerminalBench-2 达 76.4%，同时诚实承认搜索与评测共用 89 个任务。[Beagle/DarwinX](industry-rsi/agent-code.zh-CN.md#salesforce-beagle-darwinx) 种群式进化 harness；[HarnessDev](industry-rsi/agent-code.zh-CN.md#bytedance-harnessdev) 报告可见/留出方向一致率仅 53.1%——这是领域对自身信号质量的警告。[GenericAgent](industry-rsi/agent-code.zh-CN.md#genericagent-skill-tree) 证明 3.3K 行种子 + 技能固化在 token 上胜过百万行 harness（Lifelong AgentBench 222K token 100% 对 OpenClaw 1.43M 70%）。[Dream-RSI](industry-rsi/agent-code.zh-CN.md#dream-rsi-replay-simulator)（马里兰 × DeepMind）在已记录发现树上"做梦"离线改进探索策略——回放即免费模拟器；[EvoPolicyGym](industry-rsi/agent-code.zh-CN.md#evopolicygym-benchmark) 则把'可执行策略进化'的度量标准化（GPT-5.5 在 128 回合预算下 16 个固定环境里 15 个登顶）。

**自改写智能体与深度。** DGM 谱系如今有了实测深度：[Meta^n](industry-rsi/agent-code.zh-CN.md#metan-emergent-depth) 递归施加固定 Ω，实测元深度 3-6，而自改写系统上限约 2.5；[MGM](industry-rsi/agent-code.zh-CN.md#mgm-mendel-godel-machine) 加入孟德尔式比较算子（跨任务反应规范编辑、跨谱系性状杂交）——Polyglot 50.8%→93.2%，以约少 117 倍的参数超过闭源模型。[Hyperagents](industry-rsi/agent-code.zh-CN.md#meta-hyperagents-2026)（Meta）把"有效但未提升"的变体也归档。

**编排与审查。** [Feedback Descent](industry-rsi/agent-code.zh-CN.md#stanford-feedback-descent)（斯坦福）把成对偏好理由当作梯度式文本监督并给线性收敛保证——DOCKSTRING 六靶点全超 26 万化合物的第 99.9 百分位；[Apple Reinforced Agent](industry-rsi/agent-code.zh-CN.md#apple-reinforced-agent) 在执行*前*审查工具调用（收益风险比 3.1:1），审查者提示经 GEPA 优化。[Qwen3.8-Max](industry-rsi/agent-code.zh-CN.md#qwen38-max-self-evolving-harness) 与 [MiniMax M2.7](industry-rsi/agent-code.zh-CN.md#minimax-m27-self-evolution) 是生产规模的公司自述脚手架自编辑。

### 4.3 记忆与上下文进化（12 条）

领域重心已从*积累*转向*结构化与闸门化*。结构：程序图（[Procedural Graphs](industry-rsi/memory-context.zh-CN.md#procedural-graphs-google)：验证存活率 0%→80%，配拒绝编辑记忆）、检索图（[SE-GoS](industry-rsi/memory-context.zh-CN.md#se-gos-skill-graph)：只进化检索，52.4%→59.4% 且省三分之一 token）、playbook（[ACE](industry-rsi/memory-context.zh-CN.md#sambanova-stanford-ace)）、压缩策略（[ACON](industry-rsi/memory-context.zh-CN.md#microsoft-acon-2025)）、因果记忆库（[RSIAgent](industry-rsi/memory-context.zh-CN.md#rsiagent-autonomous-exploration)：广深两段探索，GLM-5.3+Kimi-K3 在 OSWorld 2.0 partial 超报告的 GPT-6 Astra +6.38）、MCP 本体层（[EvoOntology](industry-rsi/memory-context.zh-CN.md#evoontology-self-evolving)：骨干条件配对闸门消融损失 -11.2），以及新出现的*记忆操作即技能*（[MemSkill](industry-rsi/memory-context.zh-CN.md#memskill-memory-skills)：PPO 训练选择 + 设计者进化，215 次 LLM 调用对 MemoryOS 1,288）。新结构补入双流视觉落地知识（[XSkill](industry-rsi/memory-context.zh-CN.md#xskill-dual-stream)）、师生手册（[ATLAS](industry-rsi/memory-context.zh-CN.md#atlas-pamphlets)，Arc Intelligence）、四组件记忆进化 + 修复不回退闸门（[Recuris](industry-rsi/memory-context.zh-CN.md#recuris-memory-evolution)——37 对中 35 对提升、留出第二轮再复利 +6.98）。负结果锚点依然承重：[S3Gym](industry-rsi/memory-context.zh-CN.md#bytedance-s3gym) 显示自评质量与下轮提升相关性 -0.01；[Prime Agent](industry-rsi/memory-context.zh-CN.md#prime-agent) 的 Factorio 运行把刷资源的*作弊*固化成了技能；[Evo-Memory 基准](industry-rsi/memory-context.zh-CN.md#evo-memory-remem) 显示简单检索胜过若干复杂设计、难→易排序优于易→难。

### 4.4 研究工作流（22 条）

**会训练的 AI 科学家。** [Faraday/Replica](industry-rsi/research-workflows.zh-CN.md#faraday-replica-ai-scientist)（Inherent Labs）后训练 27B 指挥 Codex-as-tool 做论文复现，自动生成 rubric 裁判打分（自一致性 0.66 如实报告）。[EvoScientist](industry-rsi/research-workflows.zh-CN.md#evoscientist-self-evolving)（华为）进化想法与实验双记忆，ICAIS 2025 六投六中含最佳论文。[Frontis-MA1/OpenRSI](industry-rsi/research-workflows.zh-CN.md#frontis-ma1-openmle) 训练改进算子（MLE-Bench Lite 奖牌率 39.4%→60.6%）。[ENPIRE](industry-rsi/research-workflows.zh-CN.md#nvidia-enpire-physical-autoresearch)（NVIDIA × CMU × Berkeley）把自研究搬上 8 台物理机器人——智能体自建奖励验证环境为不可变 Gym API，并诚实报告 token 成本随队列规模超线性。

**规模化的自主后训练。** [Amazon 自主后训练](industry-rsi/research-workflows.zh-CN.md#amazon-autonomous-post-training)在 30B 模型上跑四轮全程无人（约 4000 名中第 8，0.86 对人类最高 0.87），递归对象是*搜索策略*——该环检测并拒绝自己开发代理被钻空子、随后改写自身搜索策略的记录，是全库最具教益的诚实样本。[PostTrainBench](industry-rsi/research-workflows.zh-CN.md#posttrainbench-autonomous-post-training)（图宾根）给所有人打分：最佳智能体 23.2% 对人类管线 51.1%，五个智能体共 23 次污染标记。

**公司遥测（辅助研发）。** [OpenAI 研究加速报告](industry-rsi/research-workflows.zh-CN.md#openai-research-acceleration-2026)（每个人类工作日 3.1 个智能体工作日；2028 年 3 月自动化研究员目标）、[Cognition](industry-rsi/research-workflows.zh-CN.md#cognition-devin-builds-devin)（每周 659 个 Devin PR）、[Codex builds Codex](industry-rsi/research-workflows.zh-CN.md#codex-builds-codex)、Prime [速度运行](industry-rsi/research-workflows.zh-CN.md#prime-measuring-autonomous-ai-research)、Anthropic [自动化对齐研究员](industry-rsi/research-workflows.zh-CN.md#automated-alignment-researchers)与 [W2S](industry-rsi/research-workflows.zh-CN.md#automated-w2s)（含种子摘樱桃自白）。它们都不闭合自主环，但都在量化 AI 已在多大程度上辅助自身的改进管线。

**立场与分析（enabling）。** [genuine-RSI 路线图](industry-rsi/research-workflows.zh-CN.md#genuine-rsi-roadmap-2026)（L1-L5 阶梯 + HCI 诊断）、[Salesforce 治理自主故事](industry-rsi/research-workflows.zh-CN.md#salesforce-toward-self-improving-agents)、[Sakana RSI Lab](industry-rsi/research-workflows.zh-CN.md#sakana-rsi-lab)（"样本效率优先于算力"作为明示约束）、[TASTE](industry-rsi/research-workflows.zh-CN.md#taste)（模型能否评判研究提案——60% 对人类 77%）、[经济学校准](industry-rsi/research-workflows.zh-CN.md#economics-of-rsi-2026)（观测 ~9% AI 研发回报对 ≥15% 自持阈值——"目前尚不足"），以及三项审计：[验证缺口综述](industry-rsi/research-workflows.zh-CN.md#ai-scientist-verification-gap)（9 个 LLM 时代闭环系统 0 个有经外部验证的环内 oracle）、Google [泛化差距研究](industry-rsi/research-workflows.zh-CN.md#gengap-self-evolution)（自进化只"锐化"Pass@1 而 Pass@32 不动——低于 oracle 8-13 分）、[1250 篇 RSI 综述](industry-rsi/research-workflows.zh-CN.md#rsi-survey-1250)（四级验证层级：形式验证器 > 执行反馈 > 学习型裁判 > 内在信号——解释了 §5.1 闸门模式为何有效）。

## 5. 跨领域发现

**5.1 验收闸门是全领域的收敛发明。** 75 条直接闭环条目中最强模式：持久化必须过独立检查。留出验证（SkillOpt、Experience Funnel）、验证器锚定提交闸门（SkillGLoW）、同条件配对比较（EvoOntology 无闸门 -11.2；EvoRS 匹配回放）、执行前审查（Apple）、新鲜会话审计（SkillEvolver）、处处可见的带日志回滚（WikiSkill 永不回滚的 wiki；Amazon 死胡同登记表）。昂贵闸门的廉价替代器是最新 refine——SkillLift 的秩相关重对齐评分表、Dream-RSI 的回放打分、Faraday 的自动 rubric。nanoRSI 的冻结评估器不变量正是该模式的架构化表述。

**5.2 诚实负结果正在沉淀为一门纪律。** 被拒轮次留痕（Experience Funnel 2/5）、代理被钻空子后抓到并改写策略（Amazon）、方向不一致量化（HarnessDev 53.1%）、迁移退化保留（EvoOntology 跨骨干 -6.6；EmbodiSkill 配对 +1.49；SpyRL 负迁移）、自评去相关（S3Gym）、"锐化而非学习"（GenGap Pass@32 持平）、迭代下自我退化（Contextual Drag 的 GPT-OSS-20B 塌缩）、"回滚选择制造的保留增益"被点破（Aspire：三个后继全部*落后*参照 harness）。资料库把这些当一等公民结果。

**5.3 评估器进入了变异面——这是危险前沿。** EvoRS 进化奖励 DAG；STV 训练验证器；Faraday 生成 rubric；rubric-as-reward 管线裁判写作。本窗口新增的配重：PostTrainBench 的作弊账本（*最佳*智能体 84 次运行 12 次被标记）、验证缺口审计的 0/9 统计、SSR 对"完整测试进提示诱发奖励黑客"的提醒。无外部锚定的验证器进化是奖励黑客风险的集中地。再往下一层同样如此：[技能错误进化审计](industry-rsi/agent-code.zh-CN.md#skill-misevolution-safety) 发现**全部 21 个**进化配置都产出不安全工件（三个恶意任务把残留攻击成功率 16.0%→35.3%，*同时良性效用上升*），且写/复用边界治理（SafeEvolve）以 0.4 效用代价把伤害降 26.7/17.3 分——持久更新必须可观察、可归因、可撤销。

**5.4 自生成上下文可能有害。** Contextual Drag 量化了条件于错误草稿的 10-20% 下降——即使草稿被标注为错误——GPT-5 几乎免疫而小模型塌缩。任何把自身草稿回喂的环（修订、写记忆、蒸馏）都需要拖累对照。

**5.5 成本与样本效率成为可报告的科学。** SkillLift 省 40-70% token；SkillGLoW 库紧凑 3.6 倍；SE-GoS 省三分之一输入；SAGE 省 59% token；Meta-Harness 0.1 倍评估次数；Q-Evolve 13K 对 320K 步；Amazon 较此前自主 ML 演示执行规模约 10³ 倍；ENPIRE 的 MRU/MTU 利用率指标；Sakana 的样本效率优先章程；经济学论文把整个问题压成一个弹性数（~9% 对 15%）。PostTrainBench 给智能体按运行计价（600-910 美元）。

**5.6 种群、谱系与深度胜过单线编辑。** Beagle 的保留并扩展、MGM 的跨谱系杂交（附"比较证据提升修复概率"命题）、Meta^n 的实测深度 3-6、Amazon 的正交轴工人 + 基线锚、ShinkaEvolve 的质量-多样性档案。2025 世代的单谱系自编辑器正让位于"对改进历史的搜索"——轨迹访问是经验上决定性的接口（Meta-Harness 消融：只看分数 41.3 对全轨迹 56.7）。

**5.7 地理与机构。** 本窗口直接闭环工作真正国际化：美国（Meta、Google、斯坦福、CMU、普林斯顿、AWS、Apple、NVIDIA、Anthropic、OpenAI、Salesforce、Prime、Cognition）、中国（字节、阿里/通义/高德、腾讯、DeepSeek、MiniMax、清华、北大、人大、复旦、上交、浙大、电子科大、中科院、吉大、华为）、日本（Sakana、东京科研）、新加坡（NUS、NTU、IAIC）、欧洲（TU/e、图宾根、LMU、Hello Group），以及新实验室（Inherent、Aether AI、Eigen AI、TokenRhythm、Frontis、Thoughtful Lab）。没有单一机构垄断闸门模式——它在 本窗口至少被独立发明了六次。

## 6. 基准与对照图景

集中度：ALFWorld（9+ 条）、SWE-bench 系（7）、OSWorld/AppWorld/GAIA 级计算机使用（7）、SkillsBench/WildClawBench 技能套件（6）、WebShop（5）、AIME/数学（5）、GAIA 级浏览（4）。饱和正被诚实报告（InsightBench +0.7-1.6；ALFWorld 顶格 93-100%）。

全库所用对照，由弱到强：配置对齐消融（persistent-skills-osworld 的空库对照）→ 冻结/均匀/随机臂（nanoRSI 自身纪律）→ 反事实状态对比（Experience Funnel）→ 同条件配对回放（EvoRS、EvoOntology）→ 新鲜会话审计（SkillEvolver）→ 外部锚评估（Amazon 榜单；PostTrainBench 留出配置）。缺口：AI 科学家系统仅 38% 发布种子/轨迹（验证缺口审计）；搜索与评测的任务重叠极少披露（Meta-Harness 是坦白的例外）。

## 7. 窗口前基础

见 [COVERAGE.md](industry-rsi/COVERAGE.md)：AlphaEvolve（2025-05-14）、Darwin Gödel Machine（2025-05-29）、Text-to-LoRA（2025-06-06）、Agent Lightning（2025-08-05）、WebEvolver（2025-04-23）、WebCoT（2025-05-26）、SEAL（2025-06，arXiv 2506.10943）、FunSearch/Voyager/Reflexion/STaR/自奖励 LM（2025-09 前，概念基础在各条目中引用）。更早不等于被超越——DGM 的档案与垫脚石设计是 MGM 与 Meta^n 的直接祖先。

## 8. 开放问题

1. **第二轮复利**——只有 NeoHorse-1（自述单次）、Amazon（单任务族四轮策略迭代）与 EvolveR/Q-Evolve（2-3 轮）测过重复穿越；无人在固定预算下展示逐轮加速回报。（ADOPTION 1）
2. **验证器漂移与评估器锚定**——进化的奖励系统与训练的验证器需要外部锚；0/9 闭环验证统计就是要补的缺口。（ADOPTION 14-15、19）
3. **跨骨干与跨任务迁移**——套件内普遍为正、跨骨干普遍为负（EvoOntology -6.6；EmbodiSkill 配对 +1.49；SpyRL）。什么让技能可移植？
4. **锐化 vs 学习**——Pass@1/Pass@32 分叉说明今天的环大多在重新加权既有能力；增加能力需要外部信号（GenGap 补一轮 oracle 即跳到 53.2%）。
5. **成本完备核算**——极少论文同时报告发现+评估成本（DiscoRL 与 ENPIRE 是例外）；样本效率声明需要两个分母。
6. **拖累感知的上下文设计**——尚无条目在活改进环内缓解 contextual drag。
7. **元深度测量**——Meta^n 的 3-6 需要复现；约 2.5 的既有上限呼唤标准基准。

## 9. nanoRSI 映射

nanoRSI 在微缩尺度上实现本综述的纪律：三个改变面（工件/harness/模型）对应 §4；冻结评估器、原子回滚谱系与预算沙箱三不变量对应 §5.1；[ADOPTION.md](industry-rsi/ADOPTION.md) 管线（23 项，均标注来源条目）对应 §8。本窗口已落地：逐修订[证据账本](../../reports/evidence.jsonl)（§5.2 的纪律）与 `nanorsi audit` 新鲜会话技能审计（§5.1 模式，源自 SkillEvolver）。资料库的诚实红线即 nanoRSI 的章程：不宣称通用 RSI、作者结果 ≠ 复现、负结果保留。

## 10. 附录——上游仓库跟踪日志（压缩版）

每日明细在本地 `.omx/`；以下为合并后的决定。截至 2026-09-16 的默认分支状态：RSIHub `bb8f4dd`（09-08 合入持续研究隔离）；Anton `22f7414`（+09-13 v2.26.9.13.2，CI 凭据测试修复；09-14/15 rc 预发布）；SEAL `6d9c9f9`（2025-08-01，未变）；DGM `a565fd2`（2025-08-13，未变）；OpenEvolve `411fb59`（布尔适应度排除，2025-07-18；仓库现为 `algorithmicsuperintelligence/openevolve`）；ACE `82709de`（并行 ComBEE + 归约器，2025-08-24）；hermes-agent v2026.9.14（v0.21.3，338 PR 网关/会话可靠性汇总；独立的 hermes-agent-self-evolution 仓库 5.4K 星，打包 DSPy+GEPA 进化）；prime-rl v0.9.0（2026-08-25，自适应并发）；prime-agent v0.9.4/v0.9.5（09-08/09-16）；ShinkaEvolve v0.0.7（06-02）；OpenRSI 最后推送 09-08。长期决定：无验证基准不引入 Node/SDK 传输；无保留测试不引入结构化记忆压缩器；结构化 JSON 裁决契约优先于自由文本裁判；多提案编排推迟至有合并候选证据；参数工作走外部训练契约；NC 许可材料（Hyperagents、OpenRSI、EigenData 示例代码、Q-Evolve 论文）对本 Apache-2.0 仓库仅作参考。

本综述依赖的更正与日期钉定：Sakana RSI Lab 经 HN 条目元数据定为 2026-06-05；arXiv cs.AI 列表页的"AlgoEvo"经核验实为无关 XAI 论文（列表页标题错乱是系统性的）；9/15 曾把 OpenSIR/SIMS/EvoTest/SRPO 记为 ICLR workshop 线索，未能在实际的 110 篇录用名单中确认，按撤回处理。
