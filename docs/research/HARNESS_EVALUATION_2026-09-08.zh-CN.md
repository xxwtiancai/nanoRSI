# Skills / Harness 自进化：评估协议与 nanoRSI 的取舍

调研日期：2026-09-08。用途：为 [仓库设计提案](../design/HARNESS_PLATFORM_V0_2.zh-CN.md) 提供依据。
阅读对象为论文正文、附录和作者仓库；下文区分论文报告与项目建议。本次没有复现论文分数，也不把不同模型、预算、数据集上的提升拼成排行榜。

## 1. 定位结论

nanoRSI 应聚焦固定基础模型下，skills、提示策略和 Agent Harness 的可验证改进。最值得借鉴的是实验协议：逐任务执行记录、失败反馈、候选选择、冻结后的测试、成本核算，以及固定改进器的对照组。

三种主张需要分开：

- **Skill utility**：同一执行器加载一个 skill 后是否更好。
- **Persistent improvement**：改过的 skills/harness 是否让后续未见任务更好。
- **Recursive contribution**：让改过的 harness 参与下一轮改进，是否优于始终用初始 harness 做改进。

第三种不能仅凭第一种或第二种的结果推导出来。这是 nanoRSI 的实验定义，不是宣称学界已有统一的 RSI 判定标准。

## 2. 论文证据表

| 工作与已核验版本 | 修改对象 | 指标与实验 | 对 nanoRSI 的直接意义 |
| --- | --- | --- | --- |
| [SICA v2](https://arxiv.org/html/2504.15228v2)，§3–5 | Agent 自身的工具、提示和工作流代码 | SWE-bench Verified、LiveCodeBench 各固定抽样 50 题，另有文件编辑和符号定位任务；记录准确率、美元、耗时、tokens。效用权重为质量 0.5、成本 0.25、时间 0.25；15 轮运行约 $7,000。SWE 子集报告 17%→53%。 | 同一 Agent 可以执行任务和修改自身，但长程实验昂贵；不能只报分数而忽略预算。 |
| [DGM v2](https://arxiv.org/html/2505.22954v2)，§4、附录 C/E | 编码 Agent 的工具和工作流 | 80 次迭代；SWE 分阶段小样本筛选后扩大至 200 题；Polyglot 搜索用 50 题，另测全量。报告 solved rate；Polyglot 使用 pass@1。对照固定初始改进器、去掉开放式档案搜索；另测跨模型、跨 benchmark、跨语言迁移。 | 直接借鉴“固定改进器”消融。档案搜索是后续可研究算法，无须一开始进入 nano 内核。 |
| [GEPA v2](https://arxiv.org/pdf/2507.19457v2)，§4、附录 A/E/G | 多模块提示词 | 六个 benchmark，包括 HotpotQA、HoVer、IFBench 等；使用任务特定准确率/反馈。train 可见内容与标签，validation 仅用于选择，最终 test 独立。对比 MIPROv2、GRPO 等，并按 rollout 预算比较；另测选择策略和 merge 消融。 | 反思需要轨迹和文字反馈；必须计入验证 rollout，不能只统计产生修改所花的调用。 |
| [ACE v1](https://arxiv.org/html/2510.04618v1)，§3–4 | 可积累、局部修订的 playbook | AppWorld 用 TGC/SGC，FiNER/Formula 用 accuracy。离线遵循 train/validation/test；在线采用每题先预测、再更新。比较基础 ReAct、ICL、MIPROv2、GEPA、Dynamic Cheatsheet；消融 Reflector 与多 epoch。 | 支持局部 skill patch；离线泛化和在线持续学习必须分开报告。 |
| [Memento-Skills v1](https://arxiv.org/pdf/2603.18743v1)，§2.3、§3.1、图 10–12 | 可检索、执行、修复和新建的 skills | GAIA validation 划为 100 train/65 test，HLE 为 788/342；训练含反思重试。最终测试对照简化 read–write 版本：GAIA 52.3%→66.0%，HLE 17.9%→38.7%。有归因、重写、发现机制和生成的单元检查。 | skill 应包含指令与可选脚本；生成的自测可用于开发，但不能替代固定的外部任务评测。 |
| [Rethinking Self-Evolving Agent Skills v1](https://arxiv.org/html/2608.02636v1)，实验节、附录 A/B/C/E | 持久化 skill 文件 | 五个 benchmark、14 个模型×任务设置、42 组反馈运行；比较成功+失败、仅失败、仅成功，最多 10 轮。validation 选版本，冻结后测 test/鲁棒性/迁移。388 个候选中仅 55 个产生字节不同的 validation 新最佳；11 个设置选出进化版本，其中 9 个提高 test。 | 保存拒绝、无变化和停滞；hash 不变时分数波动不算新能力；反馈种类可以作为小型消融。 |
| [SkillsBench v4](https://arxiv.org/html/2602.12670v4)，§3–4、附录 D/L/M/N | 固定 skills 的使用效果 | 87 任务、8 领域、18 个模型×harness 配置；有/无 curated skills 配对，每条件取 3 trial，共 9,396 个槽位。task-macro reward 平均 33.9%→50.5%，+16.6 个百分点。采用容器和程序验证；reward 不全是二值。 | 借鉴配对评估和程序判分；它衡量 skill utility，并不直接提供自进化的数据划分或递归证据。 |

## 3. 阅读实验时必须保留的限定

- **SICA**：论文明确指出，短超时使初始成绩偏低，一部分收益来自文件编辑更快；正文未提供完整的独立进化重复与置信区间。不能将该子集成绩当成完整 SWE-bench 排行榜分数。
- **DGM**：搜索阶段会反复使用评测子集；论文另有跨 benchmark 的真正未见迁移。开放式搜索优于某个消融，不等于任何任务都需要复杂档案库。
- **GEPA**：这里采用 2026-02-14 的 v2；不混用 v1 摘要中的提升和 rollout 倍数。验证支出占比较大；不同优化器实际 rollout 并非完全相等，论文报告与 MIPROv2 的偏差在 10.15% 内。
- **ACE**：在线先预测再更新，和冻结 skill 后一次性测 test 是不同问题。不能把在线多次适应后的分数作为同等条件的离线结果。
- **Memento-Skills**：训练重试曲线不是每轮独立 test 曲线；未找到独立进化 seeds、完整 token/USD 预算和置信区间。LLM 冻结，但 router embedding 另行训练，因此并非整个系统完全没有参数训练。
- **Rethinking**：重复部署与独立重跑进化不同。其 GPT 设置在固定面板上做三次部署复测；SearchQA 的复测均值出现负增益。论文比较了 oracle 并行采样和顺序细化；oracle 是上界参考，不能当成现实可直接部署的选择器。
- **SkillsBench**：v4 与早期版本的任务数、试验数、聚合结果不同；v4 使用 healthy-first trial 选择及超时回填。成本只覆盖部分配置。不同任务上的 skill 长度分组，不足以证明“删短任何 skill 都会更好”。

以上“未找到”仅表示本次核验正文/附录未确认该信息，不断言作者从未做过。

## 4. 最新 Harness 工作补充

[Prime Agent v1](https://arxiv.org/html/2608.23552v1)（2026-08-24）强调固定支出下的分数、长程执行恢复、资源核算以及持久化 skills/memory。它在 nanoGPT 实验中也报告了 harness 对最终纪录影响小于噪声的情况。这支持记录执行失败和性能随预算变化，但它的守护进程、递归子 Agent 与 UI 不适合作为 nanoRSI 首版范围。

## 5. nano 项目的启发

[nanoGPT](https://github.com/karpathy/nanoGPT) 将可运行训练和模型实现放在容易阅读、可修改的代码中，同时提供基线和小实验。[autoresearch](https://github.com/karpathy/autoresearch) 把可改对象、单次时间预算和指标收得很窄：默认改 train.py、训练五分钟、观察验证指标再决定保留。

**对本项目的推论**：nano 应意味着一个读得懂、跑得通、有真实对照的完整实验。保留少量可靠边界；优先写一个真实 skills 示例，而不是泛化出各种模型训练、插件、分布式搜索和服务端模块。保持标准库内核是本仓库自己的约束，不能从 nanoGPT 推出所有 nano 项目都必须零依赖。

## 6. 推荐的最低评估标准（项目设计）

1. 固定模型与推理配置、工具、任务清单、验证器版本；记录不可控制的供应商漂移。
2. train 提供允许披露的执行轨迹；validation 选择候选；test 在所有比较组冻结之后才运行。
3. 同题、同预算配对比较初始和最终版本，报告任务宏平均分、百分点差、成本、耗时、失败率。
4. 至少区分无 skill、固定初始 skill、多轮改进；递归主张额外比较固定/进化 proposer harness。
5. 保留每次尝试与每次执行。超时、错误、拒绝、重复候选和 API 失败均不可从成本账中消失。
6. 用多次独立进化检查搜索稳定性，用重复部署检查执行随机性；两者分别统计。
7. 无收益或负迁移是有效实验结果。平台验收检查协议与证据完整，不要求自动产生正向结论。

后续具体数据合同、目录、成本口径和迁移验收见 [v0.2 设计提案](../design/HARNESS_PLATFORM_V0_2.zh-CN.md)。
