# 第一次运行 nanoRSI 模型实验

[English](QUICKSTART.md) · [代码任务格式](CODING_LAB.zh-CN.md)

本指南从申请 API key 开始，跑完一个小型 Python 修复实验并生成最终报告。固定模型先修复任务代码，再提出可复用 Markdown 技能的修改；nanoRSI 用独立任务比较这些技能。不训练模型权重，也不保证获得提升。

## 1. 安装

准备 **Python 3.11 或更新版本**、**Git** 和终端。以下命令适用于 macOS/Linux shell；如有需要，将 `python3.11` 换为本机安装的 Python 3.11+ 可执行文件。

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
nanorsi --help
```

保持虚拟环境启用，在仓库目录执行后续命令。`nanorsi new` 创建独立实验工作区和 Git 仓库，不调用模型。

```bash
nanorsi new coding ./coding-lab --goal "通过可复用技能改进可靠的 Python 修复"
```

预期看到创建成功信息，以及 `coding-lab/nanorsi.toml`、任务数据、模型适配器和 `target/agent/skills/`。

生成的模型、提案与评测命令固定使用创建工作区时的 Python 解释器，编辑 TOML 时请保留。移动或删除虚拟环境后，应使用所需解释器创建新工作区（或在 baseline 前修正命令）；`configure` 不会重写这些命令。

## 2. 获取 API 权限并选择接口

登录 ChatGPT、Claude 或其他聊天产品的网页，**不等于**为 nanoRSI 配置 API 凭据。使用托管服务时，到服务商官方控制台创建 API key，按要求开通 API 权限与计费，并选择该账号可用的模型 ID。不要公开密钥。使用本地服务时，需要自行启动兼容模型服务器，并填写它实际提供的模型 ID。

内置桥接发送 **OpenAI 兼容的 `/chat/completions` 请求**。填写下表中的基础 URL，不要再追加 `/chat/completions`。原生 Anthropic Messages 和 OpenAI Responses 协议需要其他适配器，仅换 URL 不够。

| 服务商 | API key 控制台 | `--base-url` | `--model` 填什么 |
| --- | --- | --- | --- |
| OpenAI | [API keys](https://platform.openai.com/api-keys) | `https://api.openai.com/v1` | 账号已开通的准确 API 模型 ID；要求新参数的模型使用 `--token-parameter max_completion_tokens`（[API 文档](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)） |
| OpenRouter | [Keys](https://openrouter.ai/settings/keys) | `https://openrouter.ai/api/v1` | 模型目录中的完整 provider/model 标识（[入门文档](https://openrouter.ai/docs/quickstart)） |
| DeepSeek | [开放平台](https://platform.deepseek.com/) | `https://api.deepseek.com` | [官方 API 指南](https://api-docs.deepseek.com/)中当前可用的模型 ID |
| Z.AI / GLM | [API keys](https://z.ai/manage-apikey/apikey-list) | `https://api.z.ai/api/paas/v4`（通用 API）；符合 Coding Plan 集成条件时使用 `https://api.z.ai/api/coding/paas/v4` | 账号已开通的准确模型 ID；公开演示使用 `glm-5.3-flash` 和 `--thinking disabled`。参见[端点及集成适用条件](https://docs.z.ai/devpack/tool/others)与[通用 API](https://docs.z.ai/api-reference/introduction)。 |
| 本地兼容服务器 | 服务器允许无鉴权请求时不需要 key | `http://localhost:8000/v1` | 本地服务器实际提供的准确模型 ID |

服务商的模型目录会变化。**执行前必须替换每条命令中的 `YOUR_MODEL_ID`**，它只是占位符，不是真实可用模型。有条件时选择固定快照。HTTP 格式兼容不代表模型一定遵守 nanoRSI 的 JSON 动作协议。自动集成测试使用带鉴权的本地 HTTP 测试服务，并不能证明付费服务兼容或模型获得提升。

[独立 GLM 实测](../examples/results/v0.4.0/README.md)记录了请求与返回的准确模型及实际结果。接口兼容与订阅适用条件是两件事，请使用账号及集成获得授权的端点；nanoRSI 不会自动切换计费端点。

## 3. 配置模型与 API key

使用 OpenAI 时，替换 `YOUR_MODEL_ID` 后运行这个小预算入门配置：

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --prompt-key --token-parameter max_completion_tokens \
  --max-steps 1 --max-episodes 40
```

在终端的隐藏输入提示中粘贴 API key。`configure` 离线执行，将密钥保存到**实验工作区外**的唯一文件 `~/.config/nanorsi/keys/model-*.key`，只把其绝对路径写进 `coding-lab/nanorsi.toml`。模型、接口、token 参数和预算也会写入配置。在 POSIX 系统上，文件权限限制为仅所有者访问。不要将密钥粘贴到命令、TOML、skill、issue 或 Git 提交中。

使用 OpenRouter 或 DeepSeek 时，替换为表中的接口和准确模型 ID，并选择该模型支持的 token 参数。桥接默认使用 `max_tokens`，也可显式选择 `max_completion_tokens`。默认 token 上限为 2048；如需调整 `agent.max_tokens`、`max_turns`、`timeout_s` 等高级设置，在 baseline 前修改已有 TOML 配置。

每次 `configure` 必须且只能选择**一种**鉴权方式：

| 选项 | 行为 |
| --- | --- |
| `--prompt-key` | 隐藏交互输入，创建唯一的外部密钥文件 |
| `--api-key-file /absolute/external/path` | 使用已有密钥文件，不创建或覆盖文件 |
| `--no-api-key` | 显式使用无需鉴权的接口，通常用于本地服务 |

已有外部文件时（替换模型与路径占位符）：

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url https://api.openai.com/v1 \
  --api-key-file /absolute/external/path/model.key \
  --token-parameter max_completion_tokens --max-steps 1 --max-episodes 40
```

本地服务器：

```bash
nanorsi configure --workspace ./coding-lab \
  --model YOUR_MODEL_ID --base-url http://localhost:8000/v1 \
  --no-api-key --max-steps 1 --max-episodes 40
```

**不存在直接传密钥的 `--api-key` 参数。仅运行 `export OPENAI_API_KEY=...` 不会配置 nanoRSI。** 内置桥接不自动读取环境变量密钥或 `.env` 文件，只读取显式配置的外部文件。其他服务商的环境变量同样不会自动加载。

<details>
<summary>通过隐藏输入手动创建密钥文件</summary>

优先使用 `--prompt-key`。需要单独准备文件时，下面的 Python 命令通过 `getpass` 读取密钥，在工作区外创建唯一文件，只打印路径。密钥不会成为 shell 命令文本。

```bash
python - <<'PY'
import getpass
import os
import tempfile
import warnings
from pathlib import Path

with warnings.catch_warnings():
    warnings.simplefilter("error", getpass.GetPassWarning)
    key = getpass.getpass("Model API key: ").strip()
if not key:
    raise SystemExit("API key must not be empty")
directory = Path.home() / ".config" / "nanorsi" / "keys"
directory.mkdir(parents=True, exist_ok=True)
os.chmod(directory, 0o700)
fd, path = tempfile.mkstemp(prefix="model-", suffix=".key", dir=directory)
with os.fdopen(fd, "w", encoding="utf-8") as output:
    output.write(key + "\n")
os.chmod(path, 0o600)
print(path)
PY
```

把打印的绝对路径传给 `--api-key-file`。POSIX 上目录权限为 `700`，文件为 `600`；`chmod` 不提供等效的 Windows ACL 保护，需要使用所在平台的仅所有者访问权限。无论工作区建在哪里，都必须把密钥放在其外部。

</details>

## 4. 实验开始前检查连接

```bash
nanorsi doctor --workspace ./coding-lab
nanorsi doctor --workspace ./coding-lab --check-model
```

普通 `doctor` 离线检查本地配置和密钥文件，不验证服务商是否接受请求。`--check-model` 通过配置的桥接发送恰好一次有界请求，要求响应内容为 JSON 动作 `{"tool":"final"}`。它不建立 baseline，也不修改实验谱系。托管探测请求可能收费，且**不计入实验成本记录**。探测成功说明基本连接与动作格式可用，不证明代码能力，也不保证完整实验不会超出服务商配额。

按后文表格排除问题后再建立 baseline。在实验尚未启动时可以重新运行 `configure`。一旦实验日志已经开始，配置即固定：要更改模型、接口、密钥路径、任务数据或预算，需要创建新工作区。中断的 baseline 也算已开始。

## 5. 跑完整个改进循环

```bash
nanorsi baseline --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

| 阶段 | 实际动作与预期证据 |
| --- | --- |
| `baseline` | 用初始技能执行 4 个验证任务，记录第 0 代 |
| `run` | 执行训练任务、请求技能补丁、对照父代与候选的验证表现，记录接受、拒绝、无变化或失败的尝试 |
| `freeze --repeats 1` | 固定选中版本和最终对照面板，之后不能继续搜索 |
| `final-test` | 在 4 个未见任务上分别运行初始技能、无技能、选中技能，每种条件一次 |
| `report --format html` | 写出 `coding-lab/reports/report.html` 和配套报告数据 |
| `verify` | 检查谱系完整性，成功输出包含 `lineage: ok` |

在浏览器打开 `coding-lab/reports/report.html`。补丁被拒绝或最终分数下降，都可能是有效实验结果，不代表安装失败。解释分数前，先检查报告中的失败任务和成本缺失情况。

### 改进了什么，递归体现在哪里？

每个 episode 中，模型通过 `list`、`read`、`write`、`test`、`final` 修复一份全新的 `solution.py`。这些代码修改属于该任务的输出。跨尝试修改的是 **`target/agent/skills/**` 中持久保存的过程型 Markdown 技能**。例如，补丁可能要求 Agent 编辑前检查边界条件、编辑后验证行为。模型权重、评测器、任务和模型配置保持固定。

训练反馈帮助提出补丁，验证集决定是否接受，最终测试反馈不参与候选选择。候选必须满足配置的门槛；尝试也可能失败或没有改动。查看记录中的候选 commit 和补丁确认实际变化，不能仅凭 `run` 结束就判断发生了演进。

默认 `experiment.arm = "frozen"` 始终用初始技能提出补丁。研究递归复用时，另建工作区，在 **baseline 前**将 TOML 中的 `experiment.arm` 设为 `"self-use"`：最新接受的技能参与提出下一次补丁。两组都修改当前父代。匹配模型、任务、推理设置与预算，并在查看最终结果前冻结两组。声称递归带来收益前，需要重复独立演进实验。两种模式都不训练权重。

## 运行前确定预算

一个 **episode** 指在全新目录中执行一次任务，期间可能调用模型多次。一次**提案尝试**指尝试修改一版可复用技能。

上面的命令设置为**一次提案尝试**、**40 个搜索 episode 上限**。对于 12 题 coding 包，一次完整尝试最多使用 **16 个搜索 episode**：4 个 baseline + 4 个训练 + 4 个父代验证 + 4 个候选验证。最终面板单次重复另需 **12 个 episode，不在搜索上限内**，合计最多 **28 个任务 episode**。每题最多八次模型调用，即最多 224 次任务调用，另加一次提案调用和独立的 doctor 探测。失败或无变化提案可能少用一些 episode，但仍消耗尝试次数。

未修改的 coding 模板允许三次尝试、100 个搜索 episode，完整搜索最多使用 40 个，最终面板另加 12 个。文本编辑 `skills` 模板更大：每个分区 30 题，五次尝试，400 个搜索 episode 上限，完整搜索最多 350 个；三次重复的最终面板另需 270 个。第一次使用托管模型建议使用上面的 coding 小预算配置。

episode 和 token 上限**不是金额限额**。最终测试与连接探测额外消耗调用，提案调用另行记录。未知成本不是零。运行前查看服务商价格与配额，在 baseline 前配置预算；实验开始后调整设置需要新工作区。

## 常见问题

| 现象 | 下一步 |
| --- | --- |
| `nanorsi: command not found` | 启用 `.venv`，在仓库目录重新运行 `python -m pip install -e .` |
| 缺少 key / 文件不可读 | 使用 `--prompt-key`，或检查已有外部文件的绝对路径与所有者权限 |
| HTTP 401 | 检查 key 是否有效且属于该接口；网页登录不等于 API key |
| HTTP 403 | 检查账号、项目、模型权限与服务商政策 |
| HTTP 404 | 检查基础 URL 与准确模型 ID；`--base-url` 不包含 `/chat/completions` |
| HTTP 429 | 检查额度、计费与速率限制，减少任务量或稍后手动重试 |
| HTTP 400 / 422 | 检查服务商请求要求、模型 ID，以及 `--token-parameter max_tokens` 和 `max_completion_tokens` 的选择 |
| HTTP 5xx | 查看服务商状态，稍后手动重试 |
| 网络、DNS 或 TLS 错误 | 检查连接、证书与接口，不要关闭 TLS 校验 |
| 重定向被拒绝 | 核实最终可信服务商 URL，在 baseline 前用该 URL 重新配置 |
| JSON / 动作格式错误 | 模型必须输出要求的 JSON 动作；检查模型适用性和 token 上限，或在 baseline 前提供兼容适配器 |
| 配置冻结 / 日志已开始 | 新建工作区并配置，不要修改已记录实验的设置 |

运行中断时，`nanorsi recover --workspace ./coding-lab` 可协调陈旧的本地尝试与 worktree 状态；它不会解冻配置，也不保证失败的最终面板可以重试。已完成的最终面板幂等，未完成面板保留明确失败状态。

## 查看与复用证据

| 位置 | 内容 |
| --- | --- |
| `reports/report.html` / `reports/report.md` | 可读对照、决策与成本覆盖情况 |
| `reports/report.json` | 搜索日志导出 |
| `reports/final.json` | 冻结条件、分数与搜索/测试成本证据 |
| `lineage.jsonl` | 顺序收据、父代和候选身份 |
| `.nanorsi/runs/` | 各次尝试的上下文、提案、轨迹和评测 |

在仓库目录运行 `python examples/compare.py ./coding-lab/reports/final.json` 查看对照摘要。接受的技能由记录中的候选 commit 与 `nanorsi/gen-N` 标签标识，报告帮助你检查真正被评测的版本。

暂时没有 API？运行 `python examples/coding_tasks/prepare.py --check` 离线验证错误初始实现与参考解。`artifact` 和 `harness` 模板是脚本化离线演示，分数展示协议行为，不代表学习收益。旧模板的 heldout 参与选择，v2 工作区则有独立的最终测试阶段。

默认执行为可信本地子进程。Worktree 与收据不能向任意同用户代码隐藏标签或密钥。运行不可信程序或进行私有标签评测时，使用外部容器、虚拟机或服务；详见 [SECURITY.md](../SECURITY.md)。
