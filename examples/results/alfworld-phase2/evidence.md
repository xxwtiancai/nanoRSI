# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | 0 | rejected | -0.16666666666666674 | 1 |
| 2 | 0 | rejected | 0.0 | 1 |
| 3 | 0 | rejected | 0.0 | 1 |

## Attempt 1 — rejected (generation 0)
- Reason: improvement below minimum: -0.166667
- Diagnosis: `{"reason": "Train episodes were all won but wasted steps: redundant 'move' after a successful 'put', unnecessary 'open fridge' when cooling, and long wandering to find the desklamp/object. Guidance on task templates, direct heat/cool verbs, and avoiding duplicate placement actions should cut wasted steps and reduce the risk of exceeding max_steps on unseen episodes."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.8333333333333334 → 0.6666666666666666 (Δ -0.16666666666666674)
- Diff `.nanorsi/runs/87df9ac86a/proposal/proposal.diff` sha256 `ad1cc4505c5d`… integrity ok: target/agent/skills/alfworld/SKILL.md +22/-8

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | task_failure/0.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-003 | validation-games | ok/1.0 | ok/1.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |

## Attempt 2 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "All training episodes were won but wasted steps: redundant 'move' after a successful 'put', unnecessary 'open fridge' before cooling, and detour exploration while searching. Guidance on single-command placement, no-open heat/cool, efficient episode shape, and lamp-task search order should reduce wasted actions and invalid retries on unseen episodes of the same task types."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.8333333333333334 → 0.8333333333333334 (Δ 0.0)
- Diff `.nanorsi/runs/80c8af4a8b/proposal/proposal.diff` sha256 `476d4cb6326d`… integrity ok: target/agent/skills/alfworld/SKILL.md +24/-8

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-003 | validation-games | ok/1.0 | ok/1.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |

## Attempt 3 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The only training failure was a look-at-object-in-light episode where the agent put the object down before using the lamp, so the use action did not satisfy the goal. Adding explicit task-pattern rules (hold the object while using the lamp) plus efficiency rules against redundant placement commands and unnecessary receptacle openings should fix that failure class and reduce wasted steps across unseen episodes."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.8333333333333334 → 0.8333333333333334 (Δ 0.0)
- Diff `.nanorsi/runs/fd8925de3b/proposal/proposal.diff` sha256 `5bc362cb2905`… integrity ok: target/agent/skills/alfworld/SKILL.md +29/-4

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-003 | validation-games | ok/1.0 | ok/1.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
