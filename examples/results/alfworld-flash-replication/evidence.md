# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

## Gate summary

Read-only counts derived from the same verified lineage revisions:

- no-op: 1, rejected: 3

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | 0 | rejected | 0.0 | 1 |
| 2 | 0 | rejected | 0.0 | 1 |
| 3 | 0 | rejected | 0.0 | 1 |
| 4 | None | no-op | None | 0 |

## Attempt 1 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The failed kettle episode burned all 24 steps opening cabinets in order without prioritizing likely receptacles, and used examine redundantly. Adding object-likelihood search order, closed-receptacle awareness, and explicit task pipelines should reduce wasted exploration and improve unseen episodes across task types."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.875 (Δ 0.0)
- Diff `.nanorsi/runs/d7db08dbb0/proposal/proposal.diff` sha256 `c8dc8f0d005f`… integrity ok: target/agent/skills/alfworld/SKILL.md +43/-11

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | ok/1.0 | ok/1.0 |
| validation-003 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
| validation-006 | validation-games | ok/1.0 | ok/1.0 |
| validation-007 | validation-games | ok/1.0 | ok/1.0 |

## Attempt 2 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The kettle failure exhausted all 24 steps on unguided, near-alphabetical cabinet exploration. Adding likelihood-ordered search with open-on-arrival, no-revisit rules, and a find-transform-place plan should cut wasted navigation in unseen episodes with tight step budgets."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.875 (Δ 0.0)
- Diff `.nanorsi/runs/b1cfba8aa5/proposal/proposal.diff` sha256 `b4cd4e858898`… integrity ok: target/agent/skills/alfworld/SKILL.md +22/-0

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | ok/1.0 | ok/1.0 |
| validation-003 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
| validation-006 | validation-games | ok/1.0 | ok/1.0 |
| validation-007 | validation-games | ok/1.0 | ok/1.0 |

## Attempt 3 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The failed kettle episode wasted the budget by examining receptacles redundantly (go-to already lists contents), never opening cabinets immediately, and searching without likelihood ordering. The winning lamp episode also spent 6 steps hunting for the lamp after the task was done except for 'use'. This version adds: plan-from-goal-type, open-on-arrival, no-examine-after-go-to, likelihood-ordered search with no revisits, one-object-at-a-time carrying discipline, and budget awareness \u2014 all general, none data-specific. Previous rejections likely failed because the guidance was too vague or the gate re-ran identical episodes; these concrete behavioral rules should reduce wasted steps in unseen episodes."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.875 (Δ 0.0)
- Diff `.nanorsi/runs/088e77c4c9/proposal/proposal.diff` sha256 `17c6df729053`… integrity ok: target/agent/skills/alfworld/SKILL.md +41/-13

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | ok/1.0 | ok/1.0 |
| validation-003 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
| validation-006 | validation-games | ok/1.0 | ok/1.0 |
| validation-007 | validation-games | ok/1.0 | ok/1.0 |

## Attempt 4 — no-op (generation None)
- Reason: proposal and training change no files
- Diagnosis: `null`
- Surface: —
- score: None → None (Δ None)
- Diff `.nanorsi/runs/66ba86225a/proposal/proposal.diff` sha256 `e3b0c44298fc`… integrity ok: —
