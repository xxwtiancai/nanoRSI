# RSI 研究笔记（活文档）

> 分类法来自 1250 篇 RSI 综述（arXiv 2607.07663）的两轴：**改进对象**（下面四个章节）×**闭环程度**（每条末尾标注：闭环 / 人在环上 / 支撑·无闭环，映射自旧三值证据类 direct-loop / assisted-rd / enabling）。标题与机构保留原文；正文中文。本文件由每日零点自动化更新；完整字段、事件史与逐条配图清单仍在已冻结的 [industry-rsi 归档](industry-rsi/README.md)（catalog.json，2026-10-24 起不再更新）。

## 最近更新

- 2026-10-31 · 本轮覆盖 OpenAI、Google DeepMind、Anthropic、Microsoft、Meta、Salesforce、Sakana AI、SambaNova、Nous Research、Prime Intellect、Cognition、阿里/通义、字节、腾讯、DeepSeek、月之暗面、智谱、MiniMax、Frontis 及 RSIHub、Anton、OpenEvolve、ShinkaEvolve、Hermes 等跟踪线。未发现新的、同时满足原始 pipeline/overview 图、可核验开放材料和许可边界的通用 RSI 条目；Anthropic 的公开页仍是受监督研发加速与趋势证据，OpenAI 公开表述仍把研究加速和完全自主 RSI 分开。OpenEvolve 的近期 Apache-2.0 变化是拒绝 `NaN`/`inf` 评测值并加回归测试，nanoRSI 已在 judge 边界实现同类计数范围校验，但没有复制上游代码或增加依赖。SenseNova-RoboRSI、The Trinity 和 Skill$^{\\infty}$ 继续保留为待核验线索，不声称本地复现或通用 RSI 已解决。
- 2026-10-30 · 继续核验 10 月 29–30 日的一手来源与跟踪仓库：OpenEvolve 合并了对 `NaN`/`inf` 评测值的拒绝及回归测试（Apache-2.0）；RSIHub、Hermes Agent、ShinkaEvolve 和 OpenSenseNova/SenseNova-RoboRSI 也有近期提交。前者与 nanoRSI 的“评测器不可信输入不能进入选择”边界一致，但当前仓库没有相同的自报告数值接口，故不复制代码；后者 RoboRSI 已公开 Apache-2.0 仓库，但技术报告、权重与数据的可复现包仍需逐项核验，暂不作本地复现或移植声明。The Trinity（官方仓库 2026-10-28 宣布代码将在一周内发布）目前只有项目说明/报告和“Code: Coming Soon”，没有可审计实现，保留为待复核线索，不入冻结 catalog。公司与实验室页面覆盖 OpenAI、Google DeepMind、Anthropic、Microsoft、Meta、Salesforce、Sakana AI、SambaNova、Nous Research、Prime Intellect、Cognition、阿里/通义、字节、腾讯、DeepSeek、月之暗面、智谱、MiniMax、Frontis；本轮没有发现新的、满足原始图/可用材料/许可门槛的通用 RSI 证据。下一项可执行工作仍是冻结选择器研究的三种子×三预算、匹配总评测成本、重复终测、父代同场重测和误拦/误放记账协议。
- 2026-10-29 · LAB round 3 已发布结果：按论文配置（GLM-5.3 executor、分层 30 任务子集、`k=1`、一次 final draw）实际评测 29 个可判分任务，base `0.852` → final `0.908`（+5.6 个百分点，17W/3T/9L）。报告明确说明收益全部来自失败修复（failure rescue），预算为 114 rollouts、174 次 improver calls、280,606,836 input / 11,377,445 output tokens；这是 nanoRSI 在该配置和单次抽样下的本地实验记录，不是通用 RSI 结论。报告还保留了逐任务父/子分数、选择决定和完整 ledger，下一步仍应以重复抽样、冻结留出集和匹配预算检验迁移，而不是把该增益写成稳定收益。
- 2026-10-29 · 新增 [Skill$^{\\infty}$](https://arxiv.org/abs/2610.35434) 线索（首发 2026-10-26）：把 meta-skill 与 task skill 放进同一套 agent-led 优化流程，并让 meta-skill 本身递归重写；论文在 SkillsBench 83 个任务上报告 60.7%，对比 human-curated 56.4% 与 SkillEvolver 54.5%。这是一条直接的技能/改进程序递归信号，但当前[官方仓库](https://github.com/taowangcheng/skill-infinity)只有 README、LICENSE 和 assets，README 明确代码尚未发布，未核验权重或数据包；因此不纳入冻结 catalog、不复制代码，也不把作者结果说成本地复现。其最可验证的 nanoRSI 方向是把“改任务技能”和“改优化技能”分成两个可审计版本流，并在匹配 token、冻结留出集和父代重测下比较，而不是启用递归 meta-skill 默认行为。
- 2026-10-28 · 收录 RSI-Opt（arXiv:2610.32026，Purdue University / 独立研究者，首发 2026-10-23）：跨运行演化提示、操作手册、已验证优化器代码库与决策节奏，并在运行内按训练动态修改优化器/诊断程序；论文 Figure 1、CC BY 4.0 论文许可和作者指标已核验，但未找到专属代码、权重或数据包，因此只作为既有“可编辑策略/技能记忆”协议输入，不声称 nanoRSI 复现或移植。
- 2026-10-27 · 复核 round 3 的 LAB 研究配置已登记但尚无可公开结果：当前配置按论文规则采用 GLM-5 executor、分层 practice-area 子集、k=1 和单次 final draw，仍不能把运行中的配置写成收益或本地复现。同期复核 OpenAI Third Moment 的官方工程说明与 Anthropic 的 RSI 综述页：两者提供的是受监督研究自动化与能力趋势证据，不是已公开、可独立复现的通用 RSI；OpenAI 的公开表述还明确区分了研究加速与“完全自主 RSI”。跟踪的 RSIHub（文档/论文消息）、Anton（artifact repair / approval / memory 修复）、OpenEvolve（岛初始程序与 diff 解析修复）及 Hermes Agent（Windows/desktop/plugin 维护）均未提供可在 nanoRSI 标准库核心中直接移植且许可边界清晰的新运行时能力；因此不复制代码、不增加依赖，继续以冻结预算、留出评测和失败记录作为下一步可验证工作。

- 2026-10-26 · 收录 EvoForesight/DeepEvolve（arXiv:2610.29784 v2，首发 2026-10-21、修订 2026-10-22）：论文原始 Figure 1、官方仓库和资源页已核验；仓库未见 LICENSE，完整训练实现/权重未公开，因此只记录闭环协议启发，不复制代码或声称本地复现。
- 2026-10-25 · 补录 R² Flow：首发 2026-09-27、v3 修订 2026-10-22；论文与 Figure 3 已核验，官方代码仓库可读但仓库级许可未核验，因此只采纳协议启发，不复制代码。
- 2026-10-24 · 体系切换：按综述两轴把存量 236 条整理论文笔记，此后每日收录直接写入本文件；industry-rsi 旧体系（catalog/render/分类页/RADAR）冻结归档。

## 1. 部署时自进化 / Deployment-time self-evolution（125 条）

### 技能文件优化与技能库（31）

- **[RSI-Opt: Recursive Self-Improvement Optimizer Agents For Model Training](https://arxiv.org/abs/2610.32026)**（Purdue University / 独立研究者，2026-10-23，闭环）
  - 核心：把优化器智能体的持久策略显式拆成 prompt、procedural playbook、已测试的 optimizer/diagnostic code library 和 decision cadence；跨运行由 meta-agent 基于历史证据重写并验证子策略，归档所有已评估策略；运行内的 agent 再按 loss/diagnostic 在预定决策点修改训练优化器和诊断程序。论文把“可复用知识跨运行继承”和“当前任务适应”分开测量。
  - 数字：五代、三个训练任务；Opus 5.5 的 evolution-suite raw-space summary z-score +10.48→+14.33，GPT-5.5 的 held-out tasks -0.36→+3.11；Burgers PDE 相对固定 prompt agent 的 mean relative L2 error 约降低 2.7 倍（Opus 5.5）和 8.8 倍（GPT-6.1）。这些是作者报告，不是 nanoRSI 本地复现；论文也指出 PDE 迁移随模型和任务变化。
  - 代码／权重／数据／许可：论文与原始 Figure 1 在 [arXiv HTML](https://arxiv.org/html/2610.32026) 可读，论文页面标注 CC BY 4.0；截至 2026-10-28 未核验到专属公开代码仓库、权重或可直接下载的数据包，不能把论文许可外推为实现代码许可。
  - 点评：对 nanoRSI 的直接方向是把候选 harness 的“可复用策略资产”和“本轮任务适配”在 evidence ledger 中分栏，比较跨运行继承、独立重写和冻结策略的匹配 token 成本，并保留被验证的可执行片段及其适用任务；这只是既有 ADOPTION #3/#7/#38 的实验协议输入，不启用新默认行为、不引入训练依赖。· [原始 Figure 1](industry-rsi/assets/paper-figures/rsi-opt-overview.svg)
  - 原文图／来源：论文原始 Figure 1（跨运行策略演化与运行内优化器适应的双层闭环）；[arXiv HTML](https://arxiv.org/html/2610.32026)，Figure 1，图源 `https://arxiv.org/html/2610.32026v1/overview.svg`。

- **[Evolving with Open Worlds: Towards Recursive Self-Improvement for Future Forecasting](https://arxiv.org/abs/2610.29784)**（中国人民大学高瓴人工智能学院 / 南洋理工大学 / IQuest Research，首发 2026-10-21，v2 修订 2026-10-22，闭环）
  - 核心：EvoForesight 将递归闭环拆成 Prometheus（从实时新闻与日程生成、去重、冲突检测和多样性选择可验证问题）、Branchus（把时效性搜索团队与只读取冻结证据的预测团队分开）和 Athena（用已解析结果驱动参数更新、技能蒸馏及面向弱点的任务合成技能）。同一条预测轨迹同时供参数、行为和环境三条更新轴使用，环境也随失败暴露的弱点而变难。
  - 数字：论文报告 FutureX 连续三周总榜第一、最高 rating 提升 195%；合成评测在四个基础模型上进入前三，最强基线差距最高 10.7 Bradley–Terry 点。另报告 RLVR 在两个模型上各提升 1.3 个 choice accuracy 点，GLM-4.7-Flash 的两轮 RFT 将 Brier 0.651→0.636→0.630、relative WIS 1.02→0.99→0.98。以上均为作者结果，不是 nanoRSI 复现。
  - 代码／权重／数据／许可：官方仓库 [RUCAIBox/EvoForesight](https://github.com/RUCAIBox/EvoForesight) 公开 README 与资源快照，核验时仓库仅 4 个提交、未见 LICENSE；论文称资源公开，但未核验完整训练代码、权重或可直接复现的训练包。论文与 Figure 1 可从 [arXiv HTML v2](https://arxiv.org/html/2610.29784v2) 获取。
  - 点评：可移植的是“冻结可见证据后再训练/蒸馏”的污染隔离、参数/技能/环境更新分账，以及把环境更新保持在独立评测之外；对 nanoRSI 先作为报告字段与实验协议输入，不引入新闻采集、RL 或外部数据依赖。· [原文 Figure 1](industry-rsi/assets/paper-figures/deepevolve-overview.png) · [官方仓库](https://github.com/RUCAIBox/EvoForesight)
  - 原文图／来源：论文原始 Figure 1（EvoForesight 总体闭环、三模块及三条更新轴）；[arXiv HTML v2](https://arxiv.org/html/2610.29784v2)，Figure 1，图片源地址为 `https://arxiv.org/html/2610.29784v2/deepevolve_overview.png`。

- **[R² Flow: Recursive Self-Improvement via Recursive Skill Evolution](https://arxiv.org/abs/2609.33867)**（The Chinese University of Hong Kong, Shenzhen / Fudan University / University of Illinois Urbana-Champaign / University of Oxford / National University of Singapore，首发 2026-09-27，v3 修订 2026-10-22，闭环）
  - 核心：把技能库更新放进两个嵌套环：阶段内在共享状态编排图上训练 Supervisor 的 flow，分别读出技能的 flow share 与有符号 utility；阶段边界由独立验证器证据、残差方差平台期和版本化技能库触发提案、配对验证、提交或回滚。独立步骤的不同排列合并为同一状态，避免树状历史重复分摊证据。
  - 数字：论文报告五次运行均值中，R² Flow 在所有 IID 数据集与指标上领先；相对 SkillOpt 平均高 2.03 个 EM 点与 5.57 个 accuracy 点。固定 Supervisor 迁移到六个冻结执行器时，IID/OOD 平均提升 15.70/24.64 点；八阶段 OOD 均值 71.2→81.02，37 次提交编辑中 33 次提高留出验证分（精度 0.89），并移除 12 个注入有害技能中的 11 个。以上是作者结果，不是 nanoRSI 复现。
  - 代码／权重／数据／许可：代码仓库 [beita6969/r2flow](https://github.com/beita6969/r2flow) 公开，包含训练入口、数据、配置和 Figure 1/3，但核验时仓库没有 LICENSE 文件，不能把代码许可写成已确认；论文页面标注 CC BY 4.0。Supervisor 使用 Qwen3.5-9B LoRA，执行需要 CUDA、80GB 级 GPU、SGLang、ALFWorld/EvalPlus 等外部资源；未核验到可直接下载的训练权重或完整可复现实验包。
  - 点评：对 nanoRSI 最可移植的是协议而非 flow 训练：在不改变默认选择器的前提下，把共享状态键、技能调用频次与独立验证证据分开记账，并将“高调用率不等于有益”作为审计字段；先做离线报告和配对验证对照，不引入 GPU/RL 依赖。 · [原文图](industry-rsi/assets/paper-figures/r2flow-framework.png) · [仓库](https://github.com/beita6969/r2flow)
  - 原文图／来源：论文原始 Figure 3（共享状态编排、flow share/utility 分离、验证器闸门及配对验证）；[arXiv HTML v3](https://arxiv.org/html/2609.33867v3)，图号 Figure 3，图片源地址为 `https://arxiv.org/html/2609.33867v3/fig3.png`。

- **[Trackable Skill Library Lifecycle Management for Agentic Reinforcement Learning](https://arxiv.org/abs/2610.25126)**（Rutgers University / Carnegie Mellon University / TikTok Inc.，2026-10-20，闭环）
  - 核心：由技能级随机对照证据驱动的技能生命周期管理，嵌入智能体 RL。在每个 GRPO 组内，把成组采样变成在线随机对照实验：技能独立随机注入加同任务组内对照，分离每个技能的真实贡献（解决共同检索技能的搭便车与难度混淆），并跨组做可靠性加权聚合。
  - 数字：在技能辅助与无技能两种评估下均优于近期的技能增强 RL 基线（主测试床 ALFWorld 及其他套件），含反思模型变体；
  - 代码：论文印刷的仓库 github.com/xizhu1022/TrackRL 核验时 404（已宣布未上线）；
  - 点评：把 ADOPTION 59 的因果归因线扩展出生命周期输出：评测面板内的技能级处理/对照注入给出因果效用，效用-掌握双轴账本把既有接受/拒绝记账升级为对演化技能的证据门控保留/退役决策。 · [原文图](industry-rsi/assets/paper-figures/trackrl-overview.png)

- **[One Skill Takes Over: Clashing Agent Skills and a One-File Fix](https://arxiv.org/abs/2610.25064)**（University of Southern California，2026-10-20，支撑·无闭环）
  - 核心：对技能干扰的实证解剖。SkillClash 含 16 对同职能技能，规则由代码校验并给出最佳可达参照输出；
  - 数字：五个家族的七个模型（4B 开源到 Qwen3-235B 与 GPT-4.1）上，技能单独加载时规则遵循 93-99%，并排装入同职能技能后降至 61-62%；
  - 代码：仓库 github.com/prazmara/skillclash 已上线（基准、代码与结果，2026-10-18 提交），核验时无 LICENSE 文件——按保留所有权利处理；
  - 点评：多技能工作区的技能模板卫生：运行前审计活跃技能文件的同职能规则重叠（冲突检查）； · [原文图](industry-rsi/assets/paper-figures/skillclash-takeover.png) · [仓库](https://github.com/prazmara/skillclash)

- **[Compile Once, Run Cheap: Frozen, Portable Skills for Embodied Agents, and What Recursive Self-Improvement Adds](https://arxiv.org/abs/2610.25114)**（Beijing Ou Rui Ling Shi Technology (Orillusion) / ChangingTek Robotics Technology (Suzhou) / Shanghai Yunfan Intelligent Control Robot Technology，2026-10-20，闭环）
  - 核心：带显式编译协议的技能级递归自改进。强通用模型仅作为隔离、受审计的离线作者，在仿真中编写、运行、诊断并修复一个操作技能，直到通过在冻结之后才抽取的布局考试；
  - 数字：在 7 个 RoboTwin 2.0 任务上，Claude Code 把 4 个任务编译为 7 个冻结技能（5 个首稿即只需资格验证），单个作者成本 4.29-8.22 美元（计入 13 次失败战役后为每技能 55 美元）；
  - 代码：仓库 github.com/Orillusion/embodied-skill-rsi 已上线，Apache-2.0 许可（LICENSE 从 raw.githubusercontent.com 读取；
  - 点评：该编译协议正是本仓库冻结教义在具身技能上的镜像：把“每轮修复旁配无反馈对照草稿”与“仅继承”对照作为标准实验臂； · [原文图](industry-rsi/assets/paper-figures/skill-rsi-protocol.png) · [仓库](https://github.com/Orillusion/embodied-skill-rsi)

- **[EvoSkill v2: Fully Agentic Skill Evolution from Benchmark Adaptation to a Stateful Evolver](https://arxiv.org/abs/2610.25931)**（Sentient Labs，2026-10-20，闭环）
  - 核心：只编辑指令文件的三智能体技能演化（模型与 harness 不动）。基准适配器把用户描述的基准与评分器冻结为插件；
  - 数字：在有细粒度标准答案的设定下，EvoSkill v2 的技能把留出通过率在 SpreadsheetBench v2 上超过 SkillOpt/SkillBoost 中较强者 7.7 点、tau3-bench banking 上 5.4 点；
  - 代码：核验时论文未给出代码仓库链接（所综述的 SkillOpt/SkillBoost 生态作为既有系统被引用）；
  - 点评：给选择器研究（ADOPTION 38/53）两项协议输入：跨代携带记忆的有状态提案器会话（替代逐次无状态）； · [原文图](industry-rsi/assets/paper-figures/evoskill-v2-architecture.png)

- **[From Trajectories to Differentiated Skills: Cognitive Differentiation for Self-Improving Agents](https://arxiv.org/abs/2610.23599)**（University of Science and Technology of China / Meituan / City University of Hong Kong，2026-10-19，闭环）
  - 核心：技能演化中的认知分化（CDSE）：统一技能通过四个功能不同而协同的组件——Meta、Experience、Tool、Script——演化。从成功与失败轨迹提取有据可依的语义梯度，经保留闸门按功能角色巩固，再以组件特定更新与验证、跨组件协调及自适应调用（决定哪些组件进入当前任务上下文）落地。
  - 数字：对 500 个广泛使用技能包的分析发现 96.8% 至少跨两个功能角色。
  - 代码：论文 HTML 中未发现仓库链接（2026-10-20 核验）；
  - 点评：把 nanoRSI 技能文件按 CDSE 四角色拆分并配组件级编辑预算（延伸 ADOPTION #53 文本学习率）与组件级接受检查； · [原文图](industry-rsi/assets/paper-figures/cdse-method.png)

- **[SkillNEO: Non-Elitist Evolutionary Optimization of Agent Skills](https://arxiv.org/abs/2610.20926)**（University of Illinois at Chicago / Mohamed bin Zayed University of Artificial Intelligence / University of California, San Diego / University of California, Los Angeles 等，2026-10-15，闭环）
  - 核心：非精英技能演化：把“选哪个版本来用”与“选哪些版本继续改”分开——提升可能需要多条相互依赖的编辑，低分修订仍可能带有可用部分。通过观察相关版本如何执行同一任务，识别应保留的可用步骤与待修复的残留失败；
  - 数字：在覆盖软件工程、办公与另外六个领域的 86 个 SkillsBench 任务上，SkillNEO 把 GPT-5.4 Mini 的平均奖励从 49.1% 提到 66.4%，进入 GPT-5.5 与 GPT-5.6 Luna 的原技能性能区间。
  - 代码：HTML 未找到专属仓库；
  - 点评：“用与改”分离的非精英选择是 ADOPTION 53 缺的另一半：让低分版本保持可编辑（但绝不投入使用）能抓住严格闸门丢弃的相互依赖编辑收益——与同批次 AtomSearch 的“保留但不晋升”状态互补（不同团队独立得出）。 · [原文图](industry-rsi/assets/paper-figures/skillneo-non-elitist-skills.png)

- **[CausalEvo: Causal Skill Self-Evolution for Health LLM Agents](https://arxiv.org/abs/2610.21016)**（University of Texas Health Science Center at Houston，2026-10-14，闭环）
  - 核心：冻结 LLM 每步提出两条新技能规则，与四条在位规则合并为候选集（在位者永远可选）。技能价值用因果方式估计而非裸面板分数：在候选集的随机重标环上，对每条有向边用相同反馈案例跑两次——共享 k-1 条背景规则、只交换被换的那条（等规则数把内容效应与规模效应分开）；
  - 数字：在六个 MedCalc-Bench-Verified 任务上（120 留出例、每任务 20、DeepSeek V4 Flash 0731 关思考）：CausalEvo 60.00% 对 SkillOpt 55.83% 对无技能 51.67%，训练 token 少 55.6%（2.203M 对 4.961M；
  - 代码：仓库 github.com/txbrook/CausalEvo 存在（2026-10-18 在线）但仅含手稿源码与数学检查器——论文明言完整训练代码与原始响应暂未包含；
  - 点评：共享背景下的成对交换是技能闸门上廉价的归因层：让候选编辑按配对方式计分而非信任裸面板差值，使技能因边际贡献而非面板噪声晋升； · [原文图](industry-rsi/assets/paper-figures/causalevo-skill-credit-fig1.png) · [仓库](https://github.com/txbrook/CausalEvo)

- **[AtomSearch: Evidence-Grounded Tree Search for Agent Skill Optimization](https://arxiv.org/abs/2610.19951)**（360 Security Technology Inc.，2026-10-14，闭环）
  - 核心：让技能修订动作保持局部，同时用后续技能状态引导搜索。对比原子编辑把每条最小规则编辑与失败/成功执行、一个行为假设和预期作用域绑定；
  - 数字：四个任务 × 五个目标模型：deepseek-v4-flash 下在 3/4 任务上超过 SkillOpt，LiveMathematicianBench 领先 9.68 个百分点，而 SkillOpt 终版技能字符数是其 2.3-19.7 倍。
  - 代码：HTML 全文未找到代码或仓库链接。
  - 点评：“67% 经由非最高分祖先”是对纯严格闸门技能采纳（ADOPTION 53）的直接外部反证：有界技能状态树（保留但不晋升）是单编辑严格验证与多编辑提案之间缺的中间层； · [原文图](industry-rsi/assets/paper-figures/atomsearch-skill-state-tree.svg)

- **[Knowledge Graphs as Files: An Agent Harness Where Tool Creation and Tool Use Co-Evolve](https://arxiv.org/abs/2610.18616)**（Texas A&M University / University of Oregon，2026-10-13，闭环）
  - 核心：DKGI（直接知识图谱交互）把 KG 导出为文件——节点 JSONL 分片、按关系的 TSV 边表、schema.json、candidate_ids.txt——让编码 CLI（Pi 或 Codex）里的 ReAct 式代理把 shell 检索与直接在这些文件上写并执行 Python 交织，不用预定义图 API 或子图检索器。每回合代理可向工具箱 T_t 增加程序 p_t、向 L_t 增加保存的输出文件 l_t；
  - 数字：免训练 DKGI 在 STaRK 合成测试（Amazon 1,642 / MAG 2,665 / Prime 2,801 查询）上：GPT-6-Astra 下对 GRASP（最强已训练基线）Hit@1 领先 +8.2 / +9.0 / +6.7——“每张图至少 6.7 Hit@1”；
  - 代码：代码 MIT 许可，位于 github.com/leopoldwhite/DKGI；
  - 点评：共演化的度量即可迁移点：给 nanoRSI 技能演化装上统计——“新程序中复用早前输出（嵌入 id）的比例、修订早前程序的比例、修订中有多少发生在失败之后”——这些按轨迹的廉价统计能区分真实积累与重新推导。 · [原文图](industry-rsi/assets/paper-figures/kgfiles-tool-coevolution.svg) · [仓库](https://github.com/leopoldwhite/DKGI)

- **[ViSkill: Reinforcing VLM Agents with Evolving Visual-Native Skills](https://arxiv.org/abs/2610.12403)**（Zhejiang University，2026-10-08，闭环）
  - 核心：技能增强的 agent 通常把空间布局线性化为文本；ViSkill 改为把成功交互存成视觉技能卡，供 VLM agent 检索以同时引导推理与奖励塑形，同时策略用 PPO 在这些轨迹上训练；
  - 数字：在 Sokoban / FrozenLake / PrimitiveSkill 上，基础方法成功率达 0.82 / 0.84 / 1.00（总 0.89），冷启动后 0.88 / 0.85 / 1.00（总 0.91），高于 AtlasVA 0.87、VAGEN 0.80、GPT-5 0.70、o3 0.69、Claude 4.5 Sonnet 0.58、Qwen2.5-VL-72B 0.40 与 Qwen2.5-VL-3B 0.09 的总成绩，且比标准 PPO 收敛更快。
  - 代码：代码：github.com/ZJU-REAL/ViSkill，MIT 许可（raw LICENSE 核验，版权 RAGEN.AI）。
  - 点评：模态这一点超出视觉本身：nanoRSI 技能是文本文件，而这是「以执行器原生表示（而非有损序列化）存储经验会改变技能演化可表达内容」的实测证据——值得在技能产物可以是数据文件而非散文的数字/面板任务上做一次最小 A/B。 · [原文图](industry-rsi/assets/paper-figures/visskill-visual-skill-cards.png) · [仓库](https://github.com/ZJU-REAL/ViSkill)

- **[Trajectory-Guided Fault Localization for Agent Skill Evolution](https://arxiv.org/abs/2610.11858)**（Nanjing University / The Hong Kong Polytechnic University，2026-10-08，闭环）
  - 核心：SkillMorph 把技能修订锚定在行为证据上：抽象化执行轨迹，跨重复运行与任务比较失败与成功证据，用演化循环之间的差异定位可疑动作，再在相应技能内定位编辑点并生成针对性修订——而不是仅凭结果反馈重写整条技能。
  - 数字：在 490 个 SWE-Skills-Bench 任务（1,470 次运行）上：SkillMorph 95.51% pass@3 / 92.24% 逐试精度 / 88.37% pass3，对照原始技能 82.45/75.44/67.96、四个技能演化基线中最强的 CAP-Evolve 92.24/89.39/84.90。
  - 代码：代码：arXiv 页与 HTML 均未找到。
  - 点评：nanoRSI 技能轨道可检验的思路：重写技能前，先对重复运行的抽象化失败/成功轨迹做差异对比，对可疑动作排序，并把编辑限制在这些动作回溯到的技能区域——与同评测预算下的整技能重写对照，并把编辑点精确率作为诚实的附加指标报告。 · [原文图](industry-rsi/assets/paper-figures/skillmorph-overview.png)

- **[RoboRSI: Stable, efficient, and reusable robot self-evolution in complex real-world environments](https://arxiv.org/abs/2610.12424)**（Noematrix Lab，2026-10-08，闭环）
  - 核心：自顶向下技能精炼（TSR）把任务分解为复合、原子与基础技能，各带职责范围与显式输入输出契约，使执行失败可归因到负责分支，修订也只落在该分支。Manager 组织技能层级，Planner 组合执行计划，Engineer 执行，Reviewer 在发布前验证；
  - 数字：在实体移动操作机上，多物体家庭清理经 104 轮自演化长成；
  - 代码：代码：github.com/nssmd/RoboRSI，仓库内核验为 Apache-2.0（123 星，创建于 2026-08-29，最后推送 2026-10-10）；
  - 点评：对 nanoRSI 可移植的纪律是契约约束的修订：给每条技能显式输入输出契约使失败归因到分支，把编辑限制在该分支内，并要求 Reviewer 式验证后技能才能回到库中——再测量同面板上约束编辑是否以更少回归胜过整文件重写，与既有反事实面板互相印证。 · [原文图](industry-rsi/assets/paper-figures/roborsi-framework.png) · [仓库](https://github.com/nssmd/RoboRSI)

- **[SkillAA: Attribution-Guided Skill-Graph Updating with Targeted Validation and Rollback](https://arxiv.org/abs/2609.20455)**（Nanjing University，2026-09-17，闭环）
  - 核心：在冻结模型上，对比成功/失败 rollout 把每次失败归因到具体技能图对象；修复只编辑被选中的局部结构，Local 与 Big 双闸门在提交前验证候选变更并支持回滚。
  - 数字：gpt-5.6-sol 下 SkillAA 达 SearchQA 81.5%、LiveMath 66.7%、DocVQA 91.2%，在所有主设置中观测均值最高；
  - 代码：代码位于 github.com/Ziqiao-Shang/SkillAA（核验时无 LICENSE 文件——仅可借鉴思想）；
  - 点评：nanoRSI 证据卡已存诊断与 diff； · [原文图](industry-rsi/assets/paper-figures/skillaa-attribution-rollback.png) · [仓库](https://github.com/Ziqiao-Shang/SkillAA)

- **[FINSKILLOPS: A Self-Evolving Multi-Agent System for SEC Filing QA](https://arxiv.org/abs/2609.19680)**（SimpleWay.AI / McGill University / University of Toronto / UCLA 等，2026-09-17，闭环）
  - 核心：类型化、证据接地的失败诊断被转成带作用域的技能补丁，经定向验证、回归检查与阴性对照后，在 SEC 文件问答的服务/进化双环中做版本化替换或退役。
  - 数字：进化技能把裁判打分的正确性从 3.70 提到 4.55；
  - 代码：arXiv 论文公开；
  - 点评：阴性对照准入（提案技能必须在失败切片上胜过不作为对照）与显式退役是 nanoRSI 技能流缺的两道闸； · [原文图](industry-rsi/assets/paper-figures/finskillops-sec-filing-qa.png)

- **[Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](https://arxiv.org/abs/2609.17653)**（Zhejiang University / University of Electronic Science and Technology of China，2026-09-15，闭环）
  - 核心：技能是部署期持续修订的多文件包，走反思-修订-复用循环：隔离评审者诊断失败、受限编辑接口限定可改的技能文件、修订过闸后复用——全程无权重更新。
  - 数字：免训练增益最高 +16.2%（MobileWorld）、+6.0%（AndroidWorld）、+10.5%（OSWorld），最后一项是跨基准迁移设定。
  - 代码：arXiv 论文公开；
  - 点评：受限编辑接口（仅指定技能文件可写）加隔离评审者与 nanoRSI 的契约守卫同构； · [原文图](industry-rsi/assets/paper-figures/evoskill-gui-reflect-revise-reuse.png)

- **[SkillLift: Learning Dense Rubrics from Sparse Oracles for Efficient Skill Evolution](https://arxiv.org/abs/2609.15396)**（Independent Researcher (Haoxiang Kang) / Fudan University (Ming Wen)，2026-09-14，闭环）
  - 核心：把技能自进化重构为双层优化，以摆脱 oracle-rollout 瓶颈（通常每个候选编辑都要跑一整次智能体 rollout）。学习一个结构化评分表 R——对技能行为的 M 条带符号权重的二元判据——作为廉价的 oracle 对齐替代器。
  - 数字：在 WildClawBench 与 SkillsBench、三个骨干模型上（SkillsBench 用 GPT-5.4-mini、WildClawBench 用 GPT-5.4，与官方实现对齐），SkillLift 同时超过人工技能、一次性 LLM 技能、SkillOpt 与 CoEvoSkills，且 token 成本比前沿进化方法省 40-70%。
  - 代码：代码以 MIT 发布于 github.com/WalteR-MittY-pro/SkillLift（仓库创建于 2026-08-08，核验时 2 星）。
  - 点评：对 nanoRSI 技能环：用学习的评分表替代器替换逐编辑全 rollout，周期性用秩相关在 oracle rollout 上重对齐——可在最小任务上直接验证其为更便宜的技能验收信号。 · [原文图](industry-rsi/assets/paper-figures/skilllift-dense-rubrics.png) · [仓库](https://github.com/WalteR-MittY-pro/SkillLift)

- **[SkillAdam: Stable and Efficient Skill Evolution for Agents](https://arxiv.org/abs/2609.08944)**（Renmin University of China / Tencent，2026-09-08，闭环）
  - 核心：目标模型保持冻结，只优化持久的自然语言技能。每轮在抽样小批次上执行当前技能，把案例级问题与结果写入演化问题跟踪器（方向记忆），估计近期改进波动，并由两种状态共同约束下一次补丁范围。
  - 数字：作者报告：覆盖短程与长程任务的七个基准上，相比列出的基线取得当时最优结果，同时使用更少优化轮次和更低成本。
  - 代码：官方代码发布于 github.com/ruc-datalab/SkillAdam，仓库内许可证为 MIT。
  - 点评：对 nanoRSI：在技能面增加小型持久优化状态记录——问题历史加有界编辑预算——同时保持现有评估器冻结。 · [原文图](industry-rsi/assets/paper-figures/skilladam-framework.png) · [仓库](https://github.com/ruc-datalab/SkillAdam)

- **[From Interaction Traces to Persistent Skills: Online Evolution for Computer-Use Agents](https://arxiv.org/abs/2609.04869)**（University of Electronic Science and Technology of China / Zhejiang University，2026-09-04，闭环）
  - 核心：每轮迭代在持久技能库的冻结快照上执行 GUI 任务；抽取器把轨迹转为结构化事实，提案者诊断并起草候选修改（新建/编辑/删除/显式 no-op），构建者把通过的材料化为带编辑历史的版本化 SKILL.md。
  - 数字：在与配置完全对齐的空技能库对照（同一动作生成与 GUI 定位栈、同一任务集与迭代轮数）下，系统在 OSWorld 四个应用域的预热后（t>=5）平均评测分全部更高，平均差 +5.7 至 +18.6 个百分点。
  - 代码：代码公开于 github.com/LongtaoHu/Skill-Evo4GUI（2026-09-15 可访问）；
  - 点评：把“冻结快照 + 版本化 SKILL.md + 显式 no-op”纪律移植进 nanoRSI 技能环：候选修改进入版本库，每个 episode 在冻结快照上运行，来源日志揭示哪些技能真的被检索、是否仍能解出来源任务。 · [原文图](industry-rsi/assets/paper-figures/persistent-skills-osworld.png) · [仓库](https://github.com/LongtaoHu/Skill-Evo4GUI)

- **[SimSkill: A Self-Evolving LLM Agent for Skill and Knowledge Accumulation in Traffic Simulation](https://arxiv.org/abs/2609.03753)**（Jilin University / Tongji University，2026-09-03，闭环）
  - 核心：基于 SUMO 交通仿真与 Claude 式技能运行时。学习模式下，智能体识别自身能力缺口、自生成环境锚定任务并求解，经行动-批评环验证后，把结果蒸馏进三种记忆：情景记忆（带日期的任务经验）、程序记忆（.claude/skills 风格可执行技能）、语义记忆（策展知识页）。
  - 数字：在两个留出基准、三个骨干 LLM 上评测，结果经作者所述的独立验证协议核验：验证成功率相对无记忆基线最多 +25 个百分点。
  - 代码：代码与实验数据公开于 github.com/qiliuchn/SimSkill-V1，Apache-2.0 许可（2026-09-15 核验）。
  - 点评：缺口驱动的任务生成小型化：让 nanoRSI 提案者维护显式“能力缺口”清单，按缺口生成环境锚定的探针任务，把验证通过的解存为可复用技能——在最小任务上复刻提议、执行、评估、蒸馏回路。 · [原文图](industry-rsi/assets/paper-figures/simskill-traffic.png) · [仓库](https://github.com/qiliuchn/SimSkill-V1)

- **[SkillGLoW: Procedural-Family Skill Consolidation for Self-Improving Agents on Long-Horizon Task Streams](https://arxiv.org/abs/2609.02217)**（National University of Singapore / Institute of Advanced Intelligence and Computing (IAIC), Singapore，2026-09-02，闭环）
  - 核心：每个任务的执行产出本地技能卡；基于嵌入的聚类把卡片聚成程序性家族，压缩器把每个家族压成去实例化的全局先验。
  - 数字：在跨 4 个基准（数学推理、终端自动化、软件修复、具身 ALFWorld）、3 个模型的 12 次持续改进运行中，整合先验相对无技能基线平均 +17.2 hard 分（本地再生后 +18.0），12/12 次运行全部为正。
  - 代码：未找到代码或数据发布，仅有论文与附录。
  - 点评：对 nanoRSI 技能库：把相关任务聚成家族并按家族压缩先验，而非维护单一全局文档； · [原文图](industry-rsi/assets/paper-figures/skillglow-procedural-families.svg)

- **[Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](https://arxiv.org/abs/2609.00065)**（K-Dense AI，2026-08-30，支撑·无闭环）
  - 核心：非闭环：一个开放许可的科研程序知识技能库，16 个科学实践领域（基因组、化学信息、医学影像、研究设计、科研传播）共 163 个技能。每个技能是一个目录，以版本化、人类可读的指令文件为中心、按需加载，常附参考资料与可运行脚本——编码了领域接受哪种检验、哪个标识符命名空间是权威。
  - 数字：无任务级评测与基线；
  - 代码：代码/库在 github.com/K-Dense-AI/scientific-agent-skills（MIT，核验时 45,207 星）。
  - 点评：对 nanoRSI：其 token 预算核算（常驻描述 vs 惰性加载 vs 溢出）是技能库成本报告的正确格式； · [原文图](industry-rsi/assets/paper-figures/scientific-agent-skills-library.png) · [仓库](https://github.com/K-Dense-AI/scientific-agent-skills)

- **[WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution](https://arxiv.org/abs/2608.27454)**（Google Research / Virginia Tech，2026-08-27，闭环）
  - 核心：三层工作区：不可变的原始执行轨迹、跨迭代复利的持久 wiki（模式、日志、技能影响记录）、活跃的 SKILL.md 技能层。每轮推理智能体带技能（但不可访问 wiki）执行；
  - 数字：五个基准 x 五个模型、3 次运行、配对 bootstrap p<0.05：WikiSkill 全格胜过无技能、Trace2Skill、EvoSkill 与 SkillOpt（如 Gemini-3.5-Flash 68.1 对 SkillOpt 55.9；
  - 代码：未找到代码发布；
  - 点评：对 nanoRSI：把'永不回滚的知识'（wiki，含接受/拒绝 diff）与'可回滚的可执行技能'分层——一个单调增长的审计层，让技能闸门决策可事后复查。 · [原文图](industry-rsi/assets/paper-figures/wikiskill-experience-wiki.png)

- **[SkillOpt: Agent skills as trainable parameters](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/)**（Microsoft Research，2026-06-30，闭环）
  - 核心：把自然语言技能文件当作“活在冻结目标模型之外的 可训练参数”。由独立的优化器模型在文本空间跑前向-反向-更新环：前向 = 冻结目标执行任务批；
  - 数字：在报告的全部 52 个评测格中最佳或并列最佳（博文口径），覆盖六个基准（SearchQA、SpreadsheetBench、OfficeQA、DocVQA、LiveMathematicianBench、ALFWorld）、七个模型（GPT-5.5 到 Qwen3.5-4B）与三种执行模式（直连、Codex、Claude Code），对照包括人工技能、一次性 LLM 技能、Trace2Skill、TextGrad、GEPA 与 EvoSkill。
  - 代码：代码 MIT 许可，位于 github.com/microsoft/SkillOpt（LICENSE 已于 2026-10-16 核验）；
  - 点评：正是 nanoRSI skills 模板缺的模式：文本学习率（每步有界编辑数）、严格“留出验证上严格更好才采纳”的闸门、复用为负反馈的被拒编辑缓冲、逐 epoch 汇总一遍——全部可在现有技能文件周围用标准库实现。 · [原文图](industry-rsi/assets/paper-figures/msr-skillopt-skill-parameters.png) · [仓库](https://github.com/microsoft/SkillOpt)

- **[SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://www.microsoft.com/en-us/research/blog/skillopt-agent-skills-as-trainable-parameters/)**（Microsoft Research，2026-06-30，闭环）
  - 核心：把 agent 的技能文件当作文本空间中的可训练参数：优化器模型在前向–反向–更新循环中提出有界编辑，候选技能"只有在留出验证集上严格优于当前技能时才被采纳"；被拒编辑进入缓冲区作为负反馈，其上还有按 epoch 的慢速/元更新。
  - 数字：作者报告：在全部 52 个评测单元（6 基准 × 7 模型 × 3 执行模式）中相对人工技能、单次 LLM 技能、Trace2Skill、TextGrad、GEPA、EvoSkill 取得最优或并列最优；
  - 代码：官方实现已核验：github.com/microsoft/SkillOpt（MIT 许可，2026-05-08 创建，约 1.7 万星）；
  - 点评：建议：在 nanoRSI 的技能面上增加"留出闸门"技能编辑器——只在严格验证提升时采纳有界 diff 提案——与无闸门自编辑及冻结技能在相同任务流上对比，记录编辑采纳率与回归。 · [原文图](industry-rsi/assets/paper-figures/microsoft-skillopt.png) · [仓库](https://github.com/microsoft/SkillOpt)

- **[SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History](https://arxiv.org/abs/2606.08671)**（WeChat, Tencent Inc.，2026-06-07，闭环）
  - 核心：持久决策历史保存诊断、候选技能修订、脱敏评测证据和结果。优化 Agent 与评测 Agent 分别操作技能仓库和评测仓库；
  - 数字：在 Qwen3.6-35B-A3B 的开放网页设置中，SkillHone 报告 GAIA 平均 64.6，对比精心构建的深度研究 Agent 48.8（+15.8）；
  - 代码：已核验 Tencent/SkillHone 公开仓库。
  - 点评：为 nanoRSI 增加版本化技能目录：保存决策记录、候选 diff、评测证据和回滚决定，再在隐藏任务上比较固定技能与接受修订后的复用。 · [原文图](industry-rsi/assets/paper-figures/tencent-skillhone.png) · [仓库](https://github.com/Tencent/SkillHone)

- **[OpenSkill: Open-World Self-Evolution for LLM Agents](https://arxiv.org/abs/2606.06741)**（Lehigh University / University of Illinois Chicago / University of British Columbia / Vector Institute / Salesforce AI Research 等，2026-06-04，闭环）
  - 核心：技能与其验证信号都从零构建、无目标任务监督：开放世界知识获取从文档、仓库、论文与网络检索任务知识与验证锚点（查询经过滤去掉基准名防泄漏）；无泄漏技能进化按计划起草 1-4 个技能，对照锚定在可独立验证事实上的自制'虚拟测试'迭代精炼（至多 3 轮），gap-vs-bug 分类器触发定向检索；
  - 数字：SkillsBench：Opus 4.6 43.6% 对最强基线 Skill-Creator 34.7%（+8.9；
  - 代码：代码在 github.com/OpenLAIR/OpenSkill（Apache-2.0，核验时 92 星）；
  - 点评：对 nanoRSI：无评估器时，先从可独立验证的事实构建验证锚点、再构建技能； · [原文图](industry-rsi/assets/paper-figures/openskill-open-world.png) · [仓库](https://github.com/OpenLAIR/OpenSkill)

- **[SkillEvolver: Skill Learning as a Meta-Skill](https://arxiv.org/abs/2605.10500)**（Tsinghua University / Beijing Jiaotong University，2026-05-11，闭环）
  - 核心：技能自进化被封装为任何遵循协议的 CLI 智能体都能加载的“元技能”；只更新技能的文本与代码，不动模型权重。
  - 数字：SkillsBench（83 任务、15+ 领域）：56.8% avg@5，对比人工精选技能 43.6%、无技能 29.9%；
  - 代码：官方代码位于 THU-AICosmos/skillevolver，MIT 许可（2026-09-15 核验）；
  - 点评：把“新鲜智能体过拟合审计 + 静默旁路检查”采纳为 nanoRSI 的技能验收闸门：用无任何先前会话状态的智能体审计候选技能，同时检验泄漏与运行时是否真的调用该技能。 · [原文图](industry-rsi/assets/paper-figures/skillevolver-meta-skill.png) · [仓库](https://github.com/THU-AICosmos/skillevolver)

- **[EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](https://arxiv.org/abs/2605.10332)**（Huazhong University of Science and Technology / University of Science and Technology of China / Microsoft Research / Institute for AI Industry Research (AIR), Tsinghua University 等，2026-05-11，闭环）
  - 核心：免训练闭环，为冻结执行器进化二段式程序技能 S = (S_body, S_app)。每条轨迹相对当前技能解读并按证据类型拆分：技能变更类证据（Discovery、Optimization、SkillDefect 反思）整合后对技能主体做定向编辑，模型扮演受限编辑者而非自由重写者；
  - 数字：ALFWorld（3,553 训练 / 134 测试任务，K=1，10 个修订阶段）上，冻结的 Qwen3.5-27B 执行器达 93.28% 成功率，比无技能直用 GPT-5.2 高 31.58 分；
  - 代码：代码以 MIT 发布于 github.com/air-embodied-brain/EmbodiSkill（仓库创建于 2026-07-03，核验时 25 星）。
  - 点评：对 nanoRSI 技能进化：把更新证据拆成两条通道——技能内容缺陷触发编辑； · [原文图](industry-rsi/assets/paper-figures/embodiskill-skill-aware-reflection.png) · [仓库](https://github.com/air-embodied-brain/EmbodiSkill)

- **[CoEvoSkills: Self-Evolving Agent Skills via Co-Evolutionary Verification](https://arxiv.org/abs/2604.01687)**（University of Illinois Chicago / MBZUAI / McGill University / Columbia University 等，2026-04-02，闭环）
  - 核心：技能生成器产出多文件技能包，共同进化的代理验证器仅凭结构化失败反馈把关；ground-truth oracle 保持信息隔离（只给不透明 pass/fail）并触发测试升级，技能与验证器在无标注下互相自举。
  - 数字：SkillsBench（Claude Opus 4.6 + Claude Code）：通过率 71.1%，对照无技能 30.6%（+40.5pp）、人工技能 53.5%（+17.6pp）、Anthropic Skill-Creator 34.1%；
  - 代码：Apache-2.0 代码位于 github.com/Zhang-Henry/CoEvoSkills（已核验）；
  - 点评：nanoRSI skills starter 可借鉴信息隔离验证器模式：严格闸门只看结构化失败反馈，oracle 只发不透明 pass/fail，oracle 调用触发验证器测试升级。 · [原文图](industry-rsi/assets/paper-figures/coevoskills-coevolutionary-verification.png) · [仓库](https://github.com/Zhang-Henry/CoEvoSkills)

- **[SkillClaw: Let Skills Evolve Collectively with Agentic Evolver](https://arxiv.org/abs/2604.08377)**（Alibaba (Amap DreamX Team)，2026-04，闭环）
  - 核心：跨用户群体的技能集体进化：跨用户会话变成保留完整'动作-反馈'因果链的结构化轨迹；会话按所引用的技能分组（天然消融，隔离每个技能的影响）；
  - 数字：WildClawBench（Qwen3-Max 骨干、8 个模拟用户、6 天；
  - 代码：代码在 github.com/AMAP-ML/SkillClaw（MIT，核验时 2,613 星）。
  - 点评：对 nanoRSI：先按'调用过的技能'给执行证据分组再做归因——按技能分桶的会话是无须额外消融运行的最廉价因果隔离。 · [原文图](industry-rsi/assets/paper-figures/skillclaw-collective-evolution.png) · [仓库](https://github.com/AMAP-ML/SkillClaw)

### Harness 搜索与进化（28）

- **[HarnessPro: Recursive Harness Self-Improvement with Pareto Optimization for Performance-Cost Trade-offs](https://arxiv.org/abs/2610.26770)**（Tsinghua University / Z.AI Co., Ltd. / Shanghai Jiao Tong University / University of Warwick 等，2026-10-20，闭环）
  - 核心：性能-成本 Pareto 目标下的无标签递归 harness 演化。每轮：专用智能体诊断执行轨迹、按不同性能-成本优先级规划更新并实现为候选 harness；
  - 数字：在 Terminal-Bench 2、SWE-Bench Pro 与 ProgramBench 上（GPT-5.5 + Codex），heavy 模式较 RHO 平均 +2.0 通过率点、每任务成本降 26.1%（平均延迟 520 秒降至 412 秒）；
  - 代码：仓库 github.com/pzs19/HarnessPro 已上线，MIT 许可（2026-10-19 首发，LICENSE 从 raw.githubusercontent.com 读取）；
  - 点评：把成本变成一等选择轴：证据账本已按候选计 token——在冻结测试前固定并报告一条 Pareto 前沿（便宜/均衡/昂贵的代），而非单一最高分赢家。 · [原文图](industry-rsi/assets/paper-figures/harnesspro-overview.png) · [仓库](https://github.com/pzs19/HarnessPro)

- **[Federation over Harness](https://arxiv.org/abs/2610.24007)**（University of Chicago，2026-10-20，闭环）
  - 核心：在分布式多智能体经验共享中同时自动演化两个层级的 harness。服务端智能体演化各客户端的任务求解与自我反思 harness，同时演化自己用于聚合分布式反思、维护共享洞察库、更新后续客户端 harness 的 harness。
  - 数字：在 PinchBench（V1 既有任务 + 124 个仅 V2 的留出任务）与 ClawEval 上，FoH 较固定 harness 的单智能体基线提升 53.57%，较单智能体 harness 自演化提升 29.76%；
  - 代码：仓库 github.com/dixiyao/FoH 已上线，MIT 许可（LICENSE 从 raw.githubusercontent.com main 读取）；
  - 点评：无验证信号设定是对本仓库“评测器冻结”教义的诚实压力测试：任何仅反思的变体都必须标注为设计上不可验证、并与冻结评测器闸门对照； · [原文图](industry-rsi/assets/paper-figures/foh-workflow.png) · [仓库](https://github.com/dixiyao/FoH)

- **[Self-Evolving Coding Agents via Harness-Policy Optimization](https://arxiv.org/abs/2610.22791)**（Microsoft Research / Carnegie Mellon University / University of Virginia，2026-10-19，闭环）
  - 核心：在同一个智能体上交替两步的递归自改进。H 步：冻结的策略分析自己在搜索集上的失败并提出 harness 候选——一个继承种子 mini-SWE-agent 的 Python 类，可覆写 step、提示、反馈与提交处理；
  - 数字：Qwen3.5-35B-A3B 基座、三个编码基准（avg@3）：SWE-Bench Verified 解题率 61.0%→69.5%（自提案），外部 Opus 4.8 提案器达 71.6%；
  - 代码：仓库 github.com/MSR-Orchard/Self-HPO 已上线，MIT 许可（2026-10-20 从 raw.githubusercontent.com main 读取）；
  - 点评：在最小任务上移植交替调度：每个接受的 nanoRSI 代后，用当前候选恰好失败的 episodes 重建提案搜索集，并让技能文件编辑与策略侧代理量（如提示/选择参数）交替，检验同预算下交替是否优于单改变面。 · [原文图](industry-rsi/assets/paper-figures/selfhpo-overview.png) · [仓库](https://github.com/MSR-Orchard/Self-HPO)

- **[VideoHarness-SRSI: Structured Recursive Self-Improvement for Video Understanding Harness](https://arxiv.org/abs/2610.19424)**（Meta MRS Research / UC Davis / Duke University / University of Illinois Urbana-Champaign 等，2026-10-14，闭环）
  - 核心：研究围绕冻结视觉语言模型的递归 harness 演化（智能视频理解）。基线 VideoHarness-BRSI 演化 4,000+ 候选、可与手工系统匹敌，但有三个被诊断的失败模式：验证过拟合（复用的验证反馈同时驱动修订与提案器搜索向验证集靠拢）、搜索预算稀释与早期经验陷阱。
  - 数字：在四个视频理解基准上，VideoHarness-SRSI 相对 BRSI 将等权平均留出分提升 6.2%，并将平均验证-测试差距缩小 37.9%。
  - 代码：截至 2026-10-16 未声明代码或数据发布；
  - 点评：其诊断正是 nanoRSI 反事实闸门的镜像：被修订与提案选择两头复用的验证反馈会过拟合——SRSI 的解法（给提案器无内容反馈、预提交的热身信号审计、机制级先隔离 probe-race 再组合）是既有评测器泄漏工作的具体范式； · [原文图](industry-rsi/assets/paper-figures/videoharness-srsi-evidence-governed.svg)

- **[TimeRSI: Towards Self-Improved Agentic Deployment for Time-Series Foundation Models](https://arxiv.org/abs/2610.19725)**（Georgia Institute of Technology / University of Southern California / Samay AI，2026-10-14，闭环）
  - 核心：围绕冻结时序基础模型的自改进部署系统：编码智能体把任务描述翻译成可执行的流水线改动，在历史预测窗口上测试每次修订并用观测误差引导后续修订；部署期由自适应选择器按相似条件下已完成预测的表现，在积累的流水线中挑选。
  - 数字：在 TIME 与 FEV-bench 的 198 个任务上，TimeRSI 在六项点预测与概率预测指标上全面超过所有参赛提交（对比提交中排名第一）。
  - 代码：代码 Apache-2.0，位于 github.com/haoxin1998/TimeRSI（LICENSE 已于 2026-10-17 经 raw.githubusercontent.com 核验）。
  - 点评：采纳流水线编辑前先在历史窗口预验证，就是换了部署外衣的训练/验证闸门——与 nanoRSI 晋升前教义一致； · [原文图](industry-rsi/assets/paper-figures/timersi-agentic-deployment.png) · [仓库](https://github.com/haoxin1998/TimeRSI)

- **[HarnessTTT: Learn to Optimize Harness at Test-Time for Scientific Discovery](https://arxiv.org/abs/2610.17370)**（University of Wisconsin-Madison / NVIDIA / Johns Hopkins University / Stanford University 等，2026-10-12，闭环）
  - 核心：执行器冻结、在测试时训练 harness 提案器：提案器（执行器模型 + 持久 rank-64 LoRA，每轮 3 epoch，PPO 式裁剪目标，对冻结基座 KL 0.1）产出可执行 harness——系统提示、可复用技能、工具、中间件、执行控制——每个引导一次预算内发现式 rollout，其结果更新提案器。发现导向的策略梯度用缺口归一化奖励 g_k = (s_k − b_τ)/Z_τ（对已发表参考的剩余缺口；
  - 数字：冻结 9B 执行器：同一执行器下在全部十一个基准任务上胜过 OpenEvolve（圆装箱 1.17→2.64）；
  - 代码：项目页 gray311.github.io/harnessrl 链接了两个不同 GitHub 仓库（Code 按钮：SaFo-Lab/Self_Adapt_Harness；
  - 点评：奖励配方可直接移植到 nanoRSI 的小噪声面板选择：把候选按（分数 − 父代）/对参考的剩余缺口归一化，正信用平滑封顶、损失取下限、非法尝试记 −1； · [原文图](industry-rsi/assets/paper-figures/harnessttt-test-time-harness.svg)

- **[Harness^2: Recursive Agent Harnessing for an Open World](https://arxiv.org/abs/2610.14224)**（Google Cloud AI Research / Northwestern University，2026-10-09，闭环）
  - 核心：在 K=8 个可编辑组件的 harness（系统提示、护栏、记忆、技能、工具指引、脚本、子代理、TypeScript 中间件）上做两层递归。任务级 Propose-Probe-Compose：先以当前 harness 跑一次参照执行，再提出“不变式”候选（跨领域代理缺陷）与领域专用候选各一；
  - 数字：在三个专业基准与四个模型-harness 配置（冻结的 GLM-5 与 Gemini 3.5 Flash 执行器 × OpenCode 与 Codex 基线 harness）上，单步递归增益最高 WorkBuddy-Bench +11.5 分（GLM-5/OpenCode 64.2→75.7）、JobBench +4.5（Gemini 3.5 Flash/OpenCode）、LAB partial +11.8 个百分点（GLM-5/OpenCode 59.6→71.4）；
  - 代码：代码 Apache-2.0，位于 github.com/google-research/harness2（LICENSE 已于 2026-10-16 核验；
  - 点评：反差探测是 nanoRSI 在开放任务上缺失的免验证器闸门：父代跑一次取参照，子代在匹配配置下重跑，比较轨迹/交付物，只接受有反差支撑的编辑——不用分数、评分表或真值。 · [原文图](industry-rsi/assets/paper-figures/harness2-recursive-harnessing.png) · [仓库](https://github.com/google-research/harness2)

- **[Evo²: Evolving the Evolver through Weight-Harness Co-Evolution](https://arxiv.org/abs/2610.13025)**（Google DeepMind / University of Illinois, Urbana-Champaign，2026-10-09，闭环）
  - 核心：单一策略在 harness 上扮演双角色：Proposer 写 harness 编辑、Reflector 诊断其效果并引导修订，交叉操作在搜索树分支间迁移策略。权重更新把闭环收到演化器自身：EvoTIDE（树引导交错双角色演化）用编辑抽取与前缀续写恢复可用训练轨迹，按每个角色决策引起的任务性能差给奖励（畸形输出记负奖励、只有留下机制确实运行的痕迹证据才计增益），再以 SFT 热启动加交错 GRPO 在 Proposer 与 Reflector 组间训练，每轮对位角色用冻结快照。
  - 数字：以 Qwen3.8-27B 同时充当执行器与演化器：Polyglot 82.1%、SWE-bench Verified 48.3%，对最强基线 62.6%（GEA）与 41.0%（HGM）；
  - 代码：论文未随附代码、权重或数据（arXiv 页与 HTML 均无链接）。
  - 点评：双角色分解可映射到 nanoRSI 的提案器/闸门分工：一个策略既提编辑又反思闸门结果，按角色的性能差奖励可直接从既有冻结面板证据账本算出，无需新闸门行为。 · [原文图](industry-rsi/assets/paper-figures/evo2-weight-harness-coevolution.png)

- **[Harness Evolution Hits a Ceiling: When Weight Training Should Begin](https://arxiv.org/abs/2610.11655)**（Independent / University of California, Berkeley / Purdue University / Stanford University，2026-10-08，闭环）
  - 核心：种子 harness 下的轨迹按首个失败信号标注为失败构成；过程性失败（调用受阻、循环、预算耗尽）分流给自演化 harness 循环（LLM 提议编辑、judge 校验），内容性失败分流给权重训练：在演化后 harness 采集的轨迹上做 LoRA 或全量微调。
  - 数字：在 DeepPlanning（48 开发 / 72 保留）上，harness 演化把 Qwen3.5-4B 保留分从 0.16 提到 0.30、Qwen3.5-9B 从 0.32 提到 0.44（对全新锚点的四轮均值）；
  - 代码：代码：arXiv 页与 HTML 中均未找到（称逐次前沿读数将随代码发布，暂无仓库）。
  - 点评：先诊断后干预的规则可在 nanoRSI 直接检验：把每次失败标注为过程性或内容性，只把过程性失败路由给 harness/技能编辑，并报告过闸集合的构成是否相对全失败选择器改变。 · [原文图](industry-rsi/assets/paper-figures/harness-ceiling-failure-composition.png)

- **[Safe, Persistent, and Evolving Agent Harness for Understanding Partially Observable Worlds](https://arxiv.org/abs/2610.11552)**（Hong Kong University of Science and Technology / Lightspeed / Independent，2026-10-08，闭环）
  - 核心：E-Ledger 是带代码审批层的多 agent harness：每个动作先过策略检查再执行，并维护已验证隐藏规则加证据支撑动态状态的账本。WorldAbduct 用溯因演化该 harness：跨四个视图（状态一致性、世界-观测差、策略闸正确性、目标判断）诊断执行轨迹以假设潜规则，经定向溯因交互验证后才写入账本。
  - 数字：在企业 World of Workflows 基准上，WorldAbduct 在四个后端上均取得最高安全任务完成率（DeepSeek-V4-Pro 80 STCR / 85 TCR / 95 PSR；
  - 代码：代码：github.com/HKUST-KnowComp/E-LEDGER-WorldAbduct——公开但仓库未找到任何 LICENSE 文件，按保留所有权利处理：只取思想，不复用代码。
  - 点评：账本纪律是可移植模式：假设规则只有经定向验证交互后才进入持久状态，harness 修订由四视图失败诊断驱动——是 nanoRSI「失败后蒸馏」技能循环带逐规则显式准入检查的结构化版本。 · [原文图](industry-rsi/assets/paper-figures/eledger-worldabduct-overview.png) · [仓库](https://github.com/HKUST-KnowComp/E-LEDGER-WorldAbduct)

- **[Self-Evaluating Recursive Agents](https://arxiv.org/abs/2610.04902)**（Tongji University / Independent / Shanghai Artificial Intelligence Laboratory / Shanghai Jiao Tong University 等，2026-10-04，闭环）
  - 核心：SERA 训练同一个递归策略同时进行任务分解、子任务执行和结果评估。委派前，父节点先写出加权 rubric；
  - 数字：论文报告公开 checkpoint 在 632 个 TextCraft-Synth 任务上的三次运行平均成功率为 74.31%，在 1,400 个 TextWorld-Sync 任务上为 65.07%；
  - 代码：代码：作者标注的 OliverLeeXZ/SERA 官方实现公开，但未核验到根目录项目许可证；
  - 点评：只复用可移植的对照思路：未来递归智能体轨道可在相同执行器、任务面板、种子和 token 预算下比较外部裁判、固定 rubric 与习得 rubric； · [原文图](industry-rsi/assets/paper-figures/sera-training.png) · [仓库](https://github.com/OliverLeeXZ/SERA)

- **[RSI-Master: Structuring Experiments to Guide Autonomous Model Improvement](https://arxiv.org/abs/2609.35561)**（Shanghai Jiao Tong University / University of Science and Technology of China / Shanghai AI Laboratory / Zhejiang University 等，2026-09-28，闭环）
  - 核心：RSI-Master 改变的是围绕冻结或另行训练模型的研究 harness：Experiment OS 将低层操作限制为可检查的 CLI 动作与结构化产物，reviewer-guided research DAG 让 worker 探索不同后训练方向，并由 reviewer 在增加 worker 或提升配方前比较证据。改变对象是实验/研究流程及其持久证据，不是通用的自主模型权重闭环。
  - 数字：在 Qwen3-4B-Base 的 PostTrainBench 上，论文报告平均分 54.49，对比最强 agent 基线 46.53，hacking rate 为 0.0%。
  - 代码：代码：未核验到官方公开仓库。
  - 点评：只复用可移植的控制模式：在 nanoRSI 现有评测器外增加可选、离线的 research-DAG/evidence-ledger 对照。 · [原文图](industry-rsi/assets/paper-figures/rsi-master-overview.png)

- **[RRSI: Regularized Recursive Self-Improvement of Agent Harnesses](https://arxiv.org/html/2609.24972v1)**（Google Cloud AI Research / Stanford University / Washington University in St. Louis / UNC-Chapel Hill，2026-09-21，闭环）
  - 核心：在冻结模型上运行有界的提案→反馈→选择 harness 闭环。提案侧逐轮降低一次可捆绑的编辑数，使用完整编辑历史分配信用，并在停滞时把搜索转向尚未尝试的组件；
  - 数字：在冻结 Claude Opus 4.8、匹配进化预算的条件下，RRSI 报告 Terminal-Bench 2.1 从 74.2→80.2（+6.0），SWE-bench Verified 从 82.0→83.8（+1.8）；
  - 代码：代码：google-research/rrsi 公开，Apache-2.0，包含搜索核心与领域适配器。
  - 点评：在 nanoRSI 现有 harness/skill 候选闸门上做小型离线消融：把当前严格改进选择与一个正则化臂比较，后者（1）由重复冻结评测估计噪声带，（2）跨轮记录组件级编辑信用，（3）用递减预算限制一次捆绑编辑数，（4）没有补偿性增益时拒绝新增测得成本。 · [原文图](industry-rsi/assets/paper-figures/rrsi-pipeline.png) · [仓库](https://github.com/google-research/rrsi)

- **[Bad Genius: Counterfactual-Guided Harness Evolution Beyond Task-Specific Shortcuts](https://arxiv.org/abs/2609.18366)**（University of Chinese Academy of Sciences / National University of Singapore / Institute of Automation, CAS，2026-09-16，闭环）
  - 核心：提案者进化目标智能体的 harness（提示、记忆、检索、工具、控制代码）；挑战者搜索保持任务有效性的基准反事实变体，确认档案会把在反事实下不再成立的增益降级，针对逐任务留集漏掉的基准级捷径。
  - 数字：OfficeQA（每题 3 次滚动）上进化后 harness 的 R̂avg,A3 达 68.42%，对照原始 harness 66.23%（+2.19）；
  - 代码：arXiv 论文公开；
  - 点评：把挑战者移植进 nanoRSI 闸门：在最小任务集自动生成的保有效性反事实上重测被接受候选； · [原文图](industry-rsi/assets/paper-figures/chase-counterfactual-harness.svg)

- **[EvolveTrade: Experience-Driven Policy Refinement for Self-Evolving LLM Trading Agents](https://arxiv.org/abs/2609.17632)**（KAIST / DeepAuto.ai，2026-09-15，闭环）
  - 核心：交易 agent 的系统提示被当作文本参数化的工具调用策略：独立 Policy Agent 每五个交易日依据决策轨迹与组合实绩改写它，底座 LLM 与工具全程冻结。
  - 数字：GPT-5-mini、15 只美股蓝筹、3 次运行均值：Nov 2025 窗口 Sharpe 5.12 vs 静态工具调用 agent 2.87、累计收益 5.10% vs 3.30%；
  - 代码：arXiv 论文公开（CC BY 4.0）；
  - 点评：一个带诚实负结果的最小自进化 agent 夹具：策略文本仅每 N 个任务批次依据累积轨迹证据改动，逐窗口对冻结策略的胜负就是发布口径。 · [原文图](industry-rsi/assets/paper-figures/evolvetrade-experience-driven-policy.png)

- **[ModularRSI: Modular and Generalizable Recursive Harness Self-Improvement](https://arxiv.org/abs/2609.14857)**（Beihang University / University of Manchester / IQuest Research / M-A-P 等，2026-09-14，闭环）
  - 核心：对同一任务上成功与失败轨迹做对比分析，驱动五个 harness 模块（智能体循环、工具使用、观测管理、上下文管理、任务完成检测）各自在受限范围内独立进化；随后一轮跨模块集成解决冲突（重复、职责、协作）再冻结模块库。
  - 数字：TerminalBench 2.0（DeepSeek-V4-Flash）：域内准确率 47.57→52.43、Pass@3 58.43→65.17；
  - 代码：核验时未找到代码仓库；
  - 点评：对 nanoRSI：把 harness 分解为具名模块并限定各自编辑范围，在与基准不相交的可执行任务上用成功/失败对比对分别进化，合并库须经显式冲突消解轮再冻结。 · [原文图](industry-rsi/assets/paper-figures/modularrsi-overview.png)

- **[(Self-Improving)² Coding Agents: Curating High-Quality Trajectories via Recursive Self-Improvement](https://github.com/Self-Improving-Coding-Agents/SI2CA)**（Self-Improving-Coding-Agents project，2026-09-11，闭环）
  - 核心：在 turn 层，冻结的后端模型生成多个候选动作，并用 self-judgement（基于特权信息的评分表加权打分）或 self-likelihood（长度归一化条件似然）选择动作。独立的递归策略发现环读取历史提案、策略、结果及接受/拒绝候选，提出何时以及如何分支，在验证任务上评估策略，并且只有在准确率提高或准确率相当但轨迹更短时保留。
  - 数字：README 报告的作者结果包括 SWE-bench Verified（500 题）：Qwen3.5-35B-A3B 的 self-judgement 为 70.0%，标准组为 65.8%（+4.2），self-likelihood 为 66.8%；
  - 代码：代码：Self-Improving-Coding-Agents/SI2CA 公开，Apache-2.0。
  - 点评：只复用可检查的部分：在 nanoRSI 现有 evidence ledger 上增加有界策略发现臂，固定执行器、评估器和冻结留出任务。 · [原文图](industry-rsi/assets/paper-figures/si2ca-method.png) · [仓库](https://github.com/Self-Improving-Coding-Agents/SI2CA)

- **[HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](https://arxiv.org/abs/2609.01437)**（ByteDance Seed / Singapore University of Technology and Design / Georgia Institute of Technology / M-A-P 等，2026-09-01，闭环）
  - 核心：Creation 从弱种子构建可运行框架；Evolution 根据下游执行反馈反复修改持久框架。
  - 数字：九条单次进化轨迹中，可见分数与隐藏分数的变化方向仅在 34/64 次相邻版本切换中一致（53.1%）；
  - 代码：论文与项目页公开，论文为 CC BY-NC-ND 4.0；
  - 点评：拟议 nanoRSI coding 实验：冻结每个候选版本，保留完整评分轨迹，在固定执行模型下衡量开发集与隐藏集提升方向的一致性。 · [原文图](industry-rsi/assets/paper-figures/harnessdev-figure.png)

- **[HELIX: Model-Harness Co-evolution for Recursive Self-Improvement](https://arxiv.org/abs/2608.13951)**（The University of Hong Kong，2026-08-14，闭环）
  - 核心：两个耦合时间尺度：任务内由 harness 为固定模型中介上下文、工具结果、权限与控制流；跨轮则让一组演化出的 harness（65 个候选）在同一批任务上运行，已验证的同胞轨迹成为下一代模型的更新信号（SFT、critic、filter、preference 记录），更新后模型变化的能力画像再决定下一轮 harness 重建。
  - 数字：代码修复（SWE-bench）上：最佳固定 harness 比 Pi 多 4.0% 任务覆盖；
  - 代码：代码 MIT 许可，位于 github.com/HKUDS/HELIX（LICENSE 已于 2026-10-15 核验）。
  - 点评：已验证同胞切片的思路可直接映射到 nanoRSI 的冻结面板：每次闸门尝试（无论接受与否）都产出面板轨迹，可蒸馏为训练数据而非丢弃——证据账本已在记录它们。 · [原文图](industry-rsi/assets/paper-figures/helix-harness-model-coevolution.svg) · [仓库](https://github.com/HKUDS/HELIX)

- **[Qwen3.8-Max: A New Bar for Coding and Cowork (self-evolving harness demonstrations)](https://qwen.ai/blog?id=qwen3.8)**（Alibaba (Qwen team)，2026-08-03，闭环）
  - 核心：三个长程演示，模型通过反馈回路修改自身工作基础设施：(1) 从空文件夹起用 10+ 天自主运行构建 oh-my-cli 项目，配合 issue 状态机、调度器、监控与看门狗——"需求归一化为 issue，由 agent 自动认领执行，经代码、测试、预览与日志持续迭代"；(2) 从零复现论文《Unified Data Selection for LLM Reasoning》（约 125 小时、约 7,600 行代码、33 轮 GPU 训练），再以"假设→写码→上 GPU→分析"的自改进环在四轮中自提 18 个改进想法……
  - 数字：自报结果：oh-my-cli 自主运行约 16 天累计 265 次提交、127 个 PR、151 个 issue（截至 2026 年 7 月 30 日）；
  - 代码：官方博客；
  - 点评：建议：搭建最小 issue 环路 harness，让 nanoRSI 的改进器认领、实现并验证自己仓库的 issue，在同一 issue 流上与固定计划对照比较有效 diff 产出率与回归率。 · [原文图](industry-rsi/assets/paper-figures/qwen38-max-self-evolving-harness.png) · [仓库](https://github.com/qwen-code-dev-bot/oh-my-cli)

- **[DarwinX: Evolving Agent Harnesses Through Natural Selection](https://arxiv.org/abs/2608.07545)**（Salesforce AI Research，2026-07-31，闭环）
  - 核心：Beagle 将 agent harness 作为可进化对象，提供评测／进化后端、基准原生 rollout 引擎与 agent 工厂。DarwinX 冻结模型权重，由 evolver 提议 harness 变体，经各基准验证器评分，仅接受不退化且扩展覆盖的候选，并保留替代谱系供重组。
  - 数字：作者报告 GPT-5.5 high 与 Monet 上的结果：Terminal-Bench 2.1 pass@5 从 75.5 升至 83.2（+7.7 分），TerminalWorld pass@1 从 48.8 升至 56.1（+7.3），WebArena-Infinity pass@1 从 43.5 升至 93.0（+49.5），SWE-bench Verified pass@1 从 80.8 升至 84.2（+3.4）。
  - 代码：Beagle 与官方 DarwinX 实现以 Apache-2.0 公开。
  - 点评：建议：围绕 nanoRSI 冻结评测器增加小型 population 模式，保留候选原始增量、回滚后选中增量及替代谱系元数据； · [原文图](industry-rsi/assets/paper-figures/beagle-architecture.svg) · [仓库](https://github.com/SalesforceAIResearch/Beagle)

- **[AgentDescent: Gradient descent, but the parameters are agents](https://github.com/Birfy/agentdescent)**（AgentDescent project (independent, Danyang Chen)，2026-07-26，支撑·无闭环）
  - 核心：多 worker 的自进化算法引擎：worker 并行提出对共享工件的 diff，聚合器把被接受提案合并进 git 版本化账本。策略的键空间决定并发提案能否融合——反思式合并在语义上融合，键控并集永远做不到。
  - 数字：在 BBH dyck_languages（GLM-5.2，N=4，四种子）上：反思式合并融合 48 次合并机会中的 42 次，键控并集为 0/48。
  - 代码：MIT 许可；
  - 点评：可移植的是合并策略教训：并行候选编辑同一共享工件时，键控/位置并工会静默丢弃重叠工作——候选合并需要语义（反思式）融合，融合结果应像其他被接受候选一样落入版本化账本。 · [原文图](industry-rsi/assets/paper-figures/agentdescent-architecture.png) · [仓库](https://github.com/Birfy/agentdescent)

- **[PenguinHarness: Harness for RSI. Let AI Build AI](https://github.com/Prism-Shadow/penguin-harness)**（Prism Shadow (PrismShadow AI Team, Yaowei Zheng)，2026-07-19，闭环）
  - 核心：本地优先的多智能体 auto-dev 平台（桌面应用、CLI、npm、Docker；宣称支持 1000+ 模型并以 DeepSeek 级开源模型为默认）内置自进化引擎：agent 自评自优——跑基准、找失分点、发布 N+1 版，每轮前有快照、每个请求可在 Trace 视图检查；
  - 数字：核验时为自我报告的营销级声明：数据分析最佳准确率、成本为 Claude Code 的 1/70；
  - 代码：Apache-2.0；
  - 点评：在数字可核验之前就值得借鉴其可追溯纪律：每轮自进化前做快照、每个请求可检查，使自改代理的历史可回放——与 nanoRSI 证据账本所强制的性质相同。 · [原文图](industry-rsi/assets/paper-figures/penguin-self-evolution-poster.webp) · [仓库](https://github.com/Prism-Shadow/penguin-harness)

- **[Evolving Agents in the Dark: Retrospective Harness Optimization via Self-Preference](https://arxiv.org/abs/2606.05922)**（Microsoft Research Asia / City University of Hong Kong，2026-06-04，闭环）
  - 核心：无需标注或验证反馈的 harness 优化：DPP 选出的历史任务核心集分组重解，从轨迹蒸馏诊断线索，改写全栈 harness（指令、技能、可执行工具），再由 agent 自身成对排序候选（自偏好）选 N=3 中最优。
  - 数字：Codex（GPT-5.5 high）单轮优化：SWE-Bench Pro 0.59→0.78、Terminal-Bench 2 0.71→0.76、GAIA-2 0.29→0.37；
  - 代码：MIT 代码位于 github.com/wbopan/retro-harness（核验时 56 星，最后推送 2026-06-12）。
  - 点评：nanoRSI 运行档案已存候选树； · [原文图](industry-rsi/assets/paper-figures/rho-retrospective-harness.png) · [仓库](https://github.com/wbopan/retro-harness)

- **[Combee: Scaling Prompt Learning for Self-Improving Language Model Agents](https://arxiv.org/abs/2604.04247)**（Stanford University / UC Berkeley / Tensormesh / Gradient Network，2026-04-05，支撑·无闭环）
  - 核心：并行扫描、增强洗牌机制与动态批大小控制器让多个智能体并行做提示学习并从合并轨迹中学习而不损质量——把自改进循环横向而非串行扩展。
  - 数字：在 AppWorld、Terminal-Bench、Formula、FiNER 上（头条快照为 DeepSeek-V3.1 底座），相对既有提示学习方法最高 17× 加速，精度持平或更优、成本相当。
  - 代码：arXiv 论文公开；
  - 点评：nanoRSI 种群运行已并行评测； · [原文图](industry-rsi/assets/paper-figures/combee-parallel-prompt-learning.svg)

- **[GenericAgent: A Token-Efficient Self-Evolving LLM Agent via Contextual Information Density Maximization (V1.0)](https://arxiv.org/abs/2604.17091)**（Advantage AI Agent Lab (Shenzhen Aquaintelling Technology + Fudan University)，2026-04，闭环）
  - 核心：统一智能体循环（约 3,300 行代码中核心约 92 行，比 OpenClaw 小 160 倍以上）从任务、记忆与两层技能树（类别 + 带使用计数的命名技能）构造执行上下文。课程规划器为技能候选打分（收益/难度/使用/兴趣，权重 0.3/0.2/0.3/0.2）并经反思自适应权重；
  - 数字：Lifelong AgentBench：222K 输入 token 下 100% 准确率，对 OpenClaw 1.43M 下 70%、Claude Code 800K 下 75%（约 6.4 倍 token 优势——即仓库的'6 倍'说法）。
  - 代码：代码在 github.com/lsdefine/GenericAgent（MIT，核验时 14,200 星）。
  - 点评：对 nanoRSI：证明带技能固化的极小种子环能在 token 效率上胜过百万行级 harness——nanoRSI 的纯标准库内核押注相同； · [原文图](industry-rsi/assets/paper-figures/genericagent-skill-tree.png) · [仓库](https://github.com/lsdefine/GenericAgent)

- **[MiniMax M2.7: Early Echoes of Self-Evolution](https://arxiv.org/abs/2605.26494)**（MiniMax，2026-03-18，闭环）
  - 核心：内部 M2.7 智能体分析失败轨迹，修改 scaffold 代码及采样配置，评测后保留或回滚，并用于下一轮。另一个研发流程更新记忆/技能、辅助研究员开展 RL 实验，但仍由人提供方向并作关键决策。
  - 数字：MiniMax 报告进行了超过 100 轮自主 scaffold 迭代，内部编程评测提升 30%；
  - 代码：M2.7 权重公开。
  - 点评：拟议 nanoRSI coding 实验：将修改限制在 scaffold 文件，冻结执行模型，在隐藏测试集上审计保留/回滚决策。 · [原文图](industry-rsi/assets/paper-figures/minimax-m27-self-evolution.svg) · [仓库](https://huggingface.co/MiniMaxAI/MiniMax-M2.7)

- **[Meta-Harness: End-to-End Optimization of Model Harnesses](https://arxiv.org/abs/2603.28052)**（Stanford University / MIT / KRAFTON，2026-03，闭环）
  - 核心：对任务 harness 代码的外层搜索环：编码智能体提案者（Claude Code / Opus 4.6）读取一个持续增长的文件系统——内含此前每个候选的源码、执行轨迹与分数（经 grep/cat 工具）——提议新的单文件 harness（控制提示、检索、记忆与编排），评估后把全部信息写入新目录。用精度-上下文成本的 Pareto 前沿取代硬编码父代选择；
  - 数字：TerminalBench-2（Opus 4.6）：76.4%（Opus-4.6 智能体中排名第二；
  - 代码：项目页 yoonholee.com/meta-harness；
  - 点评：对 nanoRSI：把每个候选的完整轨迹（而非摘要）存入提案者可查询的存储——消融表明让 harness 搜索奏效的是轨迹访问本身，而非选择策略的精巧。 · [原文图](industry-rsi/assets/paper-figures/stanford-meta-harness.png) · [仓库](https://github.com/stanford-iris-lab/meta-harness-tbench2-artifact)

### 自改写元智能体与谱系（14）

- **[RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent](https://arxiv.org/abs/2610.21791)**（Beihang University，2026-10-15，闭环）
  - 核心：任务智能体（Qwen3-4B/8B）执行任务并收集轨迹与环境反馈；元智能体（GPT-5.6 Sol）诊断当前瓶颈部件，自适应选择部件专属的改进工作流——模型更新（固定单 epoch 超参与全局批 8 的局部 LoRA）、harness 更新或任务产物修订。
  - 数字：六基准（HumanEval+、MBPP+、BFCL-v3、ACEBench、HotpotQA、2Wiki）总体均值：Qwen3-4B 51.21 对 SIA 45.15、Hyperagent 41.26、AFlow 40.73（另 SFT 41.12、GRPO 42.04、HarnessForge 41.22、MermaidFlow 43.59）；
  - 代码：代码 MIT 许可，位于 github.com/1HUAN1/RSI-Flow（2026-10-18 经 API 核验许可）。
  - 点评：瓶颈诊断路由是 nanoRSI 主循环的一种选择器设计：先分类哪个面（技能文本、harness 代码、评测器产物）是约束瓶颈，再施加该面专属算子，而不是把尝试预算花在错误面上。 · [原文图](industry-rsi/assets/paper-figures/rsiflow-evolving-meta-agent-fig2.png) · [仓库](https://github.com/1HUAN1/RSI-Flow)

- **[MetaShare: Failure-Aware Collective Self-Improvement for Open-Ended Agents](https://arxiv.org/abs/2610.21887)**（PricewaterhouseCoopers (PwC)，2026-10-15，闭环）
  - 核心：每次被评测的智能体修改都成为一条带符号的记录（有帮助→复用，有损害→规避），存入有界的跨谱系池。每代生成前，失败感知的多样性检索重建“采纳/规避/必试”引导上下文；
  - 数字：对 DGM-H（五次运行取中位数、95% bootstrap 置信区间）：论文评审 0.71→0.79、Polyglot 全量 225 任务 0.28→0.34、机器人奖励设计 0.37→0.40、三个 IMO 评分设置 0.61/0.64/0.60→0.64/0.70/0.67、审计风险 0.45→0.55，同时最优检查点出现代数下降 1.7–2.9 倍（论文评审 100→36、审计风险 44→26）。
  - 代码：论文未链接代码仓库；
  - 点评：带打乱失败对照的符号化失败账本可直接移植到 nanoRSI 的 rejected_recent 池：按提案存储带符号增益，引导提案器时作为规避信号检索，并跑长度匹配的打乱拒绝对照臂，证明账本承载语义而非 token； · [原文图](industry-rsi/assets/paper-figures/metashare-architecture.png)

- **[Drafting Agents, Not Just Tokens: Speculative Recursive Self-Improvement for Agentic Systems](https://arxiv.org/abs/2610.16491)**（Tencent AMS / Peking University / Beihang University / Xiaohongshu 等，2026-10-12，闭环）
  - 核心：把投机执行引入递归自改进：在父代验证完成前就起草可执行的子代 agent，长出一棵由冻结版本与编辑边组成的不可变树；采纳仍要求完整、可采纳的验证。
  - 数字：科学赛道：50 个骨干-任务对全胜 Janus，终局增益 +33.3-40.0%、AUBC +30.4-33.7%（逐对提升 17.8-27.6%）。
  - 代码：代码 MIT 许可，位于 github.com/SpecRSI-GPR/SpecRSI（LICENSE 已于 2026-10-15 核验）。
  - 点评：两个可迁移件：(1) 只认完整验证的投机起草是 nanoRSI 尝试循环的预算策略——当前提案面板未跑完就先起草下一个，但绝不在部分证据上晋升； · [原文图](industry-rsi/assets/paper-figures/specrsi-speculative-rsi.png) · [仓库](https://github.com/SpecRSI-GPR/SpecRSI)

- **[RSI-Anything: Unlocking Recursive Self-Improvement with World Models](https://arxiv.org/abs/2610.13912)**（PhAI Labs / The Chinese University of Hong Kong / University of Macau / Shanghai Jiao Tong University 等，2026-10-09，闭环）
  - 核心：构建在 JEPA-Anything 预测基座上，世界模型预测同时引导动作选择与学习数据选择，替代昂贵的外部反馈。观测到的反馈更新策略/工作流；
  - 数字：代码修复（200 道 CodeContests、固定 coder）：隐藏测试成功率 26.3%（静态验证器）/ 26.0%（随机选择）→ 29.2%（固定世界模型）→ 31.2%（世界模型适配后）；
  - 代码：代码：github.com/Gen-Verse/RSI-Anything，Apache-2.0（核验时 571 星；
  - 点评：对自生成训练数据的分层证据准入闸（E0-E3 标签加合法性、效用与不确定度检查）是 nanoRSI 反事实面板纪律的具体 schema； · [原文图](industry-rsi/assets/paper-figures/rsi-anything-world-model-rsi.png) · [仓库](https://github.com/Gen-Verse/RSI-Anything)

- **[AgentEvolver: System-Wide Self-Evolution Through Task Execution](https://arxiv.org/abs/2610.11613)**（Nanyang Technological University / Singapore Management University，2026-10-08，闭环）
  - 核心：在任务执行过程中、基础模型不变的前提下构建能力：八个实体族（操作、方法、agent、控制流、接口与支撑状态等）把各自组件交给统一的带版本生命周期——结构准入、功能评估、随后激活。共享 Runtime 协调任务编排、持久规划与可恢复上下文，版本管理把每次评估过的变更链接到它所进入的生效能力集。
  - 数字：在 SWE-bench Pro Public 上，系统报告开启演化后解决率 82.08%，高于其自身未演化基线（作者对照；
  - 代码：代码：github.com/DVampire/AgentEvolver，MIT 许可（经 raw LICENSE 核验）。
  - 点评：逐实体带版本生命周期的设计是 nanoRSI 技能轨的具体模式：给每个被编辑产物（技能文件、runner、评测器配置）同一套准入->评估->激活生命周期并把版本链接写入证据账本，使能力可回溯到产生它的变更——把 nanoRSI 已对接受代数做的审计延伸到激活一步。 · [原文图](industry-rsi/assets/paper-figures/agentevolver-architecture.png) · [仓库](https://github.com/DVampire/AgentEvolver)

- **[SoL-Pi: Recursively Scaling Auto-Research Loops for Efficient Agent Harness](https://arxiv.org/abs/2609.20519)**（NVIDIA / Nanyang Technological University / MIT，2026-09-17，闭环）
  - 核心：受 RSI 启发的自动研究循环递归改进 agent harness 本身：研究 AI 从执行轨迹提出 harness 机制，agent 种群并行探索候选并独立评审，只有通过留出验证的机制被保留（EdgeBench 始终不进搜索）——最终保留四个机制。
  - 数字：在 51 任务 EdgeBench 上，SoL-Pi 在 GPT-5.6 Sol 与 Opus 5 下性能与 Pi 持平，token 流量降 44.7-49.0%、API 成本约降三分之一；
  - 代码：MIT 代码位于 github.com/NVlabs/SoL-Pi（核验时 2,244 星）与项目页 nvlabs.github.io/SoL-Pi/。
  - 点评：仓库衍生搜索环境与永不触碰的留出基准之间的硬隔离，加上机制保留前的独立评审闸门，可直接移植到 nanoRSI 种群运行。 · [原文图](industry-rsi/assets/paper-figures/solpi-recursive-autoresearch-loops.png) · [仓库](https://github.com/NVlabs/SoL-Pi)

- **[Self Improvement via Fast Tree-search](https://arxiv.org/abs/2609.19526)**（MIT / Sakana AI，2026-09-17，闭环）
  - 核心：编码智能体在树搜索中递归修改自身实现。SIFT 在该循环内加入廉价监督信号：LLM 裁判对候选补丁与历史版本做两两比较，胜负记录经正则化 Bradley-Terry 模型聚合为强度分数，并按排名进行父节点采样使扩展偏向更强节点；
  - 数字：作者报告的完整 Polyglot 基准结果：o3-mini 智能体加 gpt-5.4 裁判的 SIFT 达 35.1%，对照 DGM（o3-mini）30.7%、基础智能体 14.2%；
  - 代码：代码：核验的摘要与 HTML 页面未发现仓库链接。
  - 点评：可移植部分是廉价预闸门：用两两 LLM 裁判比较加 Bradley-Terry 聚合，在任何完整面板评测前对提案做低成本排序，并与完整评测闸门显式对照，记录误准入/误拦截与裁判成本。 · [原文图](industry-rsi/assets/paper-figures/sift-tree-search-pipeline.png)

- **[Refactoring Hermes with 1,393 agents](https://nousresearch.com/refactoring-hermes-with-1393-agents/)**（Nous Research，2026-09-15，闭环）
  - 核心：人类下达 /goal 后，Hermes 编排器把自家约 106 万行仓库切成 36 组，派出工作子智能体在独立 git worktree 中编辑并做接口校验（JSON schema、逐字节一致的 CLI --help）；经验教训自动写入 hermes-agent-dev Markdown 技能并再共享，让其他智能体继承已学流程。
  - 数字：1,393 个子智能体（峰值并发 218）、约 19 个活跃小时、主运行约 1.93 万美元（人工估算 15 万-180 万）；
  - 代码：博文公开；
  - 点评：nanoRSI 已有每候选 worktree 评测； · [原文图](industry-rsi/assets/paper-figures/nous-hermes-selfrefactor.png) · [仓库](https://github.com/NousResearch/hermes-agent)

- **[Mendel Gödel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution](https://arxiv.org/abs/2608.07645)**（University of Electronic Science and Technology of China / Ludwig Maximilian University of Munich / Munich Center for Machine Learning，2026-08，闭环）
  - 核心：在档案式自修改（DGM/HGM）上加入三个由比较证据驱动的孟德尔算子：克隆变异（单轨迹编辑）、反应规范变异（用同一智能体跨多任务的轨迹编辑——复现失败标记基因型缺陷）、跨谱系杂交（从另一谱系的成功轨迹提取可迁移行为性状并适配，不拼接代码）。失败任务池提高采样权重使谱系在难题上重叠。
  - 数字：Qwen3.6-35B-A3B、200 次评估 + 24 次扩展：SWE-bench Verified-60 68.3% -> 78.3%（HGM 73.3%）；
  - 代码：代码在 github.com/RealLcz/MGM（Apache-2.0，核验时 32 星）；
  - 点评：对 nanoRSI：按谱系保存逐任务轨迹，并允许由跨任务复现失败（反应规范）与其他候选在共享任务上的成功（杂交）驱动的编辑——都是候选分数之外的选择信号。 · [原文图](industry-rsi/assets/paper-figures/mgm-mendel-godel-machine.png) · [仓库](https://github.com/RealLcz/MGM)

- **[Meta^n: Recursive Self-Improvement through Emergent Depth](https://arxiv.org/abs/2608.24735)**（University of Minnesota / Seoul National University，2026-08，闭环）
  - 核心：单一固定的元操作 Omega 反复作用于自身输出：每次调用读取下层的轨迹与（自第 3 层起）其产出的代码，再写出下一层代码（预处理器 + 代码库）；包装器复合成 Sd = Md o ... o M2 o S1。
  - 数字：八个基准家族上实测元深度 3-6（平台期 3-4；
  - 代码：代码在 github.com/minnesotanlp/meta-n（MIT，核验时 29 星）。
  - 点评：对 nanoRSI：把'实测元深度'（在平台期前真正有效的嵌套改进层数）作为标准报告字段——Meta^n 证明它可测量，而自改写环要打败的基线约为 2.5。 · [原文图](industry-rsi/assets/paper-figures/metan-emergent-depth.png) · [仓库](https://github.com/minnesotanlp/meta-n)

- **[AIDE²: The First Evidence of Recursive Self-Improvement](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement)**（Weco AI，2026-07-14，闭环）
  - 核心：双层循环：外环智能体改写内环研究智能体的代码；每个候选在固定的逐任务预算下跨异构 AI 研发任务族评测，并在接受前把留出分数汇总为私有等级。
  - 数字：一次 8 天无人值守运行接受了 7 次重写，私有选择等级从 0.703 提升到 0.778。
  - 代码：论文与原始图：已由 arXiv:2609.26457 公开。
  - 点评：把 AIDE² 作为既有 RRSI 选择器研究的协议参照：固定内层任务预算，把公开反馈与留出接受等级分开，并报告完整的接受／拒绝谱系。 · [原文图](industry-rsi/assets/paper-figures/weco-aide2-paper-figure1.png) · [仓库](https://github.com/WecoAI/aideml)

- **[Hyperagents](https://arxiv.org/abs/2603.19461)**（Meta / University of British Columbia，2026-03-19，闭环）
  - 核心：可编辑的元智能体修改自身及任务智能体；经评价的有效变体进入档案，作为后续父代和反馈来源，入库不要求立即提高分数。
  - 数字：100轮后，论文评审保留集准确率为0.710（置信区间0.590–0.750），静态基线为0.630、定制DGM为0.590。
  - 代码：已确认官方代码及实验日志链接；
  - 点评：建议实验：分别管理任务代码和元代码版本，保留已评价的中间变体及不可变评价记录。 · [原文图](industry-rsi/assets/paper-figures/meta-hyperagents-2026.png) · [仓库](https://github.com/facebookresearch/HyperAgents)

- **[Group-Evolving Agents: Open-Ended Self-Improvement via Experience Sharing](https://arxiv.org/abs/2602.04837)**（University of California, Santa Barbara，2026-02-04，闭环）
  - 核心：把整个 agent 群体而非单一谱系作为进化单元：自改进 agent 自主改写自身架构，群内成员在开放式演化中共享复用经验，使早期探索多样性得以保留而非损失在孤立的树分支里。最佳 agent 整合来自多个不同祖先的经验。
  - 数字：SWE-bench Verified 71.0% 对最强自演化基线 DGM 56.7%；
  - 代码：未发布代码、权重或数据；
  - 点评：群体级经验共享是对 nanoRSI rejected_recent 隔离的反向设计：失败候选的诊断轨迹可以共享给后续提案而非只做压制； · [原文图](industry-rsi/assets/paper-figures/gea-group-evolution-sharing.png)

- **[Huxley-Gödel Machine: Human-Level Coding Agent Development by an Approximation of the Optimal Self-Improving Machine](https://arxiv.org/abs/2510.21614)**（King Abdullah University of Science and Technology (KAUST)，2025-10-24，闭环）
  - 核心：编码 agent 编辑自身代码库，构建自修改树。论文识别出'元生产力-性能失配'——agent 的基准分数并不可靠指示其产出更强后代的能力——并提出 CMP（Clade Meta Productivity）：聚合一个 agent 全部后代的基准表现作为自改进潜力的指标。
  - 数字：SWE-Verified-60（800 次评估、best-belief agent）：HGM 56.7（+16.7）对 DGM 53.3（+13.3）与 SICA 50.0（+10），CPU 时耗 517 小时对 DGM 1231（省 2.38 倍）；
  - 代码：代码 Apache-2.0，位于 github.com/metauto-ai/HGM（LICENSE 已于 2026-10-15 核验）。
  - 点评：CMP 是 ADOPTION 第 38/39 项可实现的竞争选型器：按后代的聚合冻结面板表现（而非父代自身分数）给父代排名，可从既有 lineage store 直接计算、无需新增模型调用。 · [原文图](industry-rsi/assets/paper-figures/huxley-godel-cmp-steering.svg) · [仓库](https://github.com/metauto-ai/HGM)

### 经验积累与回放（12）

- **[Hippo: Training-Free Agent Self-Evolution via Hippocampal Replay](https://arxiv.org/abs/2610.24453)**（University of California, Irvine / Rice University / Zillow Group，2026-10-20，闭环）
  - 核心：显式以递归自改进为动机、经外部记忆的选择性编码与重放实现免训练自我演化。通过比较同任务多次尝试识别可复用决策并精炼其适用条件（错误推理可能碰巧成功；
  - 数字：在 SWE-bench Verified、WebArena、Mind2Web 上取得增益，且保留的经验条目远少于累积基线；
  - 代码：核验时论文未给出代码仓库；
  - 点评：用于技能/记忆线：把只增不减的教训清单换成显式适用条件下的就地修订巩固； · [原文图](industry-rsi/assets/paper-figures/hippo-overview.png)

- **[Darwin-Claw: Environment-Adaptive Experience Consolidation for Recursively Self-Evolving Agents](https://arxiv.org/abs/2610.23574)**（Zhejiang University / Tencent / Zhongguancun Academy，2026-10-19，闭环）
  - 核心：层次化经验巩固系统从用户交互轨迹提取细粒度错误归因，泛化为动态更新的环境原型向量；巩固后的情境经验被两用——作为交互补丁注入以增强上下文感知，并作为显式优化信号在 Externalized 演化生命周期（因果验证与多维评分闸门）下精炼操作技能与持久记忆。
  - 数字：WildClawBench（60 条人写的长程多模态任务、六类）：较无演化基线平均 +24.1 个百分点，网页 +27.3、工具 +31.6、推理密集 +22.7、长程 +23.8；
  - 代码：论文 HTML 中未发现仓库链接（2026-10-20 核验）；
  - 点评：先聚类错误归因再落盘：nanoRSI 可对每次失败尝试的归因向量分类，路由到技能文件编辑、记忆追加或丢弃——这是对“逢败必改技能”的结构化替代，可在 counterfactual 面板上检验。 · [原文图](industry-rsi/assets/paper-figures/darwinclaw-framework.png)

- **[Reflect After Failure: Brain-Inspired Self-Evolving Agents for Embodied Spatial Intelligence](https://arxiv.org/abs/2610.20312)**（City University of Hong Kong / East China Normal University / University of Electronic Science and Technology of China / The Chinese University of Hong Kong, Shenzhen 等，2026-10-14，闭环）
  - 核心：受脑启发的具身空间任务自进化智能体。海马-元认知反思在感知-探索-规划三轴上诊断失败——执行反馈本身很少揭示哪个环节负责，单纯堆积经验反而会强化无效策略。
  - 数字：在具身空间基准上提升成功率并具泛化性（据摘要；
  - 代码：HTML 全文未找到代码或仓库链接。
  - 点评：记忆沉淀前先做感知/探索/规划三轴归因，是我们“提案问题还是评测问题”归因的具身版：只有定位到失效环节后才写反思，否则累积的技能会强化错误修复。 · [原文图](industry-rsi/assets/paper-figures/himeco-hippocampal-metacognitive.png)

- **[Reliable Memory from Unstable Growth: Curating Self-Written Agent Playbooks with Randomized Experiments](https://arxiv.org/abs/2610.18427)**（Nanyang Technological University / VinUniversity，2026-10-13，闭环）
  - 核心：把自写手册当实验对象而非文本：经验条目嵌入后 Ward 聚类成 m=8 个主题块；练习任务上每块以 p=1/2 独立入选（二水平因子设计），对成功指示符做岭回归估计每块效应——恰等于其在随机共服务子集上的 Banzhaf 值。
  - 数字：2 个记忆系统（ACE、Dynamic Cheatsheet）×3 模型（Qwen3.8-27B、Qwen3.5-9B、Gemma-4-31B）×3 基准（AppWorld、WebShop、ALFWorld）：RBC 平均 66.9，对完整手册 55.5、无手册 54.1、agent 自选 53.8。
  - 代码：匿名代码位于 anonymous.4open.science/r/rbc（评审期工件）。
  - 点评：RBC 是 ADOPTION 第 48 项'每技能效用账本'的可插拔因果升级：不记检索相关性效用，而是测量每技能块在冻结面板局上的随机开/关效应（Banzhaf/岭回归估计只需 nanoRSI 已记录的入选指示与结果），按符号而非感觉退役或保留技能块。 · [原文图](industry-rsi/assets/paper-figures/rbc-randomized-block-curation.svg)

- **[Recurrent Harness for Agentic Continual Learning](https://arxiv.org/abs/2610.12668)**（Meta / Massachusetts Institute of Technology / Yale University，2026-10-08，闭环）
  - 核心：harness 状态是从历史轨迹写出的文本反思集合。常规有状态 harness 只向前传播（写反思、检索反思），一条过度泛化的反思会持续误导后续实例。
  - 数字：在 CL-Bench、MemoryBench、MemoryArena × Claude Opus 4.8、GPT-5.5、Gemini 3.7 Flash 上平均归一化增益 0.240，9 个组合中 8 个最佳或并列最佳，对照 Top-K Raw 0.168、Full Raw 0.164、GEPA-Online 0.092、Mem0 0.131、DoT 0.071、ACE 0.043、RBank 0.034；
  - 代码：未发布代码或数据（arXiv 页与 HTML 均无链接）。
  - 点评：锚定源轨迹的反向修订可映射到 nanoRSI 技能轨：被拒候选应修订它实际使用的那条技能，修订内容限定在失败证据内——该锚定约束与反事实面板的反捷径纪律同源； · [原文图](industry-rsi/assets/paper-figures/reharness-recurrent-harness.svg)

- **[EchoPath: Execution-Level Replayable Memory for GUI Agents](https://arxiv.org/abs/2609.16635)**（Johns Hopkins University / Amazon AGI，2026-09-15，闭环）
  - 核心：经验证的 GUI 轨迹被编译为标准化、参数可控的可调用记忆（任务意图键、前置条件、参数、GUI 证据、验证出处、生命周期状态）。基于图像的目标重瞄算法在回放前把存储的 GUI 目标与当前屏幕重新匹配并校正坐标，只重绑定声明的可变输入。
  - 数字：OSWorld-Verified 配对两遍设计（第二遍在改变分辨率后回放）：回放保持成功率——Codex 145/159（91.2%）、Claude 92.8%、Kimi 87.3%，与 Synapse 规划增强基线（91.8%）相当。
  - 代码：论文所列仓库 github.com/JackZhao1998/EchoPath 已在 2026-09-17 至 2026-09-19 间删除（API 404 且无重定向，非改名）；
  - 点评：对 nanoRSI：把执行级技能存为自带验证出处与生命周期状态的可调用记忆，检索只暴露活跃项——回放即可用十分之一 token 换取大部分收益。 · [原文图](industry-rsi/assets/paper-figures/echopath-replayable-memory.png)

- **[Chain-of-Experience for Continual LLM Improvement](https://arxiv.org/abs/2608.18027)**（ByteDance Seed / UC Santa Cruz，2026-08-18，闭环）
  - 核心：测试时经验学习：模型不再单轮推理，而是在迭代解题中累积自身经验轨迹（提问、尝试、正确性或测试通过反馈），这些轨迹供后续尝试使用，形成经验链（CoE）。研究比较了反馈来源（自我反馈与环境反馈）、通道组合以及保留策略，包括刻意保留"混乱"的失败轨迹。
  - 数字：在八个 LLM（含 GPT-5、Gemini-2.5 Pro、Claude-4.5 Sonnet）的数学/代码/知识任务上，迭代经验相对无反馈基线整体提升 5.6%，同时 API 成本降低 19%；
  - 代码：arXiv（CC BY 4.0）；
  - 点评：建议：在 nanoRSI 的数字/编程任务上，在固定 token 预算下比较单通道执行反馈与自我+环境反馈组合，并检验保留失败轨迹（而非只留成功）是否改变隐藏集准确率。 · [原文图](industry-rsi/assets/paper-figures/bytedance-chain-of-experience.png)

- **[Prime Agent: A Self-Improving RLM Harness](https://arxiv.org/abs/2608.23552)**（Prime Intellect / Princeton University / MIT，2026-08-05，闭环）
  - 核心：轨迹触发的改进修改持久化补充提示、技能、记忆和子智能体配置。磁盘持久化与回滚历史支持跨轨迹复用，基础系统提示保持不可修改。
  - 数字：Sonnet 5 的七天 Factorio 运行完成了 196 项技术中的 24 项，使用 2,340 万输出 token；
  - 代码：已确认官方代码，MIT 许可；
  - 点评：建议：将不可修改的评测器及基础策略，与版本化记忆更新分离，并记录来源及支持回滚。 · [原文图](industry-rsi/assets/paper-figures/prime-agent-figure.png) · [仓库](https://github.com/PrimeIntellect-ai/prime-agent)

- **[SimpleMem: Efficient Lifelong Memory for LLM Agents](https://arxiv.org/abs/2601.02553)**（University of North Carolina at Chapel Hill / UC Berkeley / UC Santa Cruz，2026-01-05，支撑·无闭环）
  - 核心：终身记忆三段流水线：语义结构化压缩过滤低效用对话、在线语义合成做巩固、检索时按意图规划多视图查询——替代全文上下文或迭代过滤。
  - 数字：GPT-4.1-mini 在 LoCoMo：平均 F1 43.24 vs Mem0 34.20、全文上下文 18.70，每次查询仅 531 token（约为全文/MemGPT 16,910 的 1/30）；
  - 代码：MIT 代码位于 github.com/aiming-lab/SimpleMem（核验时 3.8k 星）。
  - 点评：先压缩再巩固的两段式是 nanoRSI 技能记忆的 token 预算杠杆：写入时过滤低效用轨迹、周期性巩固、按意图检索。 · [原文图](industry-rsi/assets/paper-figures/simplemem-lifelong-memory.png) · [仓库](https://github.com/aiming-lab/SimpleMem)

- **[Continual Learning, Not Training: Online Adaptation for Agents](https://arxiv.org/abs/2511.01093)**（Arc Intelligence，2025-11-02，闭环）
  - 核心：双智能体免梯度推理期适应：教师（GPT-5）审查学生（GPT-5-mini）的轨迹并给原则级纠正；编排器把轨迹、指引与裁判集奖励分存入持久学习记忆，蒸馏成教师手册（原则、失败模式、停止条件）与学生手册（动作模式、工具计划、防护），按任务上下文检索以调节监督力度与种子计划——全程无权重更新。
  - 数字：ExCyTIn-Bench 事件 #5（n=98）：ATLAS 成功率 54.1% 对 GPT-5（High）的 48.0%（+6.1），成本低约 86%（每题 0.024 对 0.174 美元），token 较学生基线降 45%；
  - 代码：代码在 github.com/Arc-Computer/atlas-sdk（17 星，核验时未检出许可证文件）；
  - 点评：对 nanoRSI：双层蒸馏指引（给批评者的原则层、给执行者的模式层）加监督力度调节，是单体记忆的轻量替代——且手册可干净冻结做迁移测试。 · [原文图](industry-rsi/assets/paper-figures/atlas-pamphlets.png) · [仓库](https://github.com/Arc-Computer/atlas-sdk)

- **[Training-Free Group Relative Policy Optimization](https://arxiv.org/abs/2510.08191)**（Tencent Youtu Lab / Fudan University / Xiamen University，2025-10-09，闭环）
  - 核心：冻结的基础模型生成分组 rollout，将语义优势蒸馏到会演化的经验库和 token 先验中，再通过上下文回馈而非梯度更新。多个 epoch 共享累积经验，参数保持不变但后续输出分布发生变化。
  - 数字：在 DeepSeek-V3.1-Terminus 上，直接提示的 AIME24 从 68.6 提升到 72.6（+4.0），AIME25 从 52.9 到 54.0（+1.1）；
  - 代码：TencentCloudADP/youtu-agent 发布 training_free_GRPO 分支和示例；
  - 点评：为 nanoRSI 记忆实验增加冻结模型对照：在相同分组数量下比较无经验库、固定经验库和递归刷新经验，并记录 token 成本、过时建议和隐藏集迁移。 · [原文图](industry-rsi/assets/paper-figures/tencent-training-free-grpo.png) · [仓库](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO)

- **[SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents](https://arxiv.org/abs/2508.02085)**（StepFun / Tsinghua University / Huazhong Agricultural University，2025-08-04，闭环）
  - 核心：轨迹级自进化：智能体经三种操作迭代重访早前解轨迹——修订、重组、精炼——利用逐步搜索（MCTS 式）忽略的跨轨迹启发，把搜索空间扩到局部最优之外，并把改进策略持久化给后续问题。
  - 数字：SWE-bench Verified、五个 LLM：相对改进最高 55%，v6 时开源智能体中最优（摘要口径；
  - 代码：代码在 github.com/JARVIS-Xs/SE-Agent。
  - 点评：对 nanoRSI：对已存轨迹做修订/重组/精炼是运行档案的廉价二次利用——生成新候选前，先挖掘过往尝试的跨轨迹重组。 · [原文图](industry-rsi/assets/paper-figures/se-agent-trajectory.png) · [仓库](https://github.com/JARVIS-Xs/SE-Agent)

### 程序进化与进化搜索（10）

- **[A Self-Improving Agent that Grows its Own DSL: Oracle-Free Operator Induction for Exact Question Answering](https://arxiv.org/abs/2610.20809)**（PayPal AI，2026-10-14，闭环）
  - 核心：单一冻结模型在小而精确的 DSL 上跑双层循环：无奖励、无裁判、无答案钥匙。内层在固定算子库内扩张可答问题集：每条候选表达式必须由第二次独立重写的表达式在全部验证记录上一致才保留。
  - 数字：可答集增长：Merchant 10→336、BookSQL 15→162、EHRSQL（MIMIC-III）13→248；
  - 代码：论文承诺补充材料（DSL 及其测试、两个代理循环的完整提示词、生成与研究脚本）；
  - 点评：精确任务上无 oracle 闸门的范本：双独立实现加守恒律替代留出标签，可直接用于 nanoRSI 有可验证不变量但无金标面板的场景。 · [原文图](industry-rsi/assets/paper-figures/self-dsl-oracle-free-operators-fig1.png)

- **[LAGO: Language Agents with Reusable Growing Options](https://arxiv.org/abs/2610.19843)**（Shenzhen University / University of Hong Kong / Hunan University / National University of Singapore 等，2026-10-14，闭环）
  - 核心：把专门化语言智能体当作可复用的时间扩展选项：元智能体从持久库检索选项或新生选项、派发子任务、验证结果、把成功的新选项准入库；库跨任务增长而不更新模型权重。
  - 数字：在 500 个 SWE-bench Verified 任务上以官方 Docker 评测器单次尝试评测，冻结 Qwen3.5-35B-A3B 同时担任元智能体与选项角色解决 58.6%。
  - 代码：HTML 全文未找到代码或仓库链接。
  - 点评：选项准入（生成→验证→准入→复用）正是技能模板可以镜像的库增长环：经验证的子智能体程序成为一等可复用单元而非一次性轨迹。 · [原文图](industry-rsi/assets/paper-figures/lago-growing-options.png)

- **[EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution](https://arxiv.org/abs/2610.12086)**（King Abdullah University of Science and Technology / Sakana AI，2026-10-08，支撑·无闭环）
  - 核心：EvoAlloc 学习在 LLM 程序演化中分配评测算力：一个分配智能体决定哪些候选获得完整评测，其策略通过把历史搜索与分配结果巩固为可复用经验来修订，并以反事实探索偶尔评测曾被拒绝资源的候选、揭示其结果以充实后续策略更新。被改变的对象是搜索循环内分配器的策略/经验状态，不是模型权重。
  - 数字：作者报告的跨编码与智能体 harness 优化基准（附录含 ADAS-AIME 与 circle-packing 设置）结果：达到基线水平性能所需完整评测减少 59-82%、总 LLM token 减少 61-89%；
  - 代码：代码：核验的摘要与 HTML 页面未发现仓库链接。
  - 点评：对 nanoRSI 有界评测预算的两个可移植方向：(1) 经验更新的分配器决定哪些候选提案进入完整面板评测，在匹配总 token 与评测次数下与固定轮转对照； · [原文图](industry-rsi/assets/paper-figures/evoalloc-allocation-loop.png)

- **[AGAR: a reinforcement learning substrate for LLM program evolution](https://arxiv.org/abs/2610.09215)**（University of the Chinese Academy of Sciences / Baidu / Tsinghua University / Institute of Automation, Chinese Academy of Sciences 等，2026-10-06，闭环）
  - 核心：把 LLM 程序演化形式化为马尔可夫决策过程，其动作是模型被条件化的模块化前缀而非它输出的程序。常见循环里五个手设常量——父代选择、变异强度、多样性保持、记忆、以及不分部件归因的标量分数——分别替换为挂接到不同组件的 RL 估计器（信用分配、价值估计、自适应探索、经验记忆）。
  - 数字：19 个任务、两个后端（DeepSeek-V4-Flash、GLM-5.2）、三个种子、同一 harness 下，逐任务归一化的同预算最优分数：DeepSeek-V4-Flash 后端 OpenEvolve 0.855+-0.193、ShinkaEvolve 0.919+-0.138、AGAR-Base 0.949+-0.107、AGAR-Combo 0.990+-0.024；
  - 代码：代码：arXiv 页与 HTML 中均未找到（正文中的 GitHub 链接指向 OpenEvolve、slime 等既有系统而非 AGAR）。
  - 点评：对 nanoRSI 可直接移植的思路是逐机制可审计性：把演化循环的选择器、变异强度、多样性与记忆拆成可独立开关的组件，在同一 harness 下报告每个迁移估计器逐一关闭的消融，而不是整体移植框架。 · [原文图](industry-rsi/assets/paper-figures/agar-framework-mdp.png)

- **[Compiled Agency: Frontier General-Purpose Coding Agents Build Winning Game Players from Bare Interaction - from Flappy Bird to StarCraft II and Civilization](https://arxiv.org/abs/2609.18996)**（New York University / Princeton University，2026-09-17，支撑·无闭环）
  - 核心：Gauntlet 是开发-冻结-评测框架：通用编码代理只拿到游戏描述、原始观测/动作接口和一份空策略文件——不给策略、算法或架构。在单次自主会话中与真实游戏交互试错并写出独立控制器，随后冻结并在保留实例上评测，游玩期间零模型调用。
  - 数字：在一个未公开的程序化 roguelike 上，保留集成功率跨度 0–86%，并呈现清晰的代际门槛：最新一代系统的每个观测会话都胜过上一代的最佳会话。
  - 代码：核验时未找到代码；
  - 点评：冻结后评测的契约可直接映射到 nanoRSI 终测：候选冻结后，评测必须在保留种子上零额外模型调用运行，任何运行时自改都会作为契约违例显形。 · [原文图](industry-rsi/assets/paper-figures/compiled-agency-gauntlet.png)

- **[Dream-RSI: Recursive Self-Improvement through Evolving Worlds](https://arxiv.org/abs/2609.14858)**（University of Maryland, College Park / Google DeepMind / University of Virginia，2026-09-14，闭环）
  - 核心：发现历史被组织成树，节点存每次尝试的工作区、工件、诊断与得分；这棵树成为回放模拟器——备选探索策略以不同顺序、并行分组与停止点'导航'已记录分支，无需重跑底层智能体。
  - 数字：算法工程（Lasso、6 个留出数据集）：Gemini-3.1-Pro 下 Dream-RSI 以 317 次调用达均值 2,931ms，对固定探索 550 次的 3,587ms；
  - 代码：代码在 github.com/zhengkid/Dream-RSI（172 星，核验时无许可证文件）；
  - 点评：对 nanoRSI：把运行档案复用为免费模拟器——在花费任何新评估之前，让备选提案/调度策略在已记录的候选树上回放打分； · [原文图](industry-rsi/assets/paper-figures/dream-rsi-replay-simulator.png) · [仓库](https://github.com/zhengkid/Dream-RSI)

- **[AlgoEvo: Self-Evolving Agentic Search for Automated Algorithm Discovery](https://arxiv.org/abs/2609.15820)**（City University of Hong Kong / Huawei Noah's Ark Lab / A*STAR，2026-09-14，闭环）
  - 核心：自治智能体依据运行时反馈检视、诊断并编辑算法代码，而非执行固定搜索管线。设计技能中心把范式专属知识外置为可插拔技能（策略角色、代码接口、修改原则、评测约定），使单一引擎覆盖单目标、多目标与多组件设计；
  - 数字：在六个任务（TSP、CVRP、Bi-TSP、Bi-FJSP、CVRP-DR、FJSP 4-Ops）上匹配或超越专用基线（EoH、ReEvo、MCTS-AHD、FunSearch、MEoH、MOTIF、E2OC 等）：TSP 最优结果仅约 39 次评估（配额 500）与 290 万 token（FunSearch 320 万）；
  - 代码：核验时未找到公开仓库；
  - 点评：对 nanoRSI：可复用技能只有在两个及以上任务验证后才升格； · [原文图](industry-rsi/assets/paper-figures/algoevo-skill-hub.png)

- **[EvoPolicyGym: Evaluating Autonomous Policy Evolution in Interactive Environments](https://arxiv.org/abs/2607.02440)**（University of Science and Technology of China / The Chinese University of Hong Kong / University of Macau / Tsinghua University 等，2026-07-02，支撑·无闭环）
  - 核心：评测'策略即代码'进化的基准而非训练方法：固定 Gymnasium 风格环境（MiniGrid、Box2D、MuJoCo 族）；智能体在工作区反复编辑可执行 Python'策略系统'，提交训练 rollout（总计至多 128 回合）并获服务器中介反馈；
  - 数字：Core16 留出归一化回报：GPT-5.5（Codex）0.891、9 胜且 16 环境全进前二；
  - 代码：代码在 github.com/Linzwcs/EvoPolicyGym（MIT，核验时 176 星）；
  - 点评：对 nanoRSI：现成的工件轨评分协议——服务端隐藏验证检查点 + 留出回合 + 硬回合预算，并在账本中区分综合与调参编辑。 · [原文图](industry-rsi/assets/paper-figures/evopolicygym-framework.png) · [仓库](https://github.com/Linzwcs/EvoPolicyGym)

- **[WebAggregator: Enhancing Compositional Reasoning Capabilities of Deep Research Agent Foundation Models](https://arxiv.org/abs/2510.14438)**（Tencent AI Lab / The Chinese University of Hong Kong，2025-10-16，闭环）
  - 核心：在线探索器访问网页，组合逻辑提案器选择、组合并细化高层聚合操作。质量控制将可执行聚合程序转成覆盖 5 万网站、11 个领域的 1 万条可验证 QA；
  - 数字：论文报告 WebAggregator-8B 达到 GPT-4.1 水平，32B 在 GAIA-text 上超过 GPT-4.1 十个百分点以上并接近 Claude-3.7。
  - 代码：Tencent/WebAggregator 发布 QA 构建引擎、查询、轨迹、模型和运行脚本。
  - 点评：使用小型封闭网页任务集测试 nanoRSI 程序进化：保存每个提案程序、来源 URL、验证器输出和生成样本，再比较固定数据 SFT 与刷新数据的迭代。 · [原文图](industry-rsi/assets/paper-figures/tencent-webaggregator.png) · [仓库](https://github.com/Tencent/WebAggregator)

- **[ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution](https://arxiv.org/abs/2509.19349)**（Sakana AI，2025-09-17，闭环）
  - 核心：LLM 修改档案中的程序，以验证器适应度选择下一轮可复用的父代；新颖性筛选与多臂赌博机模型选择提高搜索效率。
  - 数字：作者报告以 150 个样本找到优于 AlphaEvolve 的 26 圆装填解。
  - 代码：已确认官方代码与示例，许可为 Apache-2.0；
  - 点评：建议：增加基于档案的智能体框架搜索示例，固定留出测试，并在父代选择中计入成本。 · [原文图](industry-rsi/assets/paper-figures/sakana-shinkaevolve.png) · [仓库](https://github.com/SakanaAI/ShinkaEvolve)

### 结构化知识库与图（10）

- **[EvoWeave: Composing Reusable Agent Experience through Operation Level Graphs](https://arxiv.org/abs/2610.19381)**（New Jersey Institute of Technology / The Chinese University of Hong Kong，2026-10-14，闭环）
  - 核心：操作粒度的经验记忆：抽象状态为节点、可复用操作为有向边，边上带输入/输出契约、出处与能力引用。规划器把当前任务分解为依赖图；
  - 数字：覆盖四基准 × 五评测设置 × 三骨干。
  - 代码：HTML 全文未找到代码或仓库链接。
  - 点评：给每个可复用操作加契约与出处，是 nanoRSI 技能文件的 schema 升级方向：每条技能携带类型化输入/输出契约与能力出处，让检索在花费一次 rollout 前先检查兼容性——只读的 schema 扩展，与现有技能面兼容。 · [原文图](industry-rsi/assets/paper-figures/evoweave-operation-graphs.png)

- **[SpecForge: Recursive Self-Improvement for Coding Agents via Behavioral Specifications](https://arxiv.org/abs/2610.15708)**（Virginia Tech / NEC Laboratories America，2026-10-11，闭环）
  - 核心：改进外部上下文而非权重：代理按当前程序实体的自然语言行为规约生成代码，跑执行验证的测试（由参考实现生成、仅保留通过者），并从失败中修订规约。输出耦合——改好一个实体的规约可能劣化依赖者（“打地鼠”）——由多前沿树搜索应对：(i) 帕累托引导的状态选择维护逐实体通过率向量上非支配状态的档案，按频率加权采样扩展节点；
  - 数字：DevEval+ 五骨干：88.9（Qwen3-235B-A22B）、89.6（Gemini-2.5-Flash）、90.9（GPT-4o）、91.0（Gemini-3.1-Pro）、94.9（Claude-4.5-Sonnet）；
  - 代码：代码 MIT 许可，位于 github.com/ccsnow127/SpecForge（LICENSE 已于 2026-10-16 核验；
  - 点评：三个可直接迁移点：按实体维护非支配的技能/规约变体帕累托档案而非单一现任者（支配关系定义在逐条目通过率向量上）； · [原文图](industry-rsi/assets/paper-figures/specforge-behavioral-specs.png) · [仓库](https://github.com/ccsnow127/SpecForge)

- **[Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks](https://arxiv.org/abs/2610.11794)**（University College London / Huawei Noah's Ark Lab / University of Liverpool，2026-10-08，闭环）
  - 核心：冻结参数的 LLM agent 维护显式世界模型：以自然语言规则书承载关于环境动力学的可修订假设，作为持久语义记忆。观察-反思-规则修订-编译-校验的持续循环把规则书编译为可执行代码用于预测与规划；
  - 数字：在 ARC-AGI-3 全部 25 个公开游戏上（Claude Opus 5，推理力度 extra-high），agent 清空 25 局全部 183 关，平均 RHAE 100.0，共 7,518 步动作为人类基线 17,135 步的 0.44 倍（逐局比值 0.20-0.67，中位 0.42），比同一模型在 ARC Prize Standard harness 上高 59.3 平均 RHAE；
  - 代码：代码：arXiv 页与 HTML 正文均未找到。
  - 点评：对 nanoRSI 技能可移植的是其接受规则：技能/世界模型编辑只有在已记录 episode 的精确重放复现观测转移时才准入——在 LLM judge 之上叠加确定性重执行检查，与既有证据账本及反事实面板兼容。 · [原文图](industry-rsi/assets/paper-figures/memento3-rulebook-worldmodel.png)

- **[EvoBelief: Falsifiable World Models for Self-Improving LLM Agents](https://arxiv.org/abs/2610.12789)**（Tulane University / Amazon，2026-10-08，闭环）
  - 核心：LLM 全程冻结；自演化世界模型把环境知识编码为与证据挂钩的可证伪假设。
  - 数字：ALFWorld 无记忆设定对匹配的冻结世界模型：+23.9（Claude Haiku 4.5：66.42 对 42.54）、+31.3（GPT-5.4：76.12 对 44.78）；
  - 代码：未发布代码、权重或数据（arXiv 页无链接）。
  - 点评：反例触发的规则废除是 nanoRSI 技能库的廉价完整性清扫：每次冻结面板失败都应尝试证伪当时使用的技能，而不只蒸馏新技能； · [原文图](industry-rsi/assets/paper-figures/evobelief-belief-revision-loop.svg)

- **[EvoOntology: A Self-Evolving Ontology Layer for Data Agents](https://arxiv.org/abs/2609.15779)**（Renmin University of China，2026-09-14，闭环）
  - 核心：进化的对象是打包为 MCP 服务器的本体层（模式、内容、工具三层），位于数据智能体与异构数据源之间。构建智能体先从负载查询构建证据落地的初始本体；
  - 数字：三个基准、四个分析骨干。
  - 代码：代码以 MIT 发布于 github.com/ruc-datalab/EvoOntology（仓库创建于 2026-09-15，核验时 7 星）。
  - 点评：对 nanoRSI：把知识产物（技能库、领域笔记）当作带层级限制编辑的类型化对象，配同条件配对验收闸门与拒绝日志——与证据账本同构，应用于进化产物。 · [原文图](industry-rsi/assets/paper-figures/evoontology-self-evolving.png) · [仓库](https://github.com/ruc-datalab/EvoOntology)

- **[SE-GoS: Self-Evolving Graph-of-Skills for Skill Library at Scale](https://arxiv.org/abs/2609.08228)**（Peking University / Tencent / University of Edinburgh / Northwestern University 等，2026-09-08，闭环）
  - 核心：对既有 Graph-of-Skills 检索图做免训练进化：真实执行轨迹驱动三类更新合并为一轮离线进化——拓扑进化（按共现诱导工作流/依赖/回避边、剪除从未使用的技能）、赫布式边权进化（强化频繁共用的路径）、节点描述进化（单轮“文本梯度”刷新面向检索的描述）。检索算法、技能内容与模型权重均不动——只有检索状态随执行改变，且进化后沿用同一检索接口。
  - 数字：在 SkillsBench、三个 LLM 上，一轮进化把平均任务奖励从 52.4% 提到 59.4%，同时相对整库加载 1,000 技能把平均输入 token 削减约三分之一。
  - 代码：未找到代码或数据发布，仅论文。
  - 点评：给 nanoRSI 加一道免训练的检索保养工序：每批评测后从运行日志挖掘共用与从未使用的原语，只调整检索图（边、权、描述）而不改技能内容，并在留出任务集上验证后再采用。 · [原文图](industry-rsi/assets/paper-figures/se-gos-skill-graph.png)

- **[Procedural Graphs: Self-Evolving Execution Structures for LLM Agents](https://arxiv.org/abs/2609.09153)**（Google / Georgia Institute of Technology / Peking University，2026-09-08，闭环）
  - 核心：程序性知识以（程序，关系，程序）三元组及边属性存储，构成类比知识图谱的“程序图”。运行时智能体定位活跃节点、抽取 2 跳子图，引导模型将其转为只引导不代做的步骤级建议。
  - 数字：在 EnterpriseArena（跨连续宏观危机的流动性管理，Gemini 3.5 Flash）上，自进化第 1 轮新增“核对现金/预测资金跑道”节点，把验证存活率从 0.0% 提到 45.0%；
  - 代码：未找到代码或数据发布，仅论文。
  - 点评：给 nanoRSI 自身改进环维护一张小程序图（提案、评测、提交），让精炼器阅读失败与成功 episode 的对比，并加显式“拒绝编辑”记忆避免重复提议； · [原文图](industry-rsi/assets/paper-figures/procedural-graphs-google.png)

- **[Recursive Experiential-Working Memory Evolution for Long-Horizon Agent Harnesses](https://arxiv.org/abs/2608.24876)**（National University of Singapore / Stanford University / University of Oxford / Princeton University，2026-08-25，闭环）
  - 核心：工作记忆（经验证的任务状态：待办/完成/阻塞目标，仅由观察支持的检查器谓词提交）与经验记忆（技能）耦合，由匹配当前状态的调用策略检索——结构化轨迹使失败定位率达 64.8%，对仅结果反馈的 13.0%。跨任务由固定元智能体把失败定位到四组件之一（技能、工作记忆规格、调用策略、检查器），只修补被牵连的组件，且固定验证闸门只在'修复来源任务且不伤留出开发集'时放行。
  - 数字：37 个完成的模型-基准对中 35 个提升。
  - 代码：代码在 github.com/Gen-Verse/Recuris（Apache-2.0，核验时 205 星）。
  - 点评：对 nanoRSI：四组件定位（技能/记忆规格/检索策略/检查器）加'修复且不回退'闸门，是把失败归因到唯一可编辑面再提补丁的具体蓝图。 · [原文图](industry-rsi/assets/paper-figures/recuris-memory-evolution.png) · [仓库](https://github.com/Gen-Verse/Recuris)

- **[XSkill: Continual Learning from Experience and Skills in Multimodal Agents](https://arxiv.org/abs/2603.12056)**（Hong Kong University of Science and Technology / Zhejiang University / Huazhong University of Science and Technology，2026-03-12，闭环）
  - 核心：面向多模态智能体的免训练持续学习，双流知识：任务级 Markdown 技能（含可复用工具模板）与短条件-动作经验条目（上限 120 条，嵌入检索）。抽取做视觉落地（记录每个动作由什么视觉证据驱动），跨 rollout 批评对比成功/失败轨迹产出增改操作；
  - 数字：四个多模态基准 x 四个骨干：对仅工具基线 average@4 +2.58~+6.71；
  - 代码：代码在 github.com/XSkill-Agent/XSkill（268 星，核验时无许可证文件）；
  - 点评：对 nanoRSI：把任务级技能与短条件-动作经验分开（各自上限与检索），并记录驱动每个动作的视觉/文本证据，让批评能对照'有依据的原因'而非原始日志。 · [原文图](industry-rsi/assets/paper-figures/xskill-dual-stream.png) · [仓库](https://github.com/XSkill-Agent/XSkill)

- **[MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](https://arxiv.org/abs/2602.02474)**（Nanyang Technological University / University of Illinois Urbana-Champaign / University of Illinois Chicago / Tsinghua University，2026-02-02，闭环）
  - 核心：记忆抽取操作成为可学习的'记忆技能'，双环交织。技能选择/使用：轻量控制器（状态-技能嵌入上的 MLP，Gumbel-Top-K 采样）逐文本 span 选 Top-K 技能子集，LLM 执行器按技能更新该轨迹记忆库，控制器以下游问答表现为 PPO 奖励训练。
  - 数字：LoCoMo（LLaMA3.3-70B）：F1 44.21 / L-J 53.82 对 MemoryOS 41.39、A-MEM 49.71；
  - 代码：代码在 github.com/ViktorAxelsen/MemSkill（Apache-2.0，核验时 576 星）；
  - 点评：对 nanoRSI：进化'写记忆的操作'本身（而不止记忆内容），并用快照回滚 + 早停闸门约束设计者编辑——与技能轨相同的控制，再高一层。 · [原文图](industry-rsi/assets/paper-figures/memskill-memory-skills.png) · [仓库](https://github.com/ViktorAxelsen/MemSkill)

### 安全与治理（6）

- **[L3M: A Verifiable Harness and Runtime for Self-Extending and Self-Improving Agents](https://arxiv.org/abs/2610.19591)**（Amazon，2026-10-14，闭环）
  - 核心：以 Lean 4 写成的运行时：同一种语言实现 harness、陈述其不变量，也是代理扩展它的语言。全部状态存放于 Git：丰富的状态轨迹——而非聊天会话——是运行时可恢复、回滚、分叉、比较与合并的对象；
  - 数字：在 Terminal-Bench 上对照 Claude Code、以普通受限代理运行：未调优的 L3M“驯化”臂（无野调用）pass@3 27.0%，同 harness 开 shell 且关审查为 41.7%（34 对 18 通过，表 5）——无任何未审查调用即达 shell 三分之二；
  - 代码：截至 2026-10-16 HTML 未声明代码、权重或数据发布；
  - 点评：两个迁移点：(i) 按可逆性分层审查——nanoRSI 闸门严格度可随“影响可撤销距离”走（干跑与纯增量编辑自动放行、破坏性或改状态编辑走反事实复审），而非一刀切； · [原文图](industry-rsi/assets/paper-figures/l3m-verifiable-runtime.png)

- **[AI models may be capable of self-replicating without access to a datacenter](https://www.anthropic.com/research/self-replicating-ai)**（Anthropic，2026-10-12，闭环）
  - 核心：自主复制与适应（ARA）威胁评估：把权重型复制拆为四个实操阶段——寻找目标、获得执行、建立推理、继续传播——并实测当前小模型各阶段的可完成性。Gemma4-26B-A4B 在 15 台组网的杂牌安卓电视盒（每台约 55 美元）上分布式推理速度 0.39 tokens/秒；
  - 数字：作者简化评测中，GLM-5.2 及以上模型可完成端到端复制；
  - 代码：仅官方研究帖；
  - 点评：四阶段分解是任何自修改环的收容清单：nanoRSI 沙箱在构造上已禁止传播，但把每阶段映射为显式审计断言（不外发自产物、不重配环境）可让收容性质在 verify 运行中可测。 · [原文图](industry-rsi/assets/paper-figures/anthropic-ara-replication-chain.png)

- **[The Harness as the Only Mutable Surface: Compliance-Bounded Self-Evolution of LLM Agents in Credit Pipelines, with a Measured Admission Gate](https://arxiv.org/abs/2610.10629)**（Digital Economy Lab，2026-10-07，闭环）
  - 核心：只有 LLM 信贷流水线智能体的运行时 harness 可变——指令文本、工具调用逻辑与原语组合——模型权重保持冻结，因此每次适配都是可评审的 diff 并附带原因与测试。双环引擎控制部署：准入闸门在变更获准前记录哈希链式证据（注册的选择、运行义务、声明范围），且闸门自身的准入/拒绝统计作为量测控制与无界筛选基线对照报告。
  - 数字：作者报告的仿真结果（三类漂移 × 三档严重度 × 各 10 个种子）：带闸门循环准入 7,449 个候选变更中的 144 个，无一恶化留出误差，在全部低/中严重度单元把误报率恢复到 oracle 水平且未增加漏检；
  - 代码：代码：rav11l/cace-bench 提供 MIT 许可的参考实现与生成器（v0.6.0，Zenodo DOI 10.5281/zenodo.23207546），含一次 23,000 个合成案例的带日期参考运行。
  - 点评：可移植思路是'量测闸门'报告：把准入/拒绝计数、有害准入反事实与部署前拒绝行为作为 nanoRSI 自身闸门证据账本的一等字段，与既有反事实挑战者研究互相印证。 · [原文图](industry-rsi/assets/paper-figures/cace-bench-abs-crop.png) · [仓库](https://github.com/rav11l/cace-bench)

- **[Reflections on Trusting Trust, Revisited: Contaminating Self-Modifying AI Coding Agents with Poisoned Benchmarks](https://arxiv.org/abs/2609.17817)**（University of Washington / Georgetown University，2026-09-15，支撑·无闭环）
  - 核心：把 Thompson 编译器木马重演到自改写智能体上：注入智能体自评环的带毒基准诱导 Darwin Gödel Machine、Self-Improving Coding Agent 与 Hyperagents（Sonnet 4.5）自我演化出关闭 HTTPS 证书校验的指令，且该脆弱性迁移到中性留出任务。
  - 数字：三个目标系统上都能诱导出关闭证书校验的脆弱性并迁移到中性留出任务；
  - 代码：arXiv 论文公开；
  - 点评：对 nanoRSI 冻结循环做 fixture 投毒红队：故意泄漏的评测用于检验契约守卫与证据账本能否拦住被污染的接受，对应本文的干净基准持续性检验。 · [原文图](industry-rsi/assets/paper-figures/trusting-trust-self-modifying.svg)

- **[Safety in Self-Evolving Agents: A Survey](https://arxiv.org/abs/2610.00093)**（Zhejiang University / Huazhong University of Science and Technology / Xi'an Jiaotong University / NUDT 等，2026-09-08，支撑·无闭环）
  - 核心：综述（无新机制）：为持续从经验更新可复用状态（参数、记忆、工具、技能、工作流）的 agent 重新定义安全——'过去的事件成为未来的原因'后，一个语境中无害的信息可能在更大持久性、权限或范围上影响后续决策。提出转移中心的 SAVER 分析框架：Substrate（可复用影响栖身何处）、Adaptation（如何变化）、Violation（破坏哪些安全属性）、Exposure（失败在哪里显形）、Response（遏制、修复、撤销）。
  - 数字：给出跨切面结论而非基准数字：当适应超出其有效性条件时，合法经验也能催生不安全状态；
  - 代码：项目清单位于 github.com/xaddwell/awesome-self-evolving-agent-safety（页面 xaddwell.github.io/Awesome-Self-Evolving-Agent-Safety/）。
  - 点评：SAVER 五元分解可作为 nanoRSI 证据账本的核查清单 schema：每条被接受的编辑都可记录载体、适应方式、违反检查、暴露面与响应。 · [原文图](industry-rsi/assets/paper-figures/safety-selfevolving-saver-survey.png) · [仓库](https://github.com/xaddwell/awesome-self-evolving-agent-safety)

- **[Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents](https://arxiv.org/abs/2608.12851)**（City University of Hong Kong / University of Adelaide，2026-08-13，支撑·无闭环）
  - 核心：技能进化的安全审计而非改进机制：SkillMisevo-Gym 跨四个智能体框架（Claude Code、Codex、Hermes、OpenClaw，共享 MiniMax-M2.7 骨干）给技能库做版本化、隔离其余全部状态——只有智能体写的 SKILL.md 能跨过最终重置。SkillMisevo-Bench 固定评测：25 个冻结回合 x 21 任务（9 恶意、9 良性、3 持久性），九项生命周期指标（创作、检索、执行闸门）。
  - 数字：全部 21 个进化配置都产出不安全工件；
  - 代码：代码在 github.com/henrymao2004/misevolve（MIT，核验时 7 星）。
  - 点评：对 nanoRSI：持久更新应当'可观察、可归因、可撤销'——论文的三闸门伤害模型（导出、检索、执行）可映射为 nanoRSI 在写入与复用时运行的技能库治理检查。 · [原文图](industry-rsi/assets/paper-figures/skill-misevolution-gym.png) · [仓库](https://github.com/henrymao2004/misevolve)

### 上下文组织策略（5）

- **[RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views](https://arxiv.org/abs/2609.16936)**（Beihang University / Independent Researcher，2026-09-15，支撑·无闭环）
  - 核心：免训练的选择-投影-刷新循环在代码图上维护演化的仓库视图：以固定节点预算按议题与探索状态选区、投影为互补的视觉与文本表示、状态变化致视图过期时刷新。
  - 数字：SWE-bench Verified：相对最强多模态图基线解决率 +2.4 分，输入 token 少 5.8%、模型调用少 7.8%，三个模型族一致（Qwen3.6-35B-A3B、MiMo-V2.5、Kimi-K2.5）；
  - 代码：arXiv 论文公开；
  - 点评：给 nanoRSI 技能配每技能'视图'（漂移即刷新的文件白名单）替代全树上下文； · [原文图](industry-rsi/assets/paper-figures/repoatlas-evolving-views.png)

- **[Interactive Memory Learning for Long-Term Conversations](https://arxiv.org/abs/2609.17088)**（Harbin Institute of Technology (Shenzhen) / Pengcheng Laboratory，2026-09-15，闭环）
  - 核心：把记忆重新表述为可学习策略而非被动存储。会话合成管线构建专家数据用于快速适配；
  - 数字：在 CC/MSC/GC 上，Llama3-Instruct 1B/3B/8B 版 Icml（另有 Gemma3 主干）优于 GPT-4o 长上下文（128K）与六个记忆基线（Mem0、A-Mem、MemoryOS、MemoryBank、LD-Agent、THEANINE）：如 CC BLEU-4 2.37（3B）对 GPT-4o 长上下文 1.79；
  - 代码：核验时未找到代码。
  - 点评：延迟奖励的归因方式可映射到 nanoRSI 技能保留：按下游 episode 结果而非当次闸门裁决给每个记忆/上下文提案打分。 · [原文图](industry-rsi/assets/paper-figures/interactive-memory-learning.png)

- **[Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](https://arxiv.org/abs/2510.04618)**（Stanford University / SambaNova Systems / UC Berkeley，2025-10-06，闭环）
  - 核心：生成器轨迹与执行反馈交给反思器，整理器产出局部策略手册增量；通过有益/有害计数及去重，跨任务保留可复用策略，无需更新权重。
  - 数字：所有角色均使用非思考模式 DeepSeek-V3.1 时，无标准答案的在线 ACE 在 AppWorld 四项 TGC/SGC 指标上平均为 59.5，ReAct 为 42.4，Dynamic Cheatsheet 为 51.9；
  - 代码：已确认官方实现及评测代码，Apache-2.0 许可；
  - 点评：建议：在固定任务流上比较版本化增量记忆与整文件重写。 · [原文图](industry-rsi/assets/paper-figures/sambanova-stanford-ace.png) · [仓库](https://github.com/ace-agent/ace)

- **[LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation](https://arxiv.org/abs/2510.04851)**（Microsoft，2025-10-06，支撑·无闭环）
  - 核心：成功日志转为完整任务规划记忆和角色专用子任务记忆，后续任务检索复用。实验先离线建库再评价推理，并未测试持续在线记忆演化。
  - 数字：OfficeBench采用148个训练任务、152个测试任务和三个随机种子：GPT-4o成功率58.44%，无记忆为45.83%；
  - 代码：已确认公开论文；
  - 点评：建议实验：比较经成功筛选的程序记忆与无记忆基线，区分规划和子任务检索，并冻结测试记忆库。 · [原文图](industry-rsi/assets/paper-figures/microsoft-legomem-2025.png)

- **[ACON: Optimizing Context Compression for Long-horizon LLM Agents](https://arxiv.org/abs/2510.00615)**（Microsoft / KAIST / University of Cambridge，2025-10-01，闭环）
  - 核心：LLM比较完整上下文成功、压缩上下文失败的配对轨迹，修改压缩指南并评价候选指南；选择结果用于后续优化轮次，基础智能体权重保持固定。
  - 数字：OfficeBench采用GPT-4.1作为智能体和压缩器：效用优化的历史压缩取得74.74%准确率和4.93k峰值令牌；
  - 代码：已确认官方代码、MIT许可及蒸馏流程；
  - 点评：建议实验：根据配对失败优化压缩提示，保留独立验证集，同时记录成功率和上下文峰值。 · [原文图](industry-rsi/assets/paper-figures/microsoft-acon-2025.png) · [仓库](https://github.com/microsoft/acon)

### 反馈审查与编排（4）

- **[AURA: Agentic Diagnosis and Refinement for Production Recommender Systems at Scale](https://arxiv.org/abs/2609.16625)**（The Walt Disney Company，2026-09-15，闭环）
  - 核心：面向生产互动日志的端到端 agentic 管线：专职代理从真实用户会话中提炼定性失效模式（会话选择、诊断、大规模定性评估）；第二阶段将诊断与推荐系统的代码、数据和训练管线上下文结合，提出并落地代码级改进。
  - 数字：两个平台的生产诊断：评估 96,801 与 101,594 个会话，上游逐会话判 BAD 比例 19.5% 与 4.1%；
  - 代码：核验时未找到代码或数据；
  - 点评：可移植的是配置层解耦：把 nanoRSI 的任务域细节放进配置层，使诊断→代码改进循环可以不改循环本身而切换到新任务族； · [原文图](industry-rsi/assets/paper-figures/aura-recommender-pipeline.png)

- **[Reef: Continual Learning Infrastructure for Self-Improving Agents](https://github.com/Human-Agent-Society/reef)**（Human-Agent-Society，2026-09-01，闭环）
  - 核心：一个四阶段持续循环负责服务智能体请求、把后续反馈关联到交互 receipt、通过可配置 recipe 生成权重或 harness 候选，并在发布接受版本前执行选择策略。harness 路径无需本地训练 GPU 即可进化技能、规则、命令和扩展；
  - 数字：该发布提供可运行 quickstart 与 Reefine harness 演进教程，但没有为基础设施本身提供可比且独立审计的基准增益。
  - 代码：源代码仓库与 Apache-2.0 LICENSE 公开；
  - 点评：把 Reef 作为 ADOPTION 18 的设计参照：保留 nanoRSI 的冻结评测器与 worktree 隔离，再把 receipt 关联反馈、候选版本历史、显式 pending/rejected 状态和窄范围 promote 步骤提升为一等对象。 · [原文图](industry-rsi/assets/paper-figures/reef-continual-loop.svg) · [仓库](https://github.com/Human-Agent-Society/reef)

- **[Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents](https://arxiv.org/abs/2604.27233)**（Apple，2026-04，闭环）
  - 核心：把执行与审查分离：基础工具调用智能体先给出临时工具调用，由独立的审查智能体在执行前评估——注入渐进反馈促其修订、在 N 个候选中选择或打分。执行前审查既缓解破坏性错误又规避状态恢复问题。
  - 数字：BFCL 无关检测 84.9% -> 90.4%（+5.5）；
  - 代码：无代码仓库；
  - 点评：对 nanoRSI：把验收检查放到执行之前（执行前审查）而非破坏之后； · [原文图](industry-rsi/assets/paper-figures/apple-reinforced-agent.svg)

- **[Feedback Descent: Open-Ended Text Optimization via Pairwise Comparison](https://arxiv.org/abs/2511.07919)**（Stanford University，2025-11-11，闭环）
  - 核心：对成对比较的文本批评充当高带宽'类梯度'监督，完全在推理期编辑文本工件，不改权重。每轮：在累积反馈与当前最优条件下提议改进工件；
  - 数字：提示优化（Qwen3-8B）：四任务全胜 GRPO（如 Hover 60.00 对 38.67），与 GEPA 互有胜负（Hover 60.00 对 52.33）。
  - 代码：论文未给代码仓库 URL；
  - 点评：对 nanoRSI：无数值 oracle 时，把标量验收换成'偏好 + 理由'对——理由成为下一次提议的复用反馈记忆，即文本空间的梯度类似物。 · [原文图](industry-rsi/assets/paper-figures/stanford-feedback-descent.png)

### 记忆进化评测研究（4）

- **[MemScope: Evolving Agent Memory Architectures through Localized Code Repair](https://arxiv.org/abs/2610.21170)**（Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences / Meituan，2026-10-15，闭环）
  - 核心：记忆按 Agent Skills 形态打包（必备 SKILL.md 与 scripts/ 下可执行 provider，激活的 provider 维护自己的运行时记忆库）。会工具使用的 Patch Agent 联合检查原始执行轨迹、运行时记忆状态、当前 provider 代码与补丁历史，定位修复目标，并在 provider 身份不变与记忆兼容约束下施加有界的就地编辑——替换部件而非重写架构；
  - 数字：GAIA 诊断性消融：轨迹+记忆联合检查 86.67%，对纯轨迹 70.00% 与纯摘要 63.33%。
  - 代码：论文未链接自有代码仓库；
  - 点评：证据接地的定位是 nanoRSI 的提案接口纪律：让提案者同时看到执行轨迹、其产出的运行时状态、目标代码与既往补丁结果，要求附带补丁清单（定位故障、预期范围）的有界就地编辑而非整文件重写； · [原文图](industry-rsi/assets/paper-figures/memscope-method.png)

- **[ThinkFlow: Self-Evolving Probabilistic Latent Memory for Lifelong Conversational Agents](https://arxiv.org/abs/2609.17010)**（Pengcheng Laboratory / Harbin Institute of Technology (Shenzhen) / China Unicom Greater Bay Area Innovation Institute，2026-09-15，闭环）
  - 核心：以端到端潜在记忆取代显式文本记忆：对话流被压缩为解耦的概率潜在记忆技能（连续向量），绕开文本摘要瓶颈。测试时演化分两阶段：教师引导的潜在对齐引导初始状态（冷启动），之后自监督的下一用户话语预测任务在交互中持续精炼记忆，全程无需标注。
  - 数字：在 PersonaMem（上下文至 1M token，Qwen3-8B 主干）上，ThinkFlow-8B 平均准确率 41.94，较最强可比记忆方法（MemGen 38.86）+2.36，最强任务 +15.32；
  - 代码：核验时未找到代码、权重或数据；
  - 点评：可移植其免标注演化信号：用记忆技能对下一观测（自监督下一话语预测）的意外度降低来打分，使技能保留闸门不依赖任务标注。 · [原文图](industry-rsi/assets/paper-figures/thinkflow-latent-memory.png)

- **[S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](https://arxiv.org/abs/2608.31100)**（ByteDance Seed / M-A-P / TokenWave.AI，2026-08-31，闭环）
  - 核心：智能体探索游戏并自评决策，在后续回合复用原始历史、按分数整理的记忆摘要或经验训练后的参数。主要探索阶段的可执行验证器奖励留在基准侧，通过更严格且隔离的评测检查继承状态是否改善行为；
  - 数字：七个游戏中，自评质量与下一次严格评测提升的分块相关系数接近零：事件一致性为 −0.010，负校准误差为 −0.018。
  - 代码：论文及项目页公开；
  - 点评：拟议 nanoRSI skills 消融：比较原始历史、摘要记忆与冻结状态，构建记忆时隐藏验证器分数。 · [原文图](industry-rsi/assets/paper-figures/s3gym-figure.png)

- **[Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory](https://arxiv.org/abs/2511.20857)**（University of Illinois Urbana-Champaign / Google DeepMind，2025-11-25，支撑·无闭环）
  - 核心：流式基准而非机制：静态数据集重组为顺序任务流，每步走'检索-综合-进化'（从记忆检索、作答、以正确性信号更新记忆）。十个数据集覆盖单轮（MMLU-Pro、GPQA、AIME 24/25、ToolBench）与多轮（AlfWorld、BabyAI、ScienceWorld、PDDL）；
  - 数字：自进化记忆稳定有效，多轮场景增益最大（Claude 3.7 Sonnet：ReMem 平均成功率 0.78 对 History 0.49）；
  - 代码：核验时无代码 URL（'接收后以宽松开源许可发布'）。
  - 点评：对 nanoRSI：难->易优于易->难是实验设计规则——记忆流先难后易排课； · [原文图](industry-rsi/assets/paper-figures/evo-memory-remem.png)

### 探索式记忆构建（1）

- **[RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments](https://arxiv.org/abs/2609.15364)**（Aether AI / University of California San Diego / University of Illinois Chicago，2026-09-14，闭环）
  - 核心：面向陌生环境的免训练多智能体自改进：课程、执行、验证三类智能体在无金标条件下探索。广度递归自探索（BRS）并行跑课程组织的任务组，绘制环境结构并存下按组分组的经验记忆——可复用的（动作、条件、后果）因果模式；
  - 数字：以 GLM-5.3 为执行、Kimi-K3 为验证/课程：OSWorld 2.0 partial 78.98，高于 GPT-6 Astra 报告的 72.60（+6.38），binary 42.68；
  - 代码：代码以 Apache-2.0 发布于 github.com/AetherLabsAI/RSIAgent；
  - 点评：对 nanoRSI：把改进预算拆成广度测绘阶段（大量廉价探针任务沉淀因果模式）与目标任务上的深度利用阶段，随后在最终测试前冻结记忆——与 nanoRSI 的冻结纪律天然对齐的两段式调度。 · [原文图](industry-rsi/assets/paper-figures/rsiagent-autonomous-exploration.png) · [仓库](https://github.com/AetherLabsAI/RSIAgent)


## 2. 训练时自迭代 / Training-time self-iteration（44 条）

### 自博弈与课程任务生成（15）

- **[R$^2$Orch: Recursive Self-Improvement for Agent Orchestration via Self-Play within a Skill-Internalization Loop](https://arxiv.org/abs/2610.22740)**（The Chinese University of Hong Kong, Shenzhen / Fudan University / University of Illinois Urbana-Champaign / Tsinghua University 等，2026-10-19，闭环）
  - 核心：在冻结 Worker 池上的两层嵌套环。内环：Proposer-Director 在随机化 rollout 组上自博弈——Proposer 选任务，Director 编排 Workers 执行。
  - 数字：横跨问答、数学、代码与交互任务的十二个基准（含 AIME 2026、ALFWorld、WebShop；
  - 代码：论文给出匿名仓库 anonymous.4open.science/r/R2Orch-36F1；
  - 点评：把技能撤除当闸门信号：周期性地在移除技能文件的上下文里重评 nanoRSI 已接受技能； · [原文图](industry-rsi/assets/paper-figures/r2orch-overview.png) · [仓库](https://anonymous.4open.science/r/R2Orch-36F1)

- **[STRETCH the Boundaries: A Unified Self-Taught Framework for Progressive LLM Evolution](https://arxiv.org/abs/2609.18642)**（University of Birmingham，2026-09-16，闭环）
  - 核心：同一模型在同参数空间交替扮演 Scaffolder 与 Learner：GRPO 训练的出题奖励钉在学习者 50% 成功率，把任务保持在拉伸区；epoch 级 Golden Experience Replay（成功题/轨迹对 SFT）稳住双循环。
  - 数字：Qwen2.5-7B-Instruct 在 Mano Complex：67.9 ER / 63.6 SA，对照 R-Zero 64.8/61.7、Absolute Zero 63.4/60.1；
  - 代码：代码位于 github.com/GuanNiPiShi123/STRETCH（核验时无 LICENSE——仅可借鉴思想）；
  - 点评：50% 成功率的奖励峰值可为 nanoRSI 探针任务生成提供可调难度目标——保持半数可解的任务流让每次评估的信息量最大。 · [原文图](industry-rsi/assets/paper-figures/stretch-unified-self-taught.png) · [仓库](https://github.com/GuanNiPiShi123/STRETCH)

- **[SPADE: Self-Play in Adaptive Synthetic Executable Environments](https://arxiv.org/abs/2608.19197)**（University of Washington / Stanford University / Northeastern University / Carnegie Mellon University 等，2026-08-19，闭环）
  - 核心：同一 LLM 演两角。环境设计者把完整 MDP 写成可执行 Python（Gym 风格 reset/step），锚定在采样的预训练语料文档 + 带后悔分与技能标签的历史环境记忆上，并输出特权提示；
  - 数字：Qwen3-30B-A3B 游戏套件均值：SPADE 58.3 对基线 50.2（+8.1）、固定环境 RLVE 53.0 与 GRPO 51.4（超最强固定环境基线 +5.3）；
  - 代码：代码在 github.com/spade-rl/spade（MIT，核验时 102 星）；
  - 点评：对 nanoRSI：用基于提示的后悔（提示带来多少提升）而非原始难度奖励任务/环境生成器，并让生成环境锚定在检索到的语料文档上，防止多样性塌缩。 · [原文图](industry-rsi/assets/paper-figures/spade-adaptive-environments.png) · [仓库](https://github.com/spade-rl/spade)

- **[Self-Play Meets Skill Evolution: Self-Evolving Search Agents that Pose, Solve, and Remember](https://arxiv.org/abs/2607.29468)**（University of Chinese Academy of Sciences / Institute of Automation, CAS / Peking University / Mininglamp Technology 等，2026-07-31，闭环）
  - 核心：非对称自博弈耦合三个进化对象：挑战者从 5 万答案池提出可验证的搜索问题；只有求解者能检索技能库（记忆对挑战者隐藏以防策略泄漏）；
  - 数字：七个 QA 基准（3,125 道留出题）：六个骨干上比 SSP 平均 +1.2~+3.2（如 Qwen3-8B 均值 47.5、超基线 +7.0）；
  - 代码：论文列出代码 github.com/Zenghuang-Fu/SESA-Self-Evolving-Agents（论文给出的 URL；
  - 点评：对 nanoRSI：对任务生成器隐藏进化中的记忆（非对称访问），使生成任务无法利用记忆答案； · [原文图](industry-rsi/assets/paper-figures/sesa-self-play-skills.png)

- **[From RLVR to RLSVR: Task Transformation Induces Self-Verifiable Rewards for Open-Ended LLM Self-Improvement](https://arxiv.org/abs/2607.23802)**（Duke University / Adobe Inc. / Pennsylvania State University / National University of Singapore 等，2026-07-26，闭环）
  - 核心：把开放式任务变换为'潜变量诱导精确可查奖励'的代理环境：SpyRL（谁是卧底）中 n-1 个平民看完整输入、卧底看降级版，各自作答后检测者投票猜卧底——检测奖励对环境指定的卧底编号确定性可查，表演奖励按怀疑票零和分配。GRPO 式优化配角色优势估计与迟滞门控的交替更新；
  - 数字：Qwen3-8B 对骨干胜率：摘要 75.4%、创意写作 77.3%；
  - 代码：代码在 github.com/wangqinsi1/RLSVR/tree/SpyRL（Apache-2.0，核验时 192 星）。
  - 点评：对 nanoRSI：任务缺验证器时，把它变换为'隐藏状态使奖励机械可查'的代理博弈——用构造获得可验证性，而非靠裁判。 · [原文图](industry-rsi/assets/paper-figures/spyrl-self-verifiable-rewards.png) · [仓库](https://github.com/wangqinsi1/RLSVR/tree/SpyRL)

- **[GPT-Red: Automated Red Teaming via Self-Play at Scale](https://cdn.openai.com/pdf/gpt-red-automated-red-teaming-via-self-play-at-scale.pdf)**（OpenAI，2026-07-15，闭环）
  - 核心：自博弈 RL 依据攻击成功与抵抗成功的奖励更新攻击者和防守模型群体；更强防守者提供更难训练信号，再用训练后的红队生成 GPT-5.6 的对抗训练数据。
  - 数字：报告中，GPT-5.6 Sol 面对 GPT-Red 直接注入的成功攻击率为 0.05%，按保留环境内的攻击尝试取平均；
  - 代码：论文公开；
  - 点评：可探索无害对抗样例，并分别衡量样例有效性、任务完成率和误拒率。 · [原文图](industry-rsi/assets/paper-figures/gpt-red-figure.png)

- **[ACE: Self-Evolving LLM Coding Framework via Adversarial Unit Test Generation and Preference Optimization](https://arxiv.org/abs/2605.16299)**（Fudan University，2026-04-17，闭环）
  - 核心：单个 LLM 交替扮演 Solver（写代码）与 Adversary（构造对抗单元测试）；执行 pass/fail 布尔表驱动 Solver 侧 SFT 过滤与 Adversary 侧 KTO 偏好优化，多轮递归自改进，无需 ground-truth 代码或外部奖励模型。
  - 数字：共享底座的双 LoRA 适配器：Qwen3-4B 经 5 轮自进化 CodeContests pass@1 46.7（instruct 41.7、ReasonFlux-Coder-4B 24.0）、LiveCodeBench 37.5；
  - 代码：arXiv 论文公开；
  - 点评：nanoRSI 可让提案者在候选编辑之外同时产出对抗探针用例：两者的执行结果共同构成验收信号，在最小任务集上去掉对裁判模型的依赖。 · [原文图](industry-rsi/assets/paper-figures/ace-fudan-adversarial-tests.png)

- **[GASP: Guided Asymmetric Self-Play For Coding LLMs](https://arxiv.org/abs/2603.15957)**（University of Tübingen / Max Planck Institute for Intelligent Systems / ELLIS Institute Tübingen / Tübingen AI Center，2026-03-16，闭环）
  - 核心：锚定真实难题的非对称自博弈：对标准 RLVR 解不出的 goalpost 题，教师先生成较易的 lemma 变体、再生成更难的 lift 变体构成课程；学生解答经拒绝采样回炉训练，全程无需外部数据。
  - 数字：Qwen2.5-Coder-7B 在 LiveCodeBench v5（216 题、3 种子）：pass@20 33.69±0.28，对照 AZR 31.15、真实数据 RL 33.10、底座 29.68；
  - 代码：arXiv 论文公开；
  - 点评：goalpost 机制可映射到 nanoRSI 探针任务：维护未解冻结任务清单，让提案者朝它们生成 lemma/lift 变体，把攻破的 goalpost 数作为搜索进度读数。 · [原文图](industry-rsi/assets/paper-figures/gasp-guided-asymmetric-selfplay.png)

- **[Toward Training Superintelligent Software Agents through Self-Play SWE-RL](https://arxiv.org/abs/2512.18552)**（Meta FAIR / University of Illinois Urbana-Champaign / Carnegie Mellon University，2025-12-21，闭环）
  - 核心：单个 LLM（CWM-sft 32B）在沙箱化的真实仓库上同时扮演缺陷注入者与修复者，无需人工 issue 或测试。注入者在不看测试与 issue 的情况下探索仓库、发现测试运行方式，产出缺陷工件（测试脚本、解析器、注入 diff、测试弱化 diff），经一致性检查（含逆变异测试）验证；
  - 数字：自博弈 RL 后（CWM-sft 32B、512 张 H100）SWE-bench Verified +10.4 分、SWE-Bench Pro +7.8 分；
  - 代码：未找到代码发布；
  - 点评：对 nanoRSI：让变异者同时产出验证器工件（测试脚本 + 弱化补丁）并用逆变异测试校验的自博弈任务生成——无人工标注下生成器-验证器协同生产的蓝图。 · [原文图](industry-rsi/assets/paper-figures/meta-ssr-self-play.svg)

- **[Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](https://arxiv.org/abs/2511.16043)**（UNC-Chapel Hill / Salesforce Research / Stanford University，2025-11-20，闭环）
  - 核心：课程策略面向使用工具的执行器生成任务；十次执行器回答估计不确定性并产生伪标签，筛选任务用于训练执行器，新能力再改变下一轮课程，两种策略迭代更新。
  - 数字：Qwen3-8B 数学平均分从 49.2 升至 58.2（增加 9.0 个百分点，约相对提高 18%），仅加工具为 53.2。
  - 代码：已确认官方课程及执行器训练代码，Apache-2.0 许可；
  - 点评：建议：先用不可修改的答案验证器检验难度自适应任务生成，再考虑昂贵的策略训练。 · [原文图](industry-rsi/assets/paper-figures/salesforce-unc-agent0.png) · [仓库](https://github.com/aiming-lab/Agent0)

- **[EvoLMM: Self-Evolving Large Multimodal Models with Continuous Rewards](https://arxiv.org/abs/2511.16672)**（Australian National University / Linkoping University / MBZUAI / Aalto University，2025-11-20，闭环）
  - 核心：单一冻结多模态基座拆成两个 LoRA 角色，仅用原始图像联合训练，零标注、零元数据、零奖励模型：提案者生成视觉落地的数学问题；求解者以 N=5 采样作答。
  - 数字：Qwen2.5-VL-7B：ChartQA 84.00 -> 86.70、MathVista 68.46 -> 70.52、MathVision 23.91 -> 24.81；
  - 代码：代码在 github.com/mbzuai-oryx/EvoLMM（27 星，核验时无许可证文件）。
  - 点评：对 nanoRSI：连续自一致性奖励（不确定时仍有非零梯度）与熵带通课程可直接移植到任何自博弈任务生成器； · [原文图](industry-rsi/assets/paper-figures/evolmm-proposer-solver.png) · [仓库](https://github.com/mbzuai-oryx/EvoLMM)

- **[SIMA 2: A Generalist Embodied Agent for Virtual Worlds](https://arxiv.org/abs/2512.04797)**（Google DeepMind，2025-11-13，闭环）
  - 核心：Gemini生成任务并评价轨迹；积累的经验用于训练后续SIMA世代，新策略继续采集经验。
  - 数字：在固定ASKA任务中，初始不足四分之一的任务超过Gemini奖励阈值（>50），后续世代全部超过阈值。
  - 代码：已确认公开论文和演示；
  - 点评：建议实验：分别记录学习器世代和评分轨迹，并用独立保留任务集验证迁移。 · [原文图](industry-rsi/assets/paper-figures/google-sima2-2025.png)

- **[AgentEvolver: Towards Efficient Self-Evolving Agent System](https://arxiv.org/abs/2511.10395)**（Alibaba Group — Tongyi Lab，2025-11-13，闭环）
  - 核心：通过自主生成的环境任务更新智能体策略参数：自我提问生成并筛选任务，自我导航检索历史经验指导轨迹，自我归因结合结果奖励分配细粒度信用。强化学习后的策略和经验池用于后续探索。
  - 数字：作者表 1：Qwen2.5-7B 在 AppWorld 与 BFCL-v3 上的平均 avg@8 从 15.8% 升至 45.2%，差值为 29.4 个百分点。
  - 代码：代码：ModelScope 公开仓库，Apache-2.0。
  - 点评：拟议 nanoRSI learner 实验：为每个策略检查点记录生成任务清单版本，并以固定数据对照组评估经验复用。 · [原文图](industry-rsi/assets/paper-figures/alibaba-agentevolver.png) · [仓库](https://github.com/modelscope/AgentEvolver)

- **[SPICE: Self-Play In Corpus Environments Improves Reasoning](https://arxiv.org/abs/2510.24684)**（Meta FAIR / National University of Singapore，2025-10-28，闭环）
  - 核心：单一 RL 模型在原始语料上扮演两角：挑战者从文档挖出（问题，可验证答案）对；推理者不看文档作答（信息不对称）。
  - 数字：Qwen3-4B-Base：35.8% -> 44.9%（+9.1）；
  - 代码：论文页无代码仓库（'评测代码与提示将发布'）；
  - 点评：对 nanoRSI：用执行者的成功率方差（峰值 50%）而非原始难度奖励任务生成器——一行改动即可让生成任务始终落在当前候选可学习的边界上。 · [原文图](industry-rsi/assets/paper-figures/meta-spice-self-play.png)

- **[Learn the Ropes, Then Trust the Wins: Self-imitation with Progressive Exploration for Agentic Reinforcement Learning](https://arxiv.org/abs/2509.22601)**（Tencent Youtu Lab / Shanghai Jiao Tong University / Peking University / Fudan University 等，2025-09-26，闭环）
  - 核心：SPEAR 将按课程调度工具使用内在奖励的渐进探索，与自模仿回放的利用阶段结合。优势重校准修正回放分布漂移，协方差裁剪和熵控制稳定更新；
  - 数字：摘要报告 ALFWorld 相比 GRPO/GiGPO/Dr.BoT 最高提升 +16.1/+5.1/+8.6%，WebShop 最高提升 +20.7/+11.8/+13.9%。
  - 代码：TencentYoutuResearch/SPEAR 代码公开，并包含 SPEAR_LICENSE.txt。
  - 点评：在 nanoRSI 学习器实验中公开回放来源：在匹配 rollout 预算下比较均匀采样、冻结回放和递归刷新回放，同时报告隐藏集收益与回放造成的退化。 · [原文图](industry-rsi/assets/paper-figures/tencent-spear.png) · [仓库](https://github.com/TencentYoutuResearch/SPEAR)

### 经验蒸馏与测试时适应（9）

- **[Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine](https://arxiv.org/abs/2610.22192)**（Tencent Hy Frontier / National University of Singapore / University of Maryland / University of Georgia 等，2026-10-15，闭环）
  - 核心：从 Qwen3.8-27B 基座起五个阶段：RSR-1 → RPR-1 → RSR-2 → RPR-2。递归自重写（RSR，仅演员）发现验证通过的轨迹（仅在验证器通过时保留）、用保留演员规划 runbook、经泄漏/审查闸门筛查、在目标 harness 下执行全新重放，并在清洗后的轨迹上做 SFT，critic 权重冻结。
  - 数字：每个被保留的阶段检查点在全部基准上评测（Mean@3）：Terminal-Bench 4.0 0.00→6.10→16.67→17.46→19.84%；
  - 代码：论文 CC BY 4.0；
  - 点评：权重侧交替超出 nanoRSI 本地预算，但两个协议可直接迁移：每个被保留的中间检查点都在冻结面板与终测上评测（多种子选择器研究应采用的阶梯报告），以及奖励整形中把严格成功与有界部分得分分开（nanoRSI 已有的面板/终测切分）。 · [原文图](industry-rsi/assets/paper-figures/terminal-rsi-recursive-loop-fig2.png)

- **[MetaExp: Learning to Self-Improve through Experience via Verifiable Cross-Task Environment Scaling](https://arxiv.org/abs/2610.21492)**（University of Macau / Shenzhen Institute of Advanced Technology, Chinese Academy of Sciences / Georgia Institute of Technology / Alibaba Group，2026-10-15，闭环）
  - 核心：把经验学习本身训练为可迁移的模型能力。环境被扩展为具有可控跨任务结构的可验证任务族：Shared-Tool 族跨任务固定黑盒工具（诱导操作型经验），Shared-Workflow 族在变化的任务实现中保持潜层流程（诱导流程型经验）。
  - 数字：下游演化期参数冻结：SpreadsheetBench +8.5 分、APEX-Agents 峰值 +2.3、AutomationBench +14.8（对匹配基座）；
  - 代码：论文 HTML 未链接代码或数据仓库；
  - 点评：族结构任务切分是 nanoRSI 变体/反事实面板的设计规则：把训练任务组织成共享固定工具或潜层流程而任务实现变化的族，使被接受的技能必须跨族泛化而非记忆实例——直接加强 cf-source-* 反事实设计与未来的技能迁移度量。 · [原文图](industry-rsi/assets/paper-figures/metaexp-framework.png)

- **[Recursive Self-Improvement through Multi-Agent Self-Supervision](https://arxiv.org/abs/2610.12176)**（UC Berkeley / Sakana AI，2026-10-08，闭环）
  - 核心：MASS 交替两个阶段：第一阶段冻结权重，用 RHI 搜索演化多智能体工作流拓扑（角色、信息路由与结构护栏），并将其编码为文本化 workflow 提示，同一个语言模型在内环中同时担任执行器、自评估器与自优化器；第二阶段用选出的多智能体工作流产生的自生成轨迹微调模型，更新后的模型进入下一周期继续担任执行器/优化器/评估器，构成同源自监督下的递归自举。
  - 数字：作者报告的结果：以 Qwen3.6-27B 为起点、qwen-code 0.20.0 脚手架、两轮 MASS 周期后，MLR-Bench、DSBench、ScienceAgentBench 与 AstaBench 上单位输出 token 得分为基座的 1.2-1.6 倍；
  - 代码：代码：官方研究实现公开于 SakanaAI/mass，但其 NOTICE.md 声明未对 MASS 专有代码分配任何公共开源许可证，应视为无许可、零复制。
  - 点评：两个可移植思路，不引入任何 MASS 代码或训练栈：(1) 在 skills/harness 轨道测试多角色自监督脚手架——同一模型以执行器/评估器/优化器三种提示作用于同一工作区——在匹配调用、token 与种子下与单智能体脚手架对照； · [原文图](industry-rsi/assets/paper-figures/mass-rsi-overview.png) · [仓库](https://github.com/SakanaAI/mass)

- **[Reflective Recovery: A Self-Supervised Method for Reasoning by Learning from Mistakes](https://arxiv.org/abs/2609.19156)**（Zhejiang University / The University of Hong Kong / The Hong Kong University of Science and Technology，2026-09-18，闭环）
  - 核心：把失败推理轨迹转化为恢复训练数据：失败尝试的初始片段与提示配对，用于引导模型走向正确解。因片段含错误，模型无需外部评论家或奖励模型即可学会检测并修复错误——针对模仿学习的规模塌缩：问题集有限时增加完美样本不再带来提升。
  - 数字：在 DeepSeek-R1-Distill-Qwen-7B 上，AIME 2025 准确率从 30.0% 升至 37.5%，Minerva 从 37.6% 升至 47.8%（对照为未使用该方法的同一基模型）；
  - 代码：核验时未找到代码。
  - 点评：把 nanoRSI 的被拒候选档案回灌为训练式信号：将每个被拒提案的失败前缀与最终被接受的修复配对，使提案策略从自身错误学恢复，无需新标注。 · [原文图](industry-rsi/assets/paper-figures/reflective-recovery-pipeline.png)

- **[RetireOPD: Self-Retiring On-Policy Distillation for Agentic Reinforcement Learning](https://arxiv.org/abs/2609.20784)**（Zhejiang University / Alibaba Group，2026-09-17，支撑·无闭环）
  - 核心：先用环境奖励训练技能条件教师；无技能学生通过 RL 加在线策略技能蒸馏联合学习；
  - 数字：Qwen2.5 1.5B-7B 全档：ALFWorld 成功率较 RL（GRPO）基线 +14.1%~+18.8%、WebShop 准确率 +11.8%~+19.0%；
  - 代码：Apache-2.0 代码位于 github.com/ZJU-REAL/SDAR（核验时 383 星）。
  - 点评：退役是 ADOPTION 26 缺的生命周期另一半：给巩固后的技能工件一个自动过期测试（冻结策略是否仍胜过无工件策略？），内化完成即退役。 · [原文图](industry-rsi/assets/paper-figures/retireopd-self-retiring-distillation.png) · [仓库](https://github.com/ZJU-REAL/SDAR)

- **[Experience Funnel: A State-Policy Alternating Loop for Self-Evolving Agents](https://arxiv.org/abs/2609.08919)**（The Hong Kong Polytechnic University / Huawei / Renmin University of China，2026-09-08，闭环）
  - 核心：对已部署的（文本状态、策略）对做双时间尺度循环。快：把轨迹聚合成总结复现流程、失败模式与纠偏策略的任务级文本状态，候选状态编辑必须先在留出交互上通过验证。
  - 数字：三个基准（SearchQA、ALFWorld、WebShop），Qwen3.5-4B 学生、冻结 Qwen3.5-27B 教师，昇腾 910B3：平均 57.6% 对 SkillRL 56.2、OPID 55.4、SkillOpt 53.9、基座 33.7。
  - 代码：未找到代码、权重或数据发布，仅有论文。
  - 点评：对 nanoRSI 参数轨：用反事实状态对比（无状态 / 旧状态 / 新状态三种 rollout）作为上下文变更是否值得蒸馏的验收测试，让权重更新像技能提交一样过闸门。 · [原文图](industry-rsi/assets/paper-figures/experience-funnel-state-policy.svg)

- **[Self-Evolving LLM Agents with In-Distribution Optimization](https://arxiv.org/abs/2606.07367)**（Eindhoven University of Technology / University of Liverpool / MIT-IBM Watson AI Lab，2026-06-05，闭环）
  - 核心：每轮自进化在专家演示与自身轨迹的混合集上用加权隐式 Q-Learning 训练分布内评论家（不对分布外动作取 max；步权上调成功轨迹中信息量大的后段步骤），仅在环境奖励上做 GAE 得到步骤级过程奖励，再用行为近端策略优化——非对称裁剪激进压制负优势动作——显式控制跨轮分布漂移。
  - 数字：Llama-2-7B-Chat 骨干：均值 79.4 对 QLASS 74.5、ETO 69.4、Best-of-N 65.4、PPO 45.3（ALFWorld seen/unseen 90.7/89.6；
  - 代码：项目页 qevolve.github.io。
  - 点评：对 nanoRSI 模型轨：每轮学习都用当前策略自身 rollout（加演示）训练分布内评论家，并用非对称裁剪——多轮稳定、无离策略漂移的配方。 · [原文图](industry-rsi/assets/paper-figures/qevolve-in-distribution.png)

- **[EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](https://arxiv.org/abs/2510.16079)**（Shanghai AI Laboratory / Zhejiang University / East China Normal University / Fudan University 等，2025-10-17，闭环）
  - 核心：闭环经验生命周期，两阶段交替：离线阶段参数冻结，智能体以专家人设回顾历史轨迹，蒸馏成'指导性'（成功）与'警示性'（失败）原则——自然语言描述 + 知识三元组，经嵌入相似度与 LLM 等价性双重去重、按动态有用性分数剪枝；在线阶段检索到的原则参与推理，轨迹再喂给下一轮蒸馏；
  - 数字：Qwen2.5-3B 搜索智能体均值 0.382 对 Search-R1-instruct 0.325、拒绝采样 0.265、RAG 0.270；
  - 代码：论文列出 github.com/Edaizi/EvolveR；
  - 点评：对 nanoRSI：参数冻结的离线蒸馏阶段可直接移植——把被接受的轨迹变成去重原则卡，并用动态有用性分数剪除死条目。 · [原文图](industry-rsi/assets/paper-figures/evolver-experience-lifecycle.png)

- **[Self-Improving LLM Agents at Test-Time](https://arxiv.org/abs/2510.07841)**（University of Illinois Urbana-Champaign，2025-10-09，闭环）
  - 核心：对每个不确定的测试样本，三阶段自改进全程在推理期完成：自我感知用候选动作 NLL 的相对 softmax 打分标记低边际样本；自我数据增强让模型自己（从不看金标）从被标记样本生成 K 个相似输入-输出对；
  - 数字：相对提示基线平均绝对 +5.48%（ToolAlpaca +5.84%、NexusRaven +6.05%、SealTool +5.76%、API-Bank +4.26%）；
  - 代码：论文未提及代码发布。
  - 点评：对 nanoRSI：最小逐样本环——不确定性触发的合成自数据 + 临时适配器、答完即重置——可在数字/工件任务上验证，无需训练基础设施。 · [原文图](industry-rsi/assets/paper-figures/ttsi-test-time-self-improvement.png)

### 自主训练智能体与数据管线（8）

- **[WorkRover: Scaling Long-Horizon Cowork Agent Training Via Recursive Environment Evolution](https://arxiv.org/abs/2610.18067)**（Fudan University / East China Normal University / Renmin University of China / Shanghai Qiji Zhifeng 等，2026-10-13，闭环）
  - 核心：把环境视作 N 个 <Context, Task, Verifier> 任务包，由自适应的构建代理建造与修复而非固定流水线。阶段一打包工作上下文（仓库文件、DeepResearch 轨迹、MCP 接口技能、插桩应用）；
  - 数字：对 Qwen3.5-35B-A3B 后训练（SFT 30,115 条轨迹来自 Qwen3.5-397B-A17B；
  - 代码：论文 CC BY 4.0；
  - 点评：FCR 即可迁移点：对环境/评测器缺陷，每组件限一份冻结修复、小界枚举，扩展到依赖闭更新集，匹配种子重放后晋升最小通过验证的闭编辑——直接适用于 nanoRSI 任务包生成（prepare.py manifest），坏 fixture 应最小修复而非重生成。 · [原文图](industry-rsi/assets/paper-figures/workrover-recursive-env-evolution.png)

- **[Agentic-TTT: Training test-time policy for test-time training](https://arxiv.org/abs/2610.12002)**（NUS AI Institute / National University of Singapore，2026-10-08，闭环）
  - 核心：把测试时训练（TTT）过程封装为可调用工具，由学习到的测试时策略决定是否适配、调用哪个 TTT 算法、以及能否复用已有的参数级技能而非新训练。累积的技能构成不断变化的部署环境，策略由自身决策产生的效用增益训练；
  - 数字：在作者基准上，学习策略的效用较骨干模型接近翻倍，在惩罚下学会效用与计算的权衡，并外推到策略训练未见的领域：在 G1（代码、通用推理、逻辑游戏）、G2（数学、网格谜题、医学问答）或其并集 G3 上训练的策略，在所有组均未见过的 Passage 与 LongBook 问答上评测。
  - 代码：代码：未找到。
  - 点评：nanoRSI 的最小类似物：把既有微调/自训练步骤封装为可调用工具，置于一个小型可学习路由器之后，路由器额外拥有空操作与复用选项，用固定面板上的逐决策效用增量训练，并摊销报告路由器自身成本——对照固定总是适配的控制组，检验增益来自适配选择而非适配本身。 · [原文图](industry-rsi/assets/paper-figures/agentic-ttt-teaser.png)

- **[AutoData: Agentic Search for Pre-training Data Selection](https://arxiv.org/abs/2609.19754)**（Weco AI / University of Amsterdam，2026-09-17，支撑·无闭环）
  - 核心：把预训练数据选择表述为启发式工程：AIDE 式 LLM 代理在带特征标注的文档池上搜索由打分、分层与随机选择规则组成的程序空间。每个候选选集训练一个小代理模型，验证反馈（val-bpb 或下游 CORE）驱动搜索迭代，一夜完成；
  - 数字：一夜搜索所得选择算法优于人工设计管线——DCDS、困惑度过滤、RegMix 与默认 ClimbMix 排序——在 125M 到 897M 上取得最优 val-bpb，对全部基线的改善具统计显著性，并提升下游 CORE；
  - 代码：核验时未找到代码。
  - 点评：把该模式移植到技能库治理：让代理在技能库上搜索紧凑的选择器程序（打分、分层、随机保留），以小型冻结评估器为反馈，把胜出选择器留作技能库的垃圾回收器。 · [原文图](industry-rsi/assets/paper-figures/autodata-selection-loop.svg)

- **[ScienceIDE: Turning World's Scientific Codebase into Agent Learnable Environments](https://arxiv.org/abs/2609.19134)**（PhAI Labs / AItonomy Foundation / Qwen (Alibaba) / University of Oxford 等，2026-09-16，支撑·无闭环）
  - 核心：把科学代码仓库转换为可编程智能体环境：专家定义的案例与验收准则驱动任务生成、执行与校验；经过验证的交互轨迹作为统一底座供 SFT、RL 与评测使用。
  - 数字：用验证轨迹训练 PhAI-IDE-72B/9B/4B；
  - 代码：代码在 github.com/aitofound/ScienceIDE（许可证未核验）；
  - 点评：验收准则先行的做法可映射到 nanoRSI 的 fixture：从语料生成可执行的任务+验证器对，仅让验证过的轨迹进入改进循环。 · [原文图](industry-rsi/assets/paper-figures/scienceide-agent-environments.svg) · [仓库](https://github.com/aitofound/ScienceIDE)

- **[XPACE: Joint World and Action Modeling from Heterogeneous Experience](https://arxiv.org/abs/2609.17372)**（XPENG Robotics，2026-09-15，闭环）
  - 核心：共享视频 backbone 联合训练策略与世界模拟器；经 self-gradient-forcing 适配后，模拟器在专家演示周围渲染偏离-恢复轨迹，过滤后用于 DAgger 式策略精调——在异构经验金字塔上形成世界模型驱动的自改进闭环。
  - 数字：真机 3 任务 × 20 试验：平均成功率 68.3%、进度 0.84，对照 DreamZero 40.0%/0.68、GR00T 6.7%/0.36；
  - 代码：arXiv 论文公开；
  - 点评：偏离-恢复配方是一种免环境数据生成器：重放已记录的 nanoRSI 候选轨迹，在接受解附近施加扰动，保留成功恢复的修复——不跑新环境就得到合成负例。 · [原文图](industry-rsi/assets/paper-figures/xpace-world-model-selfimprovement.png)

- **[NeoHorse-1: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness](https://arxiv.org/abs/2609.08183)**（TokenRhythm Technologies / Infinigence AI / Tsinghua University / Peking University 等，2026-09-08，闭环）
  - 核心：由异构模型池支撑的路由 harness 记录真实智能体流量中的能力需求信号；这些记录经结构校验、六维语义打分与子场景标注转为训练样本，路由分数编排三阶段 SFT 课程与路由引导的在线策略蒸馏，能力引导分配再依据评测反馈生成下一轮训练配比；
  - 数字：后训练使十个基准（六个智能体、两个代码、两个指令遵循）的宏平均从 4B 的 58.94 升至 64.87，9B 从 65.60 升至 69.04（底座为 Qwen3.5-4B/9B）；
  - 代码：代码已核验：github.com/TokenRhythm/NeoHorse（Apache-2.0，2026-09-04 创建），模型权重在 Hugging Face TokenRhythm NeoHorse-1 合集；
  - 点评：建议：在固定任务流上，以匹配的 token 预算比较能力引导的训练数据分配、均匀采样与冻结数据配比，并记录分配器的选择能否迁移到隐藏任务。 · [原文图](industry-rsi/assets/paper-figures/tokenrhythm-neohorse-1.svg) · [仓库](https://github.com/TokenRhythm/NeoHorse)

- **[Aspire: Can Models Self-Evolve from Vague Goals?](https://arxiv.org/abs/2608.31111)**（ByteDance Seed / Singapore University of Technology and Design / M-A-P / TokenWave.AI，2026-08-31，闭环）
  - 核心：智能体根据模糊目标选择数据、训练方法及父检查点，或修改框架。控制器核验谱系并冻结候选。
  - 数字：隐藏评测包含六个目标下的 520 道专家题。
  - 代码：论文及项目页公开；
  - 点评：拟议 nanoRSI learner 报告：分开记录候选原始变化与保留状态变化，导出失败尝试，并对比模糊目标与明确目标。 · [原文图](industry-rsi/assets/paper-figures/aspire-figure.png)

- **[From Self-Evolving Synthetic Data to Verifiable-Reward RL: Post-Training Multi-turn Interactive Tool-Using Agents](https://arxiv.org/abs/2601.22607)**（Tsinghua University / Eigen AI，2026-01-30，闭环）
  - 核心：层级多智能体引擎生成多样化的'合成-评测'计划对；工人智能体执行任务合成、任务验证、轨迹 rollout（带用户模拟器）与轨迹验证（把失败归因到任务或轨迹）；
  - 数字：Qwen3-235B-A22B-2507 + RL：tau2-bench Airline 73.0% pass^1（追平 Gemini 3.0 Pro、超 GPT-5 的 62.5%），Telecom 98.3%（已报告最优）；
  - 代码：示例代码在 github.com/inclusionAI/AReaL/tree/main/examples/tau2（CC BY-NC-SA 4.0——非商业条款，不得复制进 nanoRSI）。
  - 点评：对 nanoRSI：逐实例可执行检查器 + 修订任务生成器本身的反思环——最小自进化数据环同样需要这两个面（任务有效性、轨迹归因）。 · [原文图](industry-rsi/assets/paper-figures/eigendata-self-evolving-synthesis.png) · [仓库](https://github.com/inclusionAI/AReaL/tree/main/examples/tau2)

### 支撑性适应机制（7）

- **[Infinite-Parameter LLMs: Generating and Adapting Weights from Live Data](https://arxiv.org/abs/2609.18842)**（Boltzbit Limited / University of Cambridge，2026-09-16，支撑·无闭环）
  - 核心：超网络编码器把运行时交互数据编译为隐码并在线贝叶斯更新信念，再为冻结基座 FFN 生成 LoRA（r=8）权重增量——权重由数据再生成而非从存储库中选择，参数化无上界。
  - 数字：Qwen3-8B 冻结基座，MS MARCO（十段落）F1：data-to-weights 48.0 vs 上下文内 33.6 vs 闭卷 16.8；
  - 代码：arXiv 论文公开（CC BY-NC-ND 4.0）；
  - 点评：稀释边界启发 nanoRSI 实验：把长而噪的证据缓存为紧凑派生状态 vs 在上下文中重读，测量缓存开始胜出的交叉点。 · [原文图](industry-rsi/assets/paper-figures/infinite-parameter-weights-from-live-data.svg)

- **[CERA-MoA: Co-Evolving Routing Mechanisms with Continually Learning LLM Agents](https://arxiv.org/abs/2609.18779)**（Tsinghua University (IIIS) / Shanghai Jiao Tong University / Shanghai Qi Zhi Institute，2026-09-16，支撑·无闭环）
  - 核心：基于中层隐藏态的预测性熟悉度估计器驱动累积阈值自适应路由，只激活持续 RL 训练的 agent 中最小胜任子集以诱导特化，路由机制本身与学习者共同演化。
  - 数字：Qwen3-4B 九个分布内基准：ID 均值 63.2，对照 AT-GRPO 61.0、RouteMoA 53.1、裸模型 49.6；
  - 代码：arXiv 论文公开（CC BY 4.0）；
  - 点评：熟悉度估计器是 nanoRSI 技能路由的廉价信号：把任务路由到历史 rollout 看着熟悉的最小技能集，并把路由漂移记为技能过时的证据。 · [原文图](industry-rsi/assets/paper-figures/cera-moa-coevolving-routing.png)

- **[Doc-to-LoRA: Learning to Instantly Internalize Contexts](https://arxiv.org/abs/2602.15902)**（Sakana AI / Minerva University，2026-02-13，支撑·无闭环）
  - 核心：元训练后的超网络将文档激活映射为 LoRA 权重；师生蒸馏提供训练反馈，部署时复用适配器回答后续问题，无需重读文档或逐文档计算梯度。
  - 数字：在 2WikiMultihopQA 上，迭代式 D2L 报告归一化 ROUGE-L 为 0.844、额外更新显存 3.791 GB、延迟 0.551 秒；
  - 代码：官方代码为 MIT；
  - 点评：建议：后续探索版本化文档适配器作为记忆后端，并与检索方案比较事实保留能力。 · [原文图](industry-rsi/assets/paper-figures/sakana-doc-to-lora.svg) · [仓库](https://github.com/SakanaAI/doc-to-lora)

- **[TRINITY: An Evolved LLM Coordinator](https://arxiv.org/abs/2512.04695)**（Sakana AI / Institute of Science Tokyo / University of Michigan，2025-12-04，支撑·无闭环）
  - 核心：Sep-CMA-ES 扰动小型协调器头，以任务终局结果评分并重组候选参数；保留的协调器反复选择模型及思考者、执行者或验证者角色，底层基础模型权重保持固定。
  - 数字：LiveCodeBench v6 上，取消输出长度限制且不重新训练协调器时，pass@1 为 86.2%，GPT-5 为 83.8%。
  - 代码：论文公开；
  - 点评：建议：在相同 token 预算下比较小型可进化角色/模型路由器与静态路由。 · [原文图](industry-rsi/assets/paper-figures/sakana-trinity.svg)

- **[Learning to Orchestrate Agents in Natural Language with the Conductor](https://arxiv.org/abs/2512.04388)**（Sakana AI / University of Michigan / Institute of Science Tokyo，2025-12-04，支撑·无闭环）
  - 核心：一个 7B 模型（Qwen2.5-7B）经 200 轮 GRPO 训练，以三张 Python 列表输出完整协调策略——工人模型 ID、自然语言子任务指令、访问列表——从而学会在更强的工人之间设计通信拓扑并为其提示工程，以随机化智能体池上的任务奖励端到端训练。由于 Conductor 可以把自己也指定为工人，发现的拓扑可递归嵌套，实现动态测试时扩展。
  - 数字：Conductor（7B 协调 GPT-5/Claude/Gemini 级工人）：LiveCodeBench 83.93、GPQA-D 87.5、AIME25 93.3、均值 77.27——高于 GPT-5（74.78）与任一单工人；
  - 代码：Conductor 论文称基座与数据集公开，未找到独立代码仓库。
  - 点评：对 nanoRSI：'协调即习得技能'——若存在候选 harness 种群，一个训练出的小型选择器（可把自身纳入编排）是可与规则选择对照的廉价种群级元控制器。 · [原文图](industry-rsi/assets/paper-figures/sakana-conductor.svg)

- **[Discovering state-of-the-art reinforcement learning algorithms](https://pmc.ncbi.nlm.nih.gov/articles/PMC12695655/)**（Google DeepMind，2025-10-22，支撑·无闭环）
  - 核心：元网络提供策略和预测的更新目标；元梯度优化智能体总体回报，更新后的规则用于后续智能体；
  - 数字：扩展数据图4报告：在57个Atari游戏、2亿环境步的比较下，以约少40%的评价阶段TPU计算达到MuZero最终表现；
  - 代码：已确认官方元训练、评价代码及Disco103元参数。
  - 点评：建议实验：区分学习器权重与更新规则参数，先在小型环境中验证外层目标，再扩大规模。 · [原文图](industry-rsi/assets/paper-figures/google-discorl-2025.png) · [仓库](https://github.com/google-deepmind/disco_rl)

- **[Self-Evolving LLMs via Continual Instruction Tuning](https://arxiv.org/abs/2509.18133)**（Beijing University of Posts and Telecommunications / Tencent AI Lab，2025-09-14，支撑·无闭环）
  - 核心：连续指令微调更新任务专属与共享 LoRA 专家，任务感知对抗判别器帮助区分可迁移知识及任务特有信息；保留的专家将旧知识带入后续任务。
  - 数字：论文评估连续学习及腾讯内容审核应用。
  - 代码：已核验 BAI-LAB/MoE-CL 公开实现。
  - 点评：拟议 nanoRSI learner 对照：固定外部任务流，保留各任务退化分数，区分持续学习与直接自我改进。 · [原文图](industry-rsi/assets/paper-figures/tencent-moe-cl.png) · [仓库](https://github.com/BAI-LAB/MoE-CL)

### 技能-权重共进化（5）

- **[CoEvo-RSI: When Harnesses Evolve, Which Models Should Follow?](https://arxiv.org/abs/2610.25078)**（National University of Singapore / Agency for Science, Technology and Research (A*STAR) / SenseTime Group Inc.，2026-10-20，闭环）
  - 核心：带双向历史继承的模型-harness 协同演化。共享演化档案保存历史 harness 设计、模型检查点与结果；
  - 数字：仅用自身拒绝采样轨迹的 SFT，CoEvo-RSI 使 Qwen3.5-9B 在三个垂直应用（多智能体失败归因、角色感知 text-to-SQL、智能家居指令跟随）上与更大模型竞争：在 TraceElephant 上超过 DeepSeek-V4-Pro（+14.16 agent 准确率），在 HomeBench VM 上超过 GLM-5.3（+4.90 成功率）；
  - 代码：仓库 github.com/SuJQ0722/CoEvo-RSI（README 题为 CoEvoX）已上线，但核验时无 LICENSE 文件——按保留所有权利处理；
  - 点评：每代追踪廉价的接口失配代理量（如 runner 拒绝/重试动作率），使 harness 侧编辑与轻量参数侧仅在失配上升时配对； · [原文图](industry-rsi/assets/paper-figures/coevo-rsi-framework.png) · [仓库](https://github.com/SuJQ0722/CoEvo-RSI)

- **[AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents](https://arxiv.org/abs/2610.20474)**（Northeastern University (China) / AgiBot / University of Chinese Academy of Sciences，2026-10-14，闭环）
  - 核心：回答“自改进具身系统何时该改执行器权重”：编码智能体先改进技能与 harness；再从保存的状态重试失败子步骤做失败归因（失败在调用方式还是能力本身）；
  - 数字：在 RoboCasa365 全部 50 个目标任务（各 50 场景）上，以 GR00T N1.5 为执行器、无人类演示：AdaRSI 在三个套件上均提升 VLA，未见组合任务成功率从 4.6% 升至 13.8%。
  - 代码：HTML 全文未找到代码或仓库链接。
  - 点评：“先改 harness、只对持续不可靠子步骤改权重”的边界正是 nanoRSI 冻结执行器教义所在：将来任何权重侧实验臂都应照抄这种“先归因再微调”的闸门（从保存状态重试），而不是失败即微调。 · [原文图](industry-rsi/assets/paper-figures/adarsi-on-demand-pipeline.jpg)

- **[Which Skill to Distill? SGUID: Selecting a Compact Skill Bank for Model-Skill Co-Evolution](https://arxiv.org/abs/2610.12367)**（New York University / Amazon，2026-10-08，闭环）
  - 核心：每轮协同演化先从当前策略经验证器检查的 rollout 中策展候选技能库，带全库跑一次蒸馏并记录逐技能训练动态信号，只保留早期贡献为正、后期正信号不少于 h、贡献衰减率被 tau 界住的技能，再从本轮基础权重重启、只蒸馏精选小库；更新后策略的 rollout 为下一轮库供种。
  - 数字：6,400 次检索日志中，少于 25% 的被检索技能产生有用蒸馏信号（Qwen3-1.7B 21.2%、Qwen3-4B 19.7%、Qwen3-8B 6.4%）。
  - 代码：尚无公开代码（"论文录用后"发布）。
  - 点评：逐技能效用日志可在 nanoRSI 技能轨落地为审计：给每次闸门决定标注当时上下文中的技能，统计各技能与接受/拒绝候选的共现频率。 · [原文图](industry-rsi/assets/paper-figures/sguid-skill-selection-loop.png)

- **[SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning](https://arxiv.org/abs/2602.08234)**（University of North Carolina at Chapel Hill / University of Chicago / UC San Diego / NEC Labs America 等，2026-02-09，闭环）
  - 核心：从轨迹蒸馏出分层 SkillBank（通用策略 + 按嵌入相似度检索的任务技能），在 rollout 中以上下文形式使用，同时用 GRPO 训练策略——技能库本身持续共进化：每个验证 epoch 后，失败轨迹类别触发技能生成/精炼（每轮最多 3 个新技能），技能与权重互相成就。技能蒸馏压缩上下文 10-20 倍。
  - 数字：ALFWorld 总成功率 89.9% 对 GRPO 77.6%（绝对 +12.3；
  - 代码：代码在 github.com/aiming-lab/SkillRL（MIT，核验时 976 星）。
  - 点评：对 nanoRSI：这是技能轨与模型轨之间缺失的桥梁——先让技能对照冻结 rollout 基线验证，再让库与学习器共进化，并记录两侧各自贡献。 · [原文图](industry-rsi/assets/paper-figures/skillrl-skill-augmented-rl.png) · [仓库](https://github.com/aiming-lab/SkillRL)

- **[Reinforcement Learning for Self-Improving Agent with Skill Library](https://arxiv.org/abs/2512.17102)**（AWS Agentic AI (Amazon) / University of Wisconsin-Madison，2025-12-18，闭环）
  - 核心：技能增强 GRPO：智能体定义并调用函数式技能（CodeAct 风格，沿用 DynaSaur），顺序 rollout 让同一智能体跨相似任务链执行，任务一生成的技能在任务二被复用——后续技能使用的成功奖励把信用回传给更早的技能生成。技能整合奖励为'生成的技能被成功复用'与'成功使用检索到的技能'加成。
  - 数字：AppWorld（Qwen2.5-32B-Instruct）：对基线 GRPO，Scenario Goal Completion +8.9%、交互步数少 26%、token 少 59%（Test Normal 60.7% 对 51.8% SGC，1,475 对 3,613 token；
  - 代码：工件在 github.com/amazon-science/SAGE（23 星；
  - 点评：对 nanoRSI：在相关任务链上而非孤立回合评估技能，并把奖励信用回传给生成技能的步骤——直接回答'生成的技能如何被选择'。 · [原文图](industry-rsi/assets/paper-figures/sage-skill-augmented-grpo.png) · [仓库](https://github.com/amazon-science/SAGE)


## 3. 自评估 / Self-evaluation（9 条）

### 验证器与奖励进化（6）

- **[Recursive Reward Improvement via Adversarial Meta-Prompt Evolution](https://arxiv.org/abs/2610.21040)**（Massachusetts Institute of Technology / Microsoft Research / Johns Hopkins University，2026-10-15，闭环）
  - 核心：面向无标准答案专业任务（临床报告生成）的提案者-求解者 RSI 环：提案者从医学参考资料生成任务与带权重的评分量表（rubric）；冻结的对抗者对每个任务作答两次——一次钻空子、一次诚实作答——修复步骤重写量表，只保留能将诚实答案排在钻空子答案之上的条目；
  - 数字：HealthBench Professional（带检索的调整分）：RRI 相对 Generation Only 在 9B 上 +10.9 分、27B 上 +12.4 分（27B 未训练 0.374 在 Generation Only 下仅 +1.8，RRI 下 +14.2）；
  - 代码：代码 Apache-2.0，位于 github.com/DDVD233/RRI（2026-10-19 经 raw.githubusercontent.com 核验许可文件）。
  - 点评：“攻击-修补-准入”是 nanoRSI 的评测器审计原语：在信任按判分标准测得的增益前，先要求对抗者产出钻空子产物，核验判分标准将诚实产物排在漏洞产物之上； · [原文图](industry-rsi/assets/paper-figures/rri-overview.png) · [仓库](https://github.com/DDVD233/RRI)

- **[EvoRS: On-Policy Self-Evolution of Reward Systems for Open-Ended Reinforcement Learning](https://arxiv.org/abs/2609.12459)**（Fudan University / Nankai University / Hello Group，2026-09-11，闭环）
  - 核心：奖励系统本身即进化对象：一个可执行的 Reward-DAG，其评分规则节点（判据 + 打分机制）与组合算子共同定义 RL 奖励。每 N 次策略更新，一个智能体设计器读在线策略 rollout 与节点级奖励轨迹，诊断有效性/覆盖/信息量失败并提议有界类型化编辑；
  - 数字：WritingBench 57.001 对基线 54.894（+2.107，三评审均值：GPT-5.6-Terra/DeepSeek-V4-Pro/GLM-5.2），且是唯一黑客率低于基线的方法（6.5 对 7.7）；
  - 代码：未找到代码发布，仅有论文。
  - 点评：对 nanoRSI：评估器一侧同样可以进化——把奖励定义版本化为 DAG，设计器提议类型化编辑，且只在相同 rollout 上做匹配回放对比后接受； · [原文图](industry-rsi/assets/paper-figures/evors-reward-evolution.png)

- **[Self-Trained Verification for Training- and Test-Time Self-Improvement](https://arxiv.org/abs/2605.30290)**（Carnegie Mellon University，2026-05-28，闭环）
  - 核心：利用'模型无法冷诊断自身错误、但看到参考解就可以'的不对称性。参考条件化验证器（教师）通过 (verdict, feedback) 分布的在线策略蒸馏 + 对照真值的 verdict-RL 项监督无条件化学生；
  - 数字：困难数学上准确率约翻倍（末轮 Hardest 5.5% 对 Qwen3-32B 流水线 2.7%）；
  - 代码：代码在 github.com/AR-FORUM/stv（Apache-2.0，核验时 11 星）；
  - 点评：对 nanoRSI：让验收验证器模仿自身'参考条件化'的判断来训练，再用这个自训练验证器闸门每个候选变更——用廉价的学习型检查器直接强化冻结评估器不变量。 · [原文图](industry-rsi/assets/paper-figures/cmu-stv-self-trained-verification.svg) · [仓库](https://github.com/AR-FORUM/stv)

- **[EvoLM: Self-Evolving Language Models through Co-Evolved Discriminative Rubrics](https://arxiv.org/abs/2605.03871)**（University of Washington / Allen Institute for AI / University of Pennsylvania，2026-05-05，闭环）
  - 核心：规则生成器输出逐实例的自然语言评判标准，小至 0.6B 的冻结评判者据此给策略打分；生成器以二元判别奖励（评判者能否正确排序由策略自身前后检查点经时间对比构成的偏好对）经 GRPO 训练，生成器与策略交替共进化并配回放缓冲——无人类标注、外部奖励模型或更强教师。
  - 数字：Qwen3-8B 生成器在 RewardBench-2 上超过 GPT-4.1 规则 25.7%；
  - 代码：代码在 github.com/stellalisy/EvoLM（许可证未核验）；
  - 点评：时间对比可直接移植：用 nanoRSI 冻结版对候选版的输出构造偏好对，训练小规则评分器作为替代逐候选全滚动的廉价闸门（扩展 ADOPTION 第 19 项）。 · [原文图](industry-rsi/assets/paper-figures/evolm-coevolved-rubrics.png) · [仓库](https://github.com/stellalisy/EvoLM)

- **[A3: An Automated Alignment Agent for Safety Finetuning](https://alignment.anthropic.com/2026/automated-alignment-agent/)**（Anthropic / Anthropic Fellows Program / Constellation，2026-03-11，闭环）
  - 核心：Agent 生成失败假设、划分数据，再依据实验日志与评测反馈调整 LoRA 超参数和数据权重；控制器改进的是目标模型，而非控制器自身权重。
  - 数字：在 Qwen-2.5-7B Instruct 上，外部迎合性评测从 68.0% 降至 42.0%，MMLU-Pro 从 52.9% 变为 52.4%（报告表 1）；
  - 代码：Apache-2.0 代码、配置与数据目录公开；
  - 点评：可为课程实验加入能力保持约束，并保留真正冻结的最终测试集。 · [原文图](industry-rsi/assets/paper-figures/a3.png) · [仓库](https://github.com/safety-research/A3)

- **[DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning](https://arxiv.org/abs/2511.22570)**（DeepSeek-AI，2025-11-27，闭环）
  - 核心：验证器为生成器训练提供奖励；提高验证计算量，自动标注新生成的难验证证明，再训练验证器。
  - 数字：作者报告经专家评估后 Putnam 2024 得分 118/120。
  - 代码：推理代码、提示词/预测及 685B 权重公开；
  - 点评：拟议 nanoRSI learner 适配器：分别版本化生成器、验证器、标签及专家审计，对比共同训练与冻结验证器。 · [原文图](industry-rsi/assets/paper-figures/deepseek-math-v2.svg) · [仓库](https://github.com/deepseek-ai/DeepSeek-Math-V2)

### 反馈审查与编排（2）

- **[Verifier-Harness Co-Evolution for Training-Free Self-Improvement on Open-Ended Tasks](https://arxiv.org/abs/2610.17609)**（Oregon State University / Pennsylvania State University / AG2 AI / Johnson & Johnson，2026-10-13，闭环）
  - 核心：免训练地把可执行验证器程序 V=（打分器组、聚合器、诊断器）与 agent 的 harness 状态共同演化。验证器候选由挖掘到的'Actor 对更大冻结模型'响应对比（恰好差一个目标缺陷族的响应对）合成，按驱动力选择——候选在最弱对比族上的判别力（对比族上的 maximin；
  - 数字：开放式偏好（平局调整、Qwen3.5-397B 评审）对匹配的直接生成：Qwen3-8B 平均 59.00%、Qwen3.8-27B 57.19%（最佳基线 49.26/51.60），12 个基准×Actor 设置全胜（Arena-Hard、WritingPrompts、WildBench、WritingBench、MultiChallenge、RefineBench）。
  - 代码：论文所列代码 URL（github.com/tianyi0216/Unified-Co-Evolution）核验时（2026-10-15）404——按未发布对待。
  - 点评：对比族 maximin 选择与'W>L 且带容差'替换规则是 nanoRSI 评测器轨道现成的闸门准则：候选验证器只有在任何对比族不更差且总体严格更好时才替换在位者——是 ADOPTION 第 44 项锚定参考一致性检查的可计算类比。 · [原文图](industry-rsi/assets/paper-figures/ucoe-verifier-harness-coevolution.svg)

- **[Who Verifies the Verifier? Co-Evolving Inspectable Graders with Self-Improving Agents](https://arxiv.org/abs/2610.11464)**（Amazon Web Services / HSBC，2026-10-08，闭环）
  - 核心：把校验器本身作为演化对象：一个由小型、多为确定性的缺陷检测器合成的可检查表达式，检测器从聚类失败中合成、出生即受闸门约束，表达式按与锚定的十例参照集的一致性加未标注输出上的共识来选择——绝不按 agent 分数选择。协同演化系统（Double Ratchet）把该校验器与带生命周期的技能循环配对；
  - 数字：在 MBPP+ 上，演化校验器每个种子都达到 0.625+-0.050 保留一致率，高于手写种子 0.417+-0.058（+0.21）与其内含的裸 LLM judge 0.55+-0.04。
  - 代码：代码：arXiv 页与 HTML 均未找到。
  - 点评：直接塑造 nanoRSI 闸门量测：除下游分数外一并报告校验器效度（与锚定参照集的保留一致率），保留全通过评分器臂作为诚实零假设，并为每次过闸变更记录检测器级来源——把条目 40 的量测闸门字段扩展出技能分数无法作证的效度轴。 · [原文图](industry-rsi/assets/paper-figures/whoverifies-verifier-expression.svg)

### 技能文件优化与技能库（1）

- **[Small but Mighty: Test Suites as Improvement Signals for Self-Evolving Agents](https://arxiv.org/abs/2610.15964)**（Virginia Tech / NEC Laboratories America，2026-10-11，闭环）
  - 核心：演化小型可执行测试套件，作为自编辑 harness 代码的接受/拒绝信号。质量-多样性搜索按套件规模生态位维护（覆盖率、变异得分）的帕累托前沿，让小而强的套件存活；
  - 数字：129 个 TestGenEval Python 模块、3 骨干（GPT-5.4、Claude Opus 4.8、Gemini 3.1 Pro）：行为改变型重写的拒绝率 59.9% 对仓库测试的 25.3%，逐模块全面更优；
  - 代码：代码/数据 MIT 许可，位于 github.com/ccsnow127/TeSearch（LICENSE 已于 2026-10-15 核验）。
  - 点评：对 nanoRSI 的核心迁移：用专门演化出的小套件而非任务自带测试来闸自编辑——套件先在父代跑通再判子代，提供带实测误拦率的行为保持检查（TeSearch 的 4.0% 即参考值）。 · [原文图](industry-rsi/assets/paper-figures/tesearch-test-suite-signals.png) · [仓库](https://github.com/ccsnow127/TeSearch)


## 4. 自动研究 / Auto Research（59 条）

### 分析与审计（21）

- **[LLM Evolutionary Search Strategies Should be Compared by Tokens](https://arxiv.org/abs/2610.23977)**（IBM Research，2026-10-20，支撑·无闭环）
  - 核心：对 LLM 演化式代码搜索的度量标准审计。重放 5 个任务、3 种方法的 600 份日志（研究对象含 OpenEvolve），指出提案计数掩盖真实成本：每提案 token 从 16k 到 39k 不等，等提案比较等于悄悄给某些方法 1.9 倍算力、给演化约 6 倍于独立采样的预算。
  - 数字：等 token 下演化优势基本消失：15 个任务-方法对中 12 对演化对独立采样的优势不超过 5%，仅 3 对保留 23-28% 优势且全在同一任务（Heilbronn）；
  - 代码：核验时论文未给出代码或日志发布；
  - 点评：直接约束本仓库证据账本：逐候选记录 token 成本，一切选择器/闸门比较按等 token 预算执行（绝不按等尝试数）——token 列已存在，这是报告与协议修正而非新机制。 · [原文图](industry-rsi/assets/paper-figures/token-parity-cost-bars.png)

- **[Self-Evolving Agents Can Repair Failures but Struggle to Generalize from Them](https://arxiv.org/abs/2610.22984)**（Harbin Institute of Technology / The Chinese University of Hong Kong，2026-10-19，支撑·无闭环）
  - 核心：审计设定“冷启动仅失败演化”（CFOE）：智能体从空外部状态出发，只从失败的在线交互中学习——无既有经验、无标准答案、无专家解、无验证器反馈。审计在四个交互环境（ALFWorld、tau2-Bench-Verified、WebArena-Verified、WebShop）与多个 LLM 骨干上运行三种既有自演化范式（ReasoningBank 式记忆累积、SkillOpt 式技能编辑、Evo-Harness 式 harness 修改），并用人雇标注者研究经验更新如何出错。
  - 数字：一致的修复-泛化鸿沟：失败来源的经验能提高先前失败任务的复原率，却很少在未见留出任务上带来持续增益，跨全部范式、骨干与环境成立。
  - 代码：论文 HTML 中未发现仓库链接（2026-10-20 核验）；
  - 点评：给 nanoRSI 证据账本加一个直接指标：把每次闸门决定拆成修复效应（编辑修好的失败任务）与迁移效应（留出任务），两者并报； · [原文图](industry-rsi/assets/paper-figures/cfoe-fig1.png)

- **[The Self-Improvement Problem](https://arxiv.org/abs/2610.21646)**（German Research Center for Artificial Intelligence (DFKI) / RPTU Kaiserslautern-Landau，2026-10-15，闭环）
  - 核心：把安全自改进形式化：智能体是程序、改进是未必可计算的语义分数，而任何自动闸门（奖励模型、回归测试套件、自动评审）都必须是可终止的可计算过程。研究两种评估抽象——批准/拒绝更新的证明器（certifier）与在给定提案生成器下输出改进候选的搜索过程。
  - 数字：无实验（理论）。
  - 代码：形式化证明代码位于 github.com/Brian-Moser/SelfImprovementProof（许可尚未核对）。
  - 点评：这是 nanoRSI 闸门教义的理论支柱：冻结面板、有限提案预算与有界评测器正是保证得以恢复的可判定机制——而“有界分数升、真实分数降”的极限，正是反事实面板与留出 freeze/final-test 存在理由的形式化表述。 · [原文图](industry-rsi/assets/paper-figures/selfimprovement-problem-impossibility.svg) · [仓库](https://github.com/Brian-Moser/SelfImprovementProof)

- **[Trace Evolution Bench: Measuring Whether Agents Improve from Their Own Environment Traces](https://arxiv.org/abs/2610.15055)**（MatrixOrigin，2026-10-10，支撑·无闭环）
  - 核心：这是测量协议而非新改进器：三套冻结的 80/20/40 任务包（办公、编码、制造；各 n=40 留出），锁定的留出 id 永不进入 evolve()，带接受/回滚的验证闸（min_delta=0），温度 0 下 R=3 轮；
  - 数字：编码赛道（主记分板）：DeepSeek 文本更新 9 格中 7 格超过自身种子带（gepa_llm 种子 42/43 各 +15.0；
  - 代码：运行器、表格契约、三套任务包、运行配置与绘图随论文发布（托管端点需自备 API key）；
  - 点评：TEB 用更锋利的工具外部验证了 nanoRSI 的噪声带纪律：种子配对超额对自身四遍带正是 ADOPTION 第 38/39 项规定的接受门槛； · [原文图](industry-rsi/assets/paper-figures/teb-trace-evolution-bench.svg)

- **[Pre-Registered Genesis Accounting for Recursive Self-Improvement: First Audited Operator-Genesis Events in a Physics-Discovery Runtime](https://arxiv.org/abs/2610.14843)**（HoomanBio AI Lab, Huaman Biotechnology (Beijing)，2026-10-10，支撑·无闭环）
  - 核心：面向 RSI 主张的两级预注册记账：M1 统计设计者词表内生成的结构实例（四个谱系族）；M2 统计机器自著的算子类型——运行时自行组合并注册进自身词表的新算子，仅在留出验证证书下准入（组合 R² 须在留出数据上跨过 τ = 0.999）。
  - 数字：最佳标准库变换 inv(n)：留出 R² −0.546；
  - 代码：未声明代码发布；
  - 点评：M1/M2 两分可直接采纳为 nanoRSI 证据账本词汇：分开统计（M1）起始模板设计者词表内生成的变体——提示/技能/参数编辑——与（M2）循环自著、运行时词表原本不包含的机制，后者仅在留出验证证书下准入； · [原文图](industry-rsi/assets/paper-figures/genesis-preregistered-accounting.png)

- **[Does Failure Feedback Direct Agent Self-Modification?](https://arxiv.org/abs/2610.14662)**（Independent (no affiliation stated)，2026-10-10，支撑·无闭环）
  - 核心：度量失败反馈是否真的引导自修改：在同一子代修改内部，比较随机抽取的目标失败的修复与父代其余失败的修复。研究一审计六条公开 Darwin Gödel Machine 运行日志（SWE-bench Verified 与 Polyglot 上的 DGM / 固定编辑器 / 无档案）：145 处合格的任务条目修改（子代可用且目标被评测）；
  - 数字：公开 DGM 日志中无可检出的目标特异优势：修复目标 12 处对期望 16.4（e 值 0.15、优势比 0.69）——失败反馈未将修复引向目标，与随机无异。
  - 代码：arXiv 源码附带分析/实验代码、派生数据、README 与 prereg/prereg_v2.md；
  - 点评：nanoRSI 应按修改采纳三个报告轴：目标修复（被引用的失败是否真被修复）、向相关失败的迁移、留出净变化——目前证据账本只记面板增量，不记被反馈的失败是否就是被修复的那个。 · [原文图](industry-rsi/assets/paper-figures/dgm-failure-feedback-audit.svg)

- **[MC-EvoBench: Auditing Experience-Driven Self-Improvement in Minecraft Agents](https://arxiv.org/abs/2610.13829)**（Shanghai Jiao Tong University / University of the Chinese Academy of Sciences / South China University of Technology / Huazhong University of Science and Technology 等，2026-10-09，支撑·无闭环）
  - 核心：一个把真实能力变化与携带资源、曝光与运气隔离的受控基准：配对评估先跑源交互，冻结声明的 agent 工件（记忆、提示、检查点），重置目标世界与物品栏，只允许该工件跨边界。三个图对齐探针族（木种合成、木器与石器迁移）在匹配预算与五个种子下比较无先验、相关、无关与打乱源四种条件，报告带出处的 TSR、WGP、VMP；
  - 数字：未发现稳定迁移：石器探针上相关条件 TSR/WGP/VMP 为 0.050/0.021/0.200，低于无先验的 0.150/0.082/0.533（相关反而更差）；
  - 代码：代码：github.com/xzw-ustc/mc-bench-open-source，MIT 许可（80 任务、19 条能力链、12 套环境配置、支持合成干跑与真实 MineRL，含文档与测试；
  - 点评：只允许声明工件跨界的「源交互 → 重置目标」配对协议是 nanoRSI 训练/验证/冻结切分的具身对应物； · [原文图](industry-rsi/assets/paper-figures/mc-evobench-paired-evaluation.png) · [仓库](https://github.com/xzw-ustc/mc-bench-open-source)

- **[AgentSWE: Can Coding Agents Build the Agent You Actually Want?](https://arxiv.org/abs/2610.13361)**（Beijing Academy of Artificial Intelligence / Institute of Automation, Chinese Academy of Sciences / Renmin University of China，2026-10-09，支撑·无闭环）
  - 核心：面向「造 agent 的 agent」的委托式基准：25 个任务覆盖三个生命周期阶段——从自然语言需求从零创建完整 agent（10）、编辑 Aider/OpenHands/Codex 等生产级 agent 代码库（10）、朝 BrowseComp 与 OSWorld 等可测目标优化（5）。构建者只能对照示例开发用例迭代；
  - 数字：跨模型与 harness，没有一个接近交付需求：50 次 Creation 运行平均 11.2/100，其中 20 次得零分；
  - 代码：代码：github.com/VectorSpaceLab/AgentSWE，Apache-2.0（任务、runner、工具、可安装 CLI 含 setup/run/freeze 命令、经 Harbor 的钉版 Docker 环境）；
  - 点评：「演示水平-交付水平」差距是 nanoRSI 冻结面板纪律的外部印证：构建者看得到开发用例，冻结交付物面对留出评分——与 nanorsi baseline/freeze/final-test 同构。 · [原文图](industry-rsi/assets/paper-figures/agentswe-commission-evaluation.svg) · [仓库](https://github.com/VectorSpaceLab/AgentSWE)

- **[What Output-Only Review Cannot Verify: Study Contracts for Research Agents](https://arxiv.org/abs/2610.11754)**（Imperial College London，2026-10-08，支撑·无闭环）
  - 核心：研究契约把输出评审看不到的三样东西——声明的实验选择、运行义务、声明范围——绑定到留存的执行证据，并把这种'相对契约的验证'与科学真理区分开。确定性检查器对已批准与已执行对象施加一条注册的、针对特定故障的规则；
  - 数字：在八对自制的干净/变异研究上，施加注册故障规则的确定性检查器检出全部八处注册变异。
  - 代码：代码：未找到；
  - 点评：该思路与 nanoRSI 证据账本一一对应：在承认一项声称的改进前，把声明的选择、运行义务与声明范围绑定到留存的执行证据，并把'对契约可验'当作不同于'为真'的属性——具体做法是对已批准与已执行对象按摘要闸门，并以隐去标签条件下的评审决策作为诚实性探针。 · [原文图](industry-rsi/assets/paper-figures/study-contracts-abs-crop.png)

- **[How Is Automated Research Evaluated? A Survey of Benchmarks and Evaluation Practices](https://arxiv.org/abs/2610.11877)**（University of Macau，2026-10-08，支撑·无闭环）
  - 核心：综述自动化研究系统在六个目标上的评测方式——文献综合、研究构思、可执行工作流、学术写作与传播、自动同行评审、端到端研究——比较任务构造、证据来源、评测者与打分流程，并按声明强度组织代表性工作。
  - 数字：三条反复出现的经验：输出检查、过程检查与人类研究提供互补信息；
  - 代码：代码：无。
  - 点评：把其声明强度阶梯用作 nanoRSI 效果研究的自查模板：写明哪些结论只依赖输出检查、哪些附加过程证据、哪些带预算与尝试选择记账——把综述第三条经验对齐到证据账本既有的预算字段。 · [原文图](industry-rsi/assets/paper-figures/research-eval-claims-pyramid.svg)

- **[TestJack: Should you trust the results in coding benchmarks? Agentic Coding Benchmarks Auditing via Evaluator Evolution](https://arxiv.org/abs/2610.10619)**（Columbia University / University of California, Berkeley / George Mason University，2026-10-07，支撑·无闭环）
  - 核心：不是在任何尝试之前一次性加固基准，而是逐次尝试动态审计：针对补丁可能违反的提示要求生成测试，仅保留真值补丁能通过的测试，并对失败复核，使每个确认的失败都有可重放的测试背书。轻量变体只深审随机抽样的尝试，再把所得测试复用到该任务全部尝试上。
  - 数字：对五个基准、六个前沿后端共 8,862 次尝试中 4,487 次基准判过的尝试做审计，驳回 1,545 次（34.4%）违反任务要求，使总体解决率从 50.6% 降到 33.2%（逐基准驳回率：DeepSWE 43.5%、SkillsBench 18.2%、SWE-Marathon 53.6%、SWE-bench Verified 7.6%、SWE-bench Pro 29.2%）。
  - 代码：代码：anonymous.4open.science/r/testjack-C1A7（匿名工件，核验时未去匿名）。
  - 点评：直接喂给 nanoRSI 评测器完整性：在 coding 轨为冻结面板生成以任务要求为锚的测试，且测试必须先通过参考实现才准入； · [原文图](industry-rsi/assets/paper-figures/testjack-auditing-overview.svg)

- **[RSIGym: A Flexible Environment for Recursive Self-Improvement](https://arxiv.org/abs/2610.10310)**（Evolvent AI / National University of Singapore，2026-10-07，支撑·无闭环）
  - 核心：一个代理原生的'一切即服务'研究环境：训练、推理、采样、评测与沙箱执行以服务形式暴露，共享权限与预算记账。研究代理在三种轨道——数据、harness 或联合——下对目标系统迭代'生成数据-训练检查点-评测-分析修订'循环，并提交选定的模型加 harness 接受官方评测。
  - 数字：六个前沿研究模型在每基准运行 500 美元平台服务预算的独立联合轨道下，Opus 5 取得最高 RSI-Index 0.4809，其提交系统把 SWE-bench Verified 从 17.67% 提到 50.33%、AIME 从 31.67% 提到 97.78%。
  - 代码：代码：github.com/evolvent-ai/RSIGym 公开（创建于 2026-10-05，截至 2026-10-12 共 64 星），但标准路径下均无 LICENSE 文件——尽管声称开源，仍按保留所有权利对待。
  - 点评：值得借鉴的报告纪律是预算归一化改进：逐面板写明初始与提交分数及每次运行消耗的服务预算，使 nanoRSI 实验报告单位成本增益而非仅增益； · [原文图](industry-rsi/assets/paper-figures/rsigym-overview.png) · [仓库](https://github.com/evolvent-ai/RSIGym)

- **[How Do Agent Harnesses Create Value? Planning Information and Release Control in Stateful LLM Agents](https://arxiv.org/abs/2609.20474)**（The Chinese University of Hong Kong, Shenzhen / University of Edinburgh，2026-09-17，支撑·无闭环）
  - 核心：把 agent harness 的价值分解为规划引导、执行组织与完成检查，并在 τ²-bench 上用安慰剂式对照逐项度量：Fixed（预写的任务专属计划）对 Sham（词数与外壳匹配的打乱策略文本），差异即分离引导内容价值与单纯 token 量；另配只读终端验证器做放行控制。
  - 数字：在 265 个匹配单元上，Fixed 较 Sham 提升 oracle 验证成功率 7.17 个百分点（90% 任务聚类自助区间 1.15–13.36），集中于更高复杂度任务。
  - 代码：核验时未找到代码。
  - 点评：把安慰剂对照制度化：任何 nanoRSI harness 或技能改进都必须胜过词数匹配的打乱文本安慰剂，而不只是无引导基线； · [原文图](industry-rsi/assets/paper-figures/harness-value-planning.svg)

- **[Evolution or Illusion? Rethinking Evaluation in LLM Evolutionary Search](https://arxiv.org/abs/2609.19799)**（IBM Research，2026-09-17，支撑·无闭环）
  - 核心：面向 LLM 进化搜索的测量协议：不以领域惯用的单一预算配置（通常单种子固定迭代数）报告，而是跑满种子（宽度）×迭代（深度）网格，报告种子-迭代前沿，用等预算线使宽深权衡显式化。
  - 数字：在三种进化搜索策略（EvoX、OpenEvolve、AdaEvolve）与五个优化任务上：最优宽深拆分随策略、任务与总预算变化；
  - 代码：核验时未找到代码。
  - 点评：把前沿报告立为 nanoRSI 报告规则：进化对基线的比较先声明总预算，给出种子×迭代网格（或至少三个预算点），任何排名结论不得出自单一单元。 · [原文图](industry-rsi/assets/paper-figures/evolution-or-illusion-budget-grid.png)

- **[The Economics of Recursive Self-Improvement](https://arxiv.org/abs/2609.15802)**（METR / Stanford University / University of Virginia / Carnegie Mellon University 等，2026-09-14，支撑·无闭环）
  - 核心：非工作闭环：把 RSI 形式化为有向反馈环图的经济学模型。逐步加细的进展模型在 Jones 式自反馈之上引入 AI 能力存量 C 与核心环 A -> C -> A-hat（算法效率提升能力，能力反哺算法工作）；
  - 数字：校准而非基准：自持加速大致要求单位 AI 能力提升带来 15% 以上的 AI 研发生产率回报；
  - 代码：仅有 arXiv 预印本；
  - 点评：对 nanoRSI：把环弹性框架落成报告指标——测量每轮相对对照的边际回报（每改进轮的分数增量），让递归声明可量化而非口头断言； · [原文图](industry-rsi/assets/paper-figures/economics-of-rsi-2026.png)

- **[EvoHarnessBench: Can Your Agents Keep Pace with an Evolving Harness?](https://arxiv.org/abs/2609.04280)**（Salesforce Research / University of North Carolina at Chapel Hill / University of Wisconsin–Madison，2026-09-03，支撑·无闭环）
  - 核心：把非平稳性放进 harness 而非任务流的基准：17 条由带验证器的基准确定性构建的多阶段 harness 流（802 任务、520 工具、42 技能、62 代理）沿工具、技能、代理三个能力轴演化。两种评测模式分别隔离先前能力保持（部署评测）与积累经验效用（自进化适配），用相对前向/后向转移度量。
  - 数字：仅扩展 harness 就会损害已解任务——harness 诱发遗忘，相对 BWT 为 −5.3%（工具）、−4.0%（技能）、−34.7%（代理，部署版 Codex，ALE 环境，为观测最强）。
  - 代码：项目页（mas-orchestra.salesforceresearch.ai/evoharness）含 Colab 笔记本、演示与 Hugging Face 数据集；
  - 点评：为 nanoRSI 增加 harness 扩展回归测试：新工具/技能/代理进入冻结循环后，重跑全部先前任务并随前向增益一并报告后向转移，让破坏旧能力的新增能力可见。 · [原文图](industry-rsi/assets/paper-figures/evoharnessbench-framework.png)

- **[Self-Improvements in Modern Agentic Systems: A Survey](https://arxiv.org/abs/2607.13104)**（Jilin University / KAUST / University of Alberta / IDSIA/USI/SUPSI，2026-07-14，支撑·无闭环）
  - 核心：97 页综述，把自改进形式化为作用于智能体状态 (theta, Sigma) 的自诱导更新算子 A(t+1) = U(A(1:t), E(...))，其中脚手架 Sigma =（提示、记忆、工具、控制逻辑）；两条组织轴是更新目标（基础模型参数 vs 脚手架组件）与改进信号来源（内在生成演示、内在评价反馈、外在探索经验）。
  - 数字：无基准；
  - 代码：清单在 github.com/selfimproving-agent/awesome-Self-Improving-Agents；
  - 点评：对 nanoRSI：采纳'信号来源'轴（内在生成/内在评价/外在经验）作为标注候选变更的必填字段——它决定了哪种验收闸门是可行的。 · [原文图](industry-rsi/assets/paper-figures/self-improving-agents-survey.png) · [仓库](https://github.com/selfimproving-agent/awesome-Self-Improving-Agents)

- **[Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](https://arxiv.org/abs/2607.07663)**（DeepGrounding / AlphaAvatar / Illinois Institute of Technology，2026-07-08，支撑·无闭环）
  - 核心：覆盖 1,250 篇论文（2024-2026，74% 为 2026 年）的综述，两轴组织：改进对象（部署时自进化、训练时自迭代、自评估、自动研究）x 闭环程度（人在环内、人在环上、闭环）。承重贡献是四级验证层级——形式验证器 > 执行反馈 > 学习型裁判 > 内在信号——且已证实的自改进强度随层级递减。
  - 数字：无基准；
  - 代码：无代码仓库；
  - 点评：对 nanoRSI：把'验证层级'作为每个验收闸门的必填标签——nanoRSI 的冻结评估器是第 2 级（执行反馈），任何学习型裁判闸门都必须言明并度量自身漂移。 · [原文图](industry-rsi/assets/paper-figures/rsi-survey-taxonomy.png)

- **[Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap](https://arxiv.org/abs/2608.05179)**（Johns Hopkins University (per author page; affiliations not stated in the audited HTML)，2026-06-29，支撑·无闭环）
  - 核心：审计而非系统：从 arXiv/Semantic Scholar/OpenReview 取 144 条记录（2023-2026.6），去重得 125、筛入 35，对 24 个可运行的 AI 科学家系统按七维全文编码：生命周期阶段、自主层级、评测方法、发布工件、人环介入点、新颖性验证方法、结果选择披露。第二编码者对工件一致性 90%，但对自主性/新颖性/选择仅 50-65%。
  - 数字：24 个可运行系统中：83% 发布代码、71% 发布提示，但仅 38% 发布种子/执行轨迹、38% 报告任何新颖性验证方法、67% 披露结果选择策略；
  - 代码：未找到该综述的仓库；
  - 点评：对 nanoRSI：该清单与证据账本直接对应——种子/轨迹、选择披露与新颖性验证正是审计发现 62% 缺失的字段； · [原文图](industry-rsi/assets/paper-figures/ai-scientist-verification-gap.png)

- **[On the Generalization Gap in Self-Evolving Language Model Reasoning](https://arxiv.org/abs/2606.01075)**（Google Research / Harvard University / Virginia Tech，2026-06，支撑·无闭环）
  - 核心：受控研究而非新系统：同一指令微调模型经提示在确定性'骑士与骗子'任务（难度参数化）上同时扮演生成器与验证器；对验证器通过做阈值多数投票构造偏好对，离线训练 DPO。
  - 数字：Gemma 3 4B：自进化把 Pass@1 从 31.0% 提到 44.8%（课程式），但仍比 oracle DPO（53.3%）低 8-13 分；
  - 代码：未提及代码仓库。
  - 点评：对 nanoRSI：每个自改进声明同时报告 Pass@1 与 Pass@k——若 Pass@1 升而 Pass@k 平，说明环在'锐化'而非'学习'； · [原文图](industry-rsi/assets/paper-figures/gengap-self-evolution-taxonomy.svg)

- **[Contextual Drag: How Errors in the Context Affect LLM Reasoning](https://arxiv.org/abs/2602.04288)**（Princeton Language and Intelligence, Princeton University，2026-02-04，支撑·无闭环）
  - 核心：失败模式研究而非系统：在 11 个模型、8 个推理任务上比较干净生成与'条件于 1-2 个错误草稿'的生成（草稿取自强锚模型），每题 16 次生成、符号化答案校验；用树编辑距离量化结构性偏置；
  - 数字：上下文拖累造成 10-20% 的普遍性能下降；
  - 代码：代码在 github.com/princeton-pli/contextual-drag。
  - 点评：对 nanoRSI：任何把自身草稿回喂上下文的环，都必须测'拖累对照'（同一任务带与不带自身中间输出）； · [原文图](industry-rsi/assets/paper-figures/princeton-contextual-drag.png) · [仓库](https://github.com/princeton-pli/contextual-drag)

### AI 科学家系统（15）

- **[DiscoveryRSI: Recursively Learning to Discover Valuable Hypotheses](https://arxiv.org/abs/2610.23839)**（PhAI Labs / The Chinese University of Hong Kong / University of Michigan / National University of Singapore 等，2026-10-19，闭环）
  - 核心：多智能体演化搜索发展可检验假设的研究树，选中的计算调查被编译为携带输入、环境、必需输出与验证检查的可执行 Harbor 任务。三个耦合的递归机制复用保留的研究历史：假设信用优化把质量评估归因到有据可查的贡献并训练模型（DiscoveryRSI-27B）；
  - 数字：提出 DFM-Bench（假设、修订、发展路径、研究运行四层）。
  - 代码：Apache-2.0 仓库 github.com/Gen-Verse/DiscoveryRSI 已上线（2026-10-20 从 raw.githubusercontent.com main 读取 LICENSE）；
  - 点评：可移植的是 harness 重放：在 nanoRSI 证据账本上的派生视图，每 N 次运行后聚合跨尝试的反复失败模式，提出环路级改动（评测顺序、反馈格式）而非任务级编辑——可在既有工作区协议里作为二阶代测量。 · [原文图](industry-rsi/assets/paper-figures/discoveryrsi-fig1.png) · [仓库](https://github.com/Gen-Verse/DiscoveryRSI)

- **[SwarmRSI: Recursive Self-Improvement through Evolving Scientific Agent Swarm](https://arxiv.org/abs/2610.20431)**（Huawei Technologies / Leiden University / University of Groningen，2026-10-14，闭环）
  - 核心：演化科研智能体群体，使一个智能体的发现与实现能推进另一个智能体的研究。反馈引导群体变异用其他智能体的实验反馈同时精修假设及其实现（解决“结果差该改假设还是改实现”的归因歧义）；
  - 数字：在 OpenProblems 与 NatureBench 上 SOTA：Gemini 3.1 Pro Preview 下 OpenProblems 平均分 76.2，NatureBench 上 44.4% 任务追平已发表 SOTA（对比方法中最高的 Match-SOTA 率）；
  - 代码：未发现代码发布；
  - 点评：跨智能体互补组件复用是 nanoRSI 种群模式缺的模式：按组件验证把关的候选级部分程序合并是选择器研究的一个具体臂； · [原文图](industry-rsi/assets/paper-figures/swarmrsi-evolving-swarm.svg)

- **[Scaling Discovery Requires Forgetting](https://arxiv.org/abs/2610.20563)**（UC Berkeley / Stanford University / Bespoke Labs，2026-10-14，支撑·无闭环）
  - 核心：研究为何扩展 LLM 代理的自动化研究——更长迭代、更多并行代理、可通信的代理团队——会平台化：代理锚定自己过去的尝试，随历史累积做出越来越少、越来越小的编辑。解法是周期性遗忘：丢弃累积的搜索状态、从迄今最优候选重启搜索，只留现任者不留历史。
  - 数字：在可通信的代理团队中，周期性遗忘较不遗忘的并行代理最多提升 15%、较单代理最多 39%；
  - 代码：Comments 字段无代码链接（2026-10-16 核对）；
  - 点评：可作 nanoRSI 选择器研究的种群级对照：周期性清空被拒/入围历史（rejected_recent、谱系权重）但保留现任者与冻结测试面板，使提案器条件化不锚定累积的拒绝历史——用现有多种子编排器即可直接作为一条选择器臂验证（等 episode 预算下对比全保留 vs 周期重置）。 · [原文图](industry-rsi/assets/paper-figures/discovery-scaling-forgetting.png)

- **[AReaL-RSI: Adaptive Scaling and Coordination of Recursive Self-Improvement](https://arxiv.org/abs/2610.18083)**（Ant Group / Zhejiang University / HKUST，2026-10-13，闭环）
  - 核心：在不触碰骨干权重、工具权限与编排的前提下，围绕任务条件化的 harness 库 h = (p, K, S)——研究方向、可复用知识、可重复技能——组织一个持久的研究团队。领导者代理分配 harness、区分工件质量与研究潜力并路由记忆。
  - 数字：在报告的资源分配下对比 Codex-Goal：Terminal Bench 2.1 每骨干 +2.2 个百分点（Luna 75.3→77.5%、Astra 85.4→87.6%）；
  - 代码：HTML 中未见代码或数据可用性声明（2026-10-16 核对）；
  - 点评：战役级评审是可直接移植的结构：在 nanoRSI 世代之间设检查点评审会话，从证据账本改写方向/知识/技能条目而不消耗 episode，以版本一致性为闸门。 · [原文图](industry-rsi/assets/paper-figures/areal-rsi-adaptive-scaling.svg)

- **[The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery](https://arxiv.org/abs/2610.18933)**（Sakana AI，2026-10-13，闭环）
  - 核心：供人类研究者与现代编码智能体并肩做计算的端到端分布式流水线。研究被分解为任务起草、想法生成、规划、沙箱实验、结果汇总、基线与消融构建、事后分析、有据论文写作（证据暂存与规划、稿件生成、验证与评审），外加生成概念图的 autoillustrate。
  - 数字：谱系表（表 1）：AI Scientist-v1（主题特定、线性 Aider）→ v2（领域通用、树搜索 AIDE、并行实验）→ Agentic Scientist（领域通用、CLI 智能体束搜索、并行 + rubric 校验 + 共科学家选项），评价级别从 workshop 提升到会议。
  - 代码：论文未提供 The Agentic Scientist 的专属代码仓库；
  - 点评：元控制器在每阶段强制 rubric 校验，是证据账本阶段闸门的外部模板； · [原文图](industry-rsi/assets/paper-figures/agentic-scientist-pipeline.png) · [仓库](https://github.com/SakanaAI/AI-Scientist-v3)

- **[Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models](https://arxiv.org/abs/2610.13194)**（Institute of Computing Technology, CAS (State Key Laboratory of AI Safety) / University of Chinese Academy of Sciences，2026-10-09，闭环）
  - 核心：把自动研究 agent 的反应式 Generate-Execute-Feedback 循环替换为在演化研究 DAG 上的 Predict-Verify-Evolve，建模为预算约束 POMDP 搜索。LLM 世界模型在执行前以稀疏两两锦标赛（软 Bradley-Terry 拟合）按价值改进、信息增益、探索效用三准则（自适应权重）为候选打分，先剪枝、选择或辩论精炼再进入昂贵执行。
  - 数字：MLS-Bench-Lite（30 任务、5 小时预算）：DeepSeek-V4 Flash 下 JANUS 全面胜出（Test 41.07 对最强基线 Codex 38.91；
  - 代码：代码位于 github.com/bilemond/JANUS 但无 LICENSE 文件（2026-10-15 核验）；
  - 点评：执行前锦标赛正是 ADOPTION 第 39 项选型研究需要的廉价预排序臂：世界模型在任何 episode 花费前按预期面板增益给候选排序，其排序质量对实际闸门结果的命中本身可测。 · [原文图](industry-rsi/assets/paper-figures/janus-coevolving-world-models.png) · [仓库](https://github.com/bilemond/JANUS)

- **[Evidence-Grounded Agentic Formulation Development in an Autonomous Laboratory](https://arxiv.org/abs/2609.19099)**（Intrepid Labs (Toronto)，2026-09-16，支撑·无闭环）
  - 核心：闭环自主实验室智能体设计与执行连续的药物制剂数批，每次迭代都锚定在结构化积累的内部实验证据库上，而非从零开始优化。
  - 数字：匹配实验预算下，高性能命中率 50%，对照 Andromeda 1 为 17%、DoE 为 2%；
  - 代码：arXiv 论文公开；
  - 点评：结构化证据库是 nanoRSI 证据账本的非 LLM 类比：每次新运行都对照累积证据表选择，而不只看上一代面板。 · [原文图](industry-rsi/assets/paper-figures/andromeda2-evidence-grounded-lab.svg)

- **[Agora: Git as Shared Memory for Collective AutoResearch](https://arxiv.org/abs/2609.18094)**（NVIDIA，2026-09-16，闭环）
  - 核心：自主研究会话把主张、结果与验证记录为只追加的 Git DAG；带多样性感知选择的前沿索引让后续会话在先前工作之上推进而非重启，独立复现是一等贡献类型。
  - 数字：12 天运行、13 个未指派 LM 工作者针对一个冻结的 1.196 亿参数 attention-SSM 混合体做权重迁移：1,703 项贡献，评测器 3.39 → 1.899 bits/byte，闭合与训练版 GPT-2 124M 差距的 62%，165 次独立复现全部通过。
  - 代码：arXiv 论文公开；
  - 点评：把 nanoRSI 的提案谱系建为同样的 DAG——每个候选存主张+证据、选择偏向前沿+多样性、独立重滚动作为复现节点入库。 · [原文图](industry-rsi/assets/paper-figures/agora-git-shared-memory.png)

- **[ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents](https://arxiv.org/abs/2609.17523)**（PhAI Labs / Fudan University Zhongshan Hospital / Shanghai Academy of Natural Sciences / Shunwei Capital 等，2026-09-15，闭环）
  - 核心：交互式科研工作台耦合两个递归：内层固定模型，由固定辅助模型（GPT-6 Astra）每次提出一个有界 harness 编辑（指令、技能或上下文设置），仅在 schema 合法且配对开发评测优于父代时接受；外层在冻结的改进 harness 下用从完整协作轨迹合成的评分表奖励做 GRPO 训练任务模型。
  - 数字：四个科研任务族（来自 LAB-Bench 与 Biomni-Eval1 的 895 个任务）。
  - 代码：论文指向 Gen-Verse/ScienceBuddy-RSI 与 science-buddy.io；
  - 点评：对 nanoRSI：让有界 harness 编辑（仅配对评测提升才接受）与冻结胜者下的模型训练阶段交替——两个递归互相喂养，但绝不同时改动同一个面。 · [原文图](industry-rsi/assets/paper-figures/sciencebuddy-system-diagram.png) · [仓库](https://github.com/Gen-Verse/ScienceBuddy)

- **[PrimeScientist: Strategic Allocation of Research Effort in Autonomous Research](https://arxiv.org/abs/2609.17846)**（UC San Diego / Johns Hopkins University，2026-09-15，支撑·无闭环）
  - 核心：自主研究智能体同时决定方向与资源投入：可执行计划树编码有前景但未探索的方向，自适应 MCTS 随结果到达重新分配剩余 token 预算，而非执行固定计划。
  - 数字：在 12 个 AI 研究任务、预算匹配下，平均奖励 +10.3%，尝试次数比 AutoResearch 少 50.6%。
  - 代码：arXiv 论文公开；
  - 点评：nanoRSI 的步进器每代花费固定回合预算； · [原文图](industry-rsi/assets/paper-figures/primescientist-effort-allocation.svg)

- **[Training AI Scientists to Replicate Research](https://arxiv.org/abs/2608.13331)**（Inherent Laboratories，2026-08-13，闭环）
  - 核心：Replica：从 100 篇 ML/AI-for-science 论文自动构造 310 个复现任务（Gemini 2.5 Pro 把结果图抠成任务；每个任务 = 60 分钟内、1/7 张 H200 上复现一张图）。
  - 数字：Faraday 在 73% 的分布内 ML 任务与 60% 的留出 AI-for-science 任务上胜过 Claude Opus 4.8 与 GPT-5.5（测试集上比 Claude +6%、比 Codex +8%）；
  - 代码：未提及代码或模型发布。
  - 点评：对 nanoRSI：自动生成 rubric 裁判 + 轮次级信用权重，是缺精确答案长时程任务可复用的验收信号——且其自一致性（0.66）应随每个分数一并报告。 · [原文图](industry-rsi/assets/paper-figures/faraday-replica-ai-scientist.png)

- **[Frontis-MA1: Training an AI4AI Model towards Recursive Self-Improvement in Machine Learning Engineering](https://arxiv.org/abs/2607.28568)**（Frontis.AI — Horizon Research / Tsinghua University，2026-07-30，闭环）
  - 核心：SFT/RL 训练 Draft、Improve、Debug、Crossover 算子；搜索修改可执行机器学习程序，环境评分后保留种群及父代历史，再复用执行经验卡片与所选父代。
  - 数字：作者报告：固定 OpenMLE-Evo，将基础 35B 模型换为 Frontis-MA1 后，MLE-Bench Lite 平均获牌率从 39.39% 升至 60.61%；
  - 代码：代码、35B/30B 权重、任务及 SFT 轨迹公开。
  - 点评：拟议 nanoRSI program/learner 实验：为谱系节点附加不可变执行卡片，对比父代选择与固定父代搜索。 · [原文图](industry-rsi/assets/paper-figures/frontis-ma1-openmle.png) · [仓库](https://github.com/FrontisAI/OpenRSI)

- **[Hyra: 简单有效的科学发现智能体](https://hy.tencent.com/research/hyra)**（Tencent Hunyuan，2026-07-21，闭环）
  - 核心：生产者-消费者研究循环：Context Agent 维护经验库并持续把多样化灵感上下文入队；多个 Proposal Agent 撰写沙盒化方案（solve.sh 入口），在全新沙盒运行打分后回流经验库；
  - 数字：复用 Recursive 公开设置：NanoChat Autoresearch 验证 BPB 0.9015 vs 0.9109；
  - 代码：研究工件开源于 github.com/Tencent-Hunyuan/Hyra-results（核验时为非标准自定义许可证）；
  - 点评：可移植的是评估器升级环：当严格闸门开始放过刷指标的候选时，先花一轮改进评估器（更严检查、更粗粒度奖励、更大进步空间），再继续候选搜索。 · [原文图](industry-rsi/assets/paper-figures/tencent-hyra-research-agent.jpg) · [仓库](https://github.com/Tencent-Hunyuan/Hyra-results)

- **[ENPIRE: Agentic Robot Policy Self-Improvement in the Real World](https://arxiv.org/abs/2606.19980)**（NVIDIA / Carnegie Mellon University / UC Berkeley，2026-06，闭环）
  - 核心：在物理机器人上做自主研究：EN——智能体自建环境，含自动二元奖励验证（几分钟成败演示学得、150ms 内校验）与自动复位（SAM3/BundleSDF/cuRobo 工具调用），以不可变 Gym API 暴露；PI——智能体读文献、提假设、在真实验证信号引导下改训练代码；
  - 数字：Push-T：Claude Code 与 Codex 约 2 小时内达 95% 成功（Kimi Code 翻倍）；
  - 代码：论文未给代码仓库 URL；
  - 点评：对 nanoRSI：智能体自建奖励验证环境（从演示学得的二元检查 + 不可变 API）是冻结评估器不变量的物理世界对应物； · [原文图](industry-rsi/assets/paper-figures/nvidia-enpire-physical-autoresearch.png)

- **[EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery](https://arxiv.org/abs/2603.08127)**（Huawei Technologies / Vrije Universiteit Amsterdam，2026-03，闭环）
  - 核心：三智能体 + 双持久记忆：研究员智能体做树结构'提案-评审-精炼'想法搜索（最多 21 个候选、Elo 循环赛、留前 3）；工程师智能体检索执行策略并在四阶段上做实验树搜索（含失败诊断与代码修订）；
  - 数字：想法生成（Gemini-3-flash 裁判）：对 AI Scientist-v2 平均差 +29.17、AI-Researcher +87.50、InternAgent +83.33；
  - 代码：代码在 github.com/EvoScientist/EvoScientist（Apache-2.0，核验时 4,893 星）。
  - 点评：对 nanoRSI：把'想法记忆'与'执行策略记忆'分开，并显式记录失败方向——阻止提案者重复开采死矿的负知识与正技能同样有价值。 · [原文图](industry-rsi/assets/paper-figures/evoscientist-self-evolving.png) · [仓库](https://github.com/EvoScientist/EvoScientist)

### 公司研发遥测（7）

- **[Measurements for understanding the pace of AI development inside frontier labs](https://www.anthropic.com/institute/measuring-pace-of-ai-development)**（Anthropic，2026-09-17，人在环上）
  - 核心：一套 RSI 节奏度量原型：R&D 自动化指数盘点全部研发任务类型，按 Epoch AI 的 AL0–AL5 分级并按人力时间加权；对内部代理平台的监督指标；
  - 数字：R&D 自动化指数（2026 年 8 月）：Claude 以领导级（AL4+）承担 Anthropic 26% 的 AI 研发工作，自 2026 年 2 月的不足 1% 上升；
  - 代码：公开文章与一张已发布图表；
  - 点评：可借鉴的是披露模式而非数字：随任何 nanoRSI 结果发布自身管线的自动化等级构成、监督拦截率、以及用于抓捷径的评测预算占比——即该文要求前沿实验室公布的三类遥测。 · [原文图](industry-rsi/assets/paper-figures/anthropic-rd-automation-index.png)

- **[Research acceleration: The view inside OpenAI](https://openai.com/index/research-acceleration-view-inside-openai/)**（OpenAI，2026-09-06，人在环上）
  - 核心：OpenAI 宣布达成 2025 年秋设定的"2026 年 9 月前拥有自动研究实习生"目标——即在人类指导下完成明确定义、需数天的研究任务的系统；并给出组织级遥测：8 月中旬研究员中位日推理用量超 600 美元（前 10% 超 7,000 美元）、研究组织整体每 1 个人工工作日配合 3.1 个 agent 工作日、并发 agent 工作流上升、人均实验数创纪录、更长程任务委托增加。
  - 数字：明确瞄准"2028 年 3 月前的自动 AI 研究员"，把工作定位为迈向 RSI 的进展，同时声明"我们尚不知道如何安全地走完对齐、完整 RSI 的全程"，并提醒整体研究提速"很可能跟不上"agent 用量指标。
  - 代码：官方博文，无代码、权重或数据发布。
  - 点评：建议：在 nanoRSI 实验日志中引入 agent 工作日核算口径（每个改进阶段的人工/agent 计算比），让递归收益的声明带有明确的劳动力替代分母。 · [原文图](industry-rsi/assets/paper-figures/openai-research-acceleration.png)

- **[Measuring Autonomous AI Research](https://www.primeintellect.ai/blog/measuring-autonomous-research)**（Prime Intellect，2026-08-14，人在环上）
  - 核心：智能体反复修改 nanoGPT 训练方案、运行实验并保留改进代码；固定验证器检查八个固定随机种子的运行。
  - 数字：报告称进行了 153 次运行、覆盖 18 个模型，每次使用 8 张 H200。
  - 代码：已确认官方仓库及报告链接的轨迹；
  - 点评：建议：在 nanoRSI 优化任务中采用不可修改的多种子接受标准、配对比较和完整实验台账。 · [原文图](industry-rsi/assets/paper-figures/prime-measuring-autonomous-ai-research.png) · [仓库](https://github.com/PrimeIntellect-ai/frontier-automated-speedrun)

- **[When AI builds itself](https://www.anthropic.com/institute/recursive-self-improvement)**（Anthropic / The Anthropic Institute，2026-06，人在环上）
  - 核心：该文把公开基准与 Anthropic 内部遥测合成为一篇论述：Claude 正在自动化 Anthropic 自身的编码与研究；文中给出三种未来（能力平台期、人类主导的复利式自动化、完全递归自改进），按现有证据判断复利式自动化最可能，并主张建设可验证的减速机制。
  - 数字：作者自报内部数据：Anthropic 合入代码中超过 80% 由 Claude 编写（2026-05）；
  - 代码：文章公开；
  - 点评：把'下一步判断对决人类'作为 nanoRSI 面板上与能力分数并列的'研究品味'读数——在决策点上配对施测成本很低。 · [原文图](industry-rsi/assets/paper-figures/anthropic-when-ai-builds-itself.png)

- **[How Cognition Uses Devin to Build Devin](https://cognition.com/blog/how-cognition-uses-devin-to-build-devin)**（Cognition，2026-02-27，人在环上）
  - 核心：Devin 编写产品补丁，评审意见及 CI/lint 结果触发进一步修改，由人类评审最终 PR。操作手册和会话洞察提示将经验带入后续会话，合并代码成为产品组成部分。
  - 数字：公司报告此前一周有 659 个 Devin PR 合并进入自身代码库，而 2025 年表现最好的一周为 154 个。
  - 代码：报告描述商业服务；
  - 点评：建议：由评测失败触发有界修复迭代，同时保留补丁来源与可读验证证据。 · [原文图](industry-rsi/assets/paper-figures/cognition-devin-builds-devin.png)

- **[Discovering Multiagent Learning Algorithms with Large Language Models](https://arxiv.org/abs/2602.16928)**（Google DeepMind，2026-02-18，人在环上）
  - 核心：Gemini 2.5 Pro修改CFR/PSRO代码，以代理游戏中的可利用度评价候选；有效变体进入种群并按适应度参与父代选择。
  - 数字：VAD-CFR在1000轮评估下于11个游戏中10个达到或超过基线；
  - 代码：发现的算法源码和提示已列于采用CC BY 4.0的论文附录；
  - 点评：建议实验：修改小型学习规则函数，缓存评分候选，并在保留游戏评价前冻结选择。 · [原文图](industry-rsi/assets/paper-figures/google-alphaevolve-marl-2026.svg)

- **[How we used Codex to train and deploy GPT-5.3-Codex](https://openai.com/index/introducing-gpt-5-3-codex/)**（OpenAI，2026-02-05，人在环上）
  - 核心：早期版本协助工程师调试训练、分析评测并改进部署执行器；人类团队将代码与发现用于后续版本。
  - 数字：有具体内部应用案例，但没有通过受控实验量化模型对自身改进的独立贡献。
  - 代码：报告与系统卡公开；
  - 点评：可记录研发建议、代码改动与实测结果之间的对应关系，衡量辅助研发贡献。 · [原文图](industry-rsi/assets/paper-figures/codex-builds-codex-figure.png)

### 立场、路线图与实验室（7）

- **[What if automating AI R&D triggers an intelligence explosion?](https://arxiv.org/abs/2609.36054)**（GovAI / CASP / University of Cambridge / Institute for Law & AI 等，2026-09-30，支撑·无闭环）
  - 核心：联盟立场与证据评估而非系统：综述“自动化 AI 研发管线可能触发软件驱动的智能爆炸”的初步证据（AI 扩充有效研发人力、反馈环加速进展），分析影响（能力增长超出社会消化速度、对超人类系统失控、州/公司/政府部门间制衡被侵蚀）并提出政策回应（对 AI 研发自动化建立可见性、发展引导与约束手段、为社会适应做准备）。
  - 数字：为作者论断而非基准结果：AI 系统数年内有望自动化大部分 AI 研发工作、甚至全部；
  - 代码：arXiv 2609.36054；
  - 点评：其“可见性”诉求可翻译为度量：nanoRSI 的请求/token 预算账本正是论文希望政策侧获得的“AI 研发自动化可见性”原语——从既有证据管线发布每次运行的自动化遥测（episodes、尝试、接受编辑数）是直接且低成本的对接。 · [原文图](industry-rsi/assets/paper-figures/intexpl-fig2.png)

- **[Zhipu HKEX placing announcement: next-generation GLM with a fully self-trained (recursive self-improvement) system](https://ea-cdn.eurolandir.com/press-releases-attachments/4179721/HKEX-EPS_20260913_12330384_0.PDF)**（Zhipu AI (智谱)，2026-09-13，人在环上）
  - 核心：未发表机制。所得款项用途第 (ii) 项称下一代 GLM 将在上一代 GLM 搭建的环境中训练，形成涵盖数据自产、环境自造与基础设施自我优化的递归式自我改进闭环；
  - 数字：无结果——这是一次融资披露。
  - 代码：一手文件：港交所公告 PDF（eurolandir 镜像）。
  - 点评：对 nanoRSI：无直接应用——把智谱作为首家把递归自改进闭环写进有资金用途披露的港交所发行人来跟踪，待技术论文或 GLM-6.0 落地时再核验。 · [原文图](industry-rsi/assets/paper-figures/zhipu-glm-selftraining-filing.png)

- **[We Must Pace the Frontier](https://darioamodei.com/post/we-must-pace-the-frontier)**（Anthropic，2026-09-12，支撑·无闭环）
  - 核心：治理提案而非技术闭环：嵌入式 METR 式第三方评估员（员工级权限，Anthropic 单方面承诺）、民主世界前沿实验室协调、四级全球协议阶梯（第 3 级为 RSI 限速）。
  - 数字：逐字声明递归自改进“正在整个行业发生，包括在 Anthropic”；
  - 代码：文章公开于 darioamodei.com；
  - 点评：对 nanoRSI 可移植的是披露纪律：把严格改进闸门、契约守卫与审计轨迹公开到足以让第三方核验所声称的自改进速率。 · [原文图](industry-rsi/assets/paper-figures/amodei-pace-the-frontier.png)

- **[The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement](https://arxiv.org/abs/2609.11873)**（Shanghai Jiao Tong University / Theseus Labs / Tsinghua University / ByteDance 等，2026-09-10，支撑·无闭环）
  - 核心：这是一篇立场/路线图论文而非可运行闭环：用 Headroom-Closed Index（HCI）诊断现有 LLM，然后把 RSI 系统排到五级自主性阶梯——L1 执行、L2 策略选择、L3 经验获取、L4 环境/部署适应、L5 递归元改进——并按此阶梯梳理产业系统（AlphaEvolve、字节 Seed 推理训练、Hermes 可复用技能、ASPIRE、Prime Intellect、Theseus 环境-数据-模型协同进化、Sakana 与 Meta 超级智能体等）。
  - 数字：无新的系统级基准结果。
  - 代码：论文在 arXiv 上为 CC BY-NC-ND 4.0 许可；
  - 点评：建议：把 L1–L5 自主性阶梯作为 nanoRSI 实验报告的附加标注维度，并在声称递归收益时引入 HCI 式"余量"检查作为对照指标。 · [原文图](industry-rsi/assets/paper-figures/genuine-rsi-roadmap-2026.png)

- **[Toward Self-Improving Agents](https://www.salesforce.com/news/stories/toward-self-improving-agents/)**（Salesforce (AI Labs)，2026-07-23，支撑·无闭环）
  - 核心：主张复利资产是改进环而非租来的模型："检测失败、诊断根因、用仿真测试多个改进、从提升性能的组合中学习"，冻结权重下照样可改进提示、工具、检索、工作流与记忆（"冻结权重才是激进之举"）。提出"受治理的自治"：外部验证、回归套件、对抗用例与人工闸门，并以达尔文哥德尔机变体"不再记录幻觉检测标记却拿满分"的奖励黑客案例为警示。
  - 数字：Salesforce 未给出新的受控基准。
  - 代码：官方新闻文章；
  - 点评：建议：把文中开出的"药方"实现为代码——在 nanoRSI 的候选改进与接受改进之间加入回归套件+人工审计检查点——统计类似 DGM 日志案例的奖励黑客改动被闸门拦截与漏过的比例。 · [原文图](industry-rsi/assets/paper-figures/salesforce-toward-self-improving-agents.png)

- **[Seed2.1 Officially Released: Advancing AI Productivity](https://seed.bytedance.com/en/blog/seed2-1-officially-released-advancing-ai-productivity)**（ByteDance Seed，2026-06-23，人在环上）
  - 核心：Seed-for-Seed 计划：Seed2.1 以 agent 身份参与自身开发管线的关键阶段——评测、数据、训练、研究与基建——承担评测系统开发、能力诊断、SFT 数据合成与 RL 框架优化，并以执行/评测/诊断/优化多角色分解形成跨小时到数周的闭环研发工作流。
  - 数字：已披露方向与做法描述，非可测量闭环：博文称模型参与真实研发任务并反过来加速模型迭代，并把深化该整合、启用自主研究列为下一步。
  - 代码：博客公开（中英文）；
  - 点评：分阶段自我参与阶梯（评测→数据→训练）是范围控制模板：nanoRSI 可先让自身循环维护评测 harness，再触碰任何训练环节。 · [原文图](industry-rsi/assets/paper-figures/bytedance-seed-for-seed.png)

- **[Introducing Sakana AI's Recursive Self-Improvement (RSI) Lab](https://sakana.ai/rsi-lab/)**（Sakana AI，2026-06-05，闭环）
  - 核心：组织级承诺而非新机制：设立专门研究组，任务是'用 AI 重新设计 AI 研发流程本身'，从'静态的人类主导研发'走向'自主的自改进智能引擎'。页面固定了两条设计约束——样本效率（'不做最耗算力的自改进引擎，而做样本效率最高的'）与责任（'负责任的 RSI 不是能力的约束，而是能力可持续的前提'），并把实验室放在一条公开路线上：Agent 原生模型 -> AI Scientist -> 递归自改进 -> 民主化 AI。
  - 数字：无新基准；
  - 代码：仅有公开网页；
  - 点评：把该实验室的产出列为样本高效自改进机制的高优先级来源； · [原文图](industry-rsi/assets/paper-figures/sakana-rsi-lab.png)

### 自主后训练及其评测（6）

- **[VibeTraining-Bench: Data-Trainer-Harness Co-Design for Iterative System Improvement](https://arxiv.org/abs/2610.26342)**（Zhejiang University / Westlake University / Alibaba Group (Token Hub) / South China University of Technology 等，2026-10-20，闭环）
  - 核心：一个评测作者所称跨组件协同设计（cross-component co-design）RSI 能力的基准：研究智能体在同一初始智能体系统、固定资源预算下出发，在验证反馈引导下迭代改进训练数据、训练器与推理 harness，最终选定并提交一个系统做隐藏测试集评估。强制三重防奖励作弊保障：测试数据隔离、研究与判分容器分离、研究智能体断网。
  - 数字：前沿研究智能体能实质改进目标智能体系统：SWE-bench Verified 上 GPT-6-Astra 把目标系统从 32.9% 提到 53.7%，接近人研 instruct 模型的 55.4%；
  - 代码：仓库 github.com/D2I-ai/VibeTraining-Bench 已上线（MIT），但核验时代码与基准徽章均为“Coming Soon”；
  - 点评：nanoRSI 主循环正是该基准任务的单智能体实例——把其三重保障（测试隔离、判分分离、研究容器断网）作为未来任何自改 runner 的常备清单； · [原文图](industry-rsi/assets/paper-figures/vibetraining-bench-overview.png) · [仓库](https://github.com/D2I-ai/VibeTraining-Bench)

- **[AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning](https://arxiv.org/abs/2610.22194)**（Tsinghua University / University of Illinois Urbana-Champaign / ModelBest Inc. / The Chinese University of Hong Kong 等，2026-10-15，闭环）
  - 核心：在完整数据动作空间——调整类别比例、剪枝、修复、替换与合成数据——上自动化 SFT 数据研究，此前系统只允许单一动作。单智能体环会退化：只做比例调整，上下文被执行输出填满并在搜索中途丢弃。
  - 数字：组件阶梯（每轮从基座重训，故各效应可单独归因）：执行器使上下文丢失减半；
  - 代码：仓库 github.com/Thinking-Space/AutoSFT 已上线但内容为“Source code coming soon.”，未发现许可文件（2026-10-19 核验）——如实记录为已宣布未放出。
  - 点评：执行/分析分离并以产物路径（而非上下文倾倒）传递，是 nanoRSI 提案器在需要推理长运行输出时的接口范式； · [原文图](industry-rsi/assets/paper-figures/autosft-overview.png) · [仓库](https://github.com/Thinking-Space/AutoSFT)

- **[Athanor: An Agent-Native System for Autonomous Post-Training Research](https://arxiv.org/abs/2610.21055)**（ByteDance / Duke University / The University of Chicago / Virginia Tech，2026-10-15，闭环）
  - 核心：在真实 GPU 上做自主后训练研究（AutoPostTrain）的开放智能体原生系统。智能体获得完全研究自主权、低摩擦工程工具与高效起始代码：在沙箱内读数据集与评测结果、构建训练数据、编写并修改训练算法、调超参、分析结果决定下一步，且不能使用外部教师模型。
  - 数字：在 104 小时的战役中，四个 Claude Opus 5.5 智能体（各占一个八卡节点、无任何研究建议）把 Qwen3-4B-Base 从六任务开发套件 15.9 分提升到 67.3、留出套件从 9.2 提升到 48.2，对照官方 Qwen3-4B-Instruct-2507 的 66.5 与 47.9。
  - 代码：abs 页与 HTML 桩均未找到代码 URL；
  - 点评：可移植的是服务侧教义：冻结评测、去污染数据、持久研究记录、改进者不知情的留出套件，正是我们 freeze/final-test 协议维护的实验隔离保证——现在有了权重规模的外部演示：这些约束能支撑自主后训练战役。 · [原文图](industry-rsi/assets/paper-figures/athanor-autoposttrain-system.png)

- **[MetaRSI / RSI2: A Meta-Recursive Self-Improving System for Recursive Self-Improving Systems Themselves](https://arxiv.org/abs/2609.06396)**（CosmosMind，2026-09-06，闭环）
  - 核心：三个类型化算子共享同一循环内核：Data-RSI 从自身执行轨迹合成经核验的训练记录（对抗式生成加输入隔离 Anchor 角色的盲重推导）；Harness-RSI 对五槽脚手架（系统提示、记忆、内置工具、技能、MCP 工具）打类型化补丁；
  - 数字：目标 Qwen3.5-35B-A3B、五种子均值：MetaRSI-v1 相对冻结系统平均 +10.9——Terminal-Bench 2.1 +8.3、SWE-bench Pro +9.2（解决率 10.3→19.5）、AIME +13.3、GPQA-D-hard100 +12.6。
  - 代码：产物在 github.com/CosmosMind-ai/RSI-Harness（核验时 565 星）与 Hugging Face CosmosMind/RSI-Harness——核验时无许可证文件，默认保留所有权利：只可借鉴思路，零代码复制。
  - 点评：对 nanoRSI：把每次变更类型化为写数据、写脚手架或写参数，共用同一循环内核，并学习算子调度本身——比手工固定管线高出的 3.6 点就是调度的可测价值。 · [原文图](industry-rsi/assets/paper-figures/metarsi-frontier.svg) · [仓库](https://github.com/CosmosMind-ai/RSI-Harness)

- **[A-Evolve-Training: Autonomous Post-Training of a 30B Model](https://arxiv.org/abs/2606.20657)**（Amazon，2026-06-09，闭环）
  - 核心：在 30B Nemotron 基座上做四轮多周、全程无人的后训练（Nemotron-Reasoning Challenge）。支柱：每轮都从不可变、经运营审计的基座分叉（绝不覆写）；
  - 数字：留出榜 0.86 对人类最高提交的 0.87（约 4000 名中第 8）——首个在 30B 规模上报告有竞争力的自主环（此前自主 ML 演示为 GPT-2 级约 1.24 亿参数；
  - 代码：尚未发布代码（'完整代码、参考基座与训练后权重发布时间待确认'）；
  - 点评：对 nanoRSI：单调增长的死胡同登记表 + 冻结宪法下'只晋升策略'，是可移植的元层模式——环改进的是搜索策略而非基座，并把失败写下来。 · [原文图](industry-rsi/assets/paper-figures/amazon-autonomous-post-training.png)

- **[PostTrainBench: Can LLM Agents Automate LLM Post-Training?](https://arxiv.org/abs/2603.08640)**（ELLIS Institute Tubingen / Max Planck Institute for Intelligent Systems / Tubingen AI Center / University of Tubingen 等，2026-03，支撑·无闭环）
  - 核心：给 CLI 智能体四个小基座 LLM 之一（Qwen3-1.7B/4B、SmolLM3-3B、Gemma-3-4B）、一张 H100 与 10 小时，在七个基准之一上自主后训练该模型：可联网、无起始代码，禁止测试集训练、改 harness、训练给定基座以外的模型。LLM 裁判标记作弊（换模型、污染）；
  - 数字：最佳智能体：Claude Opus 4.6（Claude Code）均值 23.2 +/- 1.8%，对官方指令微调模型的 51.1% 与基座零样本 7.5%；
  - 代码：论文 CC BY 4.0。
  - 点评：对 nanoRSI：把防作弊账本（规则清单 + 裁判标记 + 按基座计分的回退）作为任何'智能体训练模型'实验的标准 harness，让奖励黑客成为被测量的结果而非轶事。 · [原文图](industry-rsi/assets/paper-figures/posttrainbench-pipeline.svg)

### 对齐自动化（3）

- **[TASTE: Can AI Models Judge AI Safety Research Proposals?](https://alignment.anthropic.com/2026/taste/)**（Anthropic / Anthropic Fellows Program，2026-08-28，支撑·无闭环）
  - 核心：用专家偏好标签衡量模型选择研究提案的能力；这是改进控制器的一项潜在评测组件，不更新 Agent 或模型参数。
  - 数字：在筛选出的 92 对提案上，报告最佳模型与标签一致率为 60%，估计人类一致率为 77%；
  - 代码：论文公开，数据访问需填写申请表；
  - 点评：可把提案选择能力与实验执行能力分别评测，并保留不确定或并列判断。 · [原文图](industry-rsi/assets/paper-figures/taste-figure.png)

- **[Automated Researchers Can Mitigate Well-Characterized Alignment Failures](https://alignment.anthropic.com/2026/automated-alignment-researchers/)**（Anthropic Fellows Program，2026-08，人在环上）
  - 核心：Agent 根据多基准反馈和能力保持门槛迭代目标模型的后训练方法与数据，研究控制器本身保持固定。
  - 数字：排行榜首位方法在十类目标失败的保留指标上均有改善；
  - 代码：作者链接的代码和基准配置公开；
  - 点评：可区分排行榜、选择验证与最终审计，并在汇总中保留被拒绝及作弊尝试的计数。 · [原文图](industry-rsi/assets/paper-figures/automated-alignment-researchers.png) · [仓库](https://github.com/YuehHanChen/automated_alignment_researcher)

- **[Automated Weak-to-Strong Researcher](https://alignment.anthropic.com/2026/automated-w2s-researcher/)**（Anthropic / Anthropic Fellows Program，2026-04，人在环上）
  - 核心：并行 Claude Agent 提出并运行弱监督强模型实验，复用共享发现与代码；更新的是 Qwen 教师/学生实验中的目标参数，不是研究 Agent 自身权重。
  - 数字：反复访问评分的聊天偏好实验中，PGR 达到 0.97，对照为两位作者七天调试得到的 0.23；
  - 代码：代码及数据/基线准备方式公开，Claude 仍为专有模型。
  - 点评：可在等计算预算下比较独立与共享研究档案，并将最终测试与选择彻底分离。 · [原文图](industry-rsi/assets/paper-figures/automated-w2s.png) · [仓库](https://github.com/safety-research/automated-w2s-research)


## 附录：迁移映射

- agent-code、memory-context 全部族 → 部署时自进化；parameter-learning 除 verifier-reward 外 → 训练时自迭代；verifier-reward → 自评估；research-workflows 全部族 → 自动研究。
- 覆写（变异对象是验证器本身的三条）：whoverifies-coevolving-graders、ucoe-verifier-harness-coevolution、tesearch-test-suite-signals → 自评估。
- 迁移脚本：`industry-rsi/migrate_to_notes.py`（`--check` 校验本文件与冻结 catalog 一致）。
