# Contributing

## Ground rules

1. Run tests before every commit.
2. Keep the core standard-library-only.
3. Keep the nano budget enforced by `tests/test_architecture.py`.
4. Add a failing test before changing runtime behavior.
5. Update `docs/specification.md` when adding or changing a state, module, or invariant.
6. Do not add databases, services, dashboards, schedulers, plugin loaders, vendor adapters, or distributed execution to v0.1 core.

## Local verification

```bash
python -m unittest discover -v
python -m pip install -e .
```

Use Python 3.11 or newer. Git is required.

## Commit style

Explain why a change is needed in the subject, preserve decision context in the body, and include verification evidence.
