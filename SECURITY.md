# Security Policy

## Threat model

nanoRSI executes proposer, evaluator, target, and model-training commands supplied by an experiment. Treat their output and patches as untrusted.

## Required boundaries

- Use argv commands only; nanoRSI does not intentionally invoke a shell.
- Run untrusted commands in a container, VM, or equivalent sandbox.
- Keep evaluator answers and heldout data private to the evaluator process.
- Do not expose `lineage.jsonl`, `.nanorsi/lineage.key`, or accepted refs to candidate code.
- Review every proposal before enabling any unattended workflow.

## Built-in protections

- mutable-surface deny checks;
- relative-path and traversal rejection;
- exact detached Git worktree evaluation;
- evaluator fingerprint comparison;
- command timeouts;
- filtered subprocess environment;
- per-experiment lock;
- HMAC-protected append-only lineage;
- explicit stale-state recovery.

## Reporting a vulnerability

Please open a private GitHub security advisory rather than filing a public issue. Include the affected version, commands, configuration with secrets removed, and a minimal reproduction.
