# v0.4.0 measured results

These are small, authored improvement experiments run on 2026-09-12 with implementation [50556ad](https://github.com/xxwtiancai/nanoRSI/commit/50556ada9e9f81245666f2a9d6bffc13e4740cdf). Live model demos and CPU parameter-learning trials answer different questions and are reported separately. No aggregate RSI score, broad benchmark result or general recursive-improvement claim is implied.

**Evidence status:** the original local journals passed HMAC and artifact-reference verification before export. Final metrics, decisions and CPU aggregates are rebuilt from those verified records. Provider request receipts, execution plans and HTTP transport probes are separately labelled unsigned observations and are outside that HMAC verification. The files here are **unsigned public extracts**, not independently signed journal replicas. Verification keys are not published. Source hashes support inspection of the extracted bytes; local HMAC verification does not provide third-party attestation, hostile-code containment or proof of empirical generality.

## Live model demonstrations

[Summary, run settings and provider usage](live/summary.json) record six completed runs, each with seed 0 and one frozen test repeat per condition. The requested model and all returned model IDs were `glm-5.3-flash`, using `https://api.z.ai/api/coding/paas/v4` with thinking disabled. The study used **43 API requests and 87,812 input/output tokens** under a 59-request cap. Separate setup connection probes are excluded. Monetary cost is unknown; a request cap is not a dollar cap.

Program and agent tasks execute local Python; the LLM supplies improvement proposals. Skills also invokes the LLM during task execution. Every run was frozen before its final test. The table reports actual passed cases, retaining the small denominator:

| Demo | Initial → selected final cases | Source snapshots | Search attempts |
| --- | --- | --- | --- |
| `program` | [1/4 → 4/4](live/program/final.json) | [sources.json](live/program/sources.json) | [All attempts](live/program/attempts/) |
| `agent` | [1/4 → 4/4](live/agent/final.json) | [sources.json](live/agent/sources.json) | [All attempts](live/agent/attempts/) |
| `recursive` | [1/4 → 4/4](live/recursive/final.json) | [sources.json](live/recursive/sources.json) | [All attempts](live/recursive/attempts/) |
| `skills` | [0/1 → 1/1](live/skills/final.json) | [sources.json](live/skills/sources.json) | [All attempts](live/skills/attempts/) |
| `population` | [1/4 → 4/4](live/population/final.json) | [sources.json](live/population/sources.json) | [All attempts](live/population/attempts/) |
| `remote` | [1/4 → 4/4](live/remote/final.json) | [sources.json](live/remote/sources.json) | [All attempts](live/remote/attempts/) |

`agent` is the frozen-proposer harness control; `recursive` is its self-use counterpart. Skills additionally has a no-skills condition, which scored **0/1**. These are separate tasks and experiment settings, not six replications of a single benchmark.

### What the mechanisms demonstrated

- **Recursive harness:** proposal traces show the selected `plan_steps` actually processed training workflows on the second attempt. Valid planning diagnostics rose from 1/4 in [attempt 1](live/recursive/attempts/001.json) to 4/4 in [attempt 2](live/recursive/attempts/002.json). The frozen control stayed at 1/4 in its [second proposal diagnostics](live/agent/attempts/002.json). Both selected agents nevertheless reached 4/4 on the final panel, so this run demonstrates recursive use without a downstream advantage over frozen proposing. The recursive second proposal was a retained no-op.
- **Executable skill:** the task deliberately requires editing six files within four actions, including final. The selected `edit/run.py` implements reusable batch replacement, and the final trace records `skill_script_invoked`. The 0/1 → 1/1 result shows this mechanism on one held-out batch migration; it is not broad skill transfer or a general agent benchmark. [Source](live/skills/sources.json), [final trace](live/skills/final.json), [search decisions](live/skills/observations.json).
- **Population:** four attempts evaluated three source candidates, retained two distinct branches, and kept an improve no-op. The [fourth attempt](live/population/attempts/004.json) used crossover context but was rejected for no validation gain; its score equalled its parent's. [Observations](live/population/observations.json) preserve both candidate-parent IDs. The Git commit has **one parent**; the second parent is semantic source input to the proposal, not a two-parent Git merge. This does not show population search outperforming a budget-matched serial control.
- **HTTP workers:** [worker identities](live/remote-workers.json) and [transport probes](live/remote-probes.json) record two separate localhost processes, PIDs 65400 and 65401, with matching source/data/evaluator identities. This demonstrates authenticated HTTP evaluation plumbing. It is not a multi-host test, distributed training or a hardened sandbox; processes share the host filesystem. Transport probes are not improvement scores.

## Known counterexample

**The selected remote program is not a fully correct amount parser, despite passing all four final cases.** Its [`parse_amount` source](live/remote/sources.json) mishandles accounting negatives without a currency symbol, for example `"(12.5)"`. The regex matches the parentheses alternative, but the implementation detects a negative by testing whether the optional currency-symbol group is present. With no symbol it selects the other alternative's absent numeric group and calls `.replace` on `None`, causing a runner error instead of parsing −12.5.

This failure is visible in retained search evidence, not hidden by the final score:

- [Remote attempt 1](live/remote/attempts/001.json), `gate.json`: `validation-accounting` has score 0 and status `runner_error`. The candidate was accepted at validation score 3/4, improving on the initial 1/4.
- [Remote attempt 2](live/remote/attempts/002.json), `train.json`: the accepted source again fails `train-accounting` with `runner_error`.
- The second candidate's `gate.json` scores 0/4. It was [rejected](live/remote/observations.json), leaving the first candidate selected for the final 4/4 panel.

Four held-out successes are evidence for those four cases, not complete coverage of the stated parsing contract. The published selected source and failed candidate remain the measured versions; the result has not been retroactively repaired. Broader cases and independent runs are needed before making broader correctness claims.

## CPU parameter learning

[The CPU summary](parameter-learning/summary.json) covers **18 runs**: SFT, REINFORCE and LoRA × seeds 0, 1 and 2 × frozen/self-use controls. Each run used 120 train, 120 validation and 120 test examples from overlapping synthetic numeric clusters, three training attempts and one frozen final repeat. The panel contains **54 real training rounds, 20 accepted and 34 rejected candidates**. It made no model API calls; monetary cost was not measured.

The model is a four-feature, three-class softmax classifier. SFT uses cross-entropy gradients; REINFORCE uses sampled actions and rewards; LoRA updates rank-two A/B factors with frozen base weights. The selected checkpoint is evaluated without final retraining. These are real parameter updates at teaching scale, not LLM fine-tuning. The tiny LoRA factors contain 16 parameters versus 15 in the base matrix, so no parameter-efficiency claim is made.

| Method | Initial test accuracy | Selected, frozen proposer | Selected, self-use proposer |
| --- | ---: | ---: | ---: |
| SFT | 46.11% | 85.83% | 85.83% |
| REINFORCE | 46.11% | 85.56% | 86.39% |
| LoRA | 46.11% | 85.00% | 84.44% |

Each cell averages three evolution seeds. Accuracy differences use percentage points; losses in the summary retain native cross-entropy units. The checkpoint-guided proposer weights difficult training-feedback examples more heavily; frozen/self-use changes which checkpoint computes that curriculum. Across nine matched method/seed pairs, self-use was better once, worse once and tied seven times. This panel supports learning on the synthetic task, not a consistent recursive advantage or statistical significance.

### Per-run CPU evidence

| Method | Seed | Proposer | Frozen final | Initial/selected checkpoints | Search attempts |
| --- | ---: | --- | --- | --- | --- |
| sft | 0 | frozen | [final.json](parameter-learning/sft-seed-0-frozen/final.json) | [sources.json](parameter-learning/sft-seed-0-frozen/sources.json) | [Attempts](parameter-learning/sft-seed-0-frozen/attempts/) |
| sft | 0 | self-use | [final.json](parameter-learning/sft-seed-0-self-use/final.json) | [sources.json](parameter-learning/sft-seed-0-self-use/sources.json) | [Attempts](parameter-learning/sft-seed-0-self-use/attempts/) |
| sft | 1 | frozen | [final.json](parameter-learning/sft-seed-1-frozen/final.json) | [sources.json](parameter-learning/sft-seed-1-frozen/sources.json) | [Attempts](parameter-learning/sft-seed-1-frozen/attempts/) |
| sft | 1 | self-use | [final.json](parameter-learning/sft-seed-1-self-use/final.json) | [sources.json](parameter-learning/sft-seed-1-self-use/sources.json) | [Attempts](parameter-learning/sft-seed-1-self-use/attempts/) |
| sft | 2 | frozen | [final.json](parameter-learning/sft-seed-2-frozen/final.json) | [sources.json](parameter-learning/sft-seed-2-frozen/sources.json) | [Attempts](parameter-learning/sft-seed-2-frozen/attempts/) |
| sft | 2 | self-use | [final.json](parameter-learning/sft-seed-2-self-use/final.json) | [sources.json](parameter-learning/sft-seed-2-self-use/sources.json) | [Attempts](parameter-learning/sft-seed-2-self-use/attempts/) |
| rl | 0 | frozen | [final.json](parameter-learning/rl-seed-0-frozen/final.json) | [sources.json](parameter-learning/rl-seed-0-frozen/sources.json) | [Attempts](parameter-learning/rl-seed-0-frozen/attempts/) |
| rl | 0 | self-use | [final.json](parameter-learning/rl-seed-0-self-use/final.json) | [sources.json](parameter-learning/rl-seed-0-self-use/sources.json) | [Attempts](parameter-learning/rl-seed-0-self-use/attempts/) |
| rl | 1 | frozen | [final.json](parameter-learning/rl-seed-1-frozen/final.json) | [sources.json](parameter-learning/rl-seed-1-frozen/sources.json) | [Attempts](parameter-learning/rl-seed-1-frozen/attempts/) |
| rl | 1 | self-use | [final.json](parameter-learning/rl-seed-1-self-use/final.json) | [sources.json](parameter-learning/rl-seed-1-self-use/sources.json) | [Attempts](parameter-learning/rl-seed-1-self-use/attempts/) |
| rl | 2 | frozen | [final.json](parameter-learning/rl-seed-2-frozen/final.json) | [sources.json](parameter-learning/rl-seed-2-frozen/sources.json) | [Attempts](parameter-learning/rl-seed-2-frozen/attempts/) |
| rl | 2 | self-use | [final.json](parameter-learning/rl-seed-2-self-use/final.json) | [sources.json](parameter-learning/rl-seed-2-self-use/sources.json) | [Attempts](parameter-learning/rl-seed-2-self-use/attempts/) |
| lora | 0 | frozen | [final.json](parameter-learning/lora-seed-0-frozen/final.json) | [sources.json](parameter-learning/lora-seed-0-frozen/sources.json) | [Attempts](parameter-learning/lora-seed-0-frozen/attempts/) |
| lora | 0 | self-use | [final.json](parameter-learning/lora-seed-0-self-use/final.json) | [sources.json](parameter-learning/lora-seed-0-self-use/sources.json) | [Attempts](parameter-learning/lora-seed-0-self-use/attempts/) |
| lora | 1 | frozen | [final.json](parameter-learning/lora-seed-1-frozen/final.json) | [sources.json](parameter-learning/lora-seed-1-frozen/sources.json) | [Attempts](parameter-learning/lora-seed-1-frozen/attempts/) |
| lora | 1 | self-use | [final.json](parameter-learning/lora-seed-1-self-use/final.json) | [sources.json](parameter-learning/lora-seed-1-self-use/sources.json) | [Attempts](parameter-learning/lora-seed-1-self-use/attempts/) |
| lora | 2 | frozen | [final.json](parameter-learning/lora-seed-2-frozen/final.json) | [sources.json](parameter-learning/lora-seed-2-frozen/sources.json) | [Attempts](parameter-learning/lora-seed-2-frozen/attempts/) |
| lora | 2 | self-use | [final.json](parameter-learning/lora-seed-2-self-use/final.json) | [sources.json](parameter-learning/lora-seed-2-self-use/sources.json) | [Attempts](parameter-learning/lora-seed-2-self-use/attempts/) |

## How to inspect these files

Each run directory contains:

| File | Contents |
| --- | --- |
| `final.json` | Frozen conditions, task/repeat outcomes, metrics, traces and checkpoint identities where applicable |
| `sources.json` | Baseline and selected source/checkpoint text, commit IDs and content hashes |
| `attempts/NNN.json` | Available train/validation results, proposal diff, hypothesis, usage and trace, candidate snapshot when created, and sanitized training method/data/checkpoint hash records |
| `observations.json` | Extracted baseline, acceptance, rejection, no-op and population decisions |
| `audit.json` | Local-verification status and artifact counts; explicitly marks the public extract as unsigned |

A no-op has no candidate snapshot because no new source commit was created. Rejected candidates and their results remain present. This is a curated evidence export, not a complete workspace or a replayable copy of the private HMAC journal. Inspect the failed cases and proposal traces alongside the final aggregate.

[Development history](development-history.json) also retains the earlier CPU panel's protocol failures: 48 attempts failed because generated diffs lacked a recognized file header. The old driver incorrectly labelled 16 affected runs completed when only their final evaluation completed. Both issues were fixed before this release study, then all predefined seeds and controls were rerun. These development results are separate from the measured `50556ad` panel above.

## Reproduce

From the repository with Python 3.11+, Git and nanoRSI installed:

```bash
python examples/parameter_learning/run.py ./new-parameter-results
python examples/demos/run.py ./new-live-results \
  --kinds program agent recursive skills population remote \
  --model glm-5.3-flash --base-url https://api.z.ai/api/coding/paas/v4 \
  --api-key-file /absolute/external/provider.key \
  --max-requests 59 --thinking disabled --seed 0
```

Use new output directories and your own external key file. [API onboarding](../../../docs/QUICKSTART.md) explains access and model configuration; [all demo commands](../../README.md) and the [multilevel guide](../../../docs/MULTILEVEL.md) explain the protocols. Live model outputs can differ on a new run; these measured scores are not guarantees.

## 中文说明

本目录公开六项真实模型演示和 18 次 CPU 参数学习的提取证据。真实模型研究共 43 次 API 请求、87,812 tokens，不包含单独的连接探针。原始本地日志在导出前通过 HMAC 与文件引用核验；这里是**未签名的公开提取**，不公开验证密钥，也不提供独立第三方认证。

各演示不是统一基准。递归规划器在第二轮提案中确实被复用，但 frozen 与 self-use 的最终成绩均为 4/4；CPU 递归对照为一正、一负、七平。Skills 刻意要求四个动作内批处理六个文件；HTTP 仅验证两个 localhost 进程；种群保留两分支并拒绝无收益交叉，第二父代是语义输入而非 Git 合并父提交。

远程示例的选中程序虽然最终 4/4，仍无法处理没有货币符号的括号负数 `"(12.5)"`。上面的 [Known counterexample](#known-counterexample) 链接保留了验证错误、后续训练错误及第二候选被拒绝的证据。小面板全对不等于完整实现正确，更不等于通用 RSI 已解决。
