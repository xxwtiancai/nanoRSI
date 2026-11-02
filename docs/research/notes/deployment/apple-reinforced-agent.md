# Reinforced Agent: Inference-Time Feedback for Tool-Calling Agents

> Apple · 2026-04 · paper · **闭环** · [论文](https://arxiv.org/abs/2604.27233)
> 机制族：反馈审查与编排 · 来源核验 2026-09-21 · 复现状态 not-run

## Pipeline

![图 2：反馈架构——基础智能体给出临时工具调用，审查智能体在执行前评估，反馈循环直到批准或达到最大迭代。](../../industry-rsi/assets/paper-figures/apple-reinforced-agent.svg)

把执行与审查分离：基础工具调用智能体先给出临时工具调用，由独立的审查智能体在执行前评估——注入渐进反馈促其修订、在 N 个候选中选择或打分。执行前审查既缓解破坏性错误又规避状态恢复问题。审查者本身也被自动改进：GEPA（带 LLM 反思的遗传-帕累托提示进化）优化审查提示（长度增至 4.5 倍）；基础智能体不动。有益-有害双指标为审查者修正打分。

*图源：Figure 2 (inline SVG)*
## 结果（作者报告，非本地复现）

BFCL 无关检测 84.9% -> 90.4%（+5.5）；相关套件 90.9% -> 92.5%；tau2-Bench 48.7% -> 55.8%（+7.1）。收益风险比 3.1:1（o3-mini 审查者：有益 36.8% 对有害 11.7%）。GEPA 再加 +1.5-2.8%。代价：BFCL 延迟 6.2 倍（1.27s -> 7.87s），tau2-Bench 2.4 倍。

## 证据边界

基础智能体仅测 GPT-4o；GEPA 优化与收益/风险指标仅用于 BFCL；延迟倍数不小；无自动优化时手工调审查提示不可泛化。

## 对 nanoRSI 的输入

对 nanoRSI：把验收检查放到执行之前（执行前审查）而非破坏之后；用进化优化器优化审查者提示、冻结执行者。

## 来源

[arXiv abstract](https://arxiv.org/abs/2604.27233) · [Paper v1 (Figure 2, Tables, metrics)](https://arxiv.org/html/2604.27233v1) · [Apple ML research blog](https://machinelearning.apple.com/research/reinforced-agent-inference-feedback)
