<p align="center">
  <img src="docs/assets/brand/nanorsi-hero.png" alt="nanoRSI：小内核，让改进有据可查" width="100%">
</p>

<p align="center"><strong>一个最小、可审计的递归 harness 自改进循环。</strong><br>
模型冻结，围绕它的 harness 可编辑；递归做提案、探测、反差、组合——只在冻结之后才评分。</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="#快速开始">快速开始</a> ·
  <a href="#循环">循环</a> ·
  <a href="#接入真实执行器">真实执行器</a> ·
  <a href="#结果">结果</a> ·
  <a href="docs/research/RSI_NOTES.md">研究笔记</a>
</p>

---

nanoRSI v0.5 是对 **Harness²**（Google Cloud AI Research，[arXiv 2610.14224](https://arxiv.org/abs/2610.14224)）
递归机制的标准库从零实现：模型冻结，让围绕模型的 *harness* 可编辑，用执行证据改进 harness，
闭环里不放验证器。整个内核 16 个模块、约 1400 行；每一次 rollout、提案、反差、组合与评分都是
哈希链账本里的一条事件。

| 可编辑的 | 编辑如何准入 | 诚实性 |
| --- | --- | --- |
| system prompt · guardrails · memory · tool guidance · skills · scripts | 匹配配置下探测 → `mitigates` / `neutral` / `regresses` 反差，不用真值 | 分数只在 `freeze` 之后存在；预算逐次扣减；账本 `verify` 对任何改写报错 |

同一名字下有两条线。**工程轨**就是这个循环。**调研轨**是每日更新的 RSI 论文活文档，按 1250 篇
RSI 综述的两轴分类：[docs/research/RSI_NOTES.md](docs/research/RSI_NOTES.md)。

## 快速开始

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git && cd nanoRSI
python3 -m venv .venv && source .venv/bin/activate && pip install -e .

nanorsi new ./lab --goal "改进文档工作的 harness"
nanorsi configure --workspace ./lab --model 你的模型 --base-url https://api.example.com/v1 \
  --api-key-file ~/.nanorsi/keys/provider.key        # 密钥留在工作区之外
nanorsi doctor --workspace ./lab --check-model

nanorsi evolve --workspace ./lab      # 每任务：base → INV/DOM 提案 → 探测 → 反差 → 组合 → final
nanorsi freeze --workspace ./lab      # 钉住每任务选中的 harness；之后拒绝 evolve
nanorsi judge  --workspace ./lab      # 用工作区 judge 给 base 与 final 交付物评分
nanorsi report --workspace ./lab && nanorsi verify --workspace ./lab
```

模板自带四文件基础 harness、两个内置 agent 可执行的离线文档任务和一个关键词 judge——
不装任何基准，在任意 OpenAI 兼容端点上就能跑完整个生命周期。

## 循环

```text
每个任务                                        mode agg（并行，宽度）          mode seq（串行，深度）
  base1  ── 参照 rollout                        k 对候选对 base 探测，          k 轮；每轮组合
  INV    ── 一条跨领域编辑 ─┐                   再做 k 次组合                   成为下一轮的 base
  DOM    ── 一条领域编辑   ─┤ 匹配配置下各自探测
  contrast ─ 每个探测给 mitigates/neutral/regresses（不看分数）
  compose  ─ adopt / merge / keep，每个决定绑定具体观察
  final    ─ 组合后 harness 的 rollout（keep 复用参照）
  select   ─ finals > 1 时对匿名化交付物盲选
  lesson   ─ 一条有证据支撑的经验进入工作区库
```

以上每一步都是带 token 用量的账本事件，`reports/report.md` 是派生视图。论文另两个组件
（subagents、plugins）需要 nano 不自带的宿主运行时——边界见[规范](docs/specification.md)。

## 接入真实执行器

内核不知道任务由谁执行。设 `runner.kind = "command"`，把 `runner.command` 指向一个脚本：
读 `NANORSI_REQUEST`（任务、harness 目录、渲染好的 always-on 文本），写 `NANORSI_RESULT`
（轨迹、交付物、用量）。judge 是同样的形状（`NANORSI_JUDGE_REQUEST` → `n_passed / n_criteria`）。
[LAB + OpenCode 适配器](examples/lab_opencode/README.md) 就这样把论文自己的法律基准
跑在论文自己的执行器 substrate 上。

## 结果

| 研究 | 设置 | base → final partial |
| --- | --- | --- |
| [nanoRSI v0.5 on LAB](examples/results/harness2-lab-nanorsi/README.md) | 本循环，OpenCode 执行器，GLM-5.3 兼任执行器/改进器/judge | 0.859 → 0.838（−2.1 pp，3W/3T/2L）——两个 `mitigates` 采纳在终跑退化 |
| [Harness² 原始代码 on LAB](examples/results/harness2-lab-opencode/README.md) | `google-research/harness2`，同一套模型 | 0.872 → 0.892（+2.0 pp，5W/1T/2L） |
| 论文（GLM-5 / OpenCode） | 作者报告 | 0.596 → 0.714（+11.8 pp） |

v0.4 内核上的早期研究（BBH、ALFWorld、HumanEval、OpenEvolve 与 ShinkaEvolve 任务、参数学习）
原样保留在 [examples/results/](examples/results/) 作为历史证据；其任务包与运行器在
[examples/v0.4/](examples/v0.4/)，不再能在当前内核上运行。

## 诚实性规则

作者结果 ≠ 本地复现。负结果与零结果保留。不宣称通用递归自改进已解决。分数不影响选择。
预算、失败调用与未知成本始终可见。

## 许可

Apache-2.0。Harness²（Apache-2.0）提供了机制形态，未复制任何上游代码。LAB 任务
（harveyai/harvey-labs，MIT）作为已安装依赖使用。
