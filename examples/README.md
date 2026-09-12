# Harness experiment fixtures

This directory contains a small, deterministic lab for checking the skills and
harness protocol. The local task manifest is made of 90 text-file inspection
and constrained-edit fixtures: 30 each in `train`, `validation`, and `test`.
Each task includes its input files and the exact expected final files. Source
groups stay within one split so a source fixture cannot cross a split boundary.

The fixtures are protocol checks, not benchmark results. They do not execute
programs, install dependencies, or claim general agent capability.

Generate the manifest at a chosen path:

```bash
PYTHONPATH=src python examples/local_tasks/prepare.py /tmp/nanorsi-manifest.json
```

Each final experiment report must use schema version 2 and contain a non-empty
`comparison_hash` for the frozen task content, evaluator, inference
configuration, and initial target snapshot. Reports must contain baseline,
no-skills, and candidate result records with matching task/repeat pairs. The
comparison script validates those pairs, averages repeats within each task,
then gives each independent report equal weight. It reports percentage-point
deltas per report, per arm, and in a clearly labelled descriptive overall
summary. Unknown costs remain unknown while the summary reports known-cost
coverage; timing summaries use per-case deployment durations.

```bash
PYTHONPATH=src python examples/compare.py report-a.json report-b.json
```

Repeated deployments inside one report are summarized separately from
independent experiment identity. Reports with the same
`experiment_id`/`arm`/`seed` triple are rejected as duplicates.

## Executable coding tasks

The coding starter adds twelve Python utility repairs with semantic unittest grading. Validate broken starters and reference solutions without a model using `python examples/coding_tasks/prepare.py --check`, or export a manifest with `python examples/coding_tasks/prepare.py /tmp/coding.json`. These are authored starter tasks, not externally validated benchmark results. See the [coding lab guide](../docs/CODING_LAB.md) and [Chinese guide](../docs/CODING_LAB.zh-CN.md).
