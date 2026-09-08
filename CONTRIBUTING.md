# Contributing

## Ground rules

1. Run tests before every commit.
2. Keep the core standard-library-only.
3. Keep the nano budget enforced by `tests/test_architecture.py`.
4. Add a failing test before changing runtime behavior.
5. Update `docs/specification.md` when adding or changing a state, module, or invariant.
6. Do not add databases, services, dashboards, schedulers, plugin loaders, vendor adapters, or distributed execution to the core. Model bridges belong to examples/templates.
7. Keep train feedback, validation selection and final testing separate. Mocked tests must not be presented as measured model improvements.

## Local verification

```bash
PYTHONPATH=src python -m unittest discover -v
python -m pip install -e .
python -m compileall -q src examples tests
git diff --check
```

Use Python 3.11 or newer. Git is required.

## Commit style

Explain why a change is needed in the subject, preserve decision context in the body, and include verification evidence.

Use Git-native Lore trailers where they add value: `Constraint:`, `Rejected:`, `Tested:`, `Not-tested:`, `Scope-risk:` and `Directive:`. Keep commits focused. Parallel contributors must own separate files and preserve each other's changes; integration and review belong to the coordinating maintainer.
