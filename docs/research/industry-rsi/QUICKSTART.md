# Quickstart / RSI research map

[Research map](README.md) · [中文](QUICKSTART.zh-CN.md)

This page is the five-minute route through the collection. It follows a pattern used by mature open-source projects: a short value statement, a runnable or inspectable first step, then deeper concepts and reference pages. Compare the navigation in [vLLM](https://github.com/vllm-project/vllm#readme), [Transformers](https://github.com/huggingface/transformers#readme), [DeepSpeed](https://github.com/microsoft/DeepSpeed#readme) and [LangChain](https://github.com/langchain-ai/langchain#readme).

## Choose a route

| I want to… | Start here | What you get |
| --- | --- | --- |
| Understand the vocabulary | [Landscape and taxonomy](LANDSCAPE.md) | What changes, what feedback is reused, and what counts as direct, enabling or assisted evidence |
| See one research mechanism | [Parameter/data](parameter-learning.md), [Agent/code](agent-code.md), [Memory/context](memory-context.md), [Research workflows](research-workflows.md) | Figure, source locator, mechanism, result, limitations and proposed nanoRSI experiment |
| Find usable code or weights | [Open materials index](OPEN_MATERIALS.md) | Repository, checkpoint, data and license links separated per record |
| Decide what nanoRSI should implement next | [Adoption priorities](ADOPTION.md) | Ordered experiments with acceptance criteria and controls |
| Audit why a record is included | [Coverage and dates](COVERAGE.md) · [Format](FORMAT.md) | Search boundary, first-publication rule, provenance schema and update procedure |

## Read one record correctly

1. Start with the **visual source**. It is a paper figure, official research image or cropped source page. The locator and source link identify what was retained.
2. Read **what changes and how feedback is reused**. This is the mechanism boundary; it is more informative than a project slogan.
3. Check **author-reported result** and its comparator, metric, budget and split. Numbers are not nanoRSI results unless a record explicitly links a local reproduction.
4. Check **evidence limits** and **local reproduction** before using the result as a design precedent.
5. Open **code / weights / data links** separately. A public paper or repository does not automatically grant permission to redistribute weights or datasets.

## Update the collection

The canonical source is `catalog.json`. An update should add a dated primary source, a stable ID, one visual provenance record and explicit asset/license status. Then regenerate the pages and run the offline check:

```bash
python docs/research/industry-rsi/render.py
python docs/research/industry-rsi/render.py --check
```

Keep the original public date, distinguish later revisions or releases, and leave a negative result visible when a control fails. Do not turn a generic model release, a faster engineering workflow or a memory ablation into a claim of general RSI.

## What this collection is not

It is not an exhaustive industry ranking, a single benchmark score, or a claim that current systems can autonomously train their successors. It is a source-linked map for choosing small, inspectable experiments in nanoRSI.
