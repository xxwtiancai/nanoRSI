# 在不同层级运行改进实验

[English](MULTILEVEL.md) · [首次运行与 API 密钥](QUICKSTART.zh-CN.md) · [内核契约](specification.md)

nanoRSI v0.4 可以对程序、Agent 执行器、skills 和模型参数运行有界改进实验。每次实验记录改了什么、验证是否接受，以及冻结版本在独立测试任务上的表现。递归复用和种群搜索是额外的实验选择；它们本身不等于通用递归自我改进已经成立。

## 选择改进对象

| 模板 | 内核模式 | 可修改对象 | 实际执行内容 |
| --- | --- | --- | --- |
| `artifact` / `program` | `artifact`，schema 2 | `target/program.py` | Python 读取 JSON 记录并汇总；配置的 LLM 提出源码修改 |
| `harness` / `agent` | `harness`，schema 2 | `target/agent/run.py` | 本地 Agent 调度有依赖的工具；LLM 提出执行器修改 |
| `skills` | `harness`，schema 2 | `target/agent/skills/**` | LLM 根据 Markdown 指导和已声明的可执行技能编辑文件 |
| `coding` | `harness`，schema 2 | `target/agent/skills/**` | LLM 修复 Python 工具并运行公开测试；私有测试评估行为 |
| `model` / `learner` | `model`，schema 2 | `target/**`，包括保存的检查点与训练配方 | 受保护的训练器在 CPU 上更新小型分类器，无需模型 API |

正式模板名为 `artifact`、`harness`、`model`；`program`、`agent`、`learner` 是对应别名。`artifact-fixture`、`harness-fixture`、`model-contract` 明确保留 schema-1 示例与命令契约。已有 schema-1 工作区仍可运行。

## 跑完一次实验

准备 Python 3.11+、Git 并安装 nanoRSI 后，无需密钥即可运行 CPU 学习实验：

```bash
nanorsi new model ./learner-lab
nanorsi baseline --workspace ./learner-lab
nanorsi run --workspace ./learner-lab
nanorsi freeze --workspace ./learner-lab --repeats 1
nanorsi final-test --workspace ./learner-lab
nanorsi report --workspace ./learner-lab --format html
nanorsi verify --workspace ./learner-lab
```

运行真实模型的程序改进实验时，先执行 `nanorsi new artifact ./program-lab`，在 baseline 前配置服务商，再对该工作区执行同样的后续命令。Agent 模板的操作相同。[首次运行指南](QUICKSTART.zh-CN.md)解释 API 权限、外部密钥文件、连接检查和预算。聊天产品的订阅或登录不会自动完成 API 配置。

若账号有权使用 Z.ai Coding Plan 接口，可这样配置：

```bash
nanorsi configure --workspace ./program-lab \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key --thinking disabled \
  --max-steps 2 --max-episodes 200
nanorsi doctor --workspace ./program-lab --check-model
```

请替换为自己的外部密钥路径，并使用账号可用的准确模型 ID。连接成功只说明接口可用，不代表改进有效。连接检查会发出一次有界请求，费用不计入实验账本。配置命令本身离线运行；实验日志开始后，配置不可再改。

## 学习演示到底训练了什么

Learner 是一个四维输入、三分类的 softmax 分类器，数据为相互重叠的合成数值簇。JSON 检查点保存真实数值参数。每次尝试从已接受的检查点出发，应用提议的训练配方，运行 `trainer/train.py`，将产出的检查点提交为候选快照，再进行验证。被拒绝的训练保留证据，不替换已接受模型。

| 方法 | 实际更新 |
| --- | --- |
| `sft` | 使用小批量交叉熵梯度更新完整权重矩阵 |
| `rl` | 采样动作并获取环境奖励；使用带滑动基线的 REINFORCE 更新策略 |
| `lora` | 使用交叉熵梯度更新秩为二的 A、B 因子，基础权重矩阵保持冻结 |

这是教学规模的参数学习实验，不是 LLM 微调。这个小模型的 LoRA 因子有 16 个参数，基础矩阵有 15 个参数；示例展示更新机制，不宣称参数效率优势。

通过普通 CLI 跑默认的 18 次实验：三种方法 × 三个种子 × frozen/self-use 两组改进器对照。

```bash
python examples/parameter_learning/run.py ./parameter-results
```

输出目录必须是新目录。驱动器保留每条命令结果、工作区、接受与拒绝记录及最终报告，并生成 `summary.json`。已核验的 18 次实验全部完成：54 轮训练产生 20 个接受候选和 34 个拒绝候选。审计检查了父代检查点链接、训练数据哈希、LoRA 基础权重冻结，以及最终检查点身份。API 调用为零，未测量货币成本。

| 方法 | 初始测试准确率 | 选中版本：frozen 改进器 | 选中版本：self-use 改进器 |
| --- | ---: | ---: | ---: |
| SFT | 46.11% | 85.83% | 85.83% |
| REINFORCE | 46.11% | 85.56% | 86.39% |
| LoRA | 46.11% | 85.00% | 84.44% |

每格为三个独立演进种子的均值，仅对应这个合成任务。准确率差值应使用百分点，不应当成相对百分比增幅。九组匹配的 self-use 对照中，一组更好、一组更差、七组相同。参数学习改善了这个小任务，尚未显示一致的递归收益。

## 递归复用必须真的参与计算

在 baseline 前设置 `experiment.arm`。`frozen` 使用初始改进器，`self-use` 使用最近接受的改进器；两者都针对当前父代生成修改。源码哈希只能证明加载了哪个文件，不能单独证明改进后的行为影响了提案。

在 harness 中，`plan_steps` 同时用于任务执行和生成提案前的训练工作流分析。`run_propose` 调用所选改进器自己的规划函数，把步骤顺序、依赖检查和阻塞步骤写入训练反馈，再传给 LLM；`proposal_planner_used` 轨迹记录实际输出。改进规划函数因此可以影响下一次提案的输入，而不只是留下新的源码哈希。

在 learner 中，所选改进器检查点会计算允许传入的训练反馈样本的损失，并选出困难样本，在下一轮训练配方中赋予三倍采样权重。因此，frozen 与 self-use 的区别是生成课程时使用哪个检查点；两组训练本身都从当前已接受检查点继续。这让检查点指导的课程复用与普通多轮梯度训练可以分开比较。

请为对照组使用不同工作区，匹配任务、初始状态、推理设置与搜索预算，并在查看最终结果前冻结所有组。单独跑一次 self-use 不能证明递归复用带来收益。

## 可执行 skills

已声明的技能可以同时包含 `SKILL.md` 和 `run.py`。说明文件解释参数；执行器只在该技能确有脚本时暴露 `skill` 动作。例如，模型可以调用：

```json
{"tool":"skill","name":"edit","arguments":{"old":"old_name","new":"new_name"}}
```

脚本固定为 `target/agent/skills/edit/run.py`，从标准输入读取包含绝对路径 `workspace` 和 `arguments` 对象的 JSON，并返回一个 JSON 对象。运行时记录实际调用源码的哈希，限制运行时间为两秒、输出为 1 MB。参数由技能定义；上例需要脚本实现对应接口。模型动作不能自由指定命令行。候选脚本仍是受信任的本地代码。

真实模型 skills 演示要求模型在每题四个动作的预算下创建通用批量编辑脚本。证据可检验脚本是否实际调用、能否处理独立的新编辑任务。仅生成 Markdown 或脚本文件，不是已测量的能力提升。

## 种群搜索与 HTTP 工作进程

需要保留多个分支时，在冻结之前运行：

```bash
nanorsi population --workspace ./program-lab --size 3 --generations 2 --workers 2
```

请先配置足够的尝试次数和 episode 预算。协调器在启动本地候选工作线程之前预留预算，按验证成绩保留 top K，并可执行 draft、improve、debug 和 crossover 提案。交叉提案获得另一父代经过限制的可变源码；候选 DAG 记录两个父代，而 Git 提交仍只有一个源码父提交。只有协调器写入根 HMAC 日志并提升当前版本。`recover` 记录中断工作并结算预留预算；中断不提供免费重试机会。

种群并发使用本地线程与独立候选 worktree。另有 [HTTP worker 示例](../examples/remote_workers/README.md)，通过两个真实的 localhost 进程演示带鉴权的评估，并检查请求、源码、任务清单和评测器身份，可接入普通 CLI。尚未验证多主机部署、分布式训练或恶意代码隔离。

## 复现真实模型演示

```bash
python examples/demos/run.py ./live-results \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key --max-requests 60
```

默认运行 `program`、`agent`、`recursive`、`skills`、`population` 和 `remote`；可用 `--kinds` 选择子集。remote 演示自动启动和停止两个本机 worker 进程。驱动器使用真实模型提案，限制发起的模型请求数，通过共享账本串行访问服务商，在最终评估前冻结搜索，并保留失败、无变化和负收益。请求次数上限不是金额上限。输出包括 `plan.json`、`requests.jsonl`、各工作区报告和 `summary.json`。

Program 和 agent 任务通过本地 Python 执行，LLM 负责提出改进；skills 演示还会在执行任务时调用 LLM。各演示测量的内容不同，不能合并成一个“RSI 总分”。应分别报告冻结的 baseline/candidate 对照，并保留指标方向。比例指标可换算为百分点，损失值保留原始单位。

## 先看结果，再给结论

Schema-2 的 artifact、harness 和 model 默认比较 `baseline` 与 `candidate`；skills/coding 还包含 `no-skills`。Freeze 绑定条件、所选提交、指标方向和重复次数。最终评估直接读取保存的检查点，不重新训练，也不参与候选选择。验证成绩改善只是搜索结果，必须等冻结测试面板完成才能讨论最终收益。

这些小型自编任务展示可执行机制和特定任务上的观察，不代表广泛基准优势、统计显著性、无限制自修改或通用 RSI 已解决。报告应同时提供任务、种子、对照、预算、失败以及支持结论的证据。

项目独立实现了从可执行研究系统中获得的思路，包括 OpenRSI 有界 MLE 元演进场景中的思路。OpenRSI 不能作为无限制通用 RSI 已解决的证据。本 Apache-2.0 项目没有复制 OpenRSI 源码，也不将其 CC-BY-NC 许可证视为与 Apache 兼容的代码许可证。
