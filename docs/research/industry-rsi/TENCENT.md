# Tencent RSI coverage audit / 腾讯 RSI 覆盖审计

[Research map](README.md) · [中文版本](TENCENT.zh-CN.md) · [Coverage and dates](COVERAGE.md)

This page makes the Tencent search boundary explicit. It separates first-party papers and repositories that show a persistent change, earlier Tencent work outside the rolling window, and ordinary model or agent releases that do not establish recursive self-improvement. The dated catalogue remains the source of record for metrics, affiliations, licenses and figures.

## In-window records (2025-09-13 → 2026-09-13)

| Work | Change surface | What is persistent | Public implementation | Classification |
| --- | --- | --- | --- | --- |
| [SkillHone](agent-code.md#tencent-skillhone) · [paper](https://arxiv.org/abs/2606.08671) | Agent skills | Decision history and accepted skill revisions are reused by later sessions | [Tencent/SkillHone](https://github.com/Tencent/SkillHone) · MIT stated in `LICENSE` | Direct bounded loop |
| [SPEAR](parameter-learning.md#tencent-spear) · [paper](https://arxiv.org/abs/2509.22601) | Policy training | Self-imitation replay and curriculum rewards change later policy updates | [TencentYoutuResearch/SPEAR](https://github.com/TencentYoutuResearch/SPEAR) · custom SPEAR terms | Direct bounded loop |
| [MoE-CL](parameter-learning.md#tencent-moe-cl) · [paper](https://arxiv.org/abs/2509.18133) | Parameters / continual learning | LoRA experts retain knowledge across an externally supplied task sequence | [BAI-LAB/MoE-CL](https://github.com/BAI-LAB/MoE-CL) | Enabling technique / evaluation |
| [Training-Free GRPO](memory-context.md#tencent-training-free-grpo) · [paper](https://arxiv.org/abs/2510.08191) | Memory / context | A frozen model writes an experience library that changes later context | [Youtu-Agent branch](https://github.com/TencentCloudADP/youtu-agent/tree/training_free_GRPO) · MIT stated in `LICENSE` | Direct bounded loop |
| [WebAggregator / Explore-to-Evolve](agent-code.md#tencent-webaggregator) · [paper](https://arxiv.org/abs/2510.14438) | Programs / training data | Executable aggregation logic and verified QA feed later model training | [Tencent/WebAggregator](https://github.com/Tencent/WebAggregator) · custom WebAggregator terms | Direct bounded loop |

The five entries cover the distinct Tencent mechanisms found in this pass: skill artifact evolution, replay-based policy updates, continual parameter learning, frozen-model context evolution, and executable web-data construction. They are not one homogeneous “Tencent RSI model”; each has a different mutable object and control boundary.

## Earlier or adjacent Tencent leads

| Lead | Original date | Decision |
| --- | --- | --- |
| [WebEvolver](https://arxiv.org/abs/2504.21024) | 2025-04-23 | Keep as an earlier SelfEvolvingAgent foundation; outside the rolling window. |
| [WebCoT](https://arxiv.org/abs/2505.15478) | 2025-05-26 | Keep as an earlier reflection/branching/rollback lead; outside the rolling window. |
| [Cognitive Kernel-Pro](https://arxiv.org/abs/2508.00414) · [code](https://github.com/Tencent/CognitiveKernel-Pro) | 2025-08-01 | Keep as a pre-window Tencent research and code lead. |
| [VScan](https://github.com/Tencent/SelfEvolvingAgent) | 2026 | Listed in the Tencent archive, but token reduction alone does not show a persistent self-improvement loop. |
| Hunyuan model and product releases | Various | Capability releases and tool use are tracked as context only; no retained mutation/evaluation/reuse loop was established from the checked release pages. |

## Search and evidence rules

The audit checked the Tencent SelfEvolvingAgent index, Tencent and Tencent YoutuResearch repositories, Youtu-Agent branches, arXiv submission histories and v1 HTML papers. A record enters the rolling catalogue only when the first-public date is inside the window, Tencent affiliation or first-party release is explicit, and the paper describes a mutable artifact that receives feedback and affects a later iteration. Repository visibility, a later revision date, a conference date or a model release alone cannot satisfy those conditions.

Code, weights, data and licenses are audited independently. “Public repository” means that the linked files were reachable on the verification date; it does not imply that checkpoints or datasets are included. Custom Tencent terms and third-party component terms remain binding, and the catalogue records the EU-use restrictions stated by SPEAR and WebAggregator.

This is a dated engineering audit rather than a claim that every Tencent internal project is public. Future updates should add a primary source, first-public date, mutable object, feedback path, reuse path, and a source pipeline figure or official research image before promoting a lead.
