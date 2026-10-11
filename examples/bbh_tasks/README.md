# BBH program-evolution task packs (benchmark track, phase 1)

[ADOPTION item 37](../../docs/research/industry-rsi/ADOPTION.md), phase 1: move effect
evidence from self-authored panels onto public benchmark tasks. This pack ports two
tasks from [BIG-Bench-Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) (MIT; data
vendored verbatim under `data/` with a pinned commit — see [NOTICE](NOTICE)):

| Pack | BBH task | Initial solver (authored, deliberately weak) | Offline baseline (validation / test) |
| --- | --- | --- | ---: |
| `dyck` | `dyck_languages` (250 examples) | counts unmatched opens per bracket type, closes in a fixed type order — nesting order ignored | 0.78 / 0.693 |
| `bool` | `boolean_expressions` (250 examples) | left-to-right fold with recursive parentheses — operator precedence ignored | 0.90 / 0.733 |

Both initial solvers are principled naive heuristics with genuine partial credit, not
straw men, and both tasks are solvable to 1.0 by a classical algorithm (stack matching;
precedence-aware evaluation) — asserted by `tests/test_bbh_tasks.py`, which also checks
manifest determinism, split hygiene and an example-specific hardcoding screen.

## Layout

`prepare.py` is the sole generator; manifests are always regenerated, never hand-edited.
Examples are sorted by input text and split deterministically: 50 train / 50 validation /
150 test. Each example is one program-mode task (`records.json` on stdin, `summary.json`
on stdout, exact-match grading) so the **stock program evaluator runs unmodified** —
no custom scoring code, no RNG, fully offline.

## Run it

```bash
python examples/bbh_tasks/prepare.py /tmp/bbh-out          # deterministic packs
nanorsi new program ./bbh-dyck-lab --goal "Improve the bracket-completion solver in target/program.py. Propose unified diffs; keep the stdin/stdout contract fixed."
cp /tmp/bbh-out/dyck/tasks/manifest.json ./bbh-dyck-lab/tasks/manifest.json
cp /tmp/bbh-out/dyck/target/program.py  ./bbh-dyck-lab/target/program.py
cd bbh-dyck-lab && git add -A && git commit -m "swap in BBH dyck pack"
nanorsi configure --workspace . --model YOUR_MODEL --base-url YOUR_URL \
  --api-key-file /absolute/external/path --max-steps 5 --max-episodes 40
nanorsi doctor --workspace . --check-model
nanorsi baseline --workspace .      # 0.78 validation for dyck (offline)
nanorsi run --workspace .           # gated search, live model
nanorsi freeze --workspace . --repeats 1
nanorsi final-test --workspace .    # 150-example frozen panel (offline)
nanorsi report --workspace . && nanorsi verify --workspace . && nanorsi audit --workspace .
```

Swap `bool` for the second pack. Configure must precede baseline; task files must be
swapped in before baseline so the experiment journal records them.

## Honesty boundaries

The initial solvers are authored by nanoRSI (BBH ships data, not programs); upstream
author-reported BBH numbers are **not** reproduced here — these are independent nanoRSI
runs of the tasks. Answers are short strings, below the audit tool's 8-character leakage
threshold, so the leakage screen for this pack is the generator + hardcoding test, and
the known workspace trust boundary (a workspace-local proposer can read
`tasks/manifest.json`) applies. The 2026-10-11 live study and its limits:
[results/bbh-phase1](../results/bbh-phase1/README.md).
