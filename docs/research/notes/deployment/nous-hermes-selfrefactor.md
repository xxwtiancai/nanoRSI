# Refactoring Hermes with 1,393 agents

> Nous Research · 2026-09-15 · report · **闭环** · [论文](https://nousresearch.com/refactoring-hermes-with-1393-agents/) · [仓库](https://github.com/NousResearch/hermes-agent)
> 机制族：自改写元智能体与谱系 · 来源核验 2026-10-16 · 复现状态 not-run

## Pipeline

![Nous Research 官方文章题图：Hermens 用 1,393 个子智能体自主重构自身约百万行代码库。](../../industry-rsi/assets/paper-figures/nous-hermes-selfrefactor.png)

人类下达 /goal 后，Hermes 编排器把自家约 106 万行仓库切成 36 组，派出工作子智能体在独立 git worktree 中编辑并做接口校验（JSON schema、逐字节一致的 CLI --help）；经验教训自动写入 hermes-agent-dev Markdown 技能并再共享，让其他智能体继承已学流程。

*图源：Post banner graphic*
## 结果（作者报告，非本地复现）

1,393 个子智能体（峰值并发 218）、约 19 个活跃小时、主运行约 1.93 万美元（人工估算 15 万-180 万）；非测试 Python 从 1,063,826 行降至 698,363 行（−34.4%）；超 5,000 行的文件 37 → 6；超 300 行的函数 192 → 2；最长 if/elif 链 92 → 9 分支；4,000 次符号查询测试的平均返回 token 从 2,218 降至 993。

## 证据边界

无能力对照——测的是代码健康度而非任务表现；评审抓到测试漏掉的真实回归（删除公开命名、约 65 处异常处理被重写）；首次运行因鉴权 token 过期中断；模块数与部分入口导入时间变差。

## 对 nanoRSI 的输入

nanoRSI 已有每候选 worktree 评测；要补的是把事后教训自动写入技能文件供后续运行加载，让一次性失败与持久流程记忆之间闭环。

## 来源

[Nous Research blog report](https://nousresearch.com/refactoring-hermes-with-1393-agents/) · [Hermes Agent repository](https://github.com/NousResearch/hermes-agent) · [Repository LICENSE](https://github.com/NousResearch/hermes-agent/blob/main/LICENSE) · [Hermes Agent v0.21.5 release](https://github.com/NousResearch/hermes-agent/releases/tag/v2026.9.24) · [Hermes Agent v0.21.6 release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.21.6) · [hermes-agent v0.22.2 release](https://github.com/NousResearch/hermes-agent/releases/tag/v0.22.2)
