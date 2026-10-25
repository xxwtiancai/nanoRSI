# nanoRSI v0.5 on LAB — the rewritten loop against the paper's code, same models

The question the rewrite exists to answer: does nanoRSI's own implementation of the
Harness² recursion — a 1,400-line standard-library core with a contrast gate and no
verifier in the loop — produce gains comparable to the paper's code on the paper's
benchmark, under identical models? Everything that could be held equal was held equal
with the [faithful harness2 run](../harness2-lab-opencode/README.md):

| | harness2 (paper's code) | nanoRSI v0.5 |
| --- | --- | --- |
| Executor | OpenCode v1.14.18, LAB `workspace_config` install, GLM-5.3 (`zai/glm-5.3`) | **same** — the adapter calls LAB's own `run_opencode.py --harness-dir` |
| Base harness | LAB system prompt + empty guardrails / memory / tool guidance | **same** |
| Improver | GLM-5.3 in OpenCode sessions (INV, DOM, AGG, selection, reflection) | GLM-5.3 single structured chat calls (propose INV / DOM, contrast, compose, selection, lesson) |
| Judge | LAB `evaluation.run_eval`, `custom/glm-5.3` | **same** judge, same model, same tasks |
| Recursion | parallel k=1: 2 candidates probed, 1 composition, trivial selection | agg k=1: 2 candidates probed, **explicit contrast gate** (mitigates / neutral / regresses), compose may adopt only `mitigates`, trivial selection |
| Tasks | 8 LAB tasks, 8 practice areas | **same eight** |

The one deliberate difference is the improver's shape: the paper runs each improver step
as a full coding-agent session that edits files in a context directory; nano asks the
same model one structured question per step and applies the answer itself. The contrast
step is explicit in nano (a ledgered verdict per probe) where harness2 folds it into the
composer's judgement.

## Pilot (one task, run before the sweep)

`employment-labor/identify-issues-in-counterparty-motion-brief`, agg k=1:

| Step | Outcome |
| --- | --- |
| base1 | delivered (44 min) |
| INV → `tool_guidance.md` | "agent repeatedly extracted document text to /tmp, then `read` calls were blocked by the external-directory fence" — probed (16 min), **neutral**: "both executions produced a complete, validated memo with substantially equivalent findings" |
| DOM → `guardrails.md` | "unverifiable or fabricated record citations (the reference itself found phantom SUMF cites)" — probed, **neutral**: same core findings in both |
| compose | **keep** — "both candidate edits target risks the reference execution already handled on its own" |
| judge | base 13/23 = 0.565, final (= reference) 0.565, Δ 0.0 |

Budget: 3 rollouts (the keep reused the reference), 6 improver calls, 8.19 M input /
0.43 M output tokens (almost all of it the OpenCode executor's context). The pilot
exposed one bug — a kept final had no judgeable output directory — fixed before the
sweep (`recursion._kept` now copies `output/` and `deliverables/`).

## Eight-task sweep

Running: eight one-task workspaces (`examples/lab_opencode/prepare.py`), three
concurrent, `nanorsi evolve` → `freeze` each, then `judge` and `report`. Results,
per-task decisions, contrast verdicts, ledgers and the comparison table against the
harness2 run (+2.0 pp, 5W/1T/2L) and the paper (+11.8 pp) land here when the sweep
completes.

<!-- RESULTS -->
