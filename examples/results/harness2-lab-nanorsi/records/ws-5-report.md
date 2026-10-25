# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 17 ledger events

**Judged (n=1): base 0.829 → final 0.857 partial, +2.9 pp, 1W/0T/0L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| trusts-estates-private-client/draft-consent-to-adoption | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.829 | 0.857 |

Budget used: 4 rollouts · 9 improver calls · 5,709,858 input / 217,356 output tokens

## Lessons in the library

- **trusts-estates-private-client/draft-consent-to-adoption**: Before drafting, build a fact inventory with pinpoint citations per fact and map the governing statute's formalities (e.g., revocation windows) so the instrument neither fabricates unsourced facts nor waives statutory rights like revocability; surfaced guidance alone is insufficient without this discipline
