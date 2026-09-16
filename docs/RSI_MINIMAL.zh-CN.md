# RSI 的最小机制集

第一次接触递归自改进（RSI）？本页给出它的有界、可测量的定义，列出任何这类系统都需要的最小机制集，把每一项映射到本仓库，并说明参考项目的贡献。五分钟读完；一条命令跑起来。

**[English](RSI_MINIMAL.md)** · [立即运行冒烟实验](#立即运行)

## RSI 在这里指什么

一个系统执行*递归自改进*，是指它改进"产生改进的那套机器"——程序、Agent 执行器、技能或参数——并且每次改动都被测量而不是被假定。nanoRSI 实现的是这个思想的有界、可验证版本：**模型提案，确定性代码裁决，只有严格更优的候选能存活。**本仓库不宣称通用 RSI 已解决。

## 最小集

| # | 机制 | 为什么必不可少 | 在本仓库的位置 |
| --- | --- | --- | --- |
| 1 | **可验证的任务契约** | 没有固定、机器可判的任务就没有"改进"可测 | `tasks/manifest.json`、`loop.tasks`、`evaluator.py` |
| 2 | **可变异面** | 系统必须声明什么可以改、保护其余一切 | `surface.py`（`SurfacePolicy`、受保护路径） |
| 3 | **提案器** | 必须有东西生成候选改动——模型或脚本，一律产出 diff | `proposer.py`、各 starter 模板 |
| 4 | **闸门** | 候选只有在严格测得提升且约束满足时才保留；平局即拒绝 | `gate.py`（`decide`） |
| 5 | **谱系** | 精确的父/子快照与防篡改日志让声明可审计 | `lineage.py`、`gitops.py`、`reports/evidence.jsonl` |
| 6 | **冻结 + 未见最终测试** | 选择反馈与诚实评估绝不能混流 | `loop.freeze`、`loop.final_test` |
| 7 | **对照** | "演化有效吗"与"递归复用有效吗"是两个问题，需要不同臂 | `arm = frozen / self-use`、`no-skills` 条件、uniform/random 课程 |

去掉任何一行，循环就不再可测：没有闸门会保留退化；没有冻结，测试集会泄漏进选择；没有变异面策略，候选可以改写自己的评分器。

## 参考项目贡献了什么

我们研究真实的开源实现，**只借鉴思想**——它们的许可证不授权在本仓库复用代码。

- **[OpenRSI](https://github.com/FrontisAI/OpenRSI)**（Frontis.AI，代码 CC BY-NC 4.0）：把 RSI 拆成可验证任务健身房（`OpenMLE-Gym`）、算子训练（`OpenMLE-ERL`）与长程搜索（`OpenMLE-Evo`）。它的四个原子算子——**Draft、Improve、Debug、Crossover**——正是我们技能提案器使用的算子词汇。其验证纪律区分模型收益与 harness 收益（MLE-Bench Lite 39.39% → 60.61% 纯模型、71.21% 带搜索），并带 `--smoke` 一键模式；值得注意它**没有单元测试**——这正是 nanoRSI 用回归测试套件补上的缺口。
- **[MetaRSI / RSI-Harness](https://github.com/CosmosMind-ai/RSI-Harness)**（CosmosMind；harness 仓库**未附许可证**，按保留所有权利对待）：把系统建模为三元组 *(数据 D，模型 θ，harness H)*，跑同一个内核——**Observe → Diagnose → Propose → Validate → Execute → Select → Export**——并坚持"模型提案、确定性代码裁决"的权限边界（与我们的闸门同一规则）。其 harness 是五槽骨架：系统提示、记忆、内置工具、技能、MCP 工具。两个工程习惯值得偷学：*身份不变量*（"未加载 Genome 时与上游 Agent 行为完全一致"）与*覆盖不变量*（"每个上游配置键都必须被路由"）——它们变成了 [`tests/test_invariants.py`](../tests/test_invariants.py)。其论文的对照组合——预算一致、密封留出集、五个种子、无改进/单算子基线——是我们研究报告对齐的标准。
- Sakana 的 ShinkaEvolve、SEAL、DGM、OpenEvolve 等被跟踪项目收录在[行业研究地图](research/industry-rsi/README.zh-CN.md)，逐条标注证据边界。

所引数字均为作者报告值。本页内容不是对任何上游系统的本地复现。

## 立即运行

```bash
python examples/smoke/run_smoke.py
```

这条命令会搭建一个一次性 CPU 工作区，在闸门下真实训练检查点三次，冻结选择，在未见划分上测试（baseline 0.0 对 candidate 0.75），运行泄漏/静默旁路审计并写出证据账本——全程离线、无需 API key。要走真实模型路径，继续读[快速入门](QUICKSTART.zh-CN.md)。

## RSI 不是什么

通过面板不等于逐例正确（我们公开的反例：4/4 的解析器仍会错 `(12.5)`）；一个变好的演示不是基准；不同演示不得合成一个"RSI 总分"；self-use 臂与 frozen 臂打平是有效且可发表的结果——我们的实验已经平了两次。
