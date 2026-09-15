# Live skills study: frozen vs self-use arms (2026-09-16)

A small live-model study closing the comparison half of [ADOPTION item 7](../../../../docs/research/industry-rsi/ADOPTION.md) — *persistent skill evidence*: do evolved skills transfer to unseen tasks, and does self-use of accepted revisions add anything over a frozen proposer?

**Headline: evolved skills transferred to unseen tasks (0/3 → 2/3 on the frozen test panel in both arms). Self-use showed no advantage over the frozen proposer** — identical final panels; the self-use arm accepted a smaller validation gain and proposed no further changes. A tie is the honest result; it agrees with the v0.4.0 live study and does not generalize the v0.4.1 digits finding.

## Setup

Two independent skills workspaces (`arm = "frozen"`, `arm = "self-use"`), seed 0, **GLM-5.3-Flash** via the Z.ai coding-plan endpoint, thinking disabled, at most 3 attempts and 40 search episodes each, then frozen and tested once on the test split with three conditions (baseline / no-skills / candidate). Both arms share one deterministic 8-task manifest (`manifest.json`): rewrite `Name : value` inventory files into a "standard format" whose exact convention differs per variant — preserve order, deduplicate keys, or sort — so the rules are learnable from training feedback but not guessable from the instruction alone.

## Search outcomes

| Arm | Attempt 1 | Attempt 2 | Attempt 3 | Validation after search |
| --- | --- | --- | --- | ---: |
| frozen | accepted (0 → 0.667) | no-op | rejected (tie, 0.667) | 0.667 |
| self-use | accepted (0 → 0.333) | no-op | no-op | 0.333 |

Failed, no-op and tie-rejected attempts all consumed budget and are retained in each arm's `evidence.jsonl` (one record per revision: hypothesis, full diff, redacted per-case evidence, decision, integrity flags).

## Frozen final panels (1 repeat, 3 test tasks)

| Condition | frozen arm | self-use arm |
| --- | ---: | ---: |
| baseline (initial skills) | 0/3 | 0/3 |
| no-skills | 0/3 | 0/3 |
| candidate (selected skills) | **2/3** | **2/3** |

Both arms solved the preserve and dedupe test tasks; **both failed the sort task (`norm-sort-2`) in every condition** — the accepted skills encode preserve/dedupe rules only. This known counterexample is retained.

## What the skills actually learned

The accepted edits encode general rules inferred from training feedback, not task data — e.g. *"one `key=value` line per record… keys lowercased… if the same key appears more than once, keep only the first occurrence"*. The fresh-session audit (`audit.json` per arm) found **zero expected-answer leakage, zero silent-bypass scripts and zero declared-but-unloaded skills** in both arms.

## Budget

190 model calls total: frozen 108 (70,558 in / 5,587 out tokens), self-use 82 (57,456 in / 4,814 out). `cost_usd` is null — the provider returns no cost field; episode limits are not a dollar cap.

## Limits

One seed, one final repeat, three tiny authored tasks per panel, one flash-tier model, panel size three. This is not a significance claim, not a benchmark, and not evidence about self-use in general; the [v0.4.1 digits study](../recursive-digits-v0.4.1/README.md) (120 runs, 10 seeds, four controls) remains the reference for the recursive-reuse question on the parameter surface.

Files: [summary.json](summary.json) · [manifest.json](manifest.json) · per arm: [frozen/final.json](frozen/final.json) · [frozen/evidence.jsonl](frozen/evidence.jsonl) · [frozen/audit.json](frozen/audit.json) · [selfuse/final.json](selfuse/final.json) · [selfuse/evidence.jsonl](selfuse/evidence.jsonl) · [selfuse/audit.json](selfuse/audit.json)
