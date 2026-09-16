# 企业 RSI 研究地图

**2025-09-16 → 2026-09-16** · **95** 条窗口内记录

按一手来源整理企业及产学合作的论文、系统与公开成果，属于精选资料库，并非穷尽式综述。每条详情都带一张纳入仓库的论文原图、官方研究图片或原文页截图，并注明定位信息和来源链接；有核验结果时还会单独列出代码、权重或数据链接。分类与 nanoRSI 应用方向是我们的解读；除非条目链接了本地复现证据，数值均为作者报告。这些异构结果不能合成排行榜，也不能证明通用 RSI 已解决。

**直接有界闭环**：更新后的代码、记忆、数据策略、参数或学习规则影响后续迭代，但不一定改进了改进算法自身。**支撑技术／评测**：有用的适配、记忆或评测机制，尚未展示递归部署闭环。**自动化／辅助研发**：证据主要针对研究流程或独立目标模型，人类参与程度各异。这些标签表示条目的侧重点，可以有交集，不是已证明 RSI 的等级。

[快速开始](QUICKSTART.zh-CN.md) · [研究全景与分类](LANDSCAPE.zh-CN.md) · [开放材料](OPEN_MATERIALS.zh-CN.md) · [Tencent 覆盖审计](TENCENT.zh-CN.md) · [检索覆盖与日期](COVERAGE.md) · [下一步可实现的实验](ADOPTION.md) · [原文图片清单](assets/paper-figures/README.md) · [catalog.json](catalog.json) · [English](README.md) / [中文](README.zh-CN.md)

## 按改变对象浏览

| 分类 | 条目数 | 机制家族 |
| --- | ---: | --- |
| [参数与训练数据](parameter-learning.zh-CN.md) | 28 | [自博弈与课程任务生成](parameter-learning.zh-CN.md#family-self-play-curriculum) (11) · [验证器与奖励进化](parameter-learning.zh-CN.md#family-verifier-reward) (4) · [技能-权重共进化](parameter-learning.zh-CN.md#family-skill-weight-coevolution) (2) · [经验蒸馏与测试时适应](parameter-learning.zh-CN.md#family-experience-distillation) (4) · [自主训练智能体与数据管线](parameter-learning.zh-CN.md#family-autonomous-training) (3) · [支撑性适应机制](parameter-learning.zh-CN.md#family-enabling-adaptation) (4) |
| [Agent 与代码](agent-code.zh-CN.md) | 28 | [技能文件优化与技能库](agent-code.zh-CN.md#family-skill-file-optimization) (12) · [Harness 搜索与进化](agent-code.zh-CN.md#family-harness-search) (6) · [自改写元智能体与谱系](agent-code.zh-CN.md#family-self-modifying-meta-agents) (3) · [程序进化与进化搜索](agent-code.zh-CN.md#family-program-evolution) (4) · [反馈审查与编排](agent-code.zh-CN.md#family-feedback-orchestration) (2) · [安全与治理](agent-code.zh-CN.md#family-safety-governance) (1) |
| [记忆与上下文](memory-context.zh-CN.md) | 16 | [结构化知识库与图](memory-context.zh-CN.md#family-structured-knowledge) (6) · [经验积累与回放](memory-context.zh-CN.md#family-experience-accumulation) (4) · [上下文组织策略](memory-context.zh-CN.md#family-context-policies) (3) · [探索式记忆构建](memory-context.zh-CN.md#family-exploration-memory) (1) · [记忆进化评测研究](memory-context.zh-CN.md#family-memory-evolution-studies) (2) |
| [自动化研发与评测](research-workflows.zh-CN.md) | 23 | [AI 科学家系统](research-workflows.zh-CN.md#family-ai-scientists) (4) · [自主后训练及其评测](research-workflows.zh-CN.md#family-autonomous-post-training) (2) · [公司研发遥测](research-workflows.zh-CN.md#family-company-telemetry) (5) · [对齐自动化](research-workflows.zh-CN.md#family-alignment-automation) (3) · [分析与审计](research-workflows.zh-CN.md#family-analyses-audits) (6) · [立场、路线图与实验室](research-workflows.zh-CN.md#family-positions-labs) (3) |

## 时间索引

| 日期 | 工作 | 机构 | 家族 | 证据类别 |
| --- | --- | --- | --- | --- |
| 2026-09-14 | [SkillLift: Learning Dense Rubrics from Sparse Oracles for Efficient Skill Evolution](agent-code.zh-CN.md#skilllift-dense-rubrics) | Independent Researcher (Haoxiang Kang) / Fudan University (Ming Wen) | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-09-14 | [RSIAgent: Autonomous Exploration for Recursive Self-improvement in New Environments](memory-context.zh-CN.md#rsiagent-autonomous-exploration) | Aether AI / University of California San Diego / University of Illinois Chicago | 探索式记忆构建 | 直接有界闭环 |
| 2026-09-14 | [EvoOntology: A Self-Evolving Ontology Layer for Data Agents](memory-context.zh-CN.md#evoontology-self-evolving) | Renmin University of China | 结构化知识库与图 | 直接有界闭环 |
| 2026-09-14 | [The Economics of Recursive Self-Improvement](research-workflows.zh-CN.md#economics-of-rsi-2026) | METR / Stanford University / University of Virginia / Carnegie Mellon University / Columbia University / MIT / Stanford DEL / Epoch AI / Yale University / Elasticity Institute | 分析与审计 | 支撑技术／评测 |
| 2026-09-14 | [Dream-RSI: Improving Exploration Policies by Dreaming over the Discovery Tree](agent-code.zh-CN.md#dream-rsi-replay-simulator) | University of Maryland, College Park / Google DeepMind / University of Virginia | 程序进化与进化搜索 | 直接有界闭环 |
| 2026-09-11 | [EvoRS: On-Policy Self-Evolution of Reward Systems for Open-Ended Reinforcement Learning](parameter-learning.zh-CN.md#evors-reward-evolution) | Fudan University / Nankai University / Hello Group | 验证器与奖励进化 | 直接有界闭环 |
| 2026-09-10 | [The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement](research-workflows.zh-CN.md#genuine-rsi-roadmap-2026) | Shanghai Jiao Tong University / Theseus Labs / Tsinghua University / ByteDance / Shanghai AI Lab / ModelBest / Xiaohongshu Inc. / Humanlaya | 立场、路线图与实验室 | 支撑技术／评测 |
| 2026-09-08 | [NeoHorse-1: Towards Recursive Self-Improvement via Agentic Post-Training with Routing Harness](parameter-learning.zh-CN.md#tokenrhythm-neohorse-1) | TokenRhythm Technologies / Infinigence AI / Tsinghua University / Peking University / The Chinese University of Hong Kong / Alibaba Group | 自主训练智能体与数据管线 | 直接有界闭环 |
| 2026-09-08 | [SE-GoS: Self-Evolving Graph-of-Skills for Skill Library at Scale](memory-context.zh-CN.md#se-gos-skill-graph) | Peking University / Tencent / University of Edinburgh / Northwestern University / Tsinghua University | 结构化知识库与图 | 直接有界闭环 |
| 2026-09-08 | [Procedural Graphs: Self-Evolving Execution Structures for LLM Agents](memory-context.zh-CN.md#procedural-graphs-google) | Google / Georgia Institute of Technology / Peking University | 结构化知识库与图 | 直接有界闭环 |
| 2026-09-08 | [Experience Funnel: A State-Policy Alternating Loop for Self-Evolving Agents](parameter-learning.zh-CN.md#experience-funnel-state-policy) | The Hong Kong Polytechnic University / Huawei / Renmin University of China | 经验蒸馏与测试时适应 | 直接有界闭环 |
| 2026-09-06 | [Research acceleration: The view inside OpenAI](research-workflows.zh-CN.md#openai-research-acceleration-2026) | OpenAI | 公司研发遥测 | 自动化／辅助研发 |
| 2026-09-04 | [From Interaction Traces to Persistent Skills: Online Evolution for Computer-Use Agents](agent-code.zh-CN.md#persistent-skills-osworld) | University of Electronic Science and Technology of China / Zhejiang University | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-09-03 | [SimSkill: A Self-Evolving LLM Agent for Skill and Knowledge Accumulation in Traffic Simulation](agent-code.zh-CN.md#simskill-traffic) | Jilin University / Tongji University | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-09-02 | [SkillGLoW: Procedural-Family Skill Consolidation for Self-Improving Agents on Long-Horizon Task Streams](agent-code.zh-CN.md#skillglow-procedural-families) | National University of Singapore / Institute of Advanced Intelligence and Computing (IAIC), Singapore | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-09-01 | [HarnessDev: Can LLMs Create and Evolve Their Own Agent Harness?](agent-code.zh-CN.md#bytedance-harnessdev) | ByteDance Seed / Singapore University of Technology and Design / Georgia Institute of Technology / M-A-P / TokenWave.AI | Harness 搜索与进化 | 直接有界闭环 |
| 2026-08-31 | [S3Gym: Can LLMs Turn Self-Testing and Self-Judging into Self-Improvement?](memory-context.zh-CN.md#bytedance-s3gym) | ByteDance Seed / M-A-P / TokenWave.AI | 记忆进化评测研究 | 直接有界闭环 |
| 2026-08-31 | [Aspire: Can Models Self-Evolve from Vague Goals?](parameter-learning.zh-CN.md#bytedance-aspire) | ByteDance Seed / Singapore University of Technology and Design / M-A-P / TokenWave.AI | 自主训练智能体与数据管线 | 直接有界闭环 |
| 2026-08-30 | [Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents](agent-code.zh-CN.md#scientific-agent-skills-library) | K-Dense AI | 技能文件优化与技能库 | 支撑技术／评测 |
| 2026-08-28 | [TASTE: Can AI Models Judge AI Safety Research Proposals?](research-workflows.zh-CN.md#taste) | Anthropic / Anthropic Fellows Program | 对齐自动化 | 支撑技术／评测 |
| 2026-08-27 | [WikiSkill: Compiling Agent Experience into Persistent Knowledge for Skill Evolution](agent-code.zh-CN.md#wikiskill-experience-wiki) | Google Research / Virginia Tech | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-08-18 | [Chain-of-Experience for Continual LLM Improvement](memory-context.zh-CN.md#bytedance-chain-of-experience) | ByteDance Seed / UC Santa Cruz | 经验积累与回放 | 直接有界闭环 |
| 2026-08-14 | [Measuring Autonomous AI Research](research-workflows.zh-CN.md#prime-measuring-autonomous-ai-research) | Prime Intellect | 公司研发遥测 | 自动化／辅助研发 |
| 2026-08-13 | [Training AI Scientists to Replicate Research (Faraday on the Replica benchmark)](research-workflows.zh-CN.md#faraday-replica-ai-scientist) | Inherent Laboratories | AI 科学家系统 | 直接有界闭环 |
| 2026-08-05 | [Prime Agent: A Self-Improving RLM Harness](memory-context.zh-CN.md#prime-agent) | Prime Intellect / Princeton University / MIT | 经验积累与回放 | 直接有界闭环 |
| 2026-08-03 | [Qwen3.8-Max: A New Bar for Coding and Cowork (self-evolving harness demonstrations)](agent-code.zh-CN.md#qwen38-max-self-evolving-harness) | Alibaba (Qwen team) | Harness 搜索与进化 | 直接有界闭环 |
| 2026-08 | [SPADE: Self-Play in Adaptive Synthetic Executable Environments](parameter-learning.zh-CN.md#spade-adaptive-environments) | University of Washington / Stanford University / Northeastern University / Carnegie Mellon University / MIT / National University of Singapore / Seoul National University / Stevens Institute of Technology / University of Chicago | 自博弈与课程任务生成 | 直接有界闭环 |
| 2026-08 | [Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents](agent-code.zh-CN.md#skill-misevolution-safety) | City University of Hong Kong / University of Adelaide | 安全与治理 | 支撑技术／评测 |
| 2026-08 | [Recuris: Recursive Experiential-Working Memory Evolution for Long-Horizon Agents](memory-context.zh-CN.md#recuris-memory-evolution) | National University of Singapore / Stanford University / University of Oxford / Princeton University | 结构化知识库与图 | 直接有界闭环 |
| 2026-08 | [Mendel Godel Machine: Recursive Self-Improving Coding Agents via Comparative Evolution](agent-code.zh-CN.md#mgm-mendel-godel-machine) | University of Electronic Science and Technology of China / Ludwig Maximilian University of Munich / Munich Center for Machine Learning | 自改写元智能体与谱系 | 直接有界闭环 |
| 2026-08 | [Meta^n: Recursive Self-Improvement through Emergent Depth](agent-code.zh-CN.md#metan-emergent-depth) | University of Minnesota / Seoul National University | 自改写元智能体与谱系 | 直接有界闭环 |
| 2026-08 | [Automated Researchers Can Mitigate Well-Characterized Alignment Failures](research-workflows.zh-CN.md#automated-alignment-researchers) | Anthropic Fellows Program | 对齐自动化 | 自动化／辅助研发 |
| 2026-07-31 | [Self-Play Meets Skill Evolution: Self-Evolving Search Agents that Pose, Solve, and Remember](parameter-learning.zh-CN.md#sesa-self-play-skills) | University of Chinese Academy of Sciences / Institute of Automation, CAS / Peking University / Mininglamp Technology / Tsinghua University / Qilu University of Technology | 自博弈与课程任务生成 | 直接有界闭环 |
| 2026-07-31 | [Beagle / DarwinX: Evolving Agent Harnesses Through Natural Selection](agent-code.zh-CN.md#salesforce-beagle-darwinx) | Salesforce AI Research | Harness 搜索与进化 | 直接有界闭环 |
| 2026-07-30 | [Frontis-MA1: Training an AI4AI Model towards Recursive Self-Improvement in Machine Learning Engineering](research-workflows.zh-CN.md#frontis-ma1-openmle) | Frontis.AI — Horizon Research / Tsinghua University | AI 科学家系统 | 直接有界闭环 |
| 2026-07-26 | [From RLVR to RLSVR: Task Transformation Induces Self-Verifiable Rewards for Open-Ended LLM Self-Improvement](parameter-learning.zh-CN.md#spyrl-self-verifiable-rewards) | Duke University / Adobe Inc. / Pennsylvania State University / National University of Singapore / Oregon State University / Amazon | 自博弈与课程任务生成 | 直接有界闭环 |
| 2026-07-23 | [Toward Self-Improving Agents](research-workflows.zh-CN.md#salesforce-toward-self-improving-agents) | Salesforce (AI Labs) | 立场、路线图与实验室 | 支撑技术／评测 |
| 2026-07-15 | [GPT-Red: Automated Red Teaming via Self-Play at Scale](parameter-learning.zh-CN.md#gpt-red) | OpenAI | 自博弈与课程任务生成 | 直接有界闭环 |
| 2026-07-14 | [Self-Improvements in Modern Agentic Systems: A Survey](research-workflows.zh-CN.md#self-improving-agents-survey) | Jilin University / KAUST / University of Alberta / IDSIA/USI/SUPSI | 分析与审计 | 支撑技术／评测 |
| 2026-07-08 | [Recursive Self-Improvement in AI: From Bounded Self-Refinement to Autonomous Research Loops](research-workflows.zh-CN.md#rsi-survey-1250) | DeepGrounding / AlphaAvatar / Illinois Institute of Technology | 分析与审计 | 支撑技术／评测 |
| 2026-07 | [EvoPolicyGym: Benchmarking Executable-Policy Evolution in Coding Agents](agent-code.zh-CN.md#evopolicygym-benchmark) | University of Science and Technology of China / The Chinese University of Hong Kong / University of Macau / Tsinghua University / Zhejiang University / Soochow University / Brown University / Shanghai Jiao Tong University | 程序进化与进化搜索 | 支撑技术／评测 |
| 2026-06-30 | [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](agent-code.zh-CN.md#microsoft-skillopt) | Microsoft Research | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-06-29 | [Autonomous Research Agents: A Survey of AI Scientists and the Verification Gap](research-workflows.zh-CN.md#ai-scientist-verification-gap) | Johns Hopkins University (per author page; affiliations not stated in the audited HTML) | 分析与审计 | 支撑技术／评测 |
| 2026-06-09 | [Fully Autonomous Post-Training of a 30B Model with Multi-Round Agentic Search](research-workflows.zh-CN.md#amazon-autonomous-post-training) | Amazon | 自主后训练及其评测 | 直接有界闭环 |
| 2026-06-07 | [SkillHone: A Harness for Continual Agent Skill Evolution Through Persistent Decision History](agent-code.zh-CN.md#tencent-skillhone) | WeChat, Tencent Inc. | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-06-05 | [Introducing Sakana AI's Recursive Self-Improvement (RSI) Lab](research-workflows.zh-CN.md#sakana-rsi-lab) | Sakana AI | 立场、路线图与实验室 | 直接有界闭环 |
| 2026-06-05 | [Self-Evolving LLM Agents with In-Distribution Optimization](parameter-learning.zh-CN.md#qevolve-in-distribution) | Eindhoven University of Technology / University of Liverpool / MIT-IBM Watson AI Lab | 经验蒸馏与测试时适应 | 直接有界闭环 |
| 2026-06 | [OpenSkill: Open-World Self-Evolution for LLM Agents](agent-code.zh-CN.md#openskill-open-world) | Lehigh University / University of Illinois Chicago / University of British Columbia / Vector Institute / Salesforce AI Research / Massachusetts General Hospital / Harvard Medical School | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-06 | [ENPIRE: Physical Autoresearch - Self-Improving Coding Agents on Real Robots](research-workflows.zh-CN.md#nvidia-enpire-physical-autoresearch) | NVIDIA / Carnegie Mellon University / UC Berkeley | AI 科学家系统 | 直接有界闭环 |
| 2026-06 | [On the Generalization Gap in Self-Evolving Language Model Reasoning](research-workflows.zh-CN.md#gengap-self-evolution) | Google Research / Harvard University / Virginia Tech | 分析与审计 | 支撑技术／评测 |
| 2026-05-28 | [Self-Trained Verification for Training- and Test-Time Self-Improvement](parameter-learning.zh-CN.md#cmu-stv-self-trained-verification) | Carnegie Mellon University | 验证器与奖励进化 | 直接有界闭环 |
| 2026-05-11 | [SkillEvolver: Skill Learning as a Meta-Skill](agent-code.zh-CN.md#skillevolver-meta-skill) | Tsinghua University / Beijing Jiaotong University | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-05-11 | [EmbodiSkill: Skill-Aware Reflection for Self-Evolving Embodied Agents](agent-code.zh-CN.md#embodiskill-skill-aware-reflection) | Huazhong University of Science and Technology / University of Science and Technology of China / Microsoft Research / Institute for AI Industry Research (AIR), Tsinghua University / Nanjing University | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-04 | [SkillClaw: Let Skills Evolve Collectively with Agentic Evolver](agent-code.zh-CN.md#skillclaw-collective-evolution) | Alibaba (Amap DreamX Team) | 技能文件优化与技能库 | 直接有界闭环 |
| 2026-04 | [GenericAgent: A Self-Evololving Agent Growing a Skill Tree from a 3.3K-Line Seed](agent-code.zh-CN.md#genericagent-skill-tree) | Advantage AI Agent Lab (Shenzhen Aquaintelling Technology + Fudan University) | Harness 搜索与进化 | 直接有界闭环 |
| 2026-04 | [Automated Weak-to-Strong Researcher](research-workflows.zh-CN.md#automated-w2s) | Anthropic / Anthropic Fellows Program | 对齐自动化 | 自动化／辅助研发 |
| 2026-04 | [Reinforced Agent: Inference-Time Feedback Architecture for Tool-Calling Agents](agent-code.zh-CN.md#apple-reinforced-agent) | Apple | 反馈审查与编排 | 直接有界闭环 |
| 2026-03-19 | [Hyperagents](agent-code.zh-CN.md#meta-hyperagents-2026) | Meta / University of British Columbia | 自改写元智能体与谱系 | 直接有界闭环 |
| 2026-03-18 | [MiniMax M2.7: Early Echoes of Self-Evolution](agent-code.zh-CN.md#minimax-m27-self-evolution) | MiniMax | Harness 搜索与进化 | 直接有界闭环 |
| 2026-03-12 | [XSkill: Continual Learning from Experience and Skills in Multimodal Agents](memory-context.zh-CN.md#xskill-dual-stream) | Hong Kong University of Science and Technology / Zhejiang University / Huazhong University of Science and Technology | 结构化知识库与图 | 直接有界闭环 |
| 2026-03-11 | [A3: An Automated Alignment Agent for Safety Finetuning](parameter-learning.zh-CN.md#a3) | Anthropic / Anthropic Fellows Program / Constellation | 验证器与奖励进化 | 直接有界闭环 |
| 2026-03 | [Meta-Harness: End-to-End Optimization of Model Harnesses](agent-code.zh-CN.md#stanford-meta-harness) | Stanford University / MIT / KRAFTON | Harness 搜索与进化 | 直接有界闭环 |
| 2026-03 | [PostTrainBench: Can LLM Agents Automate LLM Post-Training?](research-workflows.zh-CN.md#posttrainbench-autonomous-post-training) | ELLIS Institute Tubingen / Max Planck Institute for Intelligent Systems / Tubingen AI Center / University of Tubingen / Thoughtful Lab | 自主后训练及其评测 | 支撑技术／评测 |
| 2026-03 | [EvoScientist: Self-Evolving Multi-Agent System for End-to-End Scientific Discovery](research-workflows.zh-CN.md#evoscientist-self-evolving) | Huawei Technologies / Vrije Universiteit Amsterdam | AI 科学家系统 | 直接有界闭环 |
| 2026-02-27 | [How Cognition Uses Devin to Build Devin](research-workflows.zh-CN.md#cognition-devin-builds-devin) | Cognition | 公司研发遥测 | 自动化／辅助研发 |
| 2026-02-18 | [Discovering Multiagent Learning Algorithms with Large Language Models](research-workflows.zh-CN.md#google-alphaevolve-marl-2026) | Google DeepMind | 公司研发遥测 | 自动化／辅助研发 |
| 2026-02-13 | [Doc-to-LoRA: Learning to Instantly Internalize Contexts](parameter-learning.zh-CN.md#sakana-doc-to-lora) | Sakana AI / Minerva University | 支撑性适应机制 | 支撑技术／评测 |
| 2026-02-09 | [SkillRL: Evolving Agents via Recursive Skill-Augmented Reinforcement Learning](parameter-learning.zh-CN.md#skillrl-skill-augmented-rl) | University of North Carolina at Chapel Hill / University of Chicago / UC San Diego / NEC Labs America / UC Berkeley / UC Santa Cruz | 技能-权重共进化 | 直接有界闭环 |
| 2026-02-05 | [How we used Codex to train and deploy GPT-5.3-Codex](research-workflows.zh-CN.md#codex-builds-codex) | OpenAI | 公司研发遥测 | 自动化／辅助研发 |
| 2026-02-04 | [Contextual Drag: How Errors in the Context Affect LLM Reasoning](research-workflows.zh-CN.md#princeton-contextual-drag) | Princeton Language and Intelligence, Princeton University | 分析与审计 | 支撑技术／评测 |
| 2026-02-02 | [MemSkill: Learning and Evolving Memory Skills for Self-Evolving Agents](memory-context.zh-CN.md#memskill-memory-skills) | Nanyang Technological University / University of Illinois Urbana-Champaign / University of Illinois Chicago / Tsinghua University | 结构化知识库与图 | 直接有界闭环 |
| 2026-01-30 | [From Self-Evolving Synthetic Data to Verifiable-Reward RL: Post-Training Multi-turn Interactive Tool-Using Agents](parameter-learning.zh-CN.md#eigendata-self-evolving-synthesis) | Tsinghua University / Eigen AI | 自主训练智能体与数据管线 | 直接有界闭环 |
| 2025-12-21 | [Toward Training Superintelligent Software Agents through Self-Play SWE-RL](parameter-learning.zh-CN.md#meta-ssr-self-play) | Meta FAIR / University of Illinois Urbana-Champaign / Carnegie Mellon University | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-12-18 | [SAGE: Reinforcement Learning for Self-Improving Agent with Skill Library](parameter-learning.zh-CN.md#sage-skill-augmented-grpo) | AWS Agentic AI (Amazon) / University of Wisconsin-Madison | 技能-权重共进化 | 直接有界闭环 |
| 2025-12-04 | [TRINITY: An Evolved LLM Coordinator](parameter-learning.zh-CN.md#sakana-trinity) | Sakana AI / Institute of Science Tokyo / University of Michigan | 支撑性适应机制 | 支撑技术／评测 |
| 2025-12-04 | [Conductor / Fugu: An LLM Trained to Orchestrate (and Include) Itself](parameter-learning.zh-CN.md#sakana-conductor-fugu) | Sakana AI / University of Michigan / Institute of Science Tokyo | 支撑性适应机制 | 支撑技术／评测 |
| 2025-11-27 | [DeepSeekMath-V2: Towards Self-Verifiable Mathematical Reasoning](parameter-learning.zh-CN.md#deepseek-math-v2) | DeepSeek-AI | 验证器与奖励进化 | 直接有界闭环 |
| 2025-11-25 | [Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory](memory-context.zh-CN.md#evo-memory-remem) | University of Illinois Urbana-Champaign / Google DeepMind | 记忆进化评测研究 | 支撑技术／评测 |
| 2025-11-20 | [Agent0: Unleashing Self-Evolving Agents from Zero Data via Tool-Integrated Reasoning](parameter-learning.zh-CN.md#salesforce-unc-agent0) | UNC-Chapel Hill / Salesforce Research / Stanford University | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-11-20 | [EvoLMM: Self-Evolving Large Multimodal Models with Continuous Rewards](parameter-learning.zh-CN.md#evolmm-proposer-solver) | Australian National University / Linkoping University / MBZUAI / Aalto University | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-11-13 | [SIMA 2: A Generalist Embodied Agent for Virtual Worlds](parameter-learning.zh-CN.md#google-sima2-2025) | Google DeepMind | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-11-13 | [AgentEvolver: Towards Efficient Self-Evolving Agent System](parameter-learning.zh-CN.md#alibaba-agentevolver) | Alibaba Group — Tongyi Lab | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-11-11 | [Feedback Descent: Open-Ended Text Optimization via Pairwise Comparison](agent-code.zh-CN.md#stanford-feedback-descent) | Stanford University | 反馈审查与编排 | 直接有界闭环 |
| 2025-11-02 | [ATLAS: Continual Learning, Not Training - Online Adaptation for Agents](memory-context.zh-CN.md#atlas-pamphlets) | Arc Intelligence | 经验积累与回放 | 直接有界闭环 |
| 2025-10-28 | [SPICE: Self-Play in Corpus Environments (adversarial curriculum from raw documents)](parameter-learning.zh-CN.md#meta-spice-self-play) | Meta FAIR / National University of Singapore | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-10-22 | [Discovering state-of-the-art reinforcement learning algorithms](parameter-learning.zh-CN.md#google-discorl-2025) | Google DeepMind | 支撑性适应机制 | 支撑技术／评测 |
| 2025-10-17 | [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle](parameter-learning.zh-CN.md#evolver-experience-lifecycle) | Shanghai AI Laboratory / Zhejiang University / East China Normal University / Fudan University / Shanghai Jiao Tong University / University of Science and Technology of China | 经验蒸馏与测试时适应 | 直接有界闭环 |
| 2025-10-16 | [WebAggregator: Enhancing Compositional Reasoning Capabilities of Deep Research Agent Foundation Models](agent-code.zh-CN.md#tencent-webaggregator) | Tencent AI Lab / The Chinese University of Hong Kong | 程序进化与进化搜索 | 直接有界闭环 |
| 2025-10-09 | [Self-Improving LLM Agents at Test-Time](parameter-learning.zh-CN.md#ttsi-test-time-self-improvement) | University of Illinois Urbana-Champaign | 经验蒸馏与测试时适应 | 直接有界闭环 |
| 2025-10-09 | [Training-Free Group Relative Policy Optimization](memory-context.zh-CN.md#tencent-training-free-grpo) | Tencent Youtu Lab / Fudan University / Xiamen University | 经验积累与回放 | 直接有界闭环 |
| 2025-10-06 | [Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models](memory-context.zh-CN.md#sambanova-stanford-ace) | Stanford University / SambaNova Systems / UC Berkeley | 上下文组织策略 | 直接有界闭环 |
| 2025-10-06 | [LEGOMem: Modular Procedural Memory for Multi-agent LLM Systems for Workflow Automation](memory-context.zh-CN.md#microsoft-legomem-2025) | Microsoft | 上下文组织策略 | 支撑技术／评测 |
| 2025-10-01 | [ACON: Optimizing Context Compression for Long-horizon LLM Agents](memory-context.zh-CN.md#microsoft-acon-2025) | Microsoft / KAIST / University of Cambridge | 上下文组织策略 | 直接有界闭环 |
| 2025-09-26 | [Learn the Ropes, Then Trust the Wins: Self-imitation with Progressive Exploration for Agentic Reinforcement Learning](parameter-learning.zh-CN.md#tencent-spear) | Tencent Youtu Lab / Shanghai Jiao Tong University / Peking University / Fudan University / Xiamen University | 自博弈与课程任务生成 | 直接有界闭环 |
| 2025-09-17 | [ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution](agent-code.zh-CN.md#sakana-shinkaevolve) | Sakana AI | 程序进化与进化搜索 | 直接有界闭环 |

## 历史归档——已超出当前窗口

| 日期 | 工作 | 机构 | 家族 | 证据类别 |
| --- | --- | --- | --- | --- |
| 2025-09-14 | [Self-Evolving LLMs via Continual Instruction Tuning](parameter-learning.zh-CN.md#tencent-moe-cl) | Beijing University of Posts and Telecommunications / Tencent AI Lab | 支撑性适应机制 | 支撑技术／评测 |
| 2025-08-04 | [SE-Agent: Self-Evolution Trajectory Optimization in Multi-Step Reasoning with LLM-Based Agents](memory-context.zh-CN.md#se-agent-trajectory) | StepFun / Tsinghua University / Huazhong Agricultural University | 经验积累与回放 | 直接有界闭环 |

## 日期、复用与更新

采用所引首版论文或实质成果报告的日期，不采用抓取时间、仓库活跃时间或会议年份。仅能确认月份时保留月份；条目说明区分先行公告与后续论文。代码可见不代表可以不受限复用，权重和数据可能有不同条款。本次整理未执行或复现上游系统。

更新时编辑唯一数据源 JSON，并遵循[记录格式](FORMAT.md)。窗口滚动后，生成器会将旧条目保留在历史归档中。修改指标或发布状态前需重新核对来源。

```bash
python docs/research/industry-rsi/render.py
python docs/research/industry-rsi/render.py --check
```
