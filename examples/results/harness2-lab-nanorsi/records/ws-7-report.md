# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 17 ledger events

**Judged (n=1): base 0.902 → final 0.951 partial, +4.9 pp, 1W/0T/0L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| emerging-companies-venture-capital/extract-key-terms-from-cap-table | 2 | 1 / 1 / 0 | adopt_inv | agg1 | 0.902 | 0.951 |

Budget used: 4 rollouts · 7 improver calls · 7,548,424 input / 368,073 output tokens

## Lessons in the library

- **emerging-companies-venture-capital/extract-key-terms-from-cap-table**: Run --help (or skim the header) before the first real call; if a first call fails, diagnose and retry once with a changed flag (e.g., sandbox vs. in-process mode) rather than abandoning the script or repeating the same call
