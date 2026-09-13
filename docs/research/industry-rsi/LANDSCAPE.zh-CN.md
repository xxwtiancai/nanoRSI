# 研究全景与分类／RSI research landscape

[研究地图](README.zh-CN.md) · [English](LANDSCAPE.md)

资料库按“持续改变的对象”组织内容。这样可以避免把一次记忆写入、一个学习规则和一套研发辅助流程混成同一种 RSI。

## 四种改变面

| 改变面 | 要回答的问题 | 本地图中的代表成果 |
| --- | --- | --- |
| 参数与训练数据 | 生成任务、标签、奖励或更新规则是否改变目标模型参数，并进入下一轮？ | AgentEvolver、Agent0、SIMA 2、GPT-Red、A3 |
| Agent 与代码 | 持久化程序、scaffold 或 harness 是否被修改、评测并复用？ | HarnessDev、Hyperagents、ShinkaEvolve、MiniMax M2.7 |
| 记忆与上下文 | 经验是否变成可检索上下文、playbook、适配器或记忆状态？ | ACE、ACON、LEGOMem、S3Gym、Prime Agent |
| 自动化研发与评测 | Agent 是否改进独立研究产物，或让评测闭环更可扩展？ | AAR、弱监督强模型研究器、TASTE、AlphaEvolve MARL、Prime 研发评测 |

## 证据类别

这些标签表示条目的侧重点，不是能力等级。

- **直接有界闭环**：持久化代码、记忆、策略、参数或学习规则的改变会进入后续迭代；闭环仍受任务、评测器、模型或计算预算约束。
- **支撑技术／评测**：适配、记忆、学习优化或度量帮助改进系统，但公开实验没有展示递归部署闭环。
- **自动化／辅助研发**：Agent 改进独立目标，或加速人类主导的研究流程。这对 nanoRSI 有参考价值，但不代表控制器自身得到改进。

## 阅读证据的顺序

比较两个系统时按以下顺序阅读：

1. **对象**：代码、记忆、数据策略、模型参数、学习规则或独立研究产物。
2. **反馈**：可执行测试、奖励、验证器、留出分数、人类偏好或运营评审。
3. **更新**：改了什么、谁选择、下一轮是否能看到结果。
4. **门控**：回滚、冻结测试、能力约束、人类评审，或没有门控。
5. **泛化**：新任务、领域、模型、随机种子和预算；胜负都保留。

## 导航设计

入口页保持简短，按单一任务路由到：[快速开始](QUICKSTART.zh-CN.md)、本分类页、[按改变面查看案例](README.zh-CN.md#按改变对象浏览)、[开放材料](OPEN_MATERIALS.zh-CN.md)、[落地优先级](ADOPTION.md)，最后是[检索覆盖与记录格式](COVERAGE.md)。这个顺序参考官方 [vLLM README](https://github.com/vllm-project/vllm#readme)、[Transformers README](https://github.com/huggingface/transformers#readme)、[DeepSpeed README](https://github.com/microsoft/DeepSpeed#readme) 和 [LangChain README](https://github.com/langchain-ai/langchain#readme) 中的价值说明、快速开始、能力分组、参考资料、贡献路径和边界说明。

## 边界

本地图不把准确率、吞吐、token 和成本等异构指标合成一个分数。论文图可以说明机制，但标题基准可能衡量另一种对象。模型可以协助研究者构建更好的训练流程，而它自己的权重仍保持不变。仓库公开也可能有非商业条款，或不包含权重/数据。这些区别属于证据本身，不是脚注。
