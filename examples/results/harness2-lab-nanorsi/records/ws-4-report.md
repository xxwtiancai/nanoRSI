# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 17 ledger events

**Judged (n=1): base 0.971 → final 0.824 partial, -14.7 pp, 0W/0T/1L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| litigation-dispute-resolution/analyze-counterparty-motion-to-dismiss | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.971 | 0.824 |

Budget used: 4 rollouts · 8 improver calls · 7,521,054 input / 332,089 output tokens

## Lessons in the library

- **litigation-dispute-resolution/analyze-counterparty-motion-to-dismiss**: Invest in record-verification guardrails (verbatim-quote appendices, pin-cites, citation flags) rather than broader analysis, because output quality differentiates on citation integrity, not issue discovery
