# Does recursive checkpoint reuse add value?

[简体中文](README.zh-CN.md) · [Published v0.4.1 results and evidence](../results/recursive-digits-v0.4.1/README.md)

This optional numerical experiment compares **self-use minus frozen-proposer performance**, separately from ordinary initial-to-trained learning. It runs real SFT, sampled-reward REINFORCE and rank-four LoRA updates on handwritten digit images through nanoRSI's usual search, freeze and final-test commands. It is a linear classifier experiment, not pretrained LLM fine-tuning or a general RSI claim.

## Measured results

The confirmation study on implementation `7809e7924bf806272b721fb829ef689db0263718` completed all **120 runs and 720 training rounds**: 676 candidates were accepted and 44 rejected, with no failed attempts. All runs froze before testing and matched their planned actual updates, samples and scoring work. All-measured and complete-case results therefore coincide.

| Method | Frozen | Self-use | Uniform | Random | Self-use − frozen | Positive seeds |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SFT | 89.835% | 93.489% | 92.582% | 92.390% | +3.654 pp | 10/10 |
| REINFORCE | 19.286% | 27.473% | 36.236% | 27.005% | +8.187 pp | 9/10 |
| LoRA | 79.533% | 82.060% | 82.885% | 83.736% | +2.527 pp | 8/10 |

These are mean final-test accuracies of selected checkpoints. The nominal primary Bonferroni-adjusted 98.333% bootstrap intervals for self-use minus frozen are SFT **[2.198, 5.192] pp**, REINFORCE **[1.071, 13.462] pp**, and LoRA **[0.549, 4.423] pp**. Only REINFORCE met the predeclared observed-mean ≥5 pp target with a positive adjusted lower bound; SFT and LoRA did not. This does not establish a true gain ≥5 pp. REINFORCE still lost to uniform by 8.764 pp. LoRA was 0.824 pp below uniform, with its descriptive 95% interval including zero. SFT exceeded uniform by 0.907 pp and random by 1.099 pp; these are secondary, descriptive comparisons.

SFT's mean test error fell from 10.16% to 6.51% relative to frozen priorities: **35.95% relative error reduction**, equivalent to **+3.65 pp accuracy**. This measured effect applies to the fixed data split and training setup below. [The results bundle](../results/recursive-digits-v0.4.1/README.md) includes every comparison, interval and evidence file.

## Reproduce

Python 3.11+, Git, nanoRSI and an existing NumPy installation are required for this optional adapter. The nanoRSI package/core still has no third-party runtime dependencies. No model API key, GPU, new dataset download or scikit-learn installation is needed; the attributed 57KB data file is included.

Check the Python environment you will use for the study:

```bash
python -c "import sys, numpy, nanorsi; print(sys.version); print(numpy.__version__)"
```

If NumPy is missing, install it only in that optional experiment environment; this version matches the published run:

```bash
python -m pip install numpy==2.3.3
```

```bash
# From the repository, with nanoRSI and NumPy available in this interpreter:
python examples/recursive_learning/run.py ./digits-study --phase search --workers 2
# Every planned run must now be frozen; this step is the first test-set use:
python examples/recursive_learning/run.py ./digits-study --phase final --workers 2
```

The default panel is **three methods × ten initialization/training seeds (10–19) × four policies = 120 runs**. Output directories must be new for search. `--phase final` reads the saved plan rather than silently starting a new study. `--phase all` runs the same two stages in order. Run these commands from a repository checkout, with the `python` and `nanorsi` commands using the same Python 3.11+ environment. The published run used Python 3.13 and NumPy 2.3.3; the saved plan records its exact implementation and settings. Each run retains its normal workspace and verified journal, while `summary.json` contains the panel results.

To create one inspectable workspace:

```bash
python examples/recursive_learning/prepare.py ./digits-lab --method sft --policy self-use --seed 10
nanorsi run --workspace ./digits-lab
nanorsi freeze --workspace ./digits-lab --repeats 1
nanorsi final-test --workspace ./digits-lab
nanorsi report --workspace ./digits-lab --format html
nanorsi verify --workspace ./digits-lab
```

A single workspace is a mechanism demonstration, not evidence of additional recursive benefit. Use matched full-panel controls for that question.

## Intervention and controls

Every policy scores the same 1,074 TRAIN examples each round. The prioritized curriculum upweights the highest-loss quarter using the assigned proposer checkpoint. SFT preserves each class's empirical sampling mass; RL and LoRA use the documented global-priority variant selected during validation-only development.

| Policy | Which checkpoint scores TRAIN data? | How samples are selected |
| --- | --- | --- |
| frozen | Initial checkpoint on every round | Priorities fixed to that checkpoint |
| self-use | Latest accepted checkpoint | Priorities recomputed after accepted learning |
| uniform | Latest accepted checkpoint, scores deliberately unused | Uniform sampling |
| random | Latest accepted checkpoint, scores deliberately unused | Randomly refreshed focus with matched size/concentration |

All policies continue training their own latest accepted checkpoint. They share initialization, round count, batch size, per-attempt RNG schedule, TRAIN/validation data, forward-scoring panels and validation opportunities within each method. Uniform/random have an explicit sampling-policy difference, recorded separately from the generic recursive/frozen comparison identity. Priority ranking overhead and process wall time are not claimed identical.

Each candidate is selected by **validation cross entropy**, with accuracy retained as a secondary metric. Attempt-specific random seeds prevent a rejected candidate from being replayed identically on the next attempt. Actual attempted updates, samples, scoring work, failed attempts and retained checkpoint steps are reported separately; rejection can make retained training steps unequal.

| Method | Rounds | Updates per round | Batch size | Learning rate | Priority multiplier | Class mass preserved |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| SFT | 6 | 24 | 32 | 0.3 | 9 | yes |
| REINFORCE | 6 | 8 | 32 | 0.3 | 3 | no |
| LoRA | 6 | 24 | 32 | 0.3 | 3 | no |

The effective matrix is `W + A @ B`, with shapes 65×10, 65×4 and 4×10. SFT/RL update W; LoRA freezes W and updates A/B. The RL gradient uses sampled actions and scalar rewards. Its curriculum still uses labeled TRAIN losses; it is not a fully label-free RL setting.

## Selection, held-out data and uncertainty

The data are the 1,797-image UCI/scikit-learn optical-digits subset. A fixed stratified row split (seed 20260912) contains **1,074 train, 359 validation and 364 test images**, with no duplicate images or shared source-row IDs. This is a new split of the original UCI test subset, **not the official UCI benchmark split**. Writer IDs are unavailable, so unseen-writer generalization is not established. See [data attribution and licensing](data/README.md).

Two validation-only pilot families used development initialization seeds 0, 1 and 2: 24 global-priority configurations followed by the same 24 configurations with class-mass normalization. [All 48 configurations and 576 policy/seed trial rows](pilots/README.md) are retained with source and CSV evidence. Strong global priorities often weakened the frozen control relative to uniform sampling; settings were not selected merely for a large recursive/frozen difference. The selected settings also matched or exceeded uniform/random mean validation accuracy. None of those development runs evaluated the confirmation test panel.

The confirmation settings and seeds are locked before testing. All 120 workspaces must pass the global freeze barrier before any final-test call. Per-method paired differences use the same frozen task panel. Descriptive 95% bootstrap intervals quantify variation across training seeds; the default three primary comparisons also use nominal Bonferroni-adjusted intervals for the predeclared target (observed mean at least +5 percentage points, positive adjusted lower bound, and complete matched-budget evidence). The paired percentile bootstrap uses 10,000 resamples and does not provide an exact finite-sample familywise error guarantee. Missing or failed attempts remain visible and prevent an unqualified matched-update success claim. These intervals do not measure uncertainty across new datasets or writers.

Checkpoint-based reweighting relates to established [online batch selection](https://arxiv.org/abs/1511.06343) and [prioritized replay](https://arxiv.org/abs/1511.05952). This example independently implements a simple curriculum mechanism to test recursive reuse; it does not reproduce those papers' systems or borrow their reported gains.

## Feedback size and accounting

`[evaluator].train_limit` controls the TRAIN feedback panel and defaults to four for existing starters. This study sets it to the full TRAIN split. It does not change which rows the trainer receives. The full search allowance is `V + attempts × (min(train_limit, T) + 2V)`, where T/V are TRAIN/validation row counts. Final-test episodes are separate. The training command has its own time/output limits; episodes alone do not count gradient updates or compute.

The published panel consumed 13,440 updates and 430,080 sampled examples, while selected checkpoints retained 13,072 updates. REINFORCE attempted 48 updates per run in both frozen and self-use but retained 24.0 versus 47.2 on average. The effect includes curriculum choice and validation-based acceptance, rather than comparing equal retained training depth. Rejected work stays in the actual budget. The public extract comes from verified local journals but is itself unsigned and includes neither HMAC keys nor full workspaces; its hashes support internal integrity checks, not independent authentication of the original execution. See [evidence limits](../results/recursive-digits-v0.4.1/README.md#inspectable-evidence).
