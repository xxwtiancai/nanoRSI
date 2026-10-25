# nanoRSI Charter

nanoRSI is a minimal, auditable implementation of recursive harness improvement, in the
shape of Harness² (Google Cloud AI Research, arXiv 2610.14224), written from scratch on the
Python standard library.

## Mission

Two tracks under one name:

1. **Engineering track — the loop.** A frozen model, an editable harness around it (system
   prompt, guardrails, memory, tool guidance, skills, scripts), and a task-level recursion
   that proposes edits from execution evidence, probes them under matched configuration,
   classifies the behavioral contrast without ground truth, composes the next harness, and
   judges only after a freeze. The framework must stay runnable end to end
   (`new → configure → evolve → freeze → judge → report → verify`) and must be evaluated
   on the benchmark the mechanism's authors used, against their own code, before any claim.
2. **Research track — the living notes.** A daily document of RSI papers classified on the
   two axes of the 1,250-paper RSI survey (arXiv 2607.07663), kept in
   `docs/research/RSI_NOTES.md`.

## Constraints that define "nano"

Standard library only. Core at most 2,500 lines, modules at most 300, functions at most 50.
Every rollout, proposal, contrast, composition, selection and judgement is a hash-chained
ledger event; reports are derived views. Budgets are charged before each call. Scores exist
only after `freeze` and never influence selection. Credentials live outside the workspace.

## Honesty rules

Author results are not local reproductions. Negative, null and inconclusive results are
valid and are kept. nanoRSI does not claim general recursive self-improvement, guaranteed
gains, or a hardened sandbox. Upstream code is borrowed by mechanism shape, never copied;
licenses are checked before anything is borrowed (Harness² Apache-2.0; LAB tasks MIT).

## Scope boundaries

The executor and the judge are workspace commands behind a fixed protocol; the core never
contains benchmark- or substrate-specific code. Subagents and plugins — the paper's two
remaining harness components — require a host runtime and are out of scope. Local code is
trusted; process limits are not isolation.
