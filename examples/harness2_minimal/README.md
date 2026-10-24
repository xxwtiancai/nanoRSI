# Harness2 minimal — Propose-Probe-Compose on LAB with GLM-5.3

A minimal, standard-library execution of the Harness² task-level recursion
(Google Cloud AI Research + Northwestern, arXiv 2610.14224, Apache-2.0) on its
LAB benchmark (harveyai/harvey-labs, MIT), following the engineering direction
the repository adopted on 2026-10-24. Mechanism shapes follow the paper; no
upstream code is copied (the benchmark checkout and its judge are used as
installed dependencies).

## Mechanism (k=1, one task at a time)

1. **Reference run** — the current harness executes the task once.
2. **Propose** — one INVARIANT candidate (a cross-domain agentic deficiency)
   and one DOMAIN candidate (legal-work specific), each editing exactly one
   harness component (`systemprompt.md`, `tool_guidance.md`,
   `LongTermMEMORY.md`, or a new `skills/<slug>/SKILL.md`).
3. **Probe** — both candidates rerun the same task under matched
   configuration.
4. **Contrast** — each probe is classified against the reference as
   `mitigates` / `neutral` / `regresses`, with a concrete observation, using no
   ground truth.
5. **Compose** — adopt one candidate, merge mitigating edits, or keep the
   harness; every decision is tied to probe observations. The composed harness
   produces the final run (a `keep` decision reuses the reference run).

The baseline arm runs the unmodified base harness once. LAB's own hidden-rubric
judge (`evaluation.run_eval`, per-criterion) scores both arms; the reported
metric is **Partial** (criteria passed / criteria total), the paper's headline
LAB metric. The reference magnitude is the paper's GLM-5/OpenCode single-step
gain: LAB partial 59.6 → 71.4 (**+11.8pp**).

## Deviations from the paper (documented, not hidden)

- **Executor substrate**: a minimal stdlib agent loop (chat + list/read
  documents + write deliverable, bounded turns) instead of OpenCode; the
  substrate is identical in both arms, so arm comparisons remain internally
  valid, but absolute levels are not comparable to the paper's.
- **Improver and judge models**: GLM-5.3 for both (paper: Claude Opus 4.8
  improver, Gemini-family judge). The judge is patched locally with a
  `custom/<model>` provider (OpenAI-compatible `chat.completions` against the
  configured `OPENAI_BASE_URL`); all arms are judged by the same model.
- **Scope**: a selected task subset, k=1 only, no selection stage (a k=1 pool
  has one final, selected trivially), no cross-task experience accumulation in
  this first pass.

## Running

```bash
# prerequisites: harness2 LAB setup (see local run memory), pandoc >= 3.5,
# api key file ~/.nanorsi/keys/glm-coding-plan.key
python examples/harness2_minimal/run.py \
  --lab-root .omx/harness2/dependencies/harvey-labs \
  --tasks antitrust-competition/analyze-antitrust-hsr-strategy --arm both
```

Outputs under `--runs-dir` (default `.omx/harness2_minimal_runs/`):
`ledger.jsonl` (every model call, execution and judge event with usage),
`summary.json` (per-task partials, decisions, observations, token totals), and
one directory per execution (`trajectory.md`, `output/`, `scores.json`,
`judge.log`). Deliverables are written as markdown sources and converted to the
expected `.docx` names with pandoc.
