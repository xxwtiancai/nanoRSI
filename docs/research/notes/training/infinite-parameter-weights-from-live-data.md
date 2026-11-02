# Infinite-Parameter LLMs: Generating and Adapting Weights from Live Data

> Boltzbit Limited / University of Cambridge · 2026-09-16 · paper · **支撑·无闭环** · [论文](https://arxiv.org/abs/2609.18842)
> 机制族：支撑性适应机制 · 来源核验 2026-09-19 · 复现状态 not-run

## Pipeline

![围绕隐码信念组织的架构：活数据读入信念，按需生成低秩权重增量。](../../industry-rsi/assets/paper-figures/infinite-parameter-weights-from-live-data.svg)

超网络编码器把运行时交互数据编译为隐码并在线贝叶斯更新信念，再为冻结基座 FFN 生成 LoRA（r=8）权重增量——权重由数据再生成而非从存储库中选择，参数化无上界。

*图源：Figure 3 (inline SVG)*
## 结果（作者报告，非本地复现）

Qwen3-8B 冻结基座，MS MARCO（十段落）F1：data-to-weights 48.0 vs 上下文内 33.6 vs 闭卷 16.8；SQuAD（单段干净证据）上诚实给出边界：上下文内 85.3 vs data-to-weights 51.8；稀释下学习路由 53.3 vs 稠密检索 45.3。

## 证据边界

论文为 CC BY-NC-ND 4.0（非商业——对本 Apache-2.0 仓库仅可借鉴思想）；评测限于问答型证据任务；未找到代码或权重发布。

## 对 nanoRSI 的输入

稀释边界启发 nanoRSI 实验：把长而噪的证据缓存为紧凑派生状态 vs 在上下文中重读，测量缓存开始胜出的交叉点。

## 来源

[arXiv abstract](https://arxiv.org/abs/2609.18842) · [Paper HTML (affiliations, Table 4, Figure 3)](https://arxiv.org/html/2609.18842v1)
