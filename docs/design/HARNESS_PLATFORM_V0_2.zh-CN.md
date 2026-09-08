# nanoRSI v0.2：最小 Skills / Harness 改进实验平台

状态：已按本设计实施 v0.2 的本地实验协议与参考 Runner；当前发布合同见 [内核规范](../specification.md)。真实模型收益、多 seed 外部 benchmark 复测和加固隔离适配器仍是后续实验。下文保留设计时的取舍与原始代码缺口，实施记录见 [计划](../superpowers/plans/2026-09-09-skills-harness.md)。
日期：2026-09-08。代码基线：`5b719c644e6e0f6c62e0e9c23ebb9c91721f5c87`。
依据：[论文评估调研](../research/HARNESS_EVALUATION_2026-09-08.zh-CN.md)。

## 1. 新的项目目标

**让开发者在固定基础模型和有限预算下，用少量可读代码运行 skills / Agent Harness 的改进实验，并验证改进是否能迁移到未见任务。**

英文定位草案：A minimal, hackable lab for improving agent skills and harnesses under a fixed model and a measurable budget.

首要用户是希望研究、学习或改进自己 Agent 的开发者。首次使用应能看见一个完整例子：运行任务、观察失败、修改 skill、比较候选、保留或拒绝、导出最终证据。

首版可变对象依次开放：

1. `target/agent/skills/*/SKILL.md` 与可选 scripts/resources。
2. `target/agent/policy.md`、skill 选择和使用策略。
3. 在单独实验配置中开放 `target/agent/run.py` 的工具/上下文工作流。

每个实验只开放明确的文件集合。模型参数、模型身份、评分规则、工具权限上限和预算保持固定。训练权重不进入这一版本的主线。

## 2. 三种结果主张

| 主张 | 所需证据 | 本版角色 |
| --- | --- | --- |
| skills 有用 | 同模型、同 Harness、同任务预算，有/无 skills 的配对差值 | 必备基线 |
| skills/harness 持续改进 | 初始与最终冻结版本在未见任务上的配对结果，另报搜索成本 | v0.2 主目标 |
| 递归复用有额外收益 | evolved proposer harness 与 frozen proposer harness 的匹配实验 | 后续小型实验，不能由涨分自动推出 |

一次任务内的重试属于推理策略；把修改持久化并用于下一次任务才属于跨任务改进。记录了递归调用也不等于证明了递归收益。

## 3. 架构选择

| 方案 | 优点 | 代价 | 决策 |
| --- | --- | --- | --- |
| 只提供 SKILL.md 自动改写脚本 | 最小，容易演示 | 没有可靠任务反馈、比较协议和版本证据 | 作为 proposer 示例的一部分 |
| 小型实验内核 + 可修改的参考 Harness | 保留真实闭环，容易替换模型/任务/改进器 | 必须定义少量执行和结果接口 | **采用** |
| 完整自进化 Agent 平台 | 支持复杂记忆、群体搜索、调度和 UI | 主线难读，测试与依赖显著增加 | 本版不做 |

继续使用现有 Git worktree、patch、外部 argv 命令、JSONL 和报告。内核默认顺序运行，一个 accepted parent、一个候选；历史用于追踪，暂不提供 population、Pareto archive 或插件注册。

核心总行数继续不超过 2,500；每文件 300、每函数 50 的现有预算保留。首期最多新增一个 `loop.py`，逐任务合同放入现有 `evaluator.py`。规范和架构测试的模块清单同步更新。示例代码另计但完整公布，不能把核心复杂度藏进示例来绕过预算。

## 4. 最小闭环

```text
初始化任务清单、模型配置、评分契约和父代 H0
  → baseline：验证集上的初始评估
  → execute：Hparent 在训练任务上运行，得到轨迹和反馈
  → propose：根据当前 skills、训练反馈和历史修改摘要提出 patch
  → snapshot：验证修改范围，产生精确候选 Hchild
  → evaluate：父代与候选在同组 validation 任务上配对评估
  → gate：接受 / 拒绝 / 证据不足，记录所有支出
  → 下一个 attempt，直到预算或预设停止条件触发
  → freeze：冻结各比较组的候选、模型、清单和分析规则
  → final-test：独立运行预先约定的测试与消融，写最终报告
```

主循环应在 `loop.py` 里直接读懂；反思、生成和修订先作为一个 proposer 调用完成，不拆成多 Agent 系统。

`attempt_id` 对每次提案递增，包含拒绝、无变化、格式错误和超时。`generation` 只表示 accepted parent 的更新次数；预算根据 attempts/实际执行用量计算。任何失败均保存记录，下一次从最后 accepted parent 恢复。

初版默认只接受主指标严格提高且所有约束满足的候选；相等保留父代，重复 hash 不算新一代。若将来研究“等分接受”或成本优先，应作为预先固定的独立 gate 配置，不在中途随结果改变。

## 5. 仓库形状

以下是目标结构；当前已有文件保留原位，仅列主线，不代表删除未列出的辅助模块。

```text
nanoRSI/
  src/nanorsi/
    cli.py                 参数与命令分发
    loop.py                唯一新增核心模块：有限循环与 freeze 状态
    proposer.py            训练反馈 → diff + hypothesis
    evaluator.py           episode/result 合同、外部评测调用
    gate.py                验证集比较
    lineage.py             attempts、版本和产物引用
    report.py              原始结果导出与简明报告
    config.py              固定实验合同和预算
    gitops.py              继续复用快照/worktree
    ...                    现有路径、进程、锁等辅助文件
    templates/harness/
      nanorsi.toml
      target/agent/
        run.py             一个小型、可阅读的 task/propose Runner
        policy.md
        skills/
          inspect/SKILL.md
          edit/SKILL.md
          verify/SKILL.md
      proposer/propose.py   固定驱动，选择并调用 proposer harness
      evaluator/evaluate.py 固定驱动，调用任务适配器
  examples/
    local_tasks/            小型文件/工具任务；准备与评分脚本
    adapters/              一个参考模型命令桥接与协议说明
    experiments/           固定/改进 skills、反馈消融的配置
    compare.py             读取多个独立运行，输出配对统计
  tests/
    ...
  docs/
    design/                本设计
    research/              论文证据
```

任务数据、验证器私有答案和实验输出使用独立目录；它们不因为放在 examples 中就自动进入候选快照。

首个 Runner 显式读取配置中列出的少量 skills；不做向量数据库或学习式 router。trace 记录实际加载的 skill hash，而非仅记录磁盘上存在的文件。skill 检索策略的优化留到参考任务确实需要后再引入。

保持一个外部模型命令桥接：发送规范化请求，接收响应、工具调用和真实用量。内核不绑定厂商 SDK；第一个可运行桥接在实施时使用用户已有模型接口。外部 CLI 若无法固定版本、控制全局记忆或导出用量，标为黑盒运行，不能宣称严格控制实验。无须为设计阶段安装新依赖或发起付费实验。

## 6. 最少的数据合同

沿用现有 `context.json → proposal.diff + hypothesis.json`。新增字段先在明确的 schema 版本下验证，不引入注册中心或抽象基类体系。

### Experiment manifest（冻结）

记录：实验 ID、arm、seed、模型/供应商/版本和推理参数、Runner/工具版本、可修改路径、任务分组与 split hash、验证器 hash、推理上限、搜索上限、选择与重试规则、反馈类型。

固定 seed 控制任务抽样、顺序和本地随机性；不保证远程模型确定性。不能确认模型快照时记录别名、日期和响应中可得版本，并把漂移列为限制。

### Task input（可交给候选）

`task_id, instruction, input_files, allowed_tools, limits`。不含参考答案、私有测试、选择集评分历史或最终测试结果。task_id 使用不编码答案的标识。

### Episode record（可信执行/评分端产出）

`episode_id, attempt_id, split, task_id, repeat_id, harness_commit, skill_hashes, output_ref, status, score, trace_ref, model_calls, input_tokens, output_tokens, cached_tokens, cost_usd, duration_ms`。

score 由固定 grader 产生；时长由执行端测量；调用量来自桥接/provider receipt。候选自报成本不是权威计量。缺失用量为 null，不补成 0；汇总同时报告 coverage。费用估算附价格表日期，实际计费与估算区分。

`status` 至少区分 ok、task_failure、timeout、runner_error、provider_error、invalid_output。任务失败和候选导致的崩溃计失败；平台/API 错误触发预先固定的有限重试规则，仍计成本，不能挑成功重试替代全部结果。

trace 只存模型可见输出、工具调用/返回和执行事件；不依赖供应商隐藏推理。训练 trace 可交给 proposer，validation/test trace 保留给实验报告，不流入改进上下文。

### Proposal context（按白名单生成）

当前父代、可修改文件、允许的训练轨迹与反馈、有限历史 patch/决策摘要、剩余预算、`proposer_harness_commit`。默认不传 validation 逐题结果；连同最终测试目录都不暴露给 proposer。

### Attempt record（lineage）

`attempt_id, generation, parent_commit, candidate_commit, proposer_harness_commit, candidate_hash, evaluator_fingerprint, manifest_hash, decision, reason, proposal_ref, train_results_ref, validation_results_ref, usage`。

每个产物引用附内容 hash，verify 检查引用存在且内容匹配。验证可重放判分和门禁；重新调用远程 LLM 不承诺逐字复现。

## 7. 训练、选择和最终测试

| 数据 | 改进阶段用途 | proposer 可见 | 是否能决定接受 |
| --- | --- | --- | --- |
| train | 产生执行经验和允许的任务反馈 | 是 | 可用于开发自测，不能代替 validation |
| validation | 固定规则比较父代和候选 | 不给原题/标签/轨迹；仅间接得到保留决策 | 是 |
| final-test | 所有 arm 冻结后的最终比较 | 否 | 否 |

候选执行器必须看见当次任务输入才能作答；这与 proposer 获取 validation 整套内容不同。每个 episode 使用新进程和临时工作区，持久化状态只来自冻结的 skills 快照，输出不能写回候选版本。

当前 heldout 每轮影响 gate，应在 v0.2 明确迁移为 validation 语义。新实验统一 train/validation/test；旧工作区保持 v0.1 schema，迁移产生新 manifest/新实验，不能把旧 heldout 历史改名后包装成未见测试。

`freeze` 按 validation 选定版本，保存所有 arm 的清单。最终测试只在 freeze 后运行，不能据其结果重选版本、调参或继续同一实验。绘制 test 学习曲线时，仅能在搜索结束后统一评估事先约定的 checkpoint，且标记为回顾诊断；默认只测初始与最终版本。

数据按来源仓库、文档、模板或任务家族分组拆分，避免同一题只改参数后跨 split。自建小任务用于开发协议，外部 benchmark 保留作者定义的评分与 task hash。已经读过的公开测试题无法保证基础模型未见，报告这一限制。

## 8. 可信本地与隔离评估

现有 worktree、patch deny 和 HMAC 提供版本/一致性检查，**不构成同一 OS 用户下的读取隔离**。候选可以从 evaluator 源码、Git 和宿主文件中读到答案；0600 的 key 也无法隔离同一用户运行的进程。

保留两种明确执行说明：

- 本地可信模式：最小启动路径，用于教学、协议调试和受信程序；不声称隐藏标签或防止恶意评分篡改。
- 隔离评估示例：外部容器/执行服务保管私有数据、评分器和 receipts。候选只获得导出的运行快照和当题输入；不挂载完整 Git、实验目录或宿主凭据。任务权限由固定运行器施加。

容器运行在外部适配器中，避免膨胀内核。若论文级实验宣称标签隔离，必须测试候选主动读取 evaluator、主工作区、Git 历史和 receipt key 时被拒绝。只把标签挪到另一个本地目录不满足这一要求。

## 9. 递归复用如何实现

固定 `proposer/propose.py` 保持可审计，默认禁止候选修改。它通过同一 Runner 的 `propose` 模式调用一个明确指定的 Harness 快照。

- `frozen`：每轮用 H0 产生修改，但修改目标仍是当前 accepted parent。
- `self-use`：每轮用当前 accepted parent 产生修改。

task/propose 两种模式共用被研究的 skills 和工作流，只改变输入任务与允许工具。Runner 的基础调用合同及资源限制固定。自修改时读取父代快照，patch 写到独立输出目录，不能直接修改正在执行的父代。

必须记录和检查 proposer 真正加载的 harness commit 与 skills hash；仅把路径放进 context 不算完成递归连接。用 spy Runner 验证下一轮加载关系，再进行真实模型实验。

初版默认 `frozen`，先证明 skills 改进闭环。`self-use` 是同一合同下的下一阶段配置，而非新增元 Agent 平台。

## 10. 评估指标和比较组

主指标由任务固定 grader 定义，首个本地基准采用任务 all-tests-pass。报告 task-macro mean：先在同题的重复执行间平均，再跨任务平均；多任务家族同时报告分项，防止某类样本多掩盖回归。

必要输出：

- 初始/最终 test score，配对差值 Δ（百分点）；保留原始逐题结果。
- 搜索总支出：训练执行、提案、开发检查、validation、失败重试，按阶段分别汇总。
- 部署支出：最终版本每题 calls/tokens/USD、耗时中位数/p95；最终评估支出单列。
- 每次 attempt 的候选分数、accepted score、strict-new-best、拒绝/no-op/错误率和累计预算。
- 鲁棒性/迁移结果；skill 数量、长度、使用率只作诊断，不作能力提升的代理指标。

最小比较组分阶段运行，不做全量笛卡尔积：

| 组 | 用途 | 优先级 |
| --- | --- | --- |
| 无 skills，固定 Harness | 检查初始 skills 的净作用 | M1 |
| 初始 skills，固定 Harness | 所有演化组的共同起点 | M1 |
| 多轮 skill 改进，frozen proposer | 验证持久化改进 | M2 |
| 同样算法，self-use proposer | 单独测试递归复用贡献 | M3 |
| failure-only / mixed / success-only | 只改变反馈视图的消融 | M3，按实际问题选一项 |

递归组固定相同初始版本、模型、任务、反馈规则和预算。更强的外部改进模型可做后续实验，但必须标注，避免把强模型知识迁移当成递归效果。

增加预算解释：固定版本可以获得相同单题推理上限；如比较额外推理策略，应预先固定顺序重试/选择方式。不得把 evaluator 的隐藏答案用于可部署选择器。oracle pass@k 只能标上界。

总成本用 `C_search + N × C_deploy` 与冻结版本的 `N × C_baseline` 对照；不存在节省时不报告虚构的回本点。若质量不同，同时报告质量—成本，不能只用费用比宣称胜出。

统计逻辑留在 `examples/compare.py`：至少三次独立进化报告均值、范围和每次结果；冻结版本重复部署单独统计。配对 bootstrap 以任务来源组为抽样单位，保持同题初始/最终配对；不把同题重复当独立任务。三次运行只是 pilot 下限，不自动支持强显著性结论。

## 11. 第一个真实实验

选择本地、可程序判分的文件/工具任务：定位证据、受约束编辑、编辑后验证。参考 skills 为 inspect/edit/verify；基础 Agent 应是合理的弱基线，避免故意写错算法或让 proposer 输出预制答案来制造涨分。

建议 pilot 为 90 个任务，按来源组分成 train/validation/test 各 30 个。每类任务在各 split 保持覆盖，但来源组互斥。这个规模用于检查流程和估计方差，不宣传为综合 Agent benchmark。

每次进化最多 5 个 proposal attempt；每轮抽 4 个训练任务，validation 对父代/候选使用相同 30 题和推理预算。搜索执行上限建议 400 episodes，包含 baseline 和父代重测；所有额外开发调用同样记账，达到上限即停止。模型调用 tokens/美元再设置用户环境下的硬上限；未知费用时禁止声称美元硬预算已经保证。

最终评估预算预先单独保留：H0 和最终候选各 30 题×3 次部署，持久化改进比较需要 180 episodes；无 skills 基线再保留 90，完整三组比较共 270 episodes/独立进化运行。pilot 默认每次独立进化都重新测量这两组固定基线，不复用结果当作新增独立样本。若增加 self-use 等实验组，每个额外冻结版本再加 90 episodes。各组均使用相同 frozen manifest。先完成一次端到端试验再开展三次独立进化；不要求五轮都接受。

外部有效性再选择一个官方 benchmark 的固定小子集，用其原生评分器和隔离环境复测。SkillsBench 可作为接口和任务参考，但子集结果必须标明子集，不能冠以完整 benchmark 分数。首版不同时接入 GAIA、HLE、SWE-bench 和 AppWorld。

## 12. 当前代码缺口与迁移路线

| 现有位置 | 证据与问题 | 最小迁移 |
| --- | --- | --- |
| `src/nanorsi/cli.py:51,83,104` | baseline 记录 fingerprint，后续 generation 漏记；有效第二轮会失败 | 固定契约身份跨代一致，增加多轮回归 |
| `src/nanorsi/cli.py:97` | 重命名为 score 后又按配置主指标取值，非 score 指标失败 | 保留原指标映射，测试 accuracy/minimize |
| `src/nanorsi/cli.py:64` | max_steps 按 accepted generation 计数 | attempts 与 generations 分离；失败也消耗预算 |
| `src/nanorsi/cli.py:87`、`src/nanorsi/gate.py:48` | heldout 每轮控制接受 | 明确 validation；新增 freeze 后 test |
| `src/nanorsi/proposer.py:43`、`src/nanorsi/cli.py:75` | 仅有父代 aggregate，无训练经验 | 白名单 context 加训练反馈、轨迹与 proposer 身份 |
| `src/nanorsi/templates/harness/target/agent/run.py:6` | policy 字符串分类，无实际 skill 使用 | 真实参考 Runner + 少量 skills，保留 mock 供 CI |
| `src/nanorsi/templates/harness/proposer/propose.py:6` | 固定一次性 patch | 使用失败经验生成 diff，支持 frozen/self-use |
| `src/nanorsi/evaluator.py:16` | 已有 cases/cost/time，但字段验证和记账未贯通 | 扩展既有结果合同，绑定完整产物引用 |
| `src/nanorsi/process.py:42` | subprocess 无读取隔离，输出上限未落实 | 本地模式明确限制，隔离交给适配器；执行边界强制输出/时间上限 |
| `tests/test_architecture.py:17` | 模块清单锁定 | 随新增 loop 同步规范，保留 nano 预算 |

实施时按顺序交付：

**M0：可信多轮底座。** 修复 fingerprint/指标名，补 attempts、完整结果引用与 split 语义。验收至少 `接受→拒绝→接受` 三次尝试，父链正确，拒绝消耗预算；任意主指标可用。

**M1：可用 skills 示例。** 接通一个真实模型桥接、task Runner 和本地任务集。验收日志证明 skill 文件被加载；无 skill/初始 skill 组运行同题同预算；CI 仍可离线测试合同。

**M2：五轮实验和最终报告。** 增加 bounded run、train feedback、validation gate、freeze/final-test、比较脚本。验收拒绝与超时可恢复，训练反馈可追溯，test 不影响选择，报告总支出和配对结果。

**M3：递归复用实验。** 接通 proposer Harness 快照选择，先用 spy 验证，再比较 frozen/self-use；报告正、零或负结果。完成一个外部任务子集的泛化复测之后，再决定是否需要搜索档案或技能检索优化。

实现阶段再逐项更新 charter、双语 README、specification 和对应测试；本次不把尚未实现的能力写成当前发布能力。artifact/model 的已有命令先保留兼容，停止扩展其主线，不做无关删除。

## 13. 必须覆盖的实验/工程验收

1. 相同 evaluator/manifest 身份跨三轮保留；非 score 指标正确比较。
2. accepted、rejected、no-op、provider error、timeout 全部有 attempt 和费用记录；预算终止后不再调用模型。
3. proposer context 只能引用训练证据；freeze 前 spy test evaluator 调用数为零；test 结果不能进入 promotion 函数。
4. 每题状态从干净快照开始；validation/test 不能向下一题或下一轮写入隐藏记忆。
5. self-use 下一轮加载 accepted harness；frozen 始终加载 H0；被拒绝候选永不作为下一轮 proposer。
6. episode 的 score/cost/time/hash/schema 校验严格；unknown usage 不得被当作免费。
7. 若启用隔离评估，主动读取标签、Git 元数据和 receipt key 的候选被阻止。
8. 最终报告同时显示全部配置/seed、原始逐题结果、搜索预算和部署预算；不根据 test 选择最佳组。
9. 原有 artifact/harness/model 合同 smoke 测试保留；规范与 architecture inventory 一致。

## 14. 设计调研阶段的验证（2026-09-08）

代码检查及已有测试基线：Python 3.13，`PYTHONPATH=src PATH=/opt/miniconda3/bin:$PATH /opt/miniconda3/bin/python3.13 -m unittest discover -q`，31 tests 通过。系统默认 Python 3.9 不满足项目 Python 3.11+ 要求；使用合适解释器后通过。

另在临时工作区验证两个现存问题：有效第二次 step 报 `candidate evaluator differs from baseline`；将主指标和 evaluator 同步设为 accuracy 后 step 报 `'accuracy'`。因此已有测试通过不等于多轮路径已经可用。这两个问题列入 M0，本次没有修改实现。

该阶段只交付研究与设计文档；当时未运行付费模型实验、未复现论文结果、未改变执行行为。2026-09-09 的实现与验证记录见实施计划。具体模型/任务是否产生稳定收益，仍需真实试验回答。
