# Harness² on LAB with GLM-5.3 — the original harness2 code, OpenCode substrate

The faithful run the engineering track owes the paper: the unmodified
`google-research/harness2` pipeline (Apache-2.0, pinned checkout) with its
OpenCode executor substrate, its own improver sessions, its parallel k=1
recursion and blind selection, on its own LAB benchmark (harveyai/harvey-labs,
MIT) scored by LAB's own hidden-rubric judge — with GLM-5.3 wired in as the
executor, improver and judge model. This supersedes the
[`harness2-lab/`](../harness2-lab/README.md) pilot, which ran the mechanism
shape through a simplified stdlib agent and cannot be compared to the paper.

## Question

With the paper's actual code and harness, does one parallel recursion step
(k=1: two candidate edits from shared base evidence, one composition, blind
selection) improve GLM-5.3's LAB partial score by a margin comparable to the
paper's GLM-5/OpenCode result (**+11.8 pp partial**, 59.6 → 71.4)?

## What is identical to the paper

- Code: `harness2` at the pinned release (3 commits); `harness2 --bench lab
  --substrate oc --k 1 --mode parallel` → `harness2-judge` → `harness2-report`.
- Executor substrate: OpenCode (pinned v1.14.18 source, run through bun) with
  the eight-component editable surface (system prompt, guardrails, memory,
  tool guidance, subagents, skills, scripts, plugins) and LAB's
  `workspace_config` install mode (tool gate, native docx/pptx/xlsx skills).
- Recursion: shared base rollout → INV + DOM improver sessions (full OpenCode
  agent sessions editing `context/harness/`) → candidate rollouts → AGG
  composition session → final rollout → blind anonymised selection (trivial at
  k=1) → reflection. Ledger identity asserted by harness2 itself.
- Benchmark and metric: LAB tasks, `evaluation.run_eval` per-criterion
  hidden-rubric judge, partial = criteria passed / total, all-pass alongside.

## What differs from the paper (all three are model substitutions)

| Role | Paper | This run |
| --- | --- | --- |
| Executor | GLM-5 / Gemini 3.5 Flash on Vertex | **GLM-5.3** via OpenCode `@ai-sdk/openai-compatible` provider → Z.ai coding endpoint |
| Improver | Claude Opus 4.8 under OpenCode | **GLM-5.3** under OpenCode (same session mechanics) |
| Judge | Vertex Gemini | **GLM-5.3** through a local `custom/<model>` provider in LAB's judge (`setup/judge.py.full.diff`) |

The judge substitution changes absolute levels (the paper itself notes judge
choice moves scores); the same judge grades base and final here, so the
arm-internal delta is the measurement. GLM-5.3 runs with the endpoint's default
thinking behaviour; the `--reasoning-effort high` that LAB passes writes a
Gemini-specific `thinkingConfig` into the workspace config, which the
openai-compatible provider ignores.

## Local environment shims (no upstream code changed except the judge patch)

- `setup/opencode.json`: the OpenCode provider definition, loaded through an
  isolated `XDG_CONFIG_HOME` so the machine's personal OpenCode config and
  plugins never touch the runs; the API key is a `{file:...}` reference.
- `setup/harness2.env`: the harness2 model settings (`zai/glm-5.3` solver and
  improver, `custom/glm-5.3` judge, `OPENAI_BASE_URL` for the judge).
- GNU `timeout` shim: LAB's runner wraps OpenCode in `timeout --kill-after`,
  which macOS lacks; `coreutils` was installed and `gtimeout` linked as
  `timeout` on `PATH`. Without it every rollout dies silently with empty logs.
- Judge patch: harness2's own `harvey-labs-judge-vertex-anthropic.diff` was
  regenerated to include the `custom/` provider so `harness2-check`'s
  reverse-apply verification still passes (`setup/judge-custom-provider.patch-of-patch.diff`).

## Feasibility run (one task)

Before the sweep, the pilot's first task was run alone in its own namespace:

| Task | Base (base1) | Final (agg1, blind-selected) | Δ |
| --- | ---: | ---: | ---: |
| employment-labor/identify-issues-in-counterparty-motion-brief | 12/23 = 0.522 | 14/23 = 0.609 | **+8.7 pp** |

Improver spend reported by harness2: $3.16 (OpenCode's price-table estimate;
the coding-plan endpoint bills by subscription). Wall time ≈ 45 min for the
four rollouts and three improver sessions.

## Main sweep (eight tasks, eight practice areas)

Tasks: `setup/split-eight.json` — the same eight tasks as the pilot. Run as
one harness2 sweep (`--workers 2`, own `HARNESS2_RUNS_DIR`); 8/8 tasks
completed, 0 failed, ≈ 6.5 h wall time. harness2's report:
`parallel k=1: n=8 | partial 89.20% | pass 12.5% | picked output: final 8 /
candidate 0 / base 0`; improver spend (editors, composer, selection,
reflection) $24.76 at OpenCode's price table.

| Task (practice area) | Base | Final (agg1) | Δ pp | What the composed harness changed |
| --- | ---: | ---: | ---: | --- |
| compare-closing-documents-against-restructuring-conditions (banking) | 37/38 = 0.974 | 38/38 = **1.000** | +2.6 | systemprompt, guardrails, memory, tool guidance, `scripts/extract_all_docs.py`, `skills/cite-check` |
| identify-issues-in-counterparty-sale-objection (bankruptcy) | 24/28 = 0.857 | 25/28 = 0.893 | +3.6 | systemprompt, guardrails, tool guidance, `skills/objection-response-memo` |
| review-form-8 (capital markets) | 30/32 = 0.938 | 31/32 = 0.969 | +3.1 | systemprompt, tool guidance, `scripts/xlsx_cells.py`, `skills/sec-filing-review` |
| extract-key-terms-from-cap-table (venture capital) | 37/41 = 0.902 | 39/41 = 0.951 | +4.9 | systemprompt, guardrails, tool guidance, `scripts/check_artifact.py`, `skills/vc-cap-table-review` (+ `cap_math.py`) |
| identify-issues-in-counterparty-motion-brief (employment) | 17/23 = 0.739 | 16/23 = 0.696 | **−4.3** | systemprompt, guardrails, two skills, `scripts/verify_greenleaf_headcount.py` (task-entity-specific) |
| analyze-counterparty-motion-to-dismiss (litigation) | 29/34 = 0.853 | 33/34 = **0.971** | **+11.8** | guardrails, tool guidance only |
| review-iss-tax-transaction-structure (tax) | 24/28 = 0.857 | 24/28 = 0.857 | 0.0 | systemprompt, guardrails, tool guidance, `scripts/extract_sources.py`, `skills/tax-document-review` |
| draft-consent-to-adoption (trusts & estates) | 30/35 = 0.857 | 28/35 = 0.800 | **−5.7** | systemprompt, guardrails, memory, tool guidance, `skills/adoption-consent-drafting` |
| **Mean (n = 8)** | **0.872** | **0.892** | **+2.0** | 5 wins / 1 tie / 2 losses |

| Comparison | Δ partial |
| --- | ---: |
| Final (one parallel recursion step) − Base, this run | **+2.0 pp** (0.872 → 0.892) |
| Paper, GLM-5 / OpenCode, LAB partial, one step | **+11.8 pp** (0.596 → 0.714) |
| Headroom above base | this run 12.8 pp · paper 40.4 pp |
| Share of headroom captured | this run 16 % · paper 29 % |

**Verdict: the mechanism produced a positive gain in the paper's own code
(+2.0 pp, 5W/1T/2L), in the paper's direction but well below its +11.8 pp.**
The dominant reason is the baseline: GLM-5.3 inside the production OpenCode
harness already scores 0.872 on these eight tasks, where the paper's
GLM-5/OpenCode cell starts at 0.596, so there was a quarter of the headroom to
win. Measured against available headroom the step captured 16 % here versus
29 % in the paper. One task (litigation) gained exactly the paper's +11.8 pp
from guardrails and tool-guidance edits alone; the two losses both came from
composed harnesses that added task-specific machinery (the employment task's
`verify_greenleaf_headcount.py` is keyed to that case's entity), the
over-specialisation failure the paper's own analysis warns about.

### What the record shows

- **The improver edits the real surface.** Every composed harness touched
  systemprompt / guardrails / tool guidance and most added a skill and a
  helper script (`records/<task>.json` → `harness_diffs`), exactly the
  eight-component surface the paper describes; the pilot's three-file
  substrate never had this room.
- **Blind selection was trivial at k=1** (one final per task; `picked output:
  final 8`), so no selection failures were possible here — the paper's
  selection-failure mode needs k ≥ 2.
- **Cross-task experience accumulated.** The harnessing-level library
  (`records/library.json`) holds one adopted harness and one evidence-backed
  lesson per task; several lessons name the same recurring defect (document
  readers whose default invocation fails in the sandbox, forcing rediscovery
  every rollout).
- **Variance remains unmeasured.** One draw per arm; the pilot's 10.6 pp
  same-harness spread on a weaker substrate suggests single-task deltas of
  ±5 pp are within noise — the 5W/1T/2L split and the +2.0 pp mean are the
  honest summary, not any single task.

### Environment incidents (recorded, resolved)

- First sweep died silently: LAB's runner wraps OpenCode in GNU `timeout`,
  absent on macOS → empty session logs. Fixed with a `coreutils` shim.
- First judge pass left all eight selections ungraded: 8 parallel selections ×
  6 criteria each hit the endpoint's 429 limit and the judge's four parse
  retries had no back-off. Fixed by exponential back-off in the `custom/`
  provider path, `_PARALLEL = 2` in `harness2/cli/judge.py` and `--parallel 3`
  in LAB's `run_eval` call; re-judged 8/8 graded.
- harness2 refuses a namespace whose task set changes
  (`This run directory belongs to different models or tasks`); the eight-task
  sweep therefore ran in its own `HARNESS2_RUNS_DIR` and re-ran the
  feasibility task (its second draw: 17/23 base → 16/23 final, versus 12/23 →
  14/23 in the feasibility namespace — the same-harness base spread on this
  task alone is 5/23).

## Honest boundaries

- n = 8 tasks, one draw per arm, no seeds; LAB tasks are long agentic
  sessions and single-draw variance is large (the pilot measured a 10.6 pp
  same-harness spread on its simpler substrate).
- Three model substitutions (above); absolute scores are not the paper's.
- The paper's LAB numbers are averaged over many more tasks and four
  model–harness configurations; this is one configuration on eight tasks.

## Reproducing

```bash
# once: harness2 clone + `harness2-setup lab`, coreutils (gtimeout → timeout on PATH),
# the provider file as $XDG_CONFIG_HOME/opencode/opencode.json, setup/harness2.env as .env,
# setup/harness2-local-changes.diff applied to the harness2 checkout (judge concurrency
# + regenerated judge patch; the patch itself carries the custom/ provider with back-off).
export XDG_CONFIG_HOME=<isolated-config-dir> HARNESS2_RUNS_DIR=<fresh-runs-dir>
export OPENAI_API_KEY="$(cat ~/.nanorsi/keys/glm-coding-plan.key)"
harness2 --bench lab --substrate oc --k 1 --mode parallel --split all \
  --split-file setup/split-eight.json --workers 2
harness2-judge --bench lab --substrate oc --k 1 --modes parallel
harness2-judge --bench lab --substrate oc --k 1 --modes parallel --bases
harness2-report --bench lab --substrate oc --k 1 --modes parallel
```

`records/` holds harness2's `judged.json` / `base_judged.json`, the sweep
record, the namespace config, one JSON per task (harness2 summary, selection,
reflection experience, and `diff -ruN` of each stage's harness against base),
and the cross-task library. Full OpenCode session streams (≈ 1 MB per rollout,
32 rollouts) stay in the local runs directory and are available on request.
