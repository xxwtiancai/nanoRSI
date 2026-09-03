# nanoRSI Kernel Specification

## Scope

This document is normative for v0.1. The core implements one workspace, one
authoritative parent, one child at a time, one external proposer, one canonical
evaluator, and single-parent hill climbing. It is standard-library-only.

## Module Ownership

| Module | Required responsibility |
| --- | --- |
| `src/nanorsi/__init__.py` | package identity |
| `src/nanorsi/cli.py` | argv parsing and command orchestration |
| `src/nanorsi/config.py` | strict TOML loading and cross-field validation |
| `src/nanorsi/paths.py` | relative-path normalization and containment |
| `src/nanorsi/hashing.py` | canonical JSON and deterministic tree hashes |
| `src/nanorsi/surface.py` | mutable-surface matching and diff path extraction |
| `src/nanorsi/gitops.py` | repository, worktree, patch, commit, and tag operations |
| `src/nanorsi/proposer.py` | external proposal execution and proposal parsing |
| `src/nanorsi/evaluator.py` | subprocess evaluation and result-schema validation |
| `src/nanorsi/gate.py` | accept, reject, and inconclusive decisions |
| `src/nanorsi/lineage.py` | append-only HMAC-protected JSONL events |
| `src/nanorsi/process.py` | argv-only subprocess execution and environment filtering |
| `src/nanorsi/report.py` | deterministic Markdown and JSON reports |
| `src/nanorsi/templates.py` | artifact, harness, and model template rendering |
| `src/nanorsi/doctor.py` | local preflight diagnostics |
| `src/nanorsi/locking.py` | one-operation-per-experiment lock |

## States

The legal lifecycle is:

```text
NEW
  -> DOCTOR_OK
  -> GEN0_SNAPSHOT
  -> GEN0_EVALUATED
  -> PROPOSAL_CREATED
  -> PATCH_VALIDATED
  -> CHILD_SNAPSHOT
  -> CHILD_EVALUATED
  -> GATED_ACCEPTED | GATED_REJECTED | INCONCLUSIVE
  -> LINEAGE_RECORDED
  -> REPORT_WRITTEN
```

Failure states are `PROPOSER_FAILED`, `PATCH_INVALID`, `SURFACE_VIOLATION`,
`EVALUATOR_TIMEOUT`, `EVALUATOR_INVALID`, `BUDGET_EXCEEDED`, `LOCK_BUSY`, and
`LEDGER_INVALID`.

## Invariants

1. The first lineage event is generation 0 with decision `baseline`.
2. An accepted generation has exactly the prior accepted generation as parent.
3. Candidate and parent evaluator tree hashes must match.
4. A candidate commit and tree hash are recorded before the gate decision.
5. Only mechanism-generated receipts may authenticate lineage records.
6. A rejected or inconclusive candidate is never tagged as the next parent.
7. Candidate evaluation runs in a detached Git worktree.
8. Core never imports proposer, evaluator, target, or training code.

## Module And Transition Budget

No core module may exceed 300 lines, no function may exceed 50 lines, and total
core runtime source must remain under 2,500 lines. CI must reject database,
server, dashboard, scheduler, plugin-loader, vendor-adapter, or distributed
evaluator modules in v0.1.
