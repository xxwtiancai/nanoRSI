# 编程 Agent 改进实验室

coding 入门模板回答一个具体问题：固定模型在可复用技能演进之后，能否解决更多 Python 修复任务？每个任务在全新的 `solution.py` 上执行；跨任务的搜索只修改 Markdown skills，不训练模型权重，也不把已解任务的源码积累为技能库。

## 先验证任务包

12 个独立编写的任务涵盖稳定去重、分块、递归配置合并、布尔解析、区间合并、重试延迟、嵌套查询、数字版本号、CSV 解析、滚动平均、依赖排序和请求头脱敏。每题包含完整说明、错误初始实现、公开测试、私有边界用例和参考实现。训练、验证、最终测试各有 4 个不同任务族，同族不跨分区。

```bash
python examples/coding_tasks/prepare.py --check
python examples/coding_tasks/prepare.py /tmp/coding-manifest.json
```

离线检查实际执行全部初始实现和参考解，预期初始实现通过 0/12，参考解通过 12/12。这些数字用于验证任务包，并非模型表现或自改进证据。12 题不足以证明广泛泛化能力。

## 接入模型运行

从仓库安装 nanoRSI，再创建新工作区：

```bash
nanorsi new coding ./coding-lab --goal "通过可复用技能改进可靠的 Python 修复"
```

在 baseline 前编辑 `coding-lab/nanorsi.toml` 中已有的 `[agent]`，无意改变实验时保留其他字段：

```toml
[agent]
model_command = ["python3", "adapters/model.py"]
model = "your-model-id"
base_url = "http://localhost:8000/v1"
max_turns = 8
max_tokens = 2048
timeout_s = 60
skills = ["inspect", "edit", "verify"]
```

需要鉴权的兼容接口通过 `api_key_file` 指向工作区外的绝对路径，不要提交凭据。本地兼容服务可不配置 key。有条件时固定模型快照。[模型设置与执行预算](QUICKSTART.md#choose-a-budget-before-running) 对代码和文本编辑实验都适用。

```bash
nanorsi doctor --workspace ./coding-lab
nanorsi run --workspace ./coding-lab
nanorsi freeze --workspace ./coding-lab --repeats 1
nanorsi final-test --workspace ./coding-lab
nanorsi report --workspace ./coding-lab --format html
nanorsi verify --workspace ./coding-lab
```

打开 `coding-lab/reports/report.html`，同目录还会生成 Markdown 和原始谱系。运行 `python examples/compare.py ./coding-lab/reports/final.json` 可获得机器可读对照。如需比较 frozen 和 self-use 改进器，使用配置相同的独立工作区，在 baseline 前仅改变 `experiment.arm`，并在查看任一最终结果前冻结两组。使用独立种子重复实验后再讨论可重复性。

默认最多三次提案、100 个搜索任务执行。完整三轮最多使用 40 个任务执行：4 个 baseline，加上 3 ×〔4 个训练 + 4 个父代验证 + 4 个候选验证〕。单次重复的最终面板另加 12 个。每题最多八次模型调用，每次提案另需一次调用。失败、拒绝和无变化的尝试都计入预算，最终测试在搜索上限之外单独记账。托管模型可能收费，未知成本不能按零计算。

## Agent 可以做什么

Agent 每次返回一个 JSON 动作：`list`、`read`、`write`、`test` 或 `final`。固定的 `test` 动作在一次性快照中运行指定的公开 unittest。典型流程是测试 → 检查失败 → 编辑 → 再测试 → 提交，没有任意 shell 命令工具。原来的文本编辑 `skills` 模板仍使用四种工具。

公开测试源码和有界诊断可用于学习。私有测试与参考答案不进入模型请求和训练反馈。评测器使用公开及私有测试检查程序行为，因此不同写法的正确实现也能通过。参考源码用于验证任务包，不用于逐字匹配评分。输出文件名必须符合任务输入及参考文件定义的集合。

这里是**可信本地代码执行**。生成的 Python 可能使用宿主机权限；超时、输出上限和临时目录不构成操作系统沙盒。运行不可信程序或需要真正保密的测试标签时，应使用外部容器、虚拟机或评测服务。详见 [SECURITY.md](../SECURITY.md)。

## 添加自己的任务

清单根对象保持 `schema_version: 1`。每个任务包含：

```json
{
  "task_id": "my-utility-01",
  "group_id": "my-utility-family",
  "split": "train",
  "instruction": "完整描述函数行为与边界情况。",
  "input_files": {"solution.py": "...错误的 Python 源码..."},
  "expected_files": {"solution.py": "...参考 Python 源码..."},
  "grading": {
    "kind": "python-unittest",
    "public_tests": {"test_public.py": "...导入 solution 的 unittest 源码..."},
    "private_tests": {"test_private.py": "...独立边界用例..."},
    "timeout_s": 2
  }
}
```

将示意字符串替换为实际 Python 代码。两套测试都必须加载至少一个 unittest。测试文件名为平铺的 `test_*.py`，拒绝路径穿越和绝对路径。同源任务组只能属于一个分区，三个分区均不能为空。执行限制为最多 128 个文本文件、每组源码映射 1 MB、捕获输出 16 KiB，以及大于零且不超过十秒的超时。baseline 后修改测试、模型配置或任务清单，需要创建新工作区。

## 从 OpenRSI 借鉴了什么

[OpenRSI](https://github.com/FrontisAI/OpenRSI) 将可执行任务环境、改进算子与可复验结果结合起来。具体参考包括其[任务评测器](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/OpenMLE-Gym/openmle_gym/local_evaluator.py)和[按验证指标选择最终候选的测试](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/OpenMLE-Evo/third_party/aira-evo/tests/test_final_node_selection.py)。nanoRSI 将这些思路用于小型固定模型技能实验，并保留独立的最终测试分区。

本实现和任务包均独立编写，不包含 OpenRSI 代码、提示词、数据集或模型权重。它的[非商业许可证](https://github.com/FrontisAI/OpenRSI/blob/bf2b2ee19a260cb4dba0da1a20fb2212727b6ea4/LICENSE)与 nanoRSI 的 Apache-2.0 不同。nanoRSI 没有复现或声称取得 OpenRSI 的基准成绩，也不包含其训练体系或种群搜索。
