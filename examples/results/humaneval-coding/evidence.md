# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

## Gate summary

Read-only counts derived from the same verified lineage revisions:

- failed: 1, rejected: 2

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | 0 | rejected | 0.0 | 2 |
| 2 | 0 | rejected | -0.16000000000000003 | 2 |
| 3 | None | failed | None | 0 |

## Attempt 1 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The one failure (generate_integers) came from reading 'even digits between a and b' as even integers in the range, contradicting the example generate_integers(10, 14) => []. The public tests only assert the function exists, so no test would catch this. Strengthening inspect to resolve ambiguity strictly against examples and verify to self-check every stated example (especially since public tests here are presence-only) directly targets this failure mode generically without encoding task-specific answers."}`
- Surface: target/agent/skills/inspect/SKILL.md, target/agent/skills/verify/SKILL.md
- score: 1.0 → 1.0 (Δ 0.0)
- Diff `.nanorsi/runs/c22c337204/proposal/proposal.diff` sha256 `942c9abc2dca`… integrity ok: target/agent/skills/inspect/SKILL.md +6/-0, target/agent/skills/verify/SKILL.md +6/-0

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000-separate_paren_groups | validation-problems | ok/1.0 | ok/1.0 |
| validation-001-unique_digits | validation-problems | ok/1.0 | ok/1.0 |
| validation-002-string_xor | validation-problems | ok/1.0 | ok/1.0 |
| validation-003-max_fill | validation-problems | ok/1.0 | ok/1.0 |
| validation-004-maximum | validation-problems | ok/1.0 | ok/1.0 |
| validation-005-is_sorted | validation-problems | ok/1.0 | ok/1.0 |
| validation-006-digits | validation-problems | ok/1.0 | ok/1.0 |
| validation-007-compare_one | validation-problems | ok/1.0 | ok/1.0 |
| validation-008-sum_squares | validation-problems | ok/1.0 | ok/1.0 |
| validation-009-bf | validation-problems | ok/1.0 | ok/1.0 |
| validation-010-Strongest_Extension | validation-problems | ok/1.0 | ok/1.0 |
| validation-011-eat | validation-problems | ok/1.0 | ok/1.0 |
| validation-012-parse_music | validation-problems | ok/1.0 | ok/1.0 |
| validation-013-filter_integers | validation-problems | ok/1.0 | ok/1.0 |
| validation-014-concatenate | validation-problems | ok/1.0 | ok/1.0 |
| validation-015-unique | validation-problems | ok/1.0 | ok/1.0 |
| validation-016-triples_sum_to_zero | validation-problems | ok/1.0 | ok/1.0 |
| validation-017-fib4 | validation-problems | ok/1.0 | ok/1.0 |
| validation-018-below_threshold | validation-problems | ok/1.0 | ok/1.0 |
| validation-019-common | validation-problems | ok/1.0 | ok/1.0 |
| validation-020-fibfib | validation-problems | ok/1.0 | ok/1.0 |
| validation-021-search | validation-problems | ok/1.0 | ok/1.0 |
| validation-022-total_match | validation-problems | ok/1.0 | ok/1.0 |
| validation-023-sum_product | validation-problems | ok/1.0 | ok/1.0 |
| validation-024-add | validation-problems | ok/1.0 | ok/1.0 |

## Attempt 2 — rejected (generation 0)
- Reason: improvement below minimum: -0.160000
- Diagnosis: `{"reason": "Both failures (generate_integers, is_bored) passed public tests that only assert callability, so the agent finished without checking docstring examples that contradicted its prose interpretation. Adding example-driven disambiguation to inspect and a mandatory direct example-execution step to verify addresses this recurring cause generically."}`
- Surface: target/agent/skills/inspect/SKILL.md, target/agent/skills/verify/SKILL.md
- score: 1.0 → 0.84 (Δ -0.16000000000000003)
- Diff `.nanorsi/runs/878afd81d0/proposal/proposal.diff` sha256 `e4bd56623e6a`… integrity ok: target/agent/skills/inspect/SKILL.md +4/-0, target/agent/skills/verify/SKILL.md +5/-0

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000-separate_paren_groups | validation-problems | ok/1.0 | ok/1.0 |
| validation-001-unique_digits | validation-problems | ok/1.0 | ok/1.0 |
| validation-002-string_xor | validation-problems | ok/1.0 | ok/1.0 |
| validation-003-max_fill | validation-problems | ok/1.0 | runner_error/0.0 |
| validation-004-maximum | validation-problems | ok/1.0 | ok/1.0 |
| validation-005-is_sorted | validation-problems | ok/1.0 | ok/1.0 |
| validation-006-digits | validation-problems | ok/1.0 | ok/1.0 |
| validation-007-compare_one | validation-problems | ok/1.0 | ok/1.0 |
| validation-008-sum_squares | validation-problems | ok/1.0 | ok/1.0 |
| validation-009-bf | validation-problems | ok/1.0 | ok/1.0 |
| validation-010-Strongest_Extension | validation-problems | ok/1.0 | ok/1.0 |
| validation-011-eat | validation-problems | ok/1.0 | ok/1.0 |
| validation-012-parse_music | validation-problems | ok/1.0 | task_failure/0.0 |
| validation-013-filter_integers | validation-problems | ok/1.0 | ok/1.0 |
| validation-014-concatenate | validation-problems | ok/1.0 | ok/1.0 |
| validation-015-unique | validation-problems | ok/1.0 | ok/1.0 |
| validation-016-triples_sum_to_zero | validation-problems | ok/1.0 | ok/1.0 |
| validation-017-fib4 | validation-problems | ok/1.0 | ok/1.0 |
| validation-018-below_threshold | validation-problems | ok/1.0 | ok/1.0 |
| validation-019-common | validation-problems | ok/1.0 | runner_error/0.0 |
| validation-020-fibfib | validation-problems | ok/1.0 | ok/1.0 |
| validation-021-search | validation-problems | ok/1.0 | ok/1.0 |
| validation-022-total_match | validation-problems | ok/1.0 | ok/1.0 |
| validation-023-sum_product | validation-problems | ok/1.0 | ok/1.0 |
| validation-024-add | validation-problems | ok/1.0 | runner_error/0.0 |

## Attempt 3 — failed (generation None)
- Reason: episode budget reached
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)
- Diff `.nanorsi/runs/e91826130d/proposal/proposal.diff` sha256 `4bf573a9e0d3`… integrity ok: target/agent/skills/edit/SKILL.md +5/-0, target/agent/skills/verify/SKILL.md +4/-0
