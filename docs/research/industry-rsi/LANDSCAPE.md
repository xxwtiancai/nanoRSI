# Landscape and taxonomy / RSI research landscape

[Research map](README.md) · [中文](LANDSCAPE.zh-CN.md)

The collection organizes work by the persistent surface that changes. This prevents a memory write, a learned optimizer and a research-assistance workflow from being reported as the same kind of RSI.

## Four change surfaces

| Surface | The question | Typical evidence in this map |
| --- | --- | --- |
| Parameters and training data | Do generated tasks, labels, rewards or update rules change a target model's parameters and feed a later round? | AgentEvolver, Agent0, SIMA 2, GPT-Red, A3 |
| Agents and code | Does a persistent program, scaffold or harness get edited, evaluated and reused? | HarnessDev, SkillHone, WebAggregator, Hyperagents, ShinkaEvolve, MiniMax M2.7 |
| Memory and context | Does experience become a retrievable context, playbook, adapter or memory state? | ACE, ACON, LEGOMem, S3Gym, Prime Agent, Training-Free GRPO |
| Automated research and evaluation | Does an agent improve a separate research artifact or make the evaluation loop scalable? | AAR, weak-to-strong researcher, TASTE, AlphaEvolve MARL, Prime research evaluation |

## Evidence classes

These labels describe the emphasis of an entry, not a capability ladder.

- **Direct bounded loop** — a persistent code, memory, policy, parameter or learning-rule change is reused in a later iteration. The loop remains bounded by a task, evaluator, model or compute budget.
- **Enabling technique / evaluation** — adaptation, memory, learned optimization or measurement helps an improvement system, but the published experiment does not show a recursive deployment loop.
- **Automated / assisted R&D** — an agent improves a separate target or accelerates a human-directed research workflow. This can be valuable evidence for nanoRSI without showing that the controller improves itself.

## Evidence reading order

Read records in this order when comparing two systems:

1. **Object** — code, memory, data policy, model parameters, learning rule or separate research artifact.
2. **Feedback** — executable tests, reward, verifier, held-out score, human preference or operational review.
3. **Update** — what is changed, who chooses it, and whether the next iteration sees the result.
4. **Gate** — rollback, frozen test, capability constraint, human review or no gate.
5. **Generalization** — new tasks, domains, models, seeds and budgets; record failures as well as wins.

## How the navigation is designed

The landing page deliberately stays short and routes readers to one job at a time: [Quickstart](QUICKSTART.md), this taxonomy, [cases by change surface](README.md#browse-by-what-changes), [open materials](OPEN_MATERIALS.md), [adoption priorities](ADOPTION.md), then [coverage and format](COVERAGE.md). That sequence adapts patterns visible in the official [vLLM README](https://github.com/vllm-project/vllm#readme), [Transformers README](https://github.com/huggingface/transformers#readme), [DeepSpeed README](https://github.com/microsoft/DeepSpeed#readme) and [LangChain README](https://github.com/langchain-ai/langchain#readme): value statement, quickstart, organized capabilities, reference material, contribution path and clear limits.

## Boundaries

The map does not combine heterogeneous accuracy, throughput, token and cost metrics. A paper figure can show a mechanism while its headline benchmark measures a different object. A model can help researchers build a better training run while its own weights remain fixed. An open repository can still have noncommercial terms or omit weights/data. Those distinctions are part of the evidence, not footnotes.
