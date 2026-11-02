# RSI 研究笔记

> 每篇论文一个文件，按 1250 篇 RSI 综述（arXiv 2607.07663）的**改进对象**轴分为四类目录，**闭环程度**（闭环 / 人在环上 / 支撑·无闭环）标注在每篇元信息行。模板：元信息 → Pipeline（论文主图 + 机制叙述） → 结果（作者数字）→ 证据边界 → 对 nanoRSI 的输入 → 来源。作者结果 ≠ 本地复现；负结果与边界照录。

> 冻结目录（[industry-rsi/](../industry-rsi/)，2026-10-24 起不再更新）迁移生成 236 篇；此后新增为手写深记。每日更新流水见下。

## 最近更新

- 2026-11-03 · Added [Are Self-Evolving Agents Continual Learners?](../deployment/self-evolving-agents-continual-learners.md) as a verified negative-result note with the original Figure 2 asset; recorded the stability/plasticity trade-off and retrieval-collision evidence as ADOPTION item 73. This is a read-only audit proposal; no default selector or runtime behavior changed. Rechecked tracked upstream repository activity and nanoRSI GitHub status; no portable, license-cleared core runtime change was justified.
- 2026-11-02 · 新增 [MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery](https://arxiv.org/abs/2610.39714)（Northeastern University / Broad Institute / Harvard / MIT / Microsoft Research 等，论文首发 2026-10-29）：MoLRSI 把科学文献、代码、工具和模型方法整理为可验证的 executable skills，用经验引导的 Monte Carlo tree search 组合并修订工作流；solution、refinement、execution 三类持久记忆分别保存工作流表现、修改后果与执行修复，跨任务经验改变后续搜索策略。论文把“当前任务内有经验”“跨任务 RSI 经验”“zero-search transfer”分开比较，并在 25 个来源任务排除目标的条件下报告六个抗菌任务的 test AUPRC：跨任务经验在全部六项提高，记忆池从 2 增至 25 个来源任务时平均转移约从 0.32 升至约 0.37，超过无 RSI 搜索 20 次的 0.361；湿实验中 107 个候选得到 17 个 MSSA 命中（15.9%），对照专家工作流为 241 个候选中 8.7%，pMHC 设计得到 8 个实验命中而 Claude Science 为 0。这些是作者在分子发现领域的结果，不是 nanoRSI 复现，也不能外推为通用 RSI。论文页面标注 CC BY 4.0；截至本轮未核验到官方代码、权重或可直接下载的数据/实验包，因此不复制实现。其对 nanoRSI 的可执行输入是把跨运行记忆与本轮适应分账，严格排除目标任务的来源经验，加入无搜索迁移和从零搜索对照，并在匹配 token/episode 预算下报告留出迁移、记忆池规模、父代重测和失败修复；不改变默认选择器。· [原始 Figure 1](industry-rsi/assets/paper-figures/molrsi-fig1.png)，图号 Figure 1，来源 [arXiv HTML](https://arxiv.org/html/2610.39714#S1.F1)；许可来源 [arXiv license](https://info.arxiv.org/help/license/index.html)
- 2026-11-01 · 新增 [Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories](https://arxiv.org/abs/2606.03979)（Google / Cornell，论文首发 2026-06-02，v2 修订 2026-07-10；Google Research 博客后续于 2026-10-27 发布）：Sleep 把部署后的学习分成 wake 与 offline sleep 两阶段，在预分配的 MoE/低秩记忆块中用 on-policy distillation、RL imitation 与自生成 dreaming 把短期上下文巩固为参数记忆，并用随机专家与梯度筛选进行自我改进。论文报告 Qwen3-8B 在 AIME-24/25、HMMT-25 上为 79.2/69.0/46.1（average@16），知识注入 SQuAD 单段/持续预训练为 48.9/46.2，并称 BABILong 可扩展到 10M tokens；这些均是作者结果，不是 nanoRSI 复现。原始论文为 CC BY 4.0，但未核验到官方代码、权重或数据包；官方页明确说明其固定模型架构与人为定义训练规则，故归为参数/记忆直接自改进信号，而不是可移植的标准库运行时。对 nanoRSI 的具体输入是把 wake/sleep 周期、短期记忆、巩固成本、旧能力保持和 dreaming 样本筛选分别作为实验字段，先做冻结模型/冻结评测器下的成本与遗忘记账，不实现权重更新。· [原始 Figure 1](https://arxiv.org/html/2606.03979v2#S1.F1) · [官方框架图](https://storage.googleapis.com/gweb-research2023-media/images/LLMSleep1_Framework.width-1250.png)
- 2026-10-31 · 本轮覆盖 OpenAI、Google DeepMind、Anthropic、Microsoft、Meta、Salesforce、Sakana AI、SambaNova、Nous Research、Prime Intellect、Cognition、阿里/通义、字节、腾讯、DeepSeek、月之暗面、智谱、MiniMax、Frontis 及 RSIHub、Anton、OpenEvolve、ShinkaEvolve、Hermes 等跟踪线。未发现新的、同时满足原始 pipeline/overview 图、可核验开放材料和许可边界的通用 RSI 条目；Anthropic 的公开页仍是受监督研发加速与趋势证据，OpenAI 公开表述仍把研究加速和完全自主 RSI 分开。OpenEvolve 的近期 Apache-2.0 变化是拒绝 `NaN`/`inf` 评测值并加回归测试，nanoRSI 已在 judge 边界实现同类计数范围校验，但没有复制上游代码或增加依赖。SenseNova-RoboRSI、The Trinity 和 Skill$^{\\infty}$ 继续保留为待核验线索，不声称本地复现或通用 RSI 已解决。
- 2026-10-30 · 继续核验 10 月 29–30 日的一手来源与跟踪仓库：OpenEvolve 合并了对 `NaN`/`inf` 评测值的拒绝及回归测试（Apache-2.0）；RSIHub、Hermes Agent、ShinkaEvolve 和 OpenSenseNova/SenseNova-RoboRSI 也有近期提交。前者与 nanoRSI 的“评测器不可信输入不能进入选择”边界一致，但当前仓库没有相同的自报告数值接口，故不复制代码；后者 RoboRSI 已公开 Apache-2.0 仓库，但技术报告、权重与数据的可复现包仍需逐项核验，暂不作本地复现或移植声明。The Trinity（官方仓库 2026-10-28 宣布代码将在一周内发布）目前只有项目说明/报告和“Code: Coming Soon”，没有可审计实现，保留为待复核线索，不入冻结 catalog。公司与实验室页面覆盖 OpenAI、Google DeepMind、Anthropic、Microsoft、Meta、Salesforce、Sakana AI、SambaNova、Nous Research、Prime Intellect、Cognition、阿里/通义、字节、腾讯、DeepSeek、月之暗面、智谱、MiniMax、Frontis；本轮没有发现新的、满足原始图/可用材料/许可门槛的通用 RSI 证据。下一项可执行工作仍是冻结选择器研究的三种子×三预算、匹配总评测成本、重复终测、父代同场重测和误拦/误放记账协议。
- 2026-10-29 · LAB round 3 已发布结果：按论文配置（GLM-5.3 executor、分层 30 任务子集、`k=1`、一次 final draw）实际评测 29 个可判分任务，base `0.852` → final `0.908`（+5.6 个百分点，17W/3T/9L）。报告明确说明收益全部来自失败修复（failure rescue），预算为 114 rollouts、174 次 improver calls、280,606,836 input / 11,377,445 output tokens；这是 nanoRSI 在该配置和单次抽样下的本地实验记录，不是通用 RSI 结论。报告还保留了逐任务父/子分数、选择决定和完整 ledger，下一步仍应以重复抽样、冻结留出集和匹配预算检验迁移，而不是把该增益写成稳定收益。
- 2026-10-29 · 新增 [Skill$^{\\infty}$](https://arxiv.org/abs/2610.35434) 线索（首发 2026-10-26）：把 meta-skill 与 task skill 放进同一套 agent-led 优化流程，并让 meta-skill 本身递归重写；论文在 SkillsBench 83 个任务上报告 60.7%，对比 human-curated 56.4% 与 SkillEvolver 54.5%。这是一条直接的技能/改进程序递归信号，但当前[官方仓库](https://github.com/taowangcheng/skill-infinity)只有 README、LICENSE 和 assets，README 明确代码尚未发布，未核验权重或数据包；因此不纳入冻结 catalog、不复制代码，也不把作者结果说成本地复现。其最可验证的 nanoRSI 方向是把“改任务技能”和“改优化技能”分成两个可审计版本流，并在匹配 token、冻结留出集和父代重测下比较，而不是启用递归 meta-skill 默认行为。
- 2026-10-28 · 收录 RSI-Opt（arXiv:2610.32026，Purdue University / 独立研究者，首发 2026-10-23）：跨运行演化提示、操作手册、已验证优化器代码库与决策节奏，并在运行内按训练动态修改优化器/诊断程序；论文 Figure 1、CC BY 4.0 论文许可和作者指标已核验，但未找到专属代码、权重或数据包，因此只作为既有“可编辑策略/技能记忆”协议输入，不声称 nanoRSI 复现或移植。

全部流水：[updates/2026-11.md](updates/2026-11.md) · [updates/2026-10.md](updates/2026-10.md)。

## 分类

| 分类 | 篇数 | 目录 |
| --- | ---: | --- |
| 部署时自进化 / Deployment-time self-evolution | 124 | [deployment/](deployment/) |
| 训练时自迭代 / Training-time self-iteration | 44 | [training/](training/) |
| 自评估 / Self-evaluation | 9 | [selfeval/](selfeval/) |
| 自动研究 / Auto Research | 59 | [autoresearch/](autoresearch/) |

## 冻结后手写深记

- [MoLRSI: A Recursive Self-Improving AI agent for Molecular Discovery](deployment/molrsi-molecular-discovery.md)
- [RSI-Opt: Recursive Self-Improvement for Optimizer Design](deployment/rsiopt-policy-object-evolution.md)
- [Are Self-Evolving Agents Continual Learners?](deployment/self-evolving-agents-continual-learners.md)
- [Skill$^{\infty}$: 自指技能优化（meta-skill 递归重写自身与任务技能）](deployment/skillinfinity-recursive-meta-skill.md)
- [Language Models Need Sleep: Learning to Self-Modify and Consolidate Memories](training/sleep-wake-consolidation.md)
- [更新流水（按月）](updates/2026-10.md)
- [2026-11 research updates](updates/2026-11.md)

---

旧流水（拆分前）：见 [updates/2026-10.md](updates/2026-10.md)。
