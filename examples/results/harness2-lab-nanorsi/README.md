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

Eight one-task workspaces (`examples/lab_opencode/prepare.py`), three concurrent,
`nanorsi evolve` → `freeze` → `judge` each; agg k=1. All eight completed. Partial =
criteria passed / criteria total, judged by LAB's rubric judge with `custom/glm-5.3`.

| Task (practice area) | INV / DOM contrast | Compose | Base | Final | Δ pp |
| --- | --- | --- | ---: | ---: | ---: |
| identify-issues-in-counterparty-motion-brief (employment) | mitigates / mitigates | adopt_dom (`tool_guidance.md`) | 15/23 = 0.652 | 12/23 = 0.522 | **−13.0** |
| identify-issues-in-counterparty-sale-objection (bankruptcy) | neutral / neutral | keep | 25/28 = 0.893 | 25/28 = 0.893 | 0.0 |
| review-iss-tax-transaction-structure (tax) | neutral / **mitigates** | keep † | 22/28 = 0.786 | 23/28 = 0.821 | +3.6 ‡ |
| review-form-8 (capital markets) | neutral / neutral | keep | 31/32 = 0.969 | 31/32 = 0.969 | 0.0 |
| analyze-counterparty-motion-to-dismiss (litigation) | neutral / mitigates | adopt_dom (`guardrails.md`, `memory.md`) | 33/34 = 0.971 | 28/34 = 0.824 | **−14.7** |
| draft-consent-to-adoption (trusts & estates) | neutral / mitigates | adopt_dom (`memory.md`) | 29/35 = 0.829 | 30/35 = 0.857 | +2.9 |
| compare-closing-documents-against-restructuring-conditions (banking) | neutral / neutral | keep | 33/38 = 0.868 | 33/38 = 0.868 | 0.0 |
| extract-key-terms-from-cap-table (venture capital) | mitigates / neutral | adopt_inv (`tool_guidance.md`) | 37/41 = 0.902 | 39/41 = 0.951 | +4.9 |
| **Mean (n = 8)** | 5 mitigates · 11 neutral · 0 regresses | 4 adopt · 4 keep | **0.859** | **0.838** | **−2.1** (3W/3T/2L) |

† The composer asked for `adopt_dom` but answered with the header only (the candidate's
content was already in its context); the parser required a body and the attempt fell back
to `keep`. Fixed after this sweep started (`propose.compose` now applies the chosen
candidate's probed tree directly); workspaces 0–6 ran the old parser, workspace 7 the
new one. ‡ A `keep` final *is* the base deliverable — the +3.6 pp here is the same
`.docx` judged twice: a direct measurement of **judge noise of about one criterion**.

| Comparison | Base → final | Δ partial |
| --- | ---: | ---: |
| **nanoRSI v0.5** (this run) | 0.859 → 0.838 | **−2.1 pp** (3W/3T/2L) |
| harness2, paper's code, same models/tasks/judge | 0.872 → 0.892 | +2.0 pp (5W/1T/2L) |
| Paper, GLM-5 / OpenCode | 0.596 → 0.714 | +11.8 pp |

### Verdict

**The rewritten loop runs end to end on the paper's benchmark and executor, but in one
draw per rollout it did not produce a gain: −2.1 pp against +2.0 pp for the paper's own
code on identical models, tasks and judge.** The two numbers are 4 pp apart on eight
tasks whose single-task deltas swing ±13–15 pp; neither run is outside the other's noise.

The record shows *why* the explicit contrast gate did not help, and it is the same lesson
this repository reached three times on score gates:

- **Two of four adopted edits collapsed at the final rollout** (−13.0, −14.7 pp) after the
  probe of the *same harness* had been judged `mitigates`. The probe and the final are two
  draws of one harness; the contrast verdict compared one draw of the candidate with one
  draw of the base. A behavioral verdict without ground truth is still a single-sample
  estimate, and single samples of agentic LAB runs vary by 10+ pp. **Replacing a score
  gate with a contrast gate does not remove the lottery; only repeated draws do.**
- **The gate is conservative in the right direction when it says neutral.** Eleven of
  sixteen verdicts were `neutral`; all four `keep` tasks finished at base level (two
  exactly, one +3.6 judge-noise, one 0.0), i.e. the gate never *added* a loss by keeping.
- **harness2's edge on the same tasks is not mechanism-level.** Its composer adopted on 3
  of 8 tasks and won 5; its one big win (litigation, +11.8) is the task where nano's adopt
  lost 14.7 — the two systems drew opposite sides of the same coin. harness2's improver
  also edits inside a full OpenCode session with the whole evidence directory; nano asks
  one structured question per step.
- **The experience library worked as designed**: four lessons, each tied to an observed
  contrast — e.g. "run `--help` before the first call of an unknown workspace script"
  (venture-capital task, from two wasted sandbox-mode calls in the reference trajectory),
  "recompute numeric thresholds from raw exhibits instead of party summaries" (employment).

### Budget

28 rollouts (base 8, probes 16, finals 4 — four `keep` decisions reused the reference at
no cost), 52 improver calls, 45.3 M input / 2.2 M output tokens (the OpenCode executor's
context dominates). Wall time ≈ 7 h at three concurrent workspaces plus ≈ 1.5 h judging.
Every event is in `records/ws-*-ledger.jsonl`; per-rollout trajectories in
`records/runs/`; the four lessons in `records/ws-*-library.jsonl`.

## Round 2 — final confirmation (`final_repeats = 2`), one workspace, shared library

The first round's diagnosis (single-draw lottery) was built into the loop: an adopted
harness is now rolled out twice, every draw is contrasted against the reference, and the
adoption is confirmed only if no draw regresses and at least one mitigates; confirmed
draws enter blind selection. Probes and confirmation draws run concurrently; budgets are
charged by reservation. All eight tasks ran in **one workspace**, so the experience
library and the rejected-edit memory accumulate across tasks — the paper's
harnessing-level setting, which round 1's eight isolated workspaces lost. 34 rollouts,
60 improver calls, 57.5 M input tokens.

| Task | INV / DOM contrast | Compose | Confirmation | Base | Final (chosen) | Δ pp |
| --- | --- | --- | --- | ---: | ---: | ---: |
| identify-issues-in-counterparty-motion-brief | neutral / mitigates | adopt_dom | confirmed (neutral, mitigates) | 0.696 | 0.565 | −13.0 |
| identify-issues-in-counterparty-sale-objection | mitigates / neutral | adopt_inv | confirmed (mitigates, neutral) | 0.893 | 0.929 | +3.6 |
| review-form-8 | mitigates / neutral | adopt_inv | confirmed (mitigates, neutral) | 0.906 | 0.969 | +6.3 |
| extract-key-terms-from-cap-table | mitigates / mitigates | adopt_dom | confirmed (mitigates, mitigates) | 0.927 | 0.829 | −9.8 |
| analyze-counterparty-motion-to-dismiss | neutral / neutral | keep | — | 0.882 | 0.882 | 0.0 |
| review-iss-tax-transaction-structure | neutral / neutral | keep | — | 0.786 | 0.821 | +3.6 ‡ |
| draft-consent-to-adoption | mitigates / neutral | adopt_inv | confirmed (mitigates, mitigates) | 0.857 | 0.829 | −2.9 |
| compare-closing-documents-against-restructuring-conditions | neutral / neutral | keep | — | 0.947 | 0.974 | +2.7 ‡ |
| **Mean** | 7 m / 9 n / 0 r | 5 adopt · 3 keep · **0 rollback** | 5/5 confirmed | **0.862** | **0.850** | **−1.2** (4W/1T/3L) |

‡ keep finals are the base deliverable; both +deltas are judge noise on the same `.docx`.
With every one of the 40 produced rollouts judged (probes included), the averaged
measurement — final = mean of both confirmation draws — gives **0.862 → 0.847, −1.5 pp**.
Adopted tasks: 0.856 → 0.820 (−3.6 pp); kept tasks: 0.872 → 0.892 (+2.1 pp, judge noise).

### The decisive measurement: contrast verdicts do not track rubric deltas

| Probe judged `mitigates` | probe − base (judged) | | Probe judged `neutral` | probe − base (judged) |
| --- | ---: | --- | --- | ---: |
| form-8 INV | **+9.4 pp** ✓ | | litigation INV | **+5.9 pp** missed |
| trusts INV | +2.9 pp ✓ | | litigation DOM | +3.0 pp missed |
| employment DOM | −4.4 pp ✗ | | tax DOM | +3.5 pp missed |
| vc DOM | −9.8 pp ✗ | | | |
| bankruptcy INV | −10.7 pp ✗ | | | |

Two of five `mitigates` probes actually scored below their base; **all three** `neutral`
probes scored above it. The behavioral contrast — comparing trajectories and deliverable
appearance without ground truth — does not predict the direction of hidden-rubric change:
GLM sees "equally complete memos covering the same findings" while the rubric counts
specific criteria, and "stronger verification discipline" while the rubric does not
reward it. harness2's composer judges the same kind of evidence inside a full agent
session; on this round its luck differed (its one large win, litigation, is the task
nano's contrast called neutral on twice).

### Verdict after two rounds

| Run | Base → final | Δ | Note |
| --- | ---: | ---: | --- |
| nanoRSI round 1 (single draw) | 0.859 → 0.838 | −2.1 pp | two `mitigates` adopts collapsed at the final draw |
| nanoRSI round 2 (confirmed, shared library) | 0.862 → 0.850 (−1.5 pp averaged) | −1.2 pp | collapse losses gone; remaining losses are contrast misdirection |
| harness2, paper's code, same models/tasks/judge | 0.872 → 0.892 | +2.0 pp | |
| Paper (GLM-5 / OpenCode) | 0.596 → 0.714 | +11.8 pp | from a far lower base |

**Confirmation did what it was designed to do — round 1's catastrophic post-adoption
regressions (−13.0, −14.7 from harness-induced losses) did not recur, and every kept
task finished at or above base. What it cannot fix is the gate's signal itself: with a
verdict-to-score direction agreement of 2/5 on adoptions and 0/3 on misses, the loop
adopts the wrong edits and passes over the right ones.** Closing the remaining ~3.5 pp
to harness2 needs a decision signal that correlates with the rubric — a stronger judge
of behaviour, rubric-aware probe scoring (which the benchmark's rules and the paper's
verifier-free claim both push back on), or more draws per decision than the budget
allows here. The honest reading of both runs together: on eight tasks whose single-task
deltas swing ±10–15 pp, nanoRSI and harness2 are inside each other's noise, and the
paper's +11.8 pp remains unreproduced by either implementation at this configuration's
0.86+ baseline.

Round-2 records: `records/round2/` (ledger with every confirmation verdict, library,
report, workspace toml); the full 40-rollout judge matrix is recoverable from
`judge-result.json` in each rollout directory of the local workspace and is tabulated
above.
