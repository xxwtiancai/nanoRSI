<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI：小内核，让改进有据可查" width="100%">
</p>

<p align="center"><strong>改进程序、Agent 与模型参数。</strong><br>让修改真正执行，再用未见任务衡量效果。</p>

<p align="center">
  <a href="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml"><img src="https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.11+"></a>
  <a href="pyproject.toml"><img src="https://img.shields.io/badge/runtime_dependencies-0-f4512c" alt="零第三方运行时依赖"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.4.0-f4512c" alt="版本 0.4.0"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache--2.0-171717" alt="Apache-2.0"></a>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> · <a href="#一次改进如何发生">工作流程</a> ·
  <a href="#接入你的模型">接入模型</a> · <a href="#可以研究什么">研究方向</a> · <a href="README.md">English</a>
</p>

---

程序、Agent 或权重改了一版，真的变好了吗？

**nanoRSI** 把这个问题变成一个能执行的小实验：运行任务，收集反馈，提出修改，与当前父代比较。参数模式还会真正训练并保存模型。符合条件的改动留下，然后冻结选择，用独立任务检验效果。

| 小到可以读懂 | 多种改进对象 | 每一步可以检查 |
| :---: | :---: | :---: |
| **5,000 行内核上限** | **产物 · 执行器 · 参数** | **每次尝试**留下证据 |
| 标准库 + Git | 顺序或种群搜索 | 修改、检查点、轨迹和成本 |

## 可以改进什么？

| 从哪里开始 | 实际改变什么 | 命令 |
| --- | --- | --- |
| **Artifact** | 可执行 Python 程序，由真实 LLM 提出源码改进 | `nanorsi new artifact ./program-lab` |
| **Harness** | Agent 的可执行工作流规划器与执行器 | `nanorsi new harness ./agent-lab` |
| **Model** | 在 CPU 上用 SFT、REINFORCE 或 LoRA 真正更新数值参数 | `nanorsi new model ./learner-lab` |
| **Skills / coding** | LLM Agent 使用的 Markdown 指导与已声明的 `run.py` 技能 | `nanorsi new coding ./coding-lab` |

`program`、`agent`、`learner` 分别是 artifact、harness、model 的别名。它们共用 baseline → 搜索 → freeze → final-test 生命周期。Frozen/self-use 改进器对照和有界种群搜索，让“如何产生改进”也能成为实验对象。[多层级实验指南](docs/MULTILEVEL.zh-CN.md)解释实际执行、对照方式与边界 · [English](docs/MULTILEVEL.md)。

附带任务是小型自编演示，不是广泛能力基准。参数示例是小型分类器，不是 LLM 微调。递归机制可以执行，并不自动证明递归优势，更不代表通用 RSI 已解决。

## 快速开始

准备 Python 3.11+ 和 Git：

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

先运行**真实 CPU 参数学习**，无需调用模型 API：

```bash
nanorsi new model ./learner-lab
nanorsi baseline --workspace ./learner-lab
nanorsi run --workspace ./learner-lab
nanorsi freeze --workspace ./learner-lab --repeats 1
nanorsi final-test --workspace ./learner-lab
nanorsi report --workspace ./learner-lab --format html
nanorsi verify --workspace ./learner-lab
```

打开 `learner-lab/reports/report.html`，比较初始与选中检查点在冻结测试任务上的表现；最终评估不会重新训练。Artifact、harness 或 coding 的真实模型实验，需要按下面的首次运行流程在 baseline 前配置模型。

**[首次模型实验：API key → 连接检查 → 实验 → 报告](docs/QUICKSTART.zh-CN.md)** · [English tutorial](docs/QUICKSTART.md)

## 真实模型实测

在实现版本 `50556ad` 上，六项小型演示使用 **GLM-5.3-Flash**、种子 0，每个冻结测试条件运行一次。研究共使用 **43 次 API 请求 / 87,812 tokens**，请求上限为 59，关闭 thinking；不包含单独的连接配置探针。请求与返回的模型 ID 均为 `glm-5.3-flash`。[运行设置与服务商用量](examples/results/v0.4.0/live/summary.json)。

| 演示 | 初始版本通过测试 | 选中版本通过测试 | 证据 |
| --- | ---: | ---: | --- |
| 程序改进 | 1/4 | 4/4 | [最终结果](examples/results/v0.4.0/live/program/final.json) |
| Agent：frozen 改进器 | 1/4 | 4/4 | [最终结果](examples/results/v0.4.0/live/agent/final.json) |
| 递归 Agent：self-use | 1/4 | 4/4 | [最终结果](examples/results/v0.4.0/live/recursive/final.json) |
| 可执行技能 | 0/1 | 1/1 | [最终结果](examples/results/v0.4.0/live/skills/final.json) |
| 本地种群 | 1/4 | 4/4 | [最终结果](examples/results/v0.4.0/live/population/final.json) |
| HTTP 评估：两个 localhost 进程 | 1/4 | 4/4 | [最终结果](examples/results/v0.4.0/live/remote/final.json) |

这些是不同的自编任务，不能合成一个基准或 RSI 总分。改进后的规划器确实参与了下一轮提案，但最终面板上**没有超过 frozen 改进器**。技能演示刻意要求在四个动作内批处理六个文件，no-skills 为 0/1。种群保留了两个分支，拒绝了一次没有额外收益的交叉提案。HTTP 执行仅验证了 localhost。

**远程示例选中的解析器仍无法处理 `(12.5)`，尽管最终得分为 4/4。** [反例、被拒绝尝试、源码快照与证据边界](examples/results/v0.4.0/README.md#known-counterexample)。

<p align="center"><img src="examples/results/v0.4.0/overview.png" alt="分别展示真实模型演示和 CPU 参数学习结果；两组面板不构成统一 RSI 总分。" width="100%"></p>

## 已测量的 CPU 示例

已核验面板包含三种方法 × 三个种子 × frozen/self-use 对照：**18 次实验、54 轮训练、20 个接受候选和 34 个拒绝候选**。在相互重叠的合成数值簇上，平均测试准确率为：

| 方法 | 初始版本 | 选中版本：frozen 改进器 | 选中版本：self-use 改进器 |
| --- | ---: | ---: | ---: |
| SFT | 46.11% | 85.83% | 85.83% |
| REINFORCE | 46.11% | 85.56% | 86.39% |
| LoRA | 46.11% | 85.00% | 84.44% |

这里真正更新了四维输入、三分类 softmax 模型的参数。九组匹配的 self-use 对照中，一组更好、一组更差、七组相同，尚未显示一致的递归优势。LoRA 展示冻结基础权重的更新机制，不宣称在这个小规模上的参数效率优势。API 调用为零，未测量货币成本。

运行 `python examples/parameter_learning/run.py ./parameter-results` 可复现全部 18 次实验。[公开 CPU 结果](examples/results/v0.4.0/parameter-learning/summary.json) · [逐次实验的证据](examples/results/v0.4.0/README.md#cpu-parameter-learning) · [方法与解读](docs/MULTILEVEL.zh-CN.md#学习演示到底训练了什么) · [所有演示命令](examples/README.md)。

## 运行代码改进实验

**先配置 API 权限再运行。** 登录聊天产品或仅执行 `export OPENAI_API_KEY=...` 都不会配置 nanoRSI。请在服务商控制台创建 API key，并将 `YOUR_MODEL_ID` 替换为账号可用的准确 API 模型 ID。下面使用 [OpenAI API-key 控制台](https://platform.openai.com/api-keys)；也可通过兼容的 chat-completions 接口接入[其他服务商或本地服务器](docs/QUICKSTART.zh-CN.md#2-获取-api-权限并选择接口)。

```bash
nanorsi new coding ./coding-lab --goal "学习可靠的 Python 修复技能"
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
nanorsi doctor --workspace ./coding-lab --check-model
nanorsi baseline --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

`--prompt-key` 在终端隐藏输入密钥，将它保存在工作区外，TOML 只包含文件路径。也可用 `--api-key-file /absolute/external/path`，或用 `--no-api-key` 接入无需鉴权的本地服务。普通 `doctor` 离线执行；`--check-model` 发出一次有界模型请求，可能收费且不计入实验成本记录。Configure 本身离线执行，必须在实验日志开始前完成。

打开 `coding-lab/reports/report.html`，在相同的冻结任务与重复执行配对上比较**初始技能、无技能、选中技能**。每题中模型修复一份全新的 Python 文件，并可运行公开测试。Coding 跨尝试演进的是持久技能文件，也可包含提议生成的可执行脚本；模型权重、任务数据与评测器保持固定。任务代码修复与技能补丁是不同输出。补丁被拒绝或最终没有收益，都是有效结果。

这个单次尝试配置最多使用 **16 个搜索 episode + 12 个最终测试 episode**，每题最多八次模型调用，提案另需一次。最终测试在搜索上限之外，episode 上限不是金额上限。暂时没有模型？运行 `python examples/coding_tasks/prepare.py --check` 离线验证任务包。

**[完整入门教程：API key → 连接检查 → RSI 循环 → 报告](docs/QUICKSTART.zh-CN.md)** · [English tutorial](docs/QUICKSTART.md) · [任务格式](docs/CODING_LAB.zh-CN.md)

## 一次改进如何发生

<p align="center"><img src="docs/assets/readme/experiment-loop.svg" alt="在预算内执行训练任务、修改 Skills、验证比较、保留或拒绝；结束搜索后冻结版本并测试未见任务，最终结果不回流选择。" width="100%"></p>

训练反馈用于提出下一次修改；参数模式还会在评估前运行受保护的训练器。验证集用于选择候选。最终测试在冻结之后进行，结果不会回流到接受决策。

失败、拒绝和无变化的提案也会消耗尝试预算。每个接受的版本都有明确的父代和候选 commit，方便检查整个过程。

## 接入你的模型

上面的 coding 入门包是一条完整模型实验路径；也可用 `artifact` 改进程序，或用 `harness` 改进 Agent 执行器，配置流程相同。按照[服务商与密钥配置指南](docs/QUICKSTART.zh-CN.md#2-获取-api-权限并选择接口)，可接入 OpenAI、OpenRouter、DeepSeek 或本地兼容服务器。内置桥接使用 `/chat/completions`；原生 Anthropic Messages 和 OpenAI Responses 需要自定义适配器。它不自动读取 API-key 环境变量或 `.env` 文件。

研究文本编辑协议时，执行 `nanorsi new skills ./skills-lab`，再对这个工作区执行同样的 `configure` → `doctor --check-model` → `baseline` → `run` → `freeze` → `final-test` → `report` → `verify` 流程。其 90 题清单更大：五次尝试最多使用 350 个搜索 episode，三次重复的最终面板另需 270 个。[运行前确定预算](docs/QUICKSTART.zh-CN.md#运行前确定预算)。

生成的模型、提案和评测命令使用创建工作区时的 Python 解释器，请保留这些命令。实验日志一旦开始，设置就固定；之后要修改模型或接口，需要新建工作区。

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

Skills/coding 工作区允许修改 `target/agent/skills/**`。执行器加载 Markdown 指导，在每题独立的临时目录中提供 list/read/write/final 操作。已声明的技能可以包含 `run.py`，由有界的 `skill` 动作调用固定脚本，并记录源码哈希。其他模板各自声明可修改范围。

[完整操作指南](docs/QUICKSTART.zh-CN.md) · [数据合同与状态](docs/specification.md)

</details>

## 可以研究什么

不同问题，分别做对照：

| 问题 | 对照方式 |
| --- | --- |
| 加载这些 skills 有用吗？ | 无 skills 与初始 skills |
| 演进对新任务有效吗？ | 冻结测试集上的初始与选定程序、执行器、技能或检查点 |
| 递归复用有额外收益吗？ | 固定改进器与 self-use 改进器，保持配置和预算一致 |
| 种群搜索有帮助吗？ | 相同任务、匹配预算下的顺序与种群搜索 |

`arm="frozen"` 始终通过初始 Harness 提出修改；`arm="self-use"` 通过最新接受的 Harness 提出修改。两种模式的修改目标都是当前父代。Harness 规划器还会在生成提案时预处理训练反馈，learner 检查点则为后续训练计算课程。不同组使用独立工作区，在查看最终测试结果前冻结所有组。

Skills 比较工具输出配对任务宏平均差值、分组结果、单次任务耗时和成本覆盖率，并区分独立进化与重复部署。其他模式各自生成冻结报告；不同任务的演示不应合并为一个 RSI 总分。负结果也值得留下。

[评估调研](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md) 涵盖 DGM、SICA、GEPA、ACE、Memento-Skills 和近期 skills 基准。项目的小型、可读实现风格受到 [nanoGPT](https://github.com/karpathy/nanoGPT) 与 [nanochat](https://github.com/karpathy/nanochat) 的启发。

## 接下来可以看

| 想做什么 | 入口 |
| --- | --- |
| 运行自己的实验 | [操作与 API 密钥指南](docs/QUICKSTART.zh-CN.md) · [多层级实验](docs/MULTILEVEL.zh-CN.md) |
| 看核心实现 | [实验循环](src/nanorsi/loop.py) · [参考 Runner](src/nanorsi/templates/skills/target/agent/run.py) |
| 理解设计取舍 | [项目章程](docs/PROJECT_CHARTER.md) · [v0.2 设计](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md) |
| 准备任务、比较结果 | [示例工具](examples/README.md) |
| 了解更新、参与贡献 | [变更记录](CHANGELOG.md) · [贡献说明](CONTRIBUTING.md) |

**执行边界：** 默认是可信本地运行。可选 HTTP 评估已在两个 localhost 工作进程上演示，多主机运行尚未验证。worktree 和 receipt 提供版本检查；不可信代码和真正的标签隔离需要外部容器、VM 或服务。详见 [安全模型](SECURITY.md)。

<details>
<summary><strong>开发检查与旧版模板</strong></summary>

```bash
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

CI 在 Linux/macOS 的 Python 3.11/3.12 上检查。架构测试限制内核不超过 5,000 行，每文件 300 行、每函数 50 行，并禁止第三方运行时导入。

使用 `artifact-fixture` 或 `harness-fixture` 运行旧版脚本演示，使用 `model-contract` 查看旧版外部训练契约。已有 schema-1 工作区仍可运行，其 heldout 数据参与选择。新建 artifact/harness/model 使用 schema 2 和独立最终测试。

</details>

---

<p align="center"><img src="docs/assets/brand/nanorsi-mascot.png" alt="拿着迭代卡片的 nanoRSI 小机器人" width="110"></p>
<p align="center"><strong>带一个任务来，跑一次实验，分享结果。</strong><br>
如果你也想看到更多这类 Agent 研究，欢迎给 <a href="https://github.com/xxwtiancai/nanoRSI">nanoRSI 点个 Star</a>。<br>
<a href="https://github.com/xxwtiancai/nanoRSI/issues">分享实验或报告问题</a> · <a href="CONTRIBUTING.md">参与贡献</a></p>

<p align="center">Apache-2.0 · <a href="LICENSE">许可证</a></p>
