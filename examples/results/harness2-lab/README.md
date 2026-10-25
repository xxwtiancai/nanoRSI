# Harness² minimal on LAB with GLM-5.3 — baseline vs one recursion step

The engineering track's first study after the 2026-10-24 reorganization: run
the Harness² paper's task-level recursion (k=1) end to end on its own LAB
benchmark and compare the improvement against the paper's magnitude on the
same metric. The mechanism implementation is
[`examples/harness2_minimal/`](../../harness2_minimal/README.md); this
directory publishes the run record and the comparison.

## Question

Does one Propose-Probe-Compose recursion step over a minimal editable harness
improve GLM-5.3's LAB partial score by a margin comparable to the paper's
GLM-5/OpenCode single-step gain (**+11.8 pp partial**, 59.6 → 71.4)?

## Design

- **Executor / improver / judge**: all `glm-5.3` (Z.ai coding endpoint,
  thinking disabled). The judge is LAB's own hidden-rubric scorer
  (`evaluation.run_eval`, one call per criterion), driven through a local
  `custom/<model>` provider patch (OpenAI-compatible `chat.completions` +
  `OPENAI_BASE_URL`); the same judge scores every arm.
- **Arms per task**: baseline (unmodified base harness, one draw) and
  recursion (reference run → INV + DOM single-component proposals →
  matched-config probes → mitigates/neutral/regresses contrast without ground
  truth → adopt/merge/keep compose → final run; a `keep` reuses the reference
  run). The reference run is also judged, so every task carries two draws of
  the identical base harness (baseline, reference) — a same-harness noise
  estimate.
- **Tasks**: 8 LAB tasks across 8 practice areas (analyze / review / draft;
  23–41 criteria each), chosen for moderate complexity and document-set size.
- **Metric**: partial = criteria passed / criteria total per task (the paper's
  headline LAB metric).

## Results

`summary.json` holds the per-task numbers; `ledger-pass2.jsonl` and
`ledger-pass1.jsonl` hold every model call, execution, probe, contrast,
compose decision and judge event with token usage; `pass2/` and `pass1/` hold
each execution's trajectory, scores and markdown deliverable sources.

| Task (practice area) | Baseline | Reference | Final | Compose decision |
| --- | ---: | ---: | ---: | --- |
| identify-issues-in-counterparty-motion-brief (employment) | 0.565 | 0.652 | **0.000** | adopt_dom |
| identify-issues-in-counterparty-sale-objection (bankruptcy) | 0.857 | **0.000** † | 0.714 | merge |
| review-iss-tax-transaction-structure (tax) | 0.750 | 0.857 | 0.857 | keep |
| review-form-8 (capital markets) | 0.906 | 0.938 | 0.938 | keep (compose failed ‡) |
| analyze-counterparty-motion-to-dismiss (litigation) | 0.882 | 0.794 | **0.912** | adopt_inv |
| draft-consent-to-adoption (trusts & estates) | 0.771 | 0.743 | 0.743 | keep |
| compare-closing-documents-against-restructuring-conditions (banking) | 0.763 | 0.711 | 0.711 | keep |
| extract-key-terms-from-cap-table (venture capital) | 0.512 | 0.463 | 0.463 | adopt_dom |
| **Mean (n = 8)** | **0.751** | **0.645** | **0.667** | 3 adopt/merge · 4 keep · 1 failed |

† The reference execution itself failed (unparseable actions on turn 12, no
deliverable); the merged harness produced a scored deliverable on the same
task. ‡ Both compose attempts answered without the required JSON header; the
rule fallback kept the reference harness.

| Comparison | Δ partial |
| --- | ---: |
| Final (recursion) − Baseline | **−8.4 pp** |
| Final (recursion) − Reference (same-session parent) | +2.2 pp |
| Reference − Baseline (identical harness, two draws) | −10.6 pp |
| Paper, GLM-5 / OpenCode, LAB partial, one step | **+11.8 pp** (59.6 → 71.4) |

**Verdict: the paper's single-step gain did not reproduce in this setting.**
Against the baseline arm the recursion step lost 8.4 pp; against its own
same-session reference it gained 2.2 pp. Both deltas sit inside the measured
same-harness noise band: two draws of the *identical* base harness differ by
10.6 pp on average, with one draw failing outright (0.000). Per task, the
three adopted edits split 1 win / 1 catastrophic loss / 1 tie: `adopt_inv`
on the motion-to-dismiss task is the one clean improvement (+11.8 pp over its
reference, coincidentally the paper's magnitude), `adopt_dom` on the
motion-brief task collapsed to 0/23 after a `mitigates` contrast, and the
cap-table `adopt_dom` left the score unchanged. The contrast stage rated three
edits `mitigates`, of which one improved the judged deliverable — the same
selection-failure shape the paper's own analysis records (an output scored 55
chosen over one scored 95).

### What the run record shows

- **Noise dominates effect.** On this executor the dominant failure modes are
  execution-level (an action that fails to parse, a document conversion that
  fails), and one such event moves a task by 60–90 pp. A one-draw comparison
  at n = 8 is a lottery — the conclusion this repository already reached on
  ALFWorld and HumanEval. A seeds-by-tasks grid is the minimum instrument
  before any effect claim.
- **The contrast gate is honest but weak.** `neutral` and `regresses`
  verdicts reliably led to `keep`; `mitigates` verdicts were 1-for-3 on the
  judged outcome. Behavioral contrast without a verifier admitted a harness
  that destroyed the deliverable.
- **Recursion rescues failed references.** The merge on the sale-objection
  task turned a failed run (0.000) into 0.714 — real value from the mechanism,
  but the baseline arm scored 0.857 on the same task, so it is recovery, not
  gain.
- **Document coverage is a substrate ceiling.** `.eml` sources are not
  converted by this minimal executor; several INV/DOM proposals targeted
  exactly this gap (retry-then-disclose rules) — the right diagnosis, but one
  that cannot be fixed inside the editable harness.

### Pass-1 record (kept; baseline draws only)

The first full run crashed its compose stage on three tasks: GLM answered the
compose prompt with plain fenced blocks instead of the `===FILE name===`
markers the parser required, so three `mitigates` candidates were never
adjudicated and fell back to `keep`. The parser was made tolerant and the
compose call given one retry; the recursion arm was rerun on all eight tasks
(pass-2). Pass-1 contributed the baseline draws for the first six tasks
(`ledger-pass1.jsonl`, `pass1/`); baseline draws for the last two tasks come
from pass-2.

### Budget

Executor: 11–13 model calls per execution; the recursion arm runs four to
five executions per task (≈ 50 calls, 0.7–1.2 M input tokens). Improver:
2 propose + 2 contrast + 1–2 compose calls per task. Judge: one `glm-5.3`
call per criterion per judged run (23–41 criteria × 3 judged runs per task;
judge usage runs inside the benchmark subprocess and is not in the ledgers).
Wall time ≈ 3.5 h across both passes.

## Honest boundaries

- n = 8 tasks, one draw per arm, no seeds (endpoint draws are unseeded); the
  baseline/reference pairs bound the same-harness noise.
- The executor substrate is this study's minimal stdlib agent, not OpenCode;
  absolute levels are not comparable to the paper and the arm-internal
  comparison is the measurement. Improver and judge are GLM-5.3, not the
  paper's Claude Opus 4.8 improver / Gemini judge.
- The base harness is deliberately thin (three short always-on files, no
  skills); the paper starts from production harnesses with eight components.

## Reproducing

```bash
python examples/harness2_minimal/run.py --arm both --tasks \
  employment-labor/identify-issues-in-counterparty-motion-brief,\
bankruptcy-restructuring/identify-issues-in-counterparty-sale-objection,\
tax/review-iss-tax-transaction-structure,capital-markets/review-form-8,\
litigation-dispute-resolution/analyze-counterparty-motion-to-dismiss,\
trusts-estates-private-client/draft-consent-to-adoption,\
banking-finance/compare-closing-documents-against-restructuring-conditions,\
emerging-companies-venture-capital/extract-key-terms-from-cap-table
```

Prerequisites (harness2 LAB setup, pandoc, the judge provider patch) and the
deviations from the paper are documented in the
[example README](../../harness2_minimal/README.md).
