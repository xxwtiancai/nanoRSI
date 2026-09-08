# nanoRSI

**一个小而完整的 Skills / Agent Harness 改进实验平台：固定基础模型，在有限预算下修改 Agent 的工作方式，并验证未见任务上的效果。**

内核只使用 Python 标准库和 Git。执行流程为：训练任务 → 轨迹与反馈 → skill patch → 验证集比较 → 接受或保留父代 → 冻结 → 独立最终测试。

[English README](README.md)

## 安装

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

需要 Python 3.11+ 和 Git。参考 Runner 使用外部模型命令，附带一个 OpenAI-compatible HTTP 适配器；兼容的本地模型服务可不配置 key，托管模型调用可能产生费用。

## Skills 实验

```bash
nanorsi new skills ./skills-lab --goal "改进可靠的文件编辑能力"
```

**建立 baseline 前**，修改 `skills-lab/nanorsi.toml` 中的 `[agent]`：填写真实 `model`、`base_url`；需要鉴权时配置指向工作区外文件的绝对 `api_key_file` 路径。也可以用自有 JSON 协议桥接替换 `model_command`。默认模型是待配置占位值。

```bash
nanorsi doctor --workspace ./skills-lab
nanorsi baseline --workspace ./skills-lab
nanorsi run --workspace ./skills-lab
nanorsi report --workspace ./skills-lab
nanorsi freeze --workspace ./skills-lab --repeats 3
nanorsi final-test --workspace ./skills-lab
nanorsi verify --workspace ./skills-lab
python examples/compare.py ./skills-lab/reports/final.json
```

模板包含 90 个确定性的本地文件任务，按来源组划分为 train/validation/test 各 30 个。它们用于验证协议，不是公开 benchmark，也不代表已经测得真实模型提升。

参考 Agent 实际加载 inspect、edit、verify 三个 skills，提供 list/read/write/final 操作，记录所加载内容的 hash。每题启动新进程并使用临时目录；本例不执行模型生成的 shell 命令，也不实现 skill 脚本执行或向量检索。

## 实验规则

- 默认只允许修改 `target/agent/skills/**`，单父代、单候选、顺序运行。
- 失败、拒绝、无变化都消耗尝试预算；只有严格改善且满足约束的候选成为下一代。
- train 提供任务反馈；validation 用于选择；最终 test 必须在 freeze 后运行，结果不能回流接受决策。
- `arm="frozen"` 始终使用初始 Harness 产生修改；`arm="self-use"` 使用最新接受的 Harness。修改目标都为当前父代，不同组使用独立工作区。
- 模型配置、任务数据、评分器、桥接文件从 baseline 起固定；更改它们应创建新实验。
- 保存逐题结果、skills hash、版本、完整提案与轨迹引用、费用和失败原因；未知费用/tokens 保持 null。
- 限制 attempts、任务 episodes、超时、模型轮数和输出；美元是观测值，不声称强制美元上限。

默认五轮最多需要 350 个搜索 episodes：baseline 30，加每轮 train 4、父代 validation 30、候选 validation 30；搜索上限为 400。最终测试三组各 30 题×3 次，共另需 270 episodes。提案调用单独记录。建议首次先缩小任务面板和预算。

freeze 固定重复次数（1–10）。最终测试比较初始 skills、无 skills 和选定 skills；已完成面板重复调用时复用，中断面板显式保留失败状态，避免静默重试挑选高分。比较统计区分独立进化与同一版本的重复部署。

## 离线兼容演示

```bash
nanorsi new artifact ./artifact-demo
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

原有 artifact/harness 保留为明确标注的脚本演示；model 保留外部训练合同。旧 `heldout` 参与选择，不能当作独立最终测试。v2 使用新建工作区，不能把旧数据重新命名后宣称未见测试。

## 执行边界与验证

默认是**可信本地运行**。worktree、修改范围限制和 HMAC 提供版本一致性检查，不能阻止同一 OS 用户下的程序读取宿主文件或答案。运行不可信 Harness 或要求真正的标签隔离时，需要外部容器、VM 或评测服务；本版没有内置经过加固的容器适配器。详见 [安全说明](SECURITY.md)。

```bash
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

测试包含模拟模型命令、本地 HTTP 服务、跨代接受/拒绝、预算、冻结与 self-use hash 验证。它们验证工程协议，不证明真实模型收益。内核保持不超过 2,500 行、每文件 300 行、每函数 50 行，以及零第三方运行时依赖。

## 文档

- [项目章程](docs/PROJECT_CHARTER.md)
- [内核规范](docs/specification.md)
- [设计与后续研究工作](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md)
- [论文评估协议调研](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md)
- [实施计划](docs/superpowers/plans/2026-09-09-skills-harness.md)
- [示例与比较工具](examples/README.md)
- [变更记录](CHANGELOG.md)
- [早期 RSI 调研](docs/research/RSI_SURVEY.zh-CN.md)

Apache-2.0。
