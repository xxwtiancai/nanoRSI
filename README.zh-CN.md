# nanoRSI

[![CI](https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg)](https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Runtime dependencies](https://img.shields.io/badge/runtime_dependencies-0-4C1?logo=python&logoColor=white)](pyproject.toml)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-2596BE.svg)](LICENSE)

nanoRSI 是一个小而完整的 **Recursive Self-Improvement (RSI)** 实验内核。它帮助你为 artifact、harness、model 三类目标建立可复现实验：提出一个有限修改、生成精确 Git 候选、在冻结评测契约下执行、按证据决定接受或拒绝，并留下可验证谱系。

它不是自主超智能运行时。v0.1 明确只有一个父代、一个子候选、一个外部 proposer、一个 canonical evaluator 和单父 hill-climbing。

![nanoRSI 证据闭环](docs/assets/nanorsi-loop.svg)

## 快速开始

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .

nanorsi new artifact ./artifact-demo --goal "找到最大值"
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi report --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

内置 artifact demo 完全离线运行，不需要模型 API。初始目标函数故意表现较差，mock proposer 提交一个统一 diff，冻结 evaluator 检查 gate 与 heldout 案例，只有分数和约束通过时才接受新候选。

## 三类 RSI surface

![三类 RSI surface](docs/assets/nanorsi-layers.svg)

| Surface | v0.1 内容 |
| --- | --- |
| Artifact | 离线可运行算法/工件优化闭环 |
| Harness | mock target、公开任务/私有评分、prompt 或策略修改闭环 |
| Model | 外部训练命令契约、doctor、安全与预算字段 |

Model 层不内置训练框架。nanoRSI 只负责契约、执行边界、评测与证据记录，训练本身必须由显式配置的外部命令完成。

## 安全边界

候选永远不能修改：

```text
evaluator/
proposer/
nanorsi.toml
lineage.jsonl
.nanorsi/
reports/
已接受 refs 与评分 receipt
```

每个候选都在 detached Git worktree 中评测；候选 evaluator 指纹必须与 generation 0 一致；评分只能由 nanoRSI mechanism 写入 HMAC 保护的 append-only JSONL。

外部命令均为 argv subprocess，不经过 shell，并带超时和环境过滤。对不可信 proposer、evaluator 或 target runner，请额外使用容器或沙箱。

## 常用命令

| 命令 | 说明 |
| --- | --- |
| `nanorsi new artifact PATH` | 创建 artifact 实验 |
| `nanorsi new harness PATH` | 创建 harness 实验 |
| `nanorsi new model PATH` | 创建 model 外部训练契约 |
| `nanorsi baseline` | 建立 generation 0 快照与基线 |
| `nanorsi step` | 执行一轮 proposal → evaluation → gate |
| `nanorsi report` | 输出 Markdown/JSON 报告 |
| `nanorsi verify` | 校验谱系、receipt 与父链 |
| `nanorsi recover` | 清理已死进程留下的 lock/worktree |

## 更多文档

- [RSI 前沿研究全景与架构映射调研](docs/research/RSI_SURVEY.zh-CN.md)
- [内核规范](docs/specification.md)
- [项目章程](docs/PROJECT_CHARTER.md)
- [安全策略](SECURITY.md)
- [贡献指南](CONTRIBUTING.md)
- [English README](README.md)

## 许可证

Apache-2.0
