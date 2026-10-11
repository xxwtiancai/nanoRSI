# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | None | failed | None | 0 |
| 2 | None | failed | None | 0 |
| 3 | 1 | accepted | 0.020000000000000018 | 1 |
| 4 | 1 | rejected | 0.0 | 1 |
| 5 | None | no-op | None | 0 |

## Attempt 1 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/bool-lab/.nanorsi/runs/5d579734a8/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)

## Attempt 2 — failed (generation None)
- Reason: invalid proposal files: [Errno 2] No such file or directory: '/private/tmp/bbh-live/bool-lab/.nanorsi/runs/3ca4aafedf/proposal/proposal.diff'
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)

## Attempt 3 — accepted (generation 1)
- Reason: improvement 0.020000
- Diagnosis: `{"reason": "The current solver is a single left-to-right pass that applies and/or in encounter order, ignoring precedence; it failed train-048 ('not not True and not False' returned False instead of True). Replace it with a recursive-descent parser with levels parse_or -> parse_and -> parse_not -> atom, so not binds tightest, then and, then or; parentheses recurse back into parse_or, chained prefix nots recurse on themselves, and left-associative and/or fold in loops. main and the stdin/stdout contract are untouched; all four train examples then evaluate correctly."}`
- Surface: target/program.py
- score: 0.9 → 0.92 (Δ 0.020000000000000018)
- Diff `.nanorsi/runs/4b334d29d9/proposal/proposal.diff` sha256 `44bd03365356`… integrity ok: target/program.py +40/-42

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-examples | ok/1.0 | ok/1.0 |
| validation-001 | validation-examples | ok/1.0 | ok/1.0 |
| validation-002 | validation-examples | ok/1.0 | ok/1.0 |
| validation-003 | validation-examples | ok/1.0 | ok/1.0 |
| validation-004 | validation-examples | ok/1.0 | task_failure/0.0 |
| validation-005 | validation-examples | ok/1.0 | ok/1.0 |
| validation-006 | validation-examples | ok/1.0 | ok/1.0 |
| validation-007 | validation-examples | ok/1.0 | ok/1.0 |
| validation-008 | validation-examples | ok/1.0 | ok/1.0 |
| validation-009 | validation-examples | ok/1.0 | ok/1.0 |
| validation-010 | validation-examples | ok/1.0 | task_failure/0.0 |
| validation-011 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-012 | validation-examples | ok/1.0 | ok/1.0 |
| validation-013 | validation-examples | ok/1.0 | ok/1.0 |
| validation-014 | validation-examples | ok/1.0 | ok/1.0 |
| validation-015 | validation-examples | ok/1.0 | task_failure/0.0 |
| validation-016 | validation-examples | ok/1.0 | ok/1.0 |
| validation-017 | validation-examples | ok/1.0 | ok/1.0 |
| validation-018 | validation-examples | ok/1.0 | ok/1.0 |
| validation-019 | validation-examples | task_failure/0.0 | task_failure/0.0 |
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
| validation-030 | validation-examples | ok/1.0 | ok/1.0 |
| validation-031 | validation-examples | ok/1.0 | ok/1.0 |
| validation-032 | validation-examples | ok/1.0 | ok/1.0 |
| validation-033 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-034 | validation-examples | ok/1.0 | ok/1.0 |
| validation-035 | validation-examples | ok/1.0 | ok/1.0 |
| validation-036 | validation-examples | ok/1.0 | ok/1.0 |
| validation-037 | validation-examples | ok/1.0 | ok/1.0 |
| validation-038 | validation-examples | ok/1.0 | ok/1.0 |
| validation-039 | validation-examples | ok/1.0 | ok/1.0 |
| validation-040 | validation-examples | ok/1.0 | ok/1.0 |
| validation-041 | validation-examples | ok/1.0 | ok/1.0 |
| validation-042 | validation-examples | ok/1.0 | ok/1.0 |
| validation-043 | validation-examples | ok/1.0 | ok/1.0 |
| validation-044 | validation-examples | ok/1.0 | ok/1.0 |
| validation-045 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-046 | validation-examples | task_failure/0.0 | ok/1.0 |
| validation-047 | validation-examples | ok/1.0 | ok/1.0 |
| validation-048 | validation-examples | ok/1.0 | ok/1.0 |
| validation-049 | validation-examples | ok/1.0 | ok/1.0 |

## Attempt 4 — rejected (generation 1)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The existing recursive-descent parser already evaluates with correct precedence (parse_or -> parse_and -> parse_not -> atom), and all four train cases pass with score 1.0, so the priority is general hardening without regression: strip any number of trailing ' is' sentence markers instead of just one, return 'False' on an empty token stream instead of raising IndexError, and correct the stale header comment claiming a weak left-to-right evaluator. The parse structure, solution semantics, and the main() stdin/stdout JSON contract are left untouched, so behavior on all valid BBH boolean expressions (nested parens, chained not, and/or at correct precedence) is preserved while edge inputs become robust."}`
- Surface: target/program.py
- score: 0.92 → 0.92 (Δ 0.0)
- Diff `.nanorsi/runs/e18ef7623a/proposal/proposal.diff` sha256 `22f309d71bfb`… integrity ok: target/program.py +6/-3

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-examples | ok/1.0 | ok/1.0 |
| validation-001 | validation-examples | ok/1.0 | ok/1.0 |
| validation-002 | validation-examples | ok/1.0 | ok/1.0 |
| validation-003 | validation-examples | ok/1.0 | ok/1.0 |
| validation-004 | validation-examples | task_failure/0.0 | task_failure/0.0 |
| validation-005 | validation-examples | ok/1.0 | ok/1.0 |
| validation-006 | validation-examples | ok/1.0 | ok/1.0 |
| validation-007 | validation-examples | ok/1.0 | ok/1.0 |
| validation-008 | validation-examples | ok/1.0 | ok/1.0 |
| validation-009 | validation-examples | ok/1.0 | ok/1.0 |
| validation-010 | validation-examples | task_failure/0.0 | task_failure/0.0 |
| validation-011 | validation-examples | ok/1.0 | ok/1.0 |
| validation-012 | validation-examples | ok/1.0 | ok/1.0 |
| validation-013 | validation-examples | ok/1.0 | ok/1.0 |
| validation-014 | validation-examples | ok/1.0 | ok/1.0 |
| validation-015 | validation-examples | task_failure/0.0 | task_failure/0.0 |
| validation-016 | validation-examples | ok/1.0 | ok/1.0 |
| validation-017 | validation-examples | ok/1.0 | ok/1.0 |
| validation-018 | validation-examples | ok/1.0 | ok/1.0 |
| validation-019 | validation-examples | task_failure/0.0 | task_failure/0.0 |
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
| validation-030 | validation-examples | ok/1.0 | ok/1.0 |
| validation-031 | validation-examples | ok/1.0 | ok/1.0 |
| validation-032 | validation-examples | ok/1.0 | ok/1.0 |
| validation-033 | validation-examples | ok/1.0 | ok/1.0 |
| validation-034 | validation-examples | ok/1.0 | ok/1.0 |
| validation-035 | validation-examples | ok/1.0 | ok/1.0 |
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

## Attempt 5 — no-op (generation None)
- Reason: proposal and training change no files
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)
- Diff `.nanorsi/runs/db02aae87a/proposal/proposal.diff` sha256 `e3b0c44298fc`… integrity ok: —
