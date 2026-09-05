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
| **达尔文-哥德尔机 (DGM)** | Harness / Artifact | 形式化检验或经验性验证门禁保证每次自修改必须提升全局效用 | DGM, Gödel Agent | 严禁无证明或未过验证代码合入主干 |
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
