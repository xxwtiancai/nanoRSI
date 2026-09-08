<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI：小内核，让改进有据可查" width="100%">
</p>

<p align="center"><strong>让 Agent 改进 Skills，让每次改动有据可查。</strong><br>一个小而完整、读得懂的 Skills / Agent Harness 实验平台。</p>

<p align="center">
  <a href="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml"><img src="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.11+"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/runtime_dependencies-0-f4512c" alt="零第三方运行时依赖"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.2.0-f4512c" alt="版本 0.2.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-171717" alt="Apache-2.0"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> · <a href="#一次改进如何发生">工作流程</a> ·
  <a href="#接入你的模型">接入模型</a> · <a href="#可以研究什么">研究方向</a> · <a href="README.md">English</a>
</p>

---

Skills 改了一版又一版，Agent 真的变好了吗？

**nanoRSI** 把这个问题变成一个能跑、能比较的小实验：执行任务，收集反馈，提出 skill patch，与当前版本比较。符合条件的改动留下，然后冻结版本，用未见任务检验效果。

模型权重固定，研究对象是 skills 和 Agent 的工作方式。

| 小到可以读懂 | 完整到可以运行 | 每一步可以检查 |
| :---: | :---: | :---: |
| **约 1,800 行** Python 内核 | **一个**父代、候选和循环 | **每次尝试**留下证据 |
| 标准库 + Git | 训练 → 验证 → 最终测试 | 修改、轨迹、决策和成本 |

## 为什么做 nanoRSI

- **有具体的起点。** 参考 Agent、三个 skills、模型桥接和 90 个分组本地任务。
- **主流程看得懂。** 顺序尝试、普通文件、精确 Git 快照；核心调度集中在 [loop.py](src/nanorsi/loop.py)。
- **对照实验有位置。** 比较初始 skills、无 skills 和改进后 skills，也能比较固定与 self-use 改进器。
- **结果可以追溯。** 打开 patch，查看失败轨迹、所选版本和成本记录；未知用量会明确保留。

90 个任务是开发夹具，81 项工程测试验证的是协议。真实模型上的收益，需要由实际实验回答。

## 快速开始

准备 Python 3.11+ 和 Git：

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

先运行**脚本化离线演示**，不调用模型 API：

```bash
nanorsi new artifact ./artifact-demo
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi report --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

<p align="center"><img src="docs/assets/readme/terminal-demo.svg" alt="真实离线夹具运行的终端展示：创建实验、接受候选、写出报告并校验谱系。" width="100%"></p>

<sub>基于实际离线运行输出绘制。<a href="docs/assets/readme/demo-transcript.txt">查看记录</a> · <a href="docs/assets/readme/demo-evidence.json">查看原始输出</a>。这里的分数用于展示实验协议。</sub>

## 一次改进如何发生

<p align="center"><img src="docs/assets/readme/experiment-loop.svg" alt="在预算内执行训练任务、修改 Skills、验证比较、保留或拒绝；结束搜索后冻结版本并测试未见任务，最终结果不回流选择。" width="100%"></p>

训练反馈用于提出下一次修改，验证集用于选择候选。最终测试在冻结之后进行，结果不会回流到接受决策。

失败、拒绝和无变化的提案也会消耗尝试预算。每个接受的版本都有明确的父代和候选 commit，方便检查整个过程。

## 接入你的模型

创建 skills 实验：

```bash
nanorsi new skills ./skills-lab --goal "改进可靠的文件编辑能力"
```

**建立 baseline 前**，修改 `skills-lab/nanorsi.toml` 中已有的 `[agent]` 配置。填写真实模型 ID 和兼容接口；默认模型名称是占位值。兼容的本地服务可以不使用 key，需要鉴权的接口通过工作区外的绝对路径配置 key 文件。

```toml
[agent]
model_command = ["python3", "adapters/model.py"]
model = "your-model-id"
base_url = "http://localhost:8000/v1"
max_turns = 8
skills = ["inspect", "edit", "verify"]
```

默认最多五次提案，搜索上限为 400 个任务执行。完整五轮可能使用 350 个搜索任务执行，默认最终测试另需 270 个。提案调用单独记录，托管模型可能产生费用。运行前先按 [详细指南](docs/QUICKSTART.md#choose-a-budget-before-running) 选择预算和接口：

```bash
nanorsi doctor --workspace ./skills-lab
nanorsi run --workspace ./skills-lab
nanorsi freeze --workspace ./skills-lab --repeats 3
nanorsi final-test --workspace ./skills-lab
python examples/compare.py ./skills-lab/reports/final.json
nanorsi verify --workspace ./skills-lab
```

<details>
<summary><strong>工作区里有什么？</strong></summary>

```text
skills-lab/
├── target/agent/
│   ├── run.py                 # 小型 task/propose Runner
│   └── skills/
│       ├── inspect/SKILL.md
│       ├── edit/SKILL.md
│       └── verify/SKILL.md
├── proposer/propose.py        # 固定的提案驱动
├── evaluator/evaluate.py      # 固定的任务评分器
├── adapters/model.py          # 可配置模型桥接
├── tasks/manifest.json        # 分组 train/validation/test 任务
├── nanorsi.toml               # 实验配置
└── reports/                   # 搜索证据和最终对照
```

默认只允许修改 `target/agent/skills/**`。参考 Runner 加载 Markdown skills，在每题独立的临时目录中提供 list/read/write/final 操作。本例没有实现 skill 脚本执行或向量检索。

[完整操作指南](docs/QUICKSTART.md) · [数据合同与状态](docs/specification.md)

</details>

## 可以研究什么

三个问题，分别做对照：

| 问题 | 对照方式 |
| --- | --- |
| 加载这些 skills 有用吗？ | 无 skills 与初始 skills |
| 改过的 skills 对新任务有效吗？ | 冻结测试集上的初始版本与选定版本 |
| 递归复用有额外收益吗？ | 固定改进器与 self-use 改进器，保持配置和预算一致 |

`arm="frozen"` 始终通过初始 Harness 提出修改；`arm="self-use"` 通过最新接受的 Harness 提出修改。两种模式的修改目标都是当前父代。不同组使用独立工作区，在查看最终测试结果前冻结所有组。

比较工具输出配对任务宏平均差值、分组结果、单次任务耗时和成本覆盖率，并区分独立进化与重复部署。负结果也值得留下。

[评估调研](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md) 涵盖 DGM、SICA、GEPA、ACE、Memento-Skills 和近期 skills 基准。项目的小型、可读实现风格受到 [nanoGPT](https://github.com/karpathy/nanoGPT) 与 [nanochat](https://github.com/karpathy/nanochat) 的启发。

## 接下来可以看

| 想做什么 | 入口 |
| --- | --- |
| 运行自己的实验 | [操作与预算指南](docs/QUICKSTART.md) |
| 看核心实现 | [实验循环](src/nanorsi/loop.py) · [参考 Runner](src/nanorsi/templates/skills/target/agent/run.py) |
| 理解设计取舍 | [项目章程](docs/PROJECT_CHARTER.md) · [v0.2 设计](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md) |
| 准备任务、比较结果 | [示例工具](examples/README.md) |
| 了解更新、参与贡献 | [变更记录](CHANGELOG.md) · [贡献说明](CONTRIBUTING.md) |

**执行边界：** 默认是可信本地运行。worktree 和 receipt 提供版本检查；不可信代码和真正的标签隔离需要外部容器、VM 或服务。详见 [安全模型](SECURITY.md)。

<details>
<summary><strong>开发检查与旧版模板</strong></summary>

```bash
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

CI 在 Linux/macOS 的 Python 3.11/3.12 上检查。架构测试限制内核不超过 2,500 行，每文件 300 行、每函数 50 行，并禁止第三方运行时导入。

artifact/harness 旧模板保留为脚本演示；model 保留外部训练合同。旧 heldout 数据参与选择，v2 使用新建工作区和独立最终测试。

</details>

---

<p align="center"><img src="docs/assets/brand/nanorsi-mascot.png" alt="拿着迭代卡片的 nanoRSI 小机器人" width="110"></p>
<p align="center"><strong>带一个任务来，跑一次实验，分享结果。</strong><br>
如果你也想看到更多这类 Agent 研究，欢迎给 <a href="https://github.com/xxwtiancai/nanoRSI">nanoRSI 点个 Star</a>。<br>
<a href="https://github.com/xxwtiancai/nanoRSI/issues">分享实验或报告问题</a> · <a href="CONTRIBUTING.md">参与贡献</a></p>

<p align="center">Apache-2.0 · <a href="LICENSE">许可证</a></p>
