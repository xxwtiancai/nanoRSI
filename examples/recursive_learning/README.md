# Does recursive checkpoint reuse add value?

This optional numerical experiment compares **self-use minus frozen-proposer performance**, separately from ordinary initial-to-trained learning. It runs real SFT, sampled-reward REINFORCE and rank-four LoRA updates on handwritten digit images through nanoRSI's usual search, freeze and final-test commands. It is a linear classifier experiment, not pretrained LLM fine-tuning or a general RSI claim.

Python 3.11+, Git, nanoRSI and an existing NumPy installation are required for this optional adapter. The nanoRSI package/core still has no third-party runtime dependencies. No model API key, GPU, new dataset download or scikit-learn installation is needed; the attributed 57KB data file is included.

```bash
# From the repository, with nanoRSI and NumPy available in this interpreter:
python examples/recursive_learning/run.py ./digits-study --phase search --workers 2
# Every planned run must now be frozen; this step is the first test-set use:
python examples/recursive_learning/run.py ./digits-study --phase final --workers 2
```

The default panel is **three methods × ten initialization/training seeds (10–19) × four policies = 120 runs**. Output directories must be new for search. `--phase final` reads the saved plan rather than silently starting a new study. `--phase all` runs the same two stages in order.

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

Two validation-only pilot families used development initialization seeds 0, 1 and 2: 24 global-priority configurations followed by the same 24 configurations with class-mass normalization. All pilot outcomes are retained. Strong global priorities often weakened the frozen control relative to uniform sampling; settings were not selected merely for a large recursive/frozen difference. The selected settings also matched or exceeded uniform/random mean validation accuracy. None of those development runs evaluated the confirmation test panel.

The confirmation settings and seeds are locked before testing. All 120 workspaces must pass the global freeze barrier before any final-test call. Per-method paired differences use the same frozen task panel. Descriptive 95% bootstrap intervals quantify variation across training seeds; the default three primary comparisons also use a Bonferroni-adjusted family interval for the predeclared target (at least +5 percentage points, positive adjusted lower bound, and complete matched-budget evidence). Missing or failed attempts remain visible and prevent an unqualified matched-update success claim. These intervals do not measure uncertainty across new datasets or writers.

Checkpoint-based reweighting relates to established [online batch selection](https://arxiv.org/abs/1511.06343) and [prioritized replay](https://arxiv.org/abs/1511.05952). This example independently implements a simple curriculum mechanism to test recursive reuse; it does not reproduce those papers' systems or borrow their reported gains.

## Feedback size and accounting

`[evaluator].train_limit` controls the TRAIN feedback panel and defaults to four for existing starters. This study sets it to the full TRAIN split. It does not change which rows the trainer receives. The full search allowance is `V + attempts × (min(train_limit, T) + 2V)`, where T/V are TRAIN/validation row counts. Final-test episodes are separate. The training command has its own time/output limits; episodes alone do not count gradient updates or compute.
