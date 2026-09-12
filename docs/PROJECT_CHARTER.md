# nanoRSI Charter

nanoRSI is a minimal, hackable lab for improving agent skills and harnesses under a fixed model and a measurable budget.

## Goal

Make one complete experiment easy to read, run and inspect: execute Python repair or text-edit training tasks, learn from their outcomes, propose a bounded skill patch, compare parent and candidate on validation tasks, retain the better version, freeze choices and evaluate unseen tasks.

The primary audience is developers studying or improving their own agents. Success means a correct, traceable experiment; a negative or inconclusive empirical result is valid.

## Three separate questions

1. Do skills help a fixed agent? Compare no-skills and initial-skills conditions.
2. Do evolved skills improve unseen tasks? Compare frozen initial and selected versions, with search and deployment costs disclosed.
3. Does recursive reuse contribute? Compare frozen and self-use proposer harnesses under matching task/model/budget conditions.

The implementation provides these protocols. Mocked tests do not establish live model performance or prove recursive improvement.

## Scope

- One accepted parent and one candidate at a time.
- Plain skill files, a small reference task/propose Runner and an external model bridge.
- An independently authored Python coding starter with public test feedback, private behavioral grading and descriptive HTML/Markdown reports.
- Exact Git snapshots, protected evaluation/configuration, explicit patch decisions and JSONL evidence.
- Train/validation/final-test separation; finite attempts, episodes, time and output.
- A standard-library core of at most 2,500 lines.

## Non-goals

Populations or islands, distributed evaluation, plugin registries, hosted services, hosted dashboards, marketplaces, weight training, background daemons, and universal Agent compatibility are outside this version. A hardened sandbox is an external execution concern, not something claimed by local worktrees.

Legacy artifact/harness demos and the external model-training contract remain compatible examples. They do not compete with the skills-first development focus.

## Rules

Candidates cannot change experiment scoring or model settings. Test results never influence promotion. Failed/no-op attempts and unknown costs are retained. Skills must be useful procedural artifacts rather than benchmark answers. Live claims require real experiments, versioned tasks and matching comparison budgets.
