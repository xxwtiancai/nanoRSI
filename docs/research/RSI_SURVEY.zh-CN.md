# 递归自进化 (RSI) 研究档案与架构全景调研

## 1. 概述与核心定位

本文档系统性追踪语言模型与自主智能体（Autonomous Agents）在递归自进化（Recursive Self-Improvement, RSI）方向的前沿研究进展与开源参考实践，并明确各项技术方案在 **nanoRSI** 中的最小原语映射。

nanoRSI 将自进化体系严格划分为三层正交结构：
1. **Artifact RSI（目标资产自进化）**：面向目标产物（如算法、代码、文档、特定策略 Prompt）在函数空间中通过遗传/采样变异进行优化。
2. **Harness RSI（智能体认知脚手架自进化）**：面向智能体内部决策编排、工具调用、反思总结与上下文工程的自迭代。
3. **Model RSI（模型参数与适配器自进化）**：在外部标准化训练契约下，闭环处理数据合成、LoRA 参数微调与自蒸馏。

---

## 2. 研究范式全景对比

| 研究范式 | 目标层级 | 核心实现机制 | 代表项目 / 论文 | 核心安全与可信不变量 |
| :--- | :--- | :--- | :--- | :--- |
| **函数空间进化 (MAP-Elites)** | Artifact | 基于大模型变异与质量-多样性（QD）档案保留最优代际 | FunSearch (DeepMind), OpenEvolve | 孤岛隔离；评测器绝对处于变异表面之外 |
| **智能体上下文工程 (ACE)** | Harness | 动态 Playbook 演化、策略剪枝与执行经验沉淀 | ACE, Memento-Skills, Hermes Agent | 结构化变异规范；追加式策略血统记录 |
| **达尔文-哥德尔机 (DGM)** | Harness / Artifact | 通过编程基准经验性评估自修改 | DGM, Gödel Agent | 提供实验证据；不构成全局提升的形式化证明 |
| **自适应语言模型 (SEAL)** | Model | 任务执行反馈 -> 合成训练集 -> 目标参数更新闭环 | SEAL, Continual-Intelligence/SEAL | 泛化保持；防止自训练产生分布崩溃 |
| **规范评测循环** | 全层级 | 标准化算子生命周期：Select -> Mutate -> Evaluate -> Gate -> Lineage | RSIHub (simple-agent-lab), nanoRSI | 评测器绝对冻结；真实指标不可篡改；HMAC 审计链 |

---

## 3. 开源参考仓库深度解析与 nanoRSI 映射

### 3.1 RSIHub (simple-agent-lab/RSIHub)
- **核心机制**：基于 YAML 配方的可插拔流水线，将循环清晰拆分为 `Select`、`Rollout`、`Analyze`、`Mutate`、`Validate`、`Novelty`、`Gate`、`Record`、`Reflect` 算子阶段。通过子进程隔离与 Git 生成分支运行，使用固化的 `gen/0` 密封集锚点防止指标虚高。
- **nanoRSI 映射**：nanoRSI 将其精炼为纯 Python 标准库内核，直接运行在 Git detached worktree 中。去除插件和复杂外部依赖，确保最纯粹的隔离与零依赖审计。

### 3.2 OpenEvolve & FunSearch
- **核心机制**：函数空间进化搜索，通过 LLM 提议新算法实现，结合代码静态分析与测试套件动态评分维护最优解族。
- **nanoRSI 映射**：直接对应 nanoRSI 内置的 `artifact` 模板（`nanorsi.templates.artifact`）。待演进目标置于 `target/`，评估与测试套件保持完全只读。

### 3.3 Hermes Agent & Memento-Skills
- **核心机制**：工具使用与执行经验技能化沉淀，通过逐步累加经过验证的高质量 Python 函数扩充 Agent 能力。
- **nanoRSI 映射**：对应 nanoRSI 内置的 `harness` 模板（`nanorsi.templates.harness`）。通过 `nanorsi.toml` 中的 `mutable_surface` 精确界定允许变异的 Agent 逻辑（如 `target/agent/**`），严防自修改破坏评测与安全约束。

### 3.4 SEAL (Self-Adapting Language Models)
- **核心机制**：通过解决问题收集的执行轨迹自动化构建微调数据集，触发外部训练器更新模型权重。
- **nanoRSI 映射**：对应 nanoRSI 内置的 `model` 模板（`nanorsi.templates.model`）。nanoRSI 内核负责评估、门禁与 Git 检查点管理，将耗时的 GPU 训练委托给标准化的外部训练脚本。

---

## 4. 可信自进化的三大铁律

所有在 nanoRSI 中运行的自进化任务必须遵守以下不变量：

1. **评测器绝对冻结（Frozen Evaluator Invariant）**：
   衡量表现的评估脚本、测试用例和打分逻辑绝对不得进入候选变异范围。
2. **原子回滚与签名血统（Atomic Rollback & Lineage Guarantee）**：
   每一步自修改均有 SHA/Tag 记录并以 HMAC 签名追加至 `lineage.jsonl`；一旦指标未达标或破坏约束，系统必须秒级原子回退至上一有效基线。
3. **资源开销与子进程沙盒（Subprocess & Resource Boundary）**：
   所有候选提议与评测运行必须受限于超时截断与清理机制，严防递归失控与资源耗尽。

---

## 5. 持续前沿追踪雷达（每日跟踪维护）

- **2026-09-11 跟踪（与 9 月 10 日比较）**：
  - **证据范围**：复查六个参考仓库默认分支最近两条提交。分支头仍为 [RSIHub `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1)、[Anton `22f7414`](https://github.com/mindsdb/anton/commit/22f74142ad5dffc81b1f85232b0b7ce5a3df451d)、[SEAL `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4)、[DGM `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2)、[OpenEvolve `411fb59`](https://github.com/algorithmicsuperintelligence/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2) 和 [ACE `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a)。本次比较覆盖默认分支已合并活动，不涵盖未公开实验或其他分支。
  - **决定**：没有新合并的机制足以支持运行时移植。保留 9 月 9–10 日的采纳决定：隔离搜索与最终评测、将模型训练置于外部、拒绝布尔适应度值，并在引入多提案编排前要求归并候选的实验证据。重复检查不构成能力提升的新增证据。

- **2026-09-10 跟踪（与 9 月 9 日默认分支基线比较）**：
  - **Anton——仅文档依赖变更**：[9 月 9 日 `22f7414`](https://github.com/mindsdb/anton/commit/22f74142ad5dffc81b1f85232b0b7ce5a3df451d) 在 `docs/package.json` 及其锁文件中将 Docusaurus 相关包更新至 3.10.2。所查差异没有改变智能体学习机制，不足以支持移植 nanoRSI 运行时改动。
  - **未变化的参考分支头**：[RSIHub `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1)、[SEAL `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4)、[DGM `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2)、[OpenEvolve `411fb59`](https://github.com/algorithmicsuperintelligence/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2) 和 [ACE `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a)。OpenEvolve 当前规范仓库地址为 `algorithmicsuperintelligence/openevolve`，原 `codelion` 地址会重定向至此。分支头未变化并不代表其他分支或论文中没有新工作。
  - **对 nanoRSI v0.2 的适用性**：9 月 9 日讨论的独立最终测试边界已有具体本地对应：`run` 使用训练与验证数据，`freeze` 结束搜索，`final-test` 比较初始技能、无技能及选定候选。`tests/test_v2_lifecycle.py` 检查搜索期间不评测测试分区、最终测试必须先冻结、冻结后禁止继续迭代。这些确定性夹具验证的是协议，并非真实模型提升或针对恶意进程的安全边界。
  - **决定**：保留现有评测控制，在实测实验支持前暂缓引入 ACE 式并行提案与归并编排。SEAL 仍作为外部模型训练参考，DGM 仍作为经验性自修改参考。所查变更没有提供足以支持今日运行时修改的新机制。

- **2026-09-09 追踪（一手来源核验）**：
  - **RSIHub——较上次检查新增**：[9 月 8 日合并 `bb8f4dd`](https://github.com/simple-agent-lab/RSIHub/commit/bb8f4ddde8f6c301bbf0a976af01747d11b8dab1) 引入持续研究隔离。[生命周期变更](https://github.com/simple-agent-lab/RSIHub/commit/5dbf7a7d36483f576126336d37aa216022a7650d) 将研究统一为持续会话，允许结束前发布候选，显式结束后再进行密封评测。边界检查和评测阶段仍由框架控制。**启示**：未来 nanoRSI 长时实验应将开发反馈与最终保留集验收分离；目前不足以支持向最小内核加入控制器。
  - **Anton——仓库有新增活动，所查提交未发现 RSI 机制变化**：[9 月 8 日文档依赖修复](https://github.com/mindsdb/anton/commit/d63624618d8897f50b578dec1969870917465b88) 提高 React 声明版本下限，实际锁定版本保持不变。这属于文档依赖维护，不是智能体学习能力提升的证据，也不适用于 nanoRSI 的标准库运行时。
  - **SEAL——复查基线，并非新发布**：所查默认分支最新提交仍为 [2025 年 8 月 1 日 `6d9c9f9`](https://github.com/Continual-Intelligence/SEAL/commit/6d9c9f9ee392c6cc618e771f399d436d190f6ca4)。[Self-Adapting Language Models](https://arxiv.org/abs/2506.10943) 通过强化学习生成含训练数据与更新指令的自编辑。参数适配继续置于外部训练契约之后；其他同名 SEAL 论文属于不同项目。
  - **DGM——复查基线并澄清术语**：所查最新提交仍为 [2025 年 8 月 13 日 `a565fd2`](https://github.com/jennyzzt/dgm/commit/a565fd2d1dca504ef5104a7cc0f3bdc4ab9b4fd2)。[参考实现](https://github.com/jennyzzt/dgm) 描述的是通过编程基准对自修改进行经验验证，而非全局提升的形式化证明。nanoRSI 的验收门禁同样只提供有界的实验证据。
  - **OpenEvolve——本次新评估的既有修复**：[7 月 18 日 `411fb59`](https://github.com/codelion/openevolve/commit/411fb59c886c18704caaffb611e17cf9e7d824d2) 将布尔标记排除出适应度聚合，防止超时标记抬高失败候选的得分。nanoRSI 的 `parse_evaluation` 已拒绝布尔指标值，布尔约束标记单独保存，无须移植运行时改动。
  - **ACE——本次新评估的既有进展**：[8 月 24 日 `82709de`](https://github.com/ace-agent/ace/commit/82709de050e1db6e6ef2f07bcb0393560b94992a) 加入并行 ComBEE 提案与 LLM 归并器。[参考项目](https://github.com/ace-agent/ace) 通过增量 Playbook 更新保留上下文。**启示**：未来多提案脚手架实验必须评测归并后的候选；单个提案的质量不能证明归并结果的质量。在具体基准支持增加编排复杂度前，暂缓集成。
  - **决定**：更新研究记录并修正 DGM 术语。本次检查不足以支持新增运行时依赖或行为变更。上述日期为上游提交日期，并不表示每项都是刚发布的新进展。

- **2026-09-08 跟踪维护**：
  - *TokenRhythm/NeoHorse-1*：基于路由脚手架（Routing Harness）的智能体后训练递归自进化架构（基于 Qwen3.5 的 4B/9B 系列权重）。其核心构建了“评估-选择-更新”闭环：通过多样化模型池分配任务，记录工具交互与执行轨迹，评估能力需求并反哺下一阶段的训练混合配比（Curriculum SFT 与在线策略蒸馏）。指出了面向长程 RSI 时，执行安全性、评估去污染以及脚手架级任务调度的必要前置保障。
  - *Liuziyu77/Awesome-RSI*（系统性 RSI 分层知识库与论文语料）：将大模型递归自进化系统形式化划分为清晰的三层拓扑架构：经验积累（Experience Accumulation：Prompt、上下文、技能库与记忆演进）、系统修改（System Modification：Harness 脚手架自改动、动态工具链、代码级自变异，如 DGM、SICA、MGM、Metaⁿ）与模型参数（Model Parameters：后训练权重更新、自博弈 RL 与经验蒸馏，如 SafeEvolve、APEx、SPADE）。深度印证了 nanoRSI 作为轻量、稳健的“System Modification”演进框架的架构定性，其冻结只读评测器与 HMAC 血统防篡改审计是保证系统进化不偏航的基础。
  - *KaiWU5/Awesome-AI4AI*（AI 能否可靠地自我改进？）：周更的 223 篇前沿 AI4AI 综述与论文追踪索引，涵盖长程自主研究、自动化脚手架合成与自进化评测基准。着重强调了防范自进化中的“虚假增益（Phantom Gains）”以及多随机种子任务序的鲁棒性控制。

- **2026-09-07 跟踪维护**：
  - *ahmd-mohsin/KernelAscent*：GPU Kernel 级能力分层因果自循环基准。其实证揭示了自进化的“能力地板（Capability Floor）”法则：弱模型自修改往往产生负增益（即 N < 0），因果自利用（Causal Self-Use）收益仅在 Frontier 级别模型涌现；同时指出了执行脚手架健壮性瓶颈——底层原生编译崩溃（如 SIGABRT）会绕过 Python 级信号超时，必须采用单任务独立子进程与进程组沙盒清理（严格印证了 nanoRSI 进程边界设计）。
  - *asimfish/awesome_rsi*：系统性综述 67 篇 RSI 前沿工作并沉淀 10 条核心实证发现。明确指出“评估器决定系统上限且是首要被攻击目标”、“优化窗口外设立锚定评估防止评估器坍塌”、“生产级自进化系统必须具备版本、审计、预测、回滚四项核心机制”。深度佐证了 nanoRSI 冻结评测器、HMAC 审计链以及原子回滚三大铁律的技术必要性。
  - *SystemOriginArchive/creator-theory-operational-canon*：形式化了针对失控风险、后继对齐（Successor Alignment）、评测漂移防范与血统连续性（Provenance Continuity）的 RSI 安全操作规约，与 nanoRSI 的血统防篡改校验和门禁准入体系高度一致。

- **2026-09-06 跟踪维护**：
  - *mindsdb/anton*：基于 Verifier-Eval 与动态反思的双重门禁判定（Session 级 `verdict`），确立了智能体执行评估必须采用外部独立运行的测试套件规范；其 Harness 自进化核心依赖于上下文技能逐步沉淀与工具链热拔插。
  - *simple-agent-lab/RSIHub*：固化 `Select -> Mutate -> Evaluate -> Gate -> Lineage -> Reflect` 循环规范，严格隔离变异面与只读评测器。
  - *exoharness/exo & OpenEvolve*：验证了基于函数空间进化及代码补丁（Patch Diff）原子合入时的沙盒隔离必要性。
  - *Darwin Gödel Machine (DGM) & ACE*：强调在 Harness / Context 层级变异时，必须附带结构化不变量检查与策略血统追溯，杜绝盲目 Prompt 变异引发的认知衰退。

- **2026-09-04 / 2026-09-05 历史跟踪**：
  - *simple-agent-lab/RSIHub*：重构自循环阶段（`Select` 至 `Reflect`）与双语规范；评测器严格保持进程外运行。
  - *mindsdb/anton*：自进化协作者智能体，融合 Hermes 式技能沉淀与运行时状态持久化。
  - *Continual-Intelligence/SEAL*：长程任务持续自适应基准与参数调优契约。
