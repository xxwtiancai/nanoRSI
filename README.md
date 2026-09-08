# nanoRSI

[![CI](https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml/badge.svg)](https://github.com/xxwtiancai/nanoRSI/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)

**A minimal, hackable lab for improving agent skills and harnesses under a fixed model and a measurable budget.**

nanoRSI runs a small experiment: execute training tasks, propose a skill patch, compare exact parent/candidate snapshots on validation tasks, keep or reject it, then freeze the experiment before final testing. Model weights stay fixed. The core uses Python's standard library and Git; no database, server, plugin registry or distributed scheduler.

[中文说明](README.zh-CN.md)

## Install

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Python 3.11+ and Git are required. The reference skills runner uses a configured model command; a small OpenAI-compatible HTTP bridge is included. A compatible local model server can use no key. Hosted endpoints may charge for calls.

## Run a skills experiment

```bash
nanorsi new skills ./skills-lab --goal "Improve reliable file editing"
```

Edit `skills-lab/nanorsi.toml` **before baseline**. Set `[agent].model`, `base_url`, and an absolute external `api_key_file` if authentication is needed. Alternatively replace `model_command` with your JSON-protocol bridge. The placeholder model intentionally requires configuration. Model settings, task data, evaluator and bridge files become fixed at baseline.

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

The starter contains 90 deterministic local file-editing **protocol fixtures**, grouped into 30 train, 30 validation and 30 test tasks. They exercise inspection, constrained edits and verification; they are not a public benchmark. A proposal may improve, fail or make no change. We do not promise positive gains.

The default allows changes only to `target/agent/skills/**`. The reference runner loads `inspect`, `edit` and `verify` skills, offers list/read/write/final actions, records actual skill hashes, and creates a fresh temporary task workspace for every execution. It never executes model-written shell commands. Editable skills are instructions in this starter; script execution and retrieval systems are not implemented.

## Experiment controls

- **One parent, one candidate:** rejected, failed and unchanged attempts consume the attempt budget; only strictly better valid candidates become parents.
- **Three data roles:** train results provide feedback; validation selects candidates; final-test runs only after freeze and cannot promote a candidate.
- **Two proposer modes:** `arm = "frozen"` uses the initial harness to propose changes; `arm = "self-use"` uses the latest accepted harness. Both edit the current parent. Separate workspaces are required for comparison arms.
- **Recorded evidence:** exact commits, evaluator/experiment fingerprints, task outcomes, skill hashes, proposal/trace artifacts, nullable usage and decision reasons.
- **Bounded execution:** attempts, reserved task episodes, timeouts, model turns and captured output. Missing dollar/token usage is unknown, never free. Dollar totals are observational, not a hard spending cap.
- **Fixed final panel:** freeze pins repeats (1–10). Final testing compares initial skills, no skills and selected skills. Completed panels are reused on rerun; interrupted panels are retained and explicitly flagged instead of silently retrying for a better score.

With 30 validation tasks, five attempts require up to 350 search episodes (30 baseline + five × [4 train + 30 parent + 30 candidate]); the default search cap is 400. Final testing with three repeats reserves 270 additional episodes. Proposal model calls are recorded separately. Configure smaller task panels and budgets for initial checks.

To compare methods, copy the starter before baseline, change only arm/seed, configure the same model and task data, and freeze all choices before examining test results. `examples/compare.py` reports paired task-macro scores, per-arm results, observed costs and coverage. Independent evolution runs and repeated deployments are distinct units of evidence.

## Offline compatibility demo

```bash
nanorsi new artifact ./artifact-demo
nanorsi baseline --workspace ./artifact-demo
nanorsi step --workspace ./artifact-demo
nanorsi verify --workspace ./artifact-demo
```

Legacy `artifact` and `harness` are explicitly scripted offline demos. The legacy `model` template remains an external training contract; it does not train weights in the core. Their historical `heldout` split participates in selection and is **not** a final-test set. Schema-v2 experiments require fresh workspaces.

## Commands

`new`, `doctor`, `baseline`, `step`, `run`, `evaluate`, `report`, `freeze`, `final-test`, `verify`, `recover`.

Use `--workspace PATH` for experiment commands. For v2 manual evaluation, specify `--split train` or `--split validation`. `recover` reconciles interrupted attempts and stale local worktrees; it is not a sandbox or a remote job manager.

## Trust boundary

The default is **trusted local execution**. Worktrees, mutation allowlists and HMAC receipts protect version consistency, not filesystem secrecy against code running as the same OS user. Candidate Python can otherwise read local data or keys. Use a separately configured container/VM/service for untrusted harness code or genuine private-label evaluation. No hardened container adapter is bundled. See [SECURITY.md](SECURITY.md).

## Development

```bash
PYTHONPATH=src python -m unittest discover -v
python -m compileall -q src examples tests
```

Tests include mocked model-command and local HTTP fixtures, the multi-round lifecycle and frozen/self-use hash checks. These prove protocol behavior, not live model performance. Architecture tests preserve the 2,500-line core budget, 300-line files and 50-line functions. There are no runtime third-party imports.

## Documentation

- [Kernel specification](docs/specification.md)
- [Project charter](docs/PROJECT_CHARTER.md)
- [v0.2 design and remaining research work (Chinese)](docs/design/HARNESS_PLATFORM_V0_2.zh-CN.md)
- [Paper evaluation research, 2026-09-08 (Chinese)](docs/research/HARNESS_EVALUATION_2026-09-08.zh-CN.md)
- [Implementation plan](docs/superpowers/plans/2026-09-09-skills-harness.md)
- [Example protocol and comparison tools](examples/README.md)
- [Changelog](CHANGELOG.md)
- [Earlier RSI survey](docs/research/RSI_SURVEY.md)

Apache-2.0. See [LICENSE](LICENSE).
