# 企业 RSI 研究地图

**2025-09-13 → 2026-09-13** · **28** 条窗口内记录

按一手来源整理企业及产学合作的论文、系统与公开成果，属于精选资料库，并非穷尽式综述。每条详情都带一张本地可视化证据卡，并在有核验结果时单独列出代码、权重或数据链接。分类与 nanoRSI 应用方向是我们的解读；除非条目链接了本地复现证据，数值均为作者报告。这些异构结果不能合成排行榜，也不能证明通用 RSI 已解决。

**直接有界闭环**：更新后的代码、记忆、数据策略、参数或学习规则影响后续迭代，但不一定改进了改进算法自身。**支撑技术／评测**：有用的适配、记忆或评测机制，尚未展示递归部署闭环。**自动化／辅助研发**：证据主要针对研究流程或独立目标模型，人类参与程度各异。这些标签表示条目的侧重点，可以有交集，不是已证明 RSI 的等级。

[检索覆盖、日期与早期基础](COVERAGE.md) · [下一步可实现的实验](ADOPTION.md) · [catalog.json](catalog.json) · [English](README.md) / [中文](README.zh-CN.md)

## 按改变对象浏览

| 分类 | 条目数 |
| --- | ---: |
| [参数与训练数据](parameter-learning.zh-CN.md) | 11 |
| [Agent 与代码](agent-code.zh-CN.md) | 4 |
| [记忆与上下文](memory-context.zh-CN.md) | 5 |
| [自动化研发与评测](research-workflows.zh-CN.md) | 8 |

## 时间索引

| 日期 | 工作 | 机构 | 证据类别 |
| --- | --- | --- | --- |
| 2026-09-01 | [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](agent-code.zh-CN.md#bytedance-harnessdev) | ByteDance Seed / Singapore University of Technology and Design / Georgia Institute of Technology / M-A-P / TokenWave.AI | 直接有界闭环 |
| 2026-08-31 | [S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](memory-context.zh-CN.md#bytedance-s3gym) | ByteDance Seed / M-A-P / TokenWave.AI | 直接有界闭环 |
| 2026-08-31 | [Aspire: Can Models Self-Evolve from Vague Goals?](parameter-learning.zh-CN.md#bytedance-aspire) | ByteDance Seed / Singapore University of Technology and Design / M-A-P / TokenWave.AI | 直接有界闭环 |
| 2026-08-28 | [TASTE: Can AI Models Judge AI Safety Research Proposals?](research-workflows.zh-CN.md#taste) | Anthropic / Anthropic Fellows Program | 支撑技术／评测 |
| 2026-08-14 | [Measuring Autonomous AI Research](research-workflows.zh-CN.md#prime-measuring-autonomous-ai-research) | Prime Intellect | 自动化／辅助研发 |
| 2026-08-05 | [Prime Agent: A Self-Improving RLM Harness](memory-context.zh-CN.md#prime-agent) | Prime Intellect / Princeton University / MIT | 直接有界闭环 |
| 2026-08 | [Automated Researchers Can Mitigate Well-Characterized Alignment Failures](research-workflows.zh-CN.md#automated-alignment-researchers) | Anthropic Fellows Program | 自动化／辅助研发 |
| 2026-07-30 | [Frontis-MA1: Training an AI4AI Model towards Recursive Self-Improvement in Machine Learning Engineering](research-workflows.zh-CN.md#frontis-ma1-openmle) | Frontis.AI — Horizon Research / Tsinghua University | 直接有界闭环 |
| 2026-07-15 | [GPT-Red: Automated Red Teaming via Self-Play at Scale](parameter-learning.zh-CN.md#gpt-red) | OpenAI | 直接有界闭环 |
| 2026-04 | [Automated Weak-to-Strong Researcher](research-workflows.zh-CN.md#automated-w2s) | Anthropic / Anthropic Fellows Program | 自动化／辅助研发 |
| 2026-03-19 | [Hyperagents](agent-code.zh-CN.md#meta-hyperagents-2026) | Meta / University of British Columbia | 直接有界闭环 |
| 2026-03-18 | [MiniMax M2.7: Early Echoes of Self-Evolution](agent-code.zh-CN.md#minimax-m27-self-evolution) | MiniMax | 直接有界闭环 |
| 2026-03-11 | [A3: An Automated Alignment Agent for Safety Finetuning](parameter-learning.zh-CN.md#a3) | Anthropic / Anthropic Fellows Program / Constellation | 直接有界闭环 |
| 2026-02-27 | [How Cognition Uses Devin to Build Devin](research-workflows.zh-CN.md#cognition-devin-builds-devin) | Cognition | 自动化／辅助研发 |
| 2026-02-18 | [Discovering Multiagent Learning Algorithms with Large Language Models](research-workflows.zh-CN.md#google-alphaevolve-marl-2026) | Google DeepMind | 自动化／辅助研发 |
| 2026-02-13 | [Doc-to-LoRA: Learning to Instantly Internalize Contexts](parameter-learning.zh-CN.md#sakana-doc-to-lora) | Sakana AI / Minerva University | 支撑技术／评测 |
| 2026-02-05 | [How we used Codex to train and deploy GPT-5.3-Codex](research-workflows.zh-CN.md#codex-builds-codex) | OpenAI | 自动化／辅助研发 |
| 2025-12-04 | [TRINITY: An Evolved LLM Coordinator](parameter-learning.zh-CN.md#sakana-trinity) | Sakana AI / Institute of Science Tokyo / University of Michigan | 支撑技术／评测 |
| 2025-11-27 | [DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning](parameter-learning.zh-CN.md#deepseek-math-v2) | DeepSeek-AI | 直接有界闭环 |
| 2025-11-20 | [Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](parameter-learning.zh-CN.md#salesforce-unc-agent0) | UNC-Chapel Hill / Salesforce Research / Stanford University | 直接有界闭环 |
| 2025-11-13 | [SIMA 2: A Generalist Embodied Agent for Virtual Worlds](parameter-learning.zh-CN.md#google-sima2-2025) | Google DeepMind | 直接有界闭环 |
| 2025-11-13 | [AgentEvolver: Towards Efficient Self-Evolving Agent System](parameter-learning.zh-CN.md#alibaba-agentevolver) | Alibaba Group — Tongyi Lab | 直接有界闭环 |
| 2025-10-22 | [Discovering state-of-the-art reinforcement learning algorithms](parameter-learning.zh-CN.md#google-discorl-2025) | Google DeepMind | 支撑技术／评测 |
| 2025-10-06 | [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](memory-context.zh-CN.md#sambanova-stanford-ace) | Stanford University / SambaNova Systems / UC Berkeley | 直接有界闭环 |
| 2025-10-06 | [LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation](memory-context.zh-CN.md#microsoft-legomem-2025) | Microsoft | 支撑技术／评测 |
| 2025-10-01 | [ACON: Optimizing Context Compression for Long-horizon LLM Agents](memory-context.zh-CN.md#microsoft-acon-2025) | Microsoft / KAIST / University of Cambridge | 直接有界闭环 |
| 2025-09-17 | [ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution](agent-code.zh-CN.md#sakana-shinkaevolve) | Sakana AI | 直接有界闭环 |
| 2025-09-14 | [Self-Evolving LLMs via Continual Instruction Tuning](parameter-learning.zh-CN.md#tencent-moe-cl) | Beijing University of Posts and Telecommunications / Tencent AI Lab | 支撑技术／评测 |

## 日期、复用与更新

采用所引首版论文或实质成果报告的日期，不采用抓取时间、仓库活跃时间或会议年份。仅能确认月份时保留月份；条目说明区分先行公告与后续论文。代码可见不代表可以不受限复用，权重和数据可能有不同条款。本次整理未执行或复现上游系统。

更新时编辑唯一数据源 JSON，并遵循[记录格式](FORMAT.md)。窗口滚动后，生成器会将旧条目保留在历史归档中。修改指标或发布状态前需重新核对来源。

```bash
python docs/research/industry-rsi/render.py
python docs/research/industry-rsi/render.py --check
```
