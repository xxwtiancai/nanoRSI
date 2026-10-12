# HumanEval coding task pack (benchmark track)

[HumanEval](https://github.com/openai/human-eval) (MIT, [NOTICE](NOTICE); data vendored at
pinned commit 6d43fb980f9f) is the field's standard code-generation benchmark: 164 problems,
each a Python function specified by a prompt with a docstring (including `>>>` examples) and
verified by executing the upstream test block. This pack maps every problem onto the
**stock coding template** with zero custom evaluator code:

- the agent implements `solution.py` from the prompt (initial content: prompt + `pass`);
- the public test checks only that the entry point exists — preserving official
  prompt-only semantics, since HumanEval's examples already sit in the docstring;
- the upstream test block, wrapped in unittest with an explicit `check(candidate)` call,
  runs as the private grader (`python-unittest`, 10 s timeout);
- **reference solutions never enter the workspace**: `expected_files` carries a placeholder
  (grading executes tests and never compares contents), and the pack-level test asserts no
  canonical text appears in the manifest.

Three upstream problems are transparently excluded (HumanEval/32, /38, /50): their tests
reference helpers the problem never defines (`poly`, `encode_cyclic`, `encode_shift`), so
even the canonical solution cannot pass under any faithful wrapper — a recorded upstream
defect, not a silent drop. Offline validation: all 161 remaining canonical solutions pass
their wrapped tests and a `pass`-stub passes none (the wrapper initially looked 164/164
green until the missing `check()` call was caught — an empty test always passes; the
two-directional check is what makes it meaningful).

## Splits and study standard

Deterministic selection (sorted task_id, strided): **20 train / 25 validation / 36 test**
(≥30 test problems with ≥3 final-test repeats; no-skills is the primary comparison — the
standard adopted after the ALFWorld noise findings). `prepare.py --train/--validation/--test`
adjusts sizes; non-default values must be recorded in the study using them.

## Run it

```bash
python examples/humaneval_tasks/prepare.py /tmp/he-out
nanorsi new coding ./he-lab --goal "Improve the coding skills in target/agent/skills/ from failed-problem feedback. Propose unified diffs to skill files only."
cp /tmp/he-out/humaneval/manifest.json ./he-lab/tasks/manifest.json
cd he-lab
# set [evaluator] train_limit = 20 in nanorsi.toml, then:
git add -A && git commit -m "HumanEval pack"
nanorsi configure --workspace . --model YOUR_MODEL --base-url YOUR_URL \
  --api-key-file /absolute/external/path --thinking disabled --max-steps 3 --max-episodes 220
nanorsi doctor --workspace . --check-model
nanorsi baseline --workspace . && nanorsi run --workspace .
nanorsi freeze --workspace . --repeats 3
nanorsi final-test --workspace .     # 3 conditions x 36 problems x 3 repeats
nanorsi report --workspace . && nanorsi verify --workspace . && nanorsi audit --workspace .
```

## Honesty boundaries

Upstream author-reported pass@1 numbers are **not** reproduced (different models, sampling
and the official harness); these are independent nanoRSI runs on a deterministic subsample,
with the public-test deviation documented above. The workspace trust boundary applies as
usual: a workspace-local proposer can read `tasks/manifest.json` (prompts and wrapped tests,
never reference solutions). The 2026-10-12 live study:
[results/humaneval-coding](../results/humaneval-coding/README.md).
