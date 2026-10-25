# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 17 ledger events

**Judged (n=1): base 0.652 → final 0.522 partial, -13.0 pp, 0W/0T/1L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| employment-labor/identify-issues-in-counterparty-motion-brief | 2 | 2 / 0 / 0 | adopt_dom | agg1 | 0.652 | 0.522 |

Budget used: 4 rollouts · 7 improver calls · 5,453,324 input / 337,139 output tokens

## Lessons in the library

- **employment-labor/identify-issues-in-counterparty-motion-brief**: Read every input document in full with the native read tool (re-reading in chunks if truncated) and independently recompute numeric tests from raw exhibits instead of trusting party characterizations
