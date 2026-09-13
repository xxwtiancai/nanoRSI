# 快速开始／RSI 研究地图

[研究地图](README.zh-CN.md) · [English](QUICKSTART.md)

这是五分钟阅读路径。结构参考成熟开源项目的做法：先用一句话说明价值，再给出第一个可检查的入口，然后进入概念、案例和参考页。可对照 [vLLM](https://github.com/vllm-project/vllm#readme)、[Transformers](https://github.com/huggingface/transformers#readme)、[DeepSpeed](https://github.com/microsoft/DeepSpeed#readme) 和 [LangChain](https://github.com/langchain-ai/langchain#readme) 的导航方式。

## 选择阅读路径

| 我想…… | 从这里开始 | 可以得到什么 |
| --- | --- | --- |
| 先理解术语 | [研究全景与分类](LANDSCAPE.zh-CN.md) | 改变对象、反馈复用方式，以及直接、支撑、辅助证据的区别 |
| 看一个研究机制 | [参数/数据](parameter-learning.zh-CN.md)、[Agent/代码](agent-code.zh-CN.md)、[记忆/上下文](memory-context.zh-CN.md)、[研发流程](research-workflows.zh-CN.md) | 图片、来源定位、机制、结果、边界和拟议 nanoRSI 实验 |
| 找可用代码或权重 | [开放材料索引](OPEN_MATERIALS.zh-CN.md) | 分别列出仓库、检查点、数据和许可证 |
| 决定 nanoRSI 下一步做什么 | [落地优先级](ADOPTION.md) | 按顺序排列的实验、验收标准与对照组 |
| 审计为什么收录 | [检索覆盖与日期](COVERAGE.md) · [记录格式](FORMAT.md) | 检索边界、首发日期规则、来源字段和更新方法 |

## 正确阅读一条记录

1. 先看**视觉来源**。它是论文图、官方研究图片或裁剪后的原文页，条目会注明图号/页码和来源。
2. 再看**改变对象与反馈复用**。这是机制边界，比项目宣传语更有信息量。
3. 核对**作者报告结果**中的对照、指标、预算和数据划分。除非条目明确链接了本地复现，否则数值不是 nanoRSI 结果。
4. 在把成果当作设计依据前，先看**证据边界**和**本地复现状态**。
5. 单独打开**代码／权重／数据链接**。论文或仓库公开，并不自动允许再分发权重和数据集。

## 更新资料库

`catalog.json` 是唯一数据源。新增条目应提供带日期的一手来源、稳定 ID、一条视觉来源记录，以及明确的资产/许可证状态。然后重新生成页面并运行离线检查：

```bash
python docs/research/industry-rsi/render.py
python docs/research/industry-rsi/render.py --check
```

保留原始公开日期，区分后续修订与发布；对照组失败时也保留负结果。不要把普通模型发布、工程流程加速或记忆消融包装成通用 RSI。

## 本资料库不是什么

它不是行业排名、单一 RSI 总分，也不声称当前系统能自主训练自己的后继模型。它是一张有来源链接的研究地图，用来选择小型、可检查的 nanoRSI 实验。
