# Multi-seed orchestration (selector-study prerequisite)

`run.py` runs one assembled, **not-yet-baselined** workspace template across a seed list
through the ordinary CLI lifecycle — per seed it copies the template, patches
`[experiment] seed`, and executes baseline → run → freeze `--repeats R` → final-test →
report → verify, then aggregates per-seed decisions and cross-seed condition statistics
(mean/spread over every seed × repeat draw) into `summary.json`. This is the
[selector-study protocol](../../docs/SELECTOR_STUDY_PROTOCOL.md) multi-seed requirement:
every seed is an independent frozen workspace, because the frozen protocol is immutable
per workspace (raising repeats or changing seeds after freeze is refused by design).

```bash
# 1. assemble a template: task pack in, model configured, budgets set — but do NOT baseline
python examples/multiseed/run.py ./my-template ./my-study --seeds 0,1,2 --repeats 3
```

Model-agnostic: offline fixture templates run with zero API cost (that is how
`tests/test_multiseed.py` validates the full lifecycle); live templates run exactly what
they are configured with, and `summary.json` records total model calls. The template is
never modified; each `seed-N/` workspace keeps its complete journal for the evidence
ledger, and existing seed directories are never overwritten.

Known boundary: the script does not schedule or parallelize — seeds run serially, which
matches the platform's own serialization discipline for workspaces on one machine.
