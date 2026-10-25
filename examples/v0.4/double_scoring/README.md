# Offline double-scoring (selector-study false-block accounting)

`run.py` measures what a control gate would have decided, so selector arms can report the
false-block / false-admit accounting the [selector-study protocol](../../docs/SELECTOR_STUDY_PROTOCOL.md)
requires. Two modes:

- **Recompute (default, zero cost)** — replays the pure gate decision under a control
  `GateConfig` (strict minimum, no noise band) from the journal's own parent/child metrics.
  Classifies every measured attempt as `agree`, `false_block` (selector rejected, control
  would accept) or `false_admit`. Works on any completed workspace.
- **Re-evaluate (`--evaluate-blocked`)** — for attempts whose proposal produced a diff but
  never reached measurement (pre-evaluation selectors such as the item-39 judge pre-rank),
  applies the archived proposal diff to a fresh worktree of the parent program (resolved
  via the `nanorsi/gen-N` tag chain) and runs the frozen evaluator on the validation
  panel. Offline fixtures cost nothing; live workspaces pay measurement-only episode
  costs outside the search budget.

```bash
python examples/double_scoring/run.py ./my-workspace                     # recompute
python examples/double_scoring/run.py ./my-workspace --out report.json   # write report
python examples/double_scoring/run.py ./my-workspace --evaluate-blocked  # for pre-eval selectors
```

The script never modifies the workspace journal; re-evaluation panel outputs land under
`.nanorsi/double-score-*.json`. Accounting, not selection. Validation:
`tests/test_double_scoring.py` covers strict-gate agreement, a noise-band workspace where
all three band-rejections are counted as false blocks against the control, and
reconstruction of a metric-stripped attempt from its archived diff.
