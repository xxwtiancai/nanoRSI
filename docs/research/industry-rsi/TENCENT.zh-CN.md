# Tencent RSI 覆盖审计 / Tencent RSI coverage audit

[研究地图](README.zh-CN.md) · [English](TENCENT.md) · [检索覆盖与日期](COVERAGE.md)

本页把腾讯检索边界公开化：分别列出窗口内展示持久化改变的一手论文与仓库、窗口外的腾讯工作，以及不能证明递归自我改进的普通模型或 Agent 发布。指标、机构、许可和图片仍以带日期的分类资料库为准。

## 窗口内记录（2025-09-13 → 2026-09-13）

| 工作 | 改变面 | 什么被持久化 | 公开实现 | 分类 |
| --- | --- | --- | --- | --- |
| [SkillHone](agent-code.zh-CN.md#tencent-skillhone) · [论文](https://arxiv.org/abs/2606.08671) | Agent 技能 | 决策历史与接受的技能修订被后续会话复用 | [Tencent/SkillHone](https://github.com/Tencent/SkillHone) · `LICENSE` 声明 MIT | 直接有界闭环 |
| [SPEAR](parameter-learning.zh-CN.md#tencent-spear) · [论文](https://arxiv.org/abs/2509.22601) | 策略训练 | 自模仿回放和课程奖励改变后续策略更新 | [TencentYoutuResearch/SPEAR](https://github.com/TencentYoutuResearch/SPEAR) · SPEAR 自定义条款 | 直接有界闭环 |
| [MoE-CL](parameter-learning.zh-CN.md#tencent-moe-cl) · [论文](https://arxiv.org/abs/2509.18133) | 参数／持续学习 | LoRA 专家在外部提供的任务序列中保留知识 | [BAI-LAB/MoE-CL](https://github.com/BAI-LAB/MoE-CL) | 支撑技术／评测 |
| [Training-Free GRPO](memory-context.zh-CN.md#tencent-training-free-grpo) · [论文](https://arxiv.org/abs/2510.08191) | 记忆／上下文 | 冻结模型写入经验库，改变后续上下文 | [Youtu-Agent 分支](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · `LICENSE` 声明 MIT | 直接有界闭环 |
| [WebAggregator / Explore-to-Evolve](agent-code.zh-CN.md#tencent-webaggregator) · [论文](https://arxiv.org/abs/2510.14438) | 程序／训练数据 | 可执行聚合逻辑和可验证 QA 进入后续模型训练 | [Tencent/WebAggregator](https://github.com/Tencent/WebAggregator) · WebAggregator 自定义条款 | 直接有界闭环 |

这五条覆盖本轮发现的不同腾讯机制：技能产物进化、回放策略更新、持续参数学习、冻结模型的上下文经验进化，以及可执行网页数据构建。它们不是一个同质的“腾讯 RSI 模型”，每条记录的改变对象和控制边界都不同。

## 窗口外或相邻腾讯线索

| 线索 | 首发日期 | 决定 |
| --- | --- | --- |
| [WebEvolver](https://arxiv.org/abs/2504.21024) | 2025-04-23 | 作为较早的 SelfEvolvingAgent 基础工作保留，但超出滚动窗口。 |
| [WebCoT](https://arxiv.org/abs/2505.15478) | 2025-05-26 | 作为较早的反思／分支／回滚线索保留，但超出滚动窗口。 |
| [Cognitive Kernel-Pro](https://arxiv.org/abs/2508.00414) · [代码](https://github.com/Tencent/CognitiveKernel-Pro) | 2025-08-01 | 作为窗口前的腾讯研究与代码线索保留。 |
| [VScan](https://github.com/Tencent/SelfEvolvingAgent) | 2026 | 腾讯档案中有列出，但单独的 token reduction 不展示持久自我改进闭环。 |
| 混元模型及产品发布 | 多个日期 | 仅作为背景记录；从已核验发布页未建立持久修改、评测与复用闭环。 |

## 检索与证据规则

本轮核验了 Tencent SelfEvolvingAgent 索引、Tencent 与 Tencent YoutuResearch 仓库、Youtu-Agent 分支、arXiv 提交历史及 v1 HTML 论文。只有同时满足以下条件才进入滚动资料库：首发日期在窗口内；论文机构或第一方发布关系明确；论文说明可变产物接收反馈并影响后续迭代。仓库可见、后续修订日期、会议年份或单纯模型发布都不满足条件。

代码、权重、数据和许可分别审计。“公开仓库”表示核验日可以访问链接文件，不表示仓库包含检查点或数据集。SPEAR 与 WebAggregator 的腾讯自定义条款及第三方组件条款继续有效；资料库已记录其条款写明的欧盟使用限制。

这是带日期的工程审计，不声称覆盖所有未公开的腾讯内部项目。后续更新应先补充一手来源、首发日期、改变对象、反馈路径、复用路径，以及原文 pipeline 图或官方研究图片，再提升线索等级。
