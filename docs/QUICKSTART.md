# Running your first skills experiment

Use Python 3.11+ and Git. Start from a source checkout so the comparison and task-preparation scripts are available.

```bash
git clone https://github.com/xxwtiancai/nanoRSI.git
cd nanoRSI
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Try the offline protocol

```bash
nanorsi new artifact ./artifact-demo
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi report --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

This is a scripted fixture with no model API calls. It demonstrates proposal, comparison, acceptance and traceability. Its scores are fixture outcomes, not a measurement of model skill improvement.

## Configure a real model

```bash
nanorsi new skills ./skills-lab --goal "Improve reliable file editing"
```

Edit the existing `[agent]` section in `skills-lab/nanorsi.toml` before baseline:

```toml
[agent]
model_command = ["python3", "adapters/model.py"]
model = "your-model-id"
base_url = "http://localhost:8000/v1"
max_turns = 8
max_tokens = 2048
timeout_s = 60
skills = ["inspect", "edit", "verify"]
# For an authenticated endpoint, use an external absolute path:
# api_key_file = "/absolute/path/to/model-key.txt"
```

The bundled HTTP bridge targets an OpenAI-compatible chat-completions endpoint. A compatible local server may use no key. You can replace `model_command` with a custom bridge following the exported adapter's JSON protocol. Model-specific API differences may need an adapter change before baseline. Model settings, task data and protected bridge/evaluator files become fixed at baseline.

## Choose a budget before running

The starter has 90 grouped local file tasks: 30 train, 30 validation and 30 test. They are protocol fixtures, not a public benchmark. Every search attempt uses up to four training tasks, plus up to 30 parent and 30 candidate validation tasks. With baseline, five attempts can use 350 search episodes. The default search cap is 400.

Final testing with three conditions and three repeats uses 270 additional episodes. Proposal calls are recorded separately. Model turns, time and output are bounded; dollar costs are reported when available and are not a hard spending cap. Start with a smaller, source-group-disjoint manifest for an inexpensive first run. Every split must remain nonempty.

```toml
[budget]
max_steps = 5
max_episodes = 400
max_output_bytes = 1000000
```

## Run, freeze and compare

```bash
nanorsi doctor --workspace ./skills-lab
nanorsi baseline --workspace ./skills-lab
nanorsi run --workspace ./skills-lab
nanorsi report --workspace ./skills-lab
nanorsi freeze --workspace ./skills-lab --repeats 3
nanorsi final-test --workspace ./skills-lab
nanorsi verify --workspace ./skills-lab
python examples/compare.py ./skills-lab/reports/final.json
```

The default mutable surface is `target/agent/skills/**`. The runner loads Markdown skills and exposes list/read/write/final actions in a fresh temporary task directory. Script execution and skill retrieval are not part of this starter.

Use `step` for one attempt. For v2 manual evaluation use `evaluate --split train` or `evaluate --split validation`. `freeze` fixes the final test panel and prevents continued search. Completed final panels are idempotent; incomplete panels remain explicit failures rather than silently being rerun until they score better. `recover` reconciles interrupted local attempts/worktrees.

## Compare frozen and self-use proposers

Create separate workspaces from the same initial template. Before baseline, set `experiment.arm = "frozen"` in one and `"self-use"` in the other; keep model, task data, inference settings and budget matched. Use independent seeds for separate evolution runs. Freeze every arm before examining final-test results.

- Frozen: the initial harness always proposes changes to the current parent.
- Self-use: the accepted harness proposes the next changes to the current parent.

Pass compatible final reports to `examples/compare.py`. It reports task-macro paired deltas, per-arm summaries, observed costs and coverage. Deployment repeats and independent evolution runs are distinct. A recursive wiring check proves which skills were loaded; evidence of recursive benefit requires real comparative experiments.

## Inspect the evidence

| File | Contents |
| --- | --- |
| `reports/report.md` | Human-readable search decisions and cost coverage |
| `reports/report.json` | Full search journal export |
| `reports/final.json` | Frozen comparison results and search/test cost evidence |
| `lineage.jsonl` | Sequenced receipts, parent/candidate identities and artifact references |
| `.nanorsi/runs/` | Per-attempt proposal, context, traces and evaluation files |

## Execution boundary

Default execution is trusted local subprocess execution. Worktrees and receipts do not hide labels or keys from arbitrary same-user code. Use an external container/VM/service for untrusted executable harnesses or genuine private-label evaluation; no hardened isolation adapter is bundled. See [SECURITY.md](../SECURITY.md).

Legacy artifact/harness demos and the model external-training contract remain available. Their historical heldout split participates in selection and is not an independent final test. V2 experiments start in fresh workspaces.
