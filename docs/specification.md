# nanoRSI Kernel Specification (v0.5)

nanoRSI v0.5 is a minimal, auditable implementation of recursive harness improvement
in the shape of Harness² (Google Cloud AI Research, arXiv 2610.14224): a frozen model,
an editable harness around it, and a task-level recursion that proposes edits from
execution evidence, probes them under matched configuration, classifies the behavioral
contrast without ground truth, composes the next harness, and only then — after a
freeze — judges base and final outputs. Python 3.11+ and the standard library are the
whole runtime. Local execution is trusted; this is not a sandbox.

## Module map

| Module | Responsibility |
| --- | --- |
| `src/nanorsi/__init__.py` | Version |
| `src/nanorsi/cli.py` | `new`, `configure`, `evolve`, `freeze`, `judge`, `report`, `verify`, `doctor` |
| `src/nanorsi/config.py` | One validated TOML: experiment (mode agg/seq, k, seed), model, runner, harness root, tasks, judge, budget |
| `src/nanorsi/ledger.py` | Append-only hash-chained event ledger; `verify`; usage totals; freeze state |
| `src/nanorsi/model.py` | Standard-library chat-completions client; the one reply grammar (JSON header line + fenced bodies); bounded retries |
| `src/nanorsi/harness.py` | The editable surface: four always-on files, `skills/<slug>/SKILL.md`, `scripts/<slug>.py`; validation, diff, rendering |
| `src/nanorsi/tasks.py` | Frozen task manifest (instruction, documents, deliverables) and selection |
| `src/nanorsi/runner.py` | Rollout protocol; built-in loopback document agent; external `command` runner (request.json → result.json) |
| `src/nanorsi/propose.py` | INV / DOM single-component proposals and the compose step (adopt / merge / keep tied to observations) |
| `src/nanorsi/probe.py` | Matched-configuration probe contrast: mitigates / neutral / regresses, no ground truth |
| `src/nanorsi/recursion.py` | Parallel (`agg`) and sequential (`seq`) recursion over k; budget charging; every step ledgered |
| `src/nanorsi/select.py` | Blind terminal selection over anonymised deliverables when a task has more than one final |
| `src/nanorsi/experience.py` | Harnessing-level recursion: one evidence-backed lesson per adopted harness into the workspace library |
| `src/nanorsi/judge.py` | Post-freeze judging of base and chosen finals through a workspace judge command; ungraded ≠ zero |
| `src/nanorsi/report.py` | Derived views over the ledger (per-task decisions, contrasts, scores, budget) |
| `src/nanorsi/templates.py` | The default starter: base harness, offline tasks, keyword judge |

Budgets enforced by tests: core ≤ 2,500 lines, module ≤ 300 lines, function ≤ 50 lines,
no runtime third-party imports.

## Lifecycle

```text
new → configure → evolve (per task: base → [INV, DOM] → probe → contrast → compose → final;
      k pairs in parallel or k rounds in sequence; blind selection when finals > 1; lesson)
    → freeze (choices pinned; evolve refused afterwards)
    → judge (base and chosen final per task; scores never reach the improver)
    → report / verify
```

`evolve` resumes: tasks with a `task_done` event are skipped. `configure` is refused once
the ledger has started. `judge` is refused before `freeze`.

## Harness surface

A harness is a dict `{relative path: text}` restricted to `systemprompt.md`,
`guardrails.md`, `memory.md`, `tool_guidance.md`, `skills/<slug>/SKILL.md` (first line a
description) and `scripts/<slug>.py`. At least one always-on file must be non-empty; the
always-on total is capped at 24,000 characters. `render_always_on` is what every
executor sees before the task: the always-on files, a skill index (skills load on
demand) and the script roster. Subagents and plugins — the paper's remaining two
components — need a host runtime nano does not ship.

## Rollout protocol

A rollout is one task under one harness: `{ok, delivered, trajectory, deliverables
{name: text}, usage, error}`. `runner.kind = "loopback"` runs the built-in document agent
(list / read / write_deliverable / done) on the configured model. `runner.kind =
"command"` runs a workspace command with `NANORSI_REQUEST` (json: task, harness_dir,
output_dir, always_on, label) and reads `NANORSI_RESULT`; this is how a real substrate
such as OpenCode is attached without the core knowing it. Every rollout directory
keeps `harness/`, `trajectory.md`, `deliverables/` and, for command runners,
`request.json`, `result.json`, `runner.log`.

## Recursion

Each task starts with one base rollout (`base1`). A candidate pair is one INV proposal
(cross-domain agentic deficiency) and one DOM proposal (domain-specific), each editing
exactly one component via the reply grammar; each is probed with its own rollout
(`inv<i>`, `dom<i>`) and contrasted against the base. `agg` runs k independent pairs
against the shared base and then k compositions, each rolled out as `agg<i>`. `seq` runs
k rounds where the composition becomes the next round's base (`c<t>`). A `keep`
decision reuses the reference rollout (`rollout_reused` event) instead of spending one.
Proposals that failed validation count as `regresses` for composition. Rejected
contrasts feed the next proposals as `RECENTLY REJECTED EDITS`.

## Contrast gate

`probe.contrast` compares the candidate's trajectory and deliverables with the
reference's under matched configuration and returns `mitigates`, `neutral` or
`regresses` with the observation that decides it. A candidate without a deliverable
where the reference had one is `regresses` without a model call. Compose may adopt only
`mitigates` edits; `keep` beats adopting `neutral`/`regresses`; `merge` requires two
mitigating edits on different components. A failed contrast call reads as `neutral`
and records the error.

## Selection, experience, judging

With more than one delivered final, `select.blind` shows anonymised deliverables (ids
shuffled by a seeded hash of the task) and must name exactly one; a failed selector
keeps the first delivered final and records `fallback`. If the chosen harness differs
from the base, `experience.extract` asks for one lesson the contrasts support and
appends it to `.nanorsi/library.jsonl`; later tasks see the library before proposing.
`freeze` pins `{task: chosen label}`. `judge` runs the workspace judge command
(`NANORSI_JUDGE_REQUEST` → `NANORSI_JUDGE_RESULT` with `n_passed`, `n_criteria`) on
`base1` and the chosen final; a missing or malformed result is `graded: false`, never
zero. Reports derive means, win/tie/loss counts and budget from the ledger alone.

## Budget and honesty

`[budget] max_rollouts` and `max_proposer_calls` are charged before each rollout and
each improver call (propose, contrast, compose, selection, experience); exhaustion is a
ledger event and stops the run cleanly. Usage (calls, input/output tokens) is recorded
per event and summed in reports. Scores exist only after freeze and never influence
proposals, probes or composition. The ledger is hash-chained; `verify` fails on any
rewrite.

## Credentials

The model key lives in an external file named by `[model] api_key_file`; `configure`
checks the file exists and never copies its contents. No ambient environment variables
or `.env` files are read by the core.
