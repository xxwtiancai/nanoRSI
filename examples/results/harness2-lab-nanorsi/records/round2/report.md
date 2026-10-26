# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 233 ledger events

**Judged (n=8): base 0.862 → final 0.850 partial, -1.2 pp, 4W/1T/3L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| employment-labor/identify-issues-in-counterparty-motion-brief | 2 | 2 / 2 / 0 | adopt_dom | agg1r2 | 0.696 | 0.565 |
| bankruptcy-restructuring/identify-issues-in-counterparty-sale-objection | 2 | 2 / 2 / 0 | adopt_inv | agg1r2 | 0.893 | 0.929 |
| capital-markets/review-form-8 | 2 | 2 / 2 / 0 | adopt_inv | agg1r2 | 0.906 | 0.969 |
| emerging-companies-venture-capital/extract-key-terms-from-cap-table | 2 | 4 / 0 / 0 | adopt_dom | agg1r2 | 0.927 | 0.829 |
| litigation-dispute-resolution/analyze-counterparty-motion-to-dismiss | 2 | 0 / 2 / 0 | keep | agg1 | 0.882 | 0.882 |
| tax/review-iss-tax-transaction-structure | 2 | 0 / 2 / 0 | keep | agg1 | 0.786 | 0.821 |
| trusts-estates-private-client/draft-consent-to-adoption | 2 | 3 / 1 / 0 | adopt_inv | agg1 | 0.857 | 0.829 |
| banking-finance/compare-closing-documents-against-restructuring-conditions | 2 | 0 / 2 / 0 | keep | agg1 | 0.947 | 0.974 |

Budget used: 34 rollouts · 60 improver calls · 57,510,793 input / 2,251,656 output tokens

## Lessons in the library

- **employment-labor/identify-issues-in-counterparty-motion-brief**: Prioritize capturing concrete independent-verification procedures (recompute math, verify every record cite, flag cited-but-missing evidence) over generic tool guidance
- **bankruptcy-restructuring/identify-issues-in-counterparty-sale-objection**: Adopt workflow discipline in tool guidance — read-first parsing, reading full errors before retrying, persisting extractions under the workspace scratch folder, and verifying dump tails — instead of storing the fix as episodic memory
- **capital-markets/review-form-8**: Adopt changes that fix demonstrated execution friction (wasted turns, failed tool calls) but skip neutral changes when both runs already produce complete, equivalent deliverables — keep beats adopt when the edit buys nothing observable.
- **emerging-companies-venture-capital/extract-key-terms-from-cap-table**: Persist full extractions to files, verify the tail, and recompute all totals yourself instead of trusting stated subtotals or truncated console output
- **trusts-estates-private-client/draft-consent-to-adoption**: Use the harness read tool first, persist parsed dumps to disk, and validate dump completeness (tail/line count) before relying on extracted text for deliverables
