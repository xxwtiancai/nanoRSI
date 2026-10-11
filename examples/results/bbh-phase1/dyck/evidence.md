# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | 1 | accepted | 0.21999999999999997 | 1 |
| 2 | None | failed | None | 0 |
| 3 | None | failed | None | 0 |
| 4 | None | failed | None | 0 |
| 5 | None | failed | None | 0 |

## Attempt 1 — accepted (generation 1)
- Reason: improvement 0.220000
- Diagnosis: `{"reason": "The old solver counted unmatched openers per bracket type and emitted closers grouped by bracket kind, which destroys nesting order. A stack already tracks the exact nesting: emitting opens[opener] for each opener popped from the top of the stack (reversed iteration) yields the closers in correct innermost-to-outermost order, fixing ordering failures like ( < ( [ < < [ ] > > ] ) -> \"> )\" while preserving all passing cases and the unchanged main() stdin/stdout contract."}`
- Surface: target/program.py
- score: 0.78 → 1.0 (Δ 0.21999999999999997)
- Diff `.nanorsi/runs/1ca8a31e14/proposal/proposal.diff` sha256 `0f4c048475cf`… integrity ok: target/program.py +1/-7

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-001 | validation-examples | ok/1.0 | ok/1.0 |
| validation-002 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-003 | validation-examples | ok/1.0 | ok/1.0 |
| validation-004 | validation-examples | ok/1.0 | ok/1.0 |
| validation-005 | validation-examples | ok/1.0 | ok/1.0 |
| validation-006 | validation-examples | ok/1.0 | ok/1.0 |
| validation-007 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-008 | validation-examples | ok/1.0 | ok/1.0 |
| validation-009 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-010 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-011 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-012 | validation-examples | ok/1.0 | ok/1.0 |
| validation-013 | validation-examples | ok/1.0 | ok/1.0 |
| validation-014 | validation-examples | ok/1.0 | ok/1.0 |
| validation-015 | validation-examples | ok/1.0 | ok/1.0 |
| validation-016 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-017 | validation-examples | ok/1.0 | ok/1.0 |
| validation-018 | validation-examples | ok/1.0 | ok/1.0 |
| validation-019 | validation-examples | ok/1.0 | ok/1.0 |
| validation-020 | validation-examples | ok/1.0 | ok/1.0 |
| validation-021 | validation-examples | ok/1.0 | ok/1.0 |
| validation-022 | validation-examples | ok/1.0 | ok/1.0 |
| validation-023 | validation-examples | ok/1.0 | ok/1.0 |
| validation-024 | validation-examples | ok/1.0 | ok/1.0 |
| validation-025 | validation-examples | ok/1.0 | ok/1.0 |
| validation-026 | validation-examples | ok/1.0 | ok/1.0 |
| validation-027 | validation-examples | ok/1.0 | ok/1.0 |
| validation-028 | validation-examples | ok/1.0 | ok/1.0 |
| validation-029 | validation-examples | ok/1.0 | ok/1.0 |
| validation-030 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-031 | validation-examples | ok/1.0 | ok/1.0 |
| validation-032 | validation-examples | ok/1.0 | ok/1.0 |
| validation-033 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-034 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-035 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-036 | validation-examples | ok/1.0 | ok/1.0 |
| validation-037 | validation-examples | ok/1.0 | ok/1.0 |
| validation-038 | validation-examples | ok/1.0 | ok/1.0 |
| validation-039 | validation-examples | ok/1.0 | ok/1.0 |
| validation-040 | validation-examples | ok/1.0 | ok/1.0 |
| validation-041 | validation-examples | ok/1.0 | ok/1.0 |
| validation-042 | validation-examples | ok/1.0 | ok/1.0 |
| validation-043 | validation-examples | ok/1.0 | ok/1.0 |
| validation-044 | validation-examples | ok/1.0 | ok/1.0 |
| validation-045 | validation-examples | ok/1.0 | ok/1.0 |
| validation-046 | validation-examples | ok/1.0 | ok/1.0 |
| validation-047 | validation-examples | ok/1.0 | ok/1.0 |
| validation-048 | validation-examples | ok/1.0 | ok/1.0 |
| validation-049 | validation-examples | ok/1.0 | ok/1.0 |

## Attempt 2 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/dyck-lab/.nanorsi/runs/e24c5edb33/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)

## Attempt 3 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/dyck-lab/.nanorsi/runs/42ff88374d/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)

## Attempt 4 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/dyck-lab/.nanorsi/runs/19b23ab3b1/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)

## Attempt 5 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/dyck-lab/.nanorsi/runs/8510455975/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)
