# Security and evaluation integrity

## Default trust model

nanoRSI's built-in execution is trusted local subprocess execution. Git worktrees separate candidate versions; they do not restrict what same-user Python processes can read. Local HMAC receipts detect accidental or unauthorized journal changes only while the receipt key remains outside an attacker's access.

The reference skills Runner exposes only list/read/write/final actions inside an episode directory, rejects escaping paths and symlinks, and does not offer shell execution. This limits actions exposed by that reference implementation. It is not an OS sandbox for an arbitrary replacement Runner, proposer, bridge or evaluator.

## Built-in controls

- Mutation allowlists and protected evaluator/proposer/adapter/task/config paths.
- Exact candidate commits, fixed evaluation fingerprints and hashed artifacts.
- Explicit model settings and optional external credential file.
- Filtered argv subprocess environments, finite timeouts and bounded captured output.
- POSIX process-group termination for timeouts and output overflow.
- Per-workspace lock, interrupted-attempt accounting and recovery.
- Train-only proposal feedback and frozen final-test selection boundary.

Do not place credentials inside tracked workspaces, skill files, model messages or test data. The reference adapter reads an explicitly configured external file and does not include the key in messages. Custom bridges must preserve that property. Unknown usage is not evidence of zero cost.

## Genuine private-label evaluation

For untrusted model-generated executable harness code or a claim of hidden-label isolation, use an external container/VM/service:

1. Keep the grader, test answers and receipt key in the evaluator trust domain.
2. Give the candidate an exported snapshot and only the current public task input.
3. Do not mount the full Git directory, experiment outputs, host home directory or credential store.
4. Apply filesystem, network, CPU/memory and model-service limits outside the candidate process.
5. Test an actively probing candidate against evaluator files, Git history and keys.

No hardened isolation adapter is bundled or certified in this version. Moving labels to another same-user directory, omitting labels from stdout, or setting a file to mode 0600 is insufficient.

## Operational limits

Freezing prevents automated search from consuming final-test outcomes; it cannot stop a human from reading a public test set and designing a new experiment around it. Cloud model aliases and external endpoints can drift despite frozen configuration. Record model snapshots when available and disclose uncertainty.

If an operation dies, `recover` reconciles local attempt/worktree state. It is not a remote-job supervisor and cannot guarantee cleanup after host failure. Incomplete final panels are identified explicitly; do not silently retry until a favorable score appears.

## Reporting

Please use a private GitHub security advisory for vulnerabilities. Include version, sanitized configuration and a minimal reproduction; do not publish credentials or private benchmark answers.
