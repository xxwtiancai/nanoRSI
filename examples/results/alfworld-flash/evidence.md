# nanoRSI evidence ledger

One record per proposal revision: diagnosis, candidate diff, redacted per-case
evaluator evidence and the accept/reject decision, with artifact integrity flags.
Structured data: `evidence.jsonl`; raw journal: `lineage.jsonl`.

## Gate summary

Read-only counts derived from the same verified lineage revisions:

- accepted: 1, rejected: 3

| Attempt | Generation | Decision | Δ metric | Files |
| ---: | ---: | --- | --- | --- |
| 1 | 0 | rejected | 0.0 | 1 |
| 2 | 0 | rejected | -0.25 | 1 |
| 3 | 0 | rejected | 0.0 | 1 |
| 4 | 1 | accepted | 0.125 | 1 |

## Attempt 1 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "All train episodes were won but with wasted exploration steps (e.g., 9-10 searches before finding the object). Adding goal-type plan templates, likely-location search order, open-before-give-up, and one-instance-at-a-time sequencing should shorten unseen episodes and avoid partial two-object tasks, without changing any successful patterns."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.875 (Δ 0.0)
- Diff `.nanorsi/runs/763684c721/proposal/proposal.diff` sha256 `cbe66eda1389`… integrity ok: target/agent/skills/alfworld/SKILL.md +18/-8

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
- Reason: improvement below minimum: -0.250000
- Diagnosis: `{"reason": "The lost episode burned its entire step budget walking through cabinets without opening them and never retrieved the kettle. Adding task-type pipelines, likely-location search order, mandatory open-after-arrive for closed receptacles, and already-located skip rules should cut wasted exploration steps on unseen episodes of all goal types."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.625 (Δ -0.25)
- Diff `.nanorsi/runs/6b95acfe3b/proposal/proposal.diff` sha256 `fd4daa6bdbfc`… integrity ok: target/agent/skills/alfworld/SKILL.md +49/-9

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | task_failure/0.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | ok/1.0 | ok/1.0 |
| validation-003 | validation-games | task_failure/0.0 | task_failure/0.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
| validation-006 | validation-games | ok/1.0 | ok/1.0 |
| validation-007 | validation-games | ok/1.0 | task_failure/0.0 |

## Attempt 3 — rejected (generation 0)
- Reason: improvement below minimum: 0.000000
- Diagnosis: `{"reason": "The lost kettle episode spent 20 steps searching cabinets before checking tables, then ran out of steps right after cleaning without placing the object. Adding likely-location search order, mandatory open-after-go for closed receptacles, task-type pipelines, and an explicit finish-placement-under-step-pressure rule should cut wasted exploration steps and prevent episodes ending with the goal object still in inventory."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 0.875 (Δ 0.0)
- Diff `.nanorsi/runs/ba4beb589e/proposal/proposal.diff` sha256 `e813b5c55174`… integrity ok: target/agent/skills/alfworld/SKILL.md +20/-6

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

## Attempt 4 — accepted (generation 1)
- Reason: improvement 0.125000
- Diagnosis: `{"reason": "The lost episode exhausted its budget opening cabinet after cabinet without reserving steps for cleaning and delivery. Adding open-before-contents awareness, likely-first search order, step budgeting with a reserved delivery phase, no-revisit rule, and goal-type pipelines should cut wasted exploration and ensure tasks finish within the step limit on unseen episodes."}`
- Surface: target/agent/skills/alfworld/SKILL.md
- score: 0.875 → 1.0 (Δ 0.125)
- Diff `.nanorsi/runs/74015f60c3/proposal/proposal.diff` sha256 `6bd23da093f2`… integrity ok: target/agent/skills/alfworld/SKILL.md +18/-0

### Cases

| Task | Group | Parent | Candidate |
| --- | --- | --- | --- |
| validation-000 | validation-games | ok/1.0 | ok/1.0 |
| validation-001 | validation-games | ok/1.0 | ok/1.0 |
| validation-002 | validation-games | ok/1.0 | ok/1.0 |
| validation-003 | validation-games | task_failure/0.0 | ok/1.0 |
| validation-004 | validation-games | ok/1.0 | ok/1.0 |
| validation-005 | validation-games | ok/1.0 | ok/1.0 |
| validation-006 | validation-games | ok/1.0 | ok/1.0 |
| validation-007 | validation-games | ok/1.0 | ok/1.0 |
