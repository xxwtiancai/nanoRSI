# Reproducible improvement experiments

[English multilevel guide](../docs/MULTILEVEL.md) · [中文多层级指南](../docs/MULTILEVEL.zh-CN.md) · [API keys and first run](../docs/QUICKSTART.md) · [中文入门](../docs/QUICKSTART.zh-CN.md)

Run these commands from the repository with Python 3.11+, Git and nanoRSI installed. Every output directory must be new so earlier outcomes are retained. The canonical starters are `artifact`, `harness` and `model`; `program`, `agent` and `learner` remain aliases. Each experiment uses the ordinary CLI and the same protected evaluation contract.

## CPU parameter learning: no API required

```bash
python examples/parameter_learning/run.py ./parameter-results
```

This runs three methods × three seeds × frozen/self-use proposer controls: 18 independent evolution runs with three training attempts each. The trainer performs actual SFT, REINFORCE or LoRA gradients on a four-feature, three-class softmax model, writes a checkpoint, and lets validation accept or reject it. Freeze selects existing checkpoints; final evaluation does not retrain.

The proposer reads its assigned checkpoint, ranks allowed training examples by loss and adjusts the next curriculum. Frozen/self-use therefore tests checkpoint-guided curriculum reuse, while both groups continue training from the current accepted checkpoint. `summary.json` includes every trial, per-method/control means, loss and accuracy, plus paired self-use differences. Per-workspace command logs and `reports/final.json` retain the underlying outcomes.

The verified panel had 54 training rounds, 20 accepted and 34 rejected candidates. Mean selected test accuracy was 84.44–86.39%, from an initial 46.11%, on overlapping synthetic numeric clusters. Nine matched self-use comparisons yielded one positive, one negative and seven ties. These are teaching-scale results, not LLM fine-tuning or a consistent recursive advantage. The tiny LoRA adapter has 16 parameters versus 15 in its base matrix; no parameter-efficiency claim is made. [Full table and interpretation](../docs/MULTILEVEL.md#what-the-learning-demo-actually-trains).

## Live model proposals with a request cap

Configure API access first. The example below assumes your account supports this exact model on Z.ai's Coding Plan endpoint; replace the external key-file path with your own:

```bash
python examples/demos/run.py ./live-results \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key --max-requests 60
```

Use the [onboarding guide](../docs/QUICKSTART.md) for other providers, exact model IDs and connection checks. Keys stay outside experiment workspaces; the ledger records requests and usage, not secrets. The cumulative request cap includes request starts that subsequently fail. Provider access is serialized even when candidate work runs concurrently. This is not a dollar cap; token bounds, provider pricing and unknown cost coverage still matter.

| Demo kind | What is exercised |
| --- | --- |
| `program` | An LLM improves a locally executed JSON record summarizer |
| `agent` | An LLM improves an executable workflow planner using a frozen proposer |
| `recursive` | The accepted planner also preprocesses training workflows for the next proposal |
| `skills` | An LLM creates reusable batch-edit guidance and an executable skill under a four-action task limit |
| `population` | Local candidate branches, validation-ranked top K and crossover through the normal kernel |
| `remote` | Optional authenticated HTTP evaluation with two localhost worker processes |

The first five kinds run by default. Select a subset with, for example, `--kinds program agent`, or use `--kinds remote` for HTTP evaluation. Use `--ledger /absolute/path/requests.jsonl` to share a cumulative cap across invocations; each output directory must still be new. The driver writes `plan.json`, request receipts, per-workspace lineage/HTML/final reports and `summary.json`. It freezes all successful searches before inspecting their final results, and keeps failed, unchanged and negative outcomes.

Program and agent evaluation runs local Python; their model calls produce improvement proposals. Skills also uses the LLM while completing tasks. These authored tasks are not equivalent benchmarks and must not be averaged into a single RSI score. A successful provider probe is evidence of access only. A validation gain remains provisional until the frozen final panel is complete.

## Two-process HTTP transport proof

```bash
python examples/remote_workers/demo.py --output ./http-proof
```

No model API is needed. Two independently started localhost worker processes evaluate the same initial program and write `transport-proof.json` with source/request/data/evaluator hashes and distinct process identities. This checks authenticated transport, not improvement. See the [worker guide](remote_workers/README.md) for the fixed wire protocol and ordinary-CLI integration. Multi-host deployment, distributed training and hardened candidate-code isolation are unverified.

## Coding task pack

```bash
python examples/coding_tasks/prepare.py --check
python examples/coding_tasks/prepare.py /tmp/coding.json
```

Twelve Python utility repairs use semantic unittest grading. Public tests give debugging feedback; private tests grade behavior. The check validates broken starters and reference solutions offline. The tasks are independently authored starter examples, not an externally validated benchmark. See the [coding guide](../docs/CODING_LAB.md) and [中文指南](../docs/CODING_LAB.zh-CN.md).

## Text-edit protocol fixtures

```bash
PYTHONPATH=src python examples/local_tasks/prepare.py /tmp/nanorsi-manifest.json
```

The 90 fixtures contain 30 tasks per train/validation/test split. Each task has input files and expected final files; source groups do not cross split boundaries. These deterministic fixtures check file-editing and experiment protocols. They do not establish general agent capability. For the older scripted whole-experiment demos, create `artifact-fixture` or `harness-fixture`; `model-contract` retains the schema-1 external-training contract.

## Compare matching final reports

```bash
PYTHONPATH=src python examples/compare.py report-a.json report-b.json
```

Reports must have schema 2, matching `comparison_hash`, mode, frozen conditions and task identities. Within each report, conditions must use matching task/repeat pairs; deployment repeat counts may differ between independent reports. Artifact/harness/model starters compare baseline/candidate; skills/coding also include no-skills. The score comparison averages deployments within a task and tasks within a run, then gives each independent evolution run equal weight. It reports paired percentage-point changes and per-arm summaries. For a loss primary metric, read the frozen report's direction and native-unit metric values rather than interpreting loss as a percentage score.

Repeated deployments are distinct from independent evolution runs. Duplicate `experiment_id`/`arm`/`seed` identities are rejected. Unknown monetary costs remain unknown; reports disclose known-cost coverage and per-case deployment timing. Matching task names alone is insufficient for pooling experiments.
