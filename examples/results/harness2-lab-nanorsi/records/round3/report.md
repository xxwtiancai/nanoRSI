# nanoRSI report — lab-opencode

mode `agg` · k=1 · model `glm-5.3` · runner `command` · frozen · 794 ledger events

**Judged (n=29): base 0.852 → final 0.908 partial, +5.6 pp, 17W/3T/9L**

| task | proposals | mitigates / neutral / regresses | decisions | chosen | base | final |
| --- | ---: | --- | --- | --- | ---: | ---: |
| antitrust-competition/draft-commitments-proposal | 2 | 0 / 2 / 0 | keep | agg1 | 0.869 | 0.852 |
| arbitration-international-dispute-resolution/draft-arbitrator-nomination-letter | 2 | 0 / 2 / 0 | keep | agg1 | 0.952 | 0.976 |
| banking-finance/extract-intercreditor-agreement-terms | 2 | 2 / 0 / 0 | merge | agg1 | 0.897 | 0.793 |
| bankruptcy-restructuring/compare-competing-bid-terms-against-stalking-horse-asset-purchase-agreement | 2 | 2 / 0 / 0 | merge | agg1 | 0.941 | 0.956 |
| capital-markets/compare-closing-documents-against-closing-checklist | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.875 | 0.906 |
| corporate-governance/extract-key-changes-from-proposed-regulation | 2 | 2 / 0 / 0 | merge | agg1 | 1.000 | 1.000 |
| corporate-governance/assess-impact-of-new-state-privacy-law-on-multi | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.901 | 0.930 |
| corporate-ma/draft-issues-list-for-restrictive-covenant-agreement | 2 | 2 / 0 / 0 | merge | agg1 | 0.981 | 1.000 |
| corporate-ma/extract-payoff-and-release-requirements-from-credit-facilities | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.908 | 0.908 |
| corporate-ma/analyze-qoe-reconciliation | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.824 | 0.756 |
| data-privacy-cybersecurity/identify-issues-in-transfer-impact-assessment | 2 | 1 / 1 / 0 | adopt_inv | agg1 | 0.848 | 0.879 |
| diligence/gaming-strategic-acquisition | 2 | 1 / 0 / 1 | adopt_inv | agg1 | — | — |
| emerging-companies-venture-capital/analyze-counterparty-markup-of-stock-purchase-agreement | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.915 | 0.979 |
| employment-labor/compare-employee-handbook-against-state-requirements | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.962 | 0.943 |
| energy-natural-resources/draft-markup-of-intercreditor-agreement | 2 | 1 / 1 / 0 | adopt_inv | agg1 | 0.036 | 0.873 |
| environmental-esg/extract-reporting-obligations-from-consent-decree | 2 | 2 / 0 / 0 | merge | agg1 | 0.769 | 0.782 |
| funds-asset-management/analyze-fund-economics-comparison | 2 | 1 / 0 / 1 | adopt_inv | agg1 | 0.925 | 0.745 |
| healthcare-life-sciences/draft-enterprise-saas-vendor-onboarding-due-diligence | 2 | 1 / 1 / 0 | adopt_inv | agg1 | 0.964 | 0.982 |
| immigration/compare-i | 2 | 0 / 2 / 0 | keep | agg1 | 0.909 | 0.909 |
| insurance/extract-insurance-policy-terms | 2 | 2 / 0 / 0 | merge | agg1 | 0.985 | 0.970 |
| intellectual-property/identify-tech-license-term-sheet-issues | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.878 | 0.902 |
| intellectual-property/compare-executed-supply-agreement-against-approved-template | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.875 | 0.893 |
| intellectual-property/update-data-processing-agreement-template-for-new-gdpr-adequacy-decision | 2 | 2 / 0 / 0 | merge | agg1 | 0.942 | 0.981 |
| international-trade-sanctions/compare-ownership-structure-against-sanctioned-parties-list | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.981 | 0.963 |
| litigation-dispute-resolution/draft-defective-industrial-equipment-product-liability | 2 | 1 / 1 / 0 | adopt_dom | agg1 | 0.848 | 0.899 |
| real-estate/review-real-estate-diligence | 2 | 0 / 2 / 0 | keep | agg1 | 1.000 | 0.982 |
| structured-finance-securitization/extract-key-terms-from-warehouse-credit-facility-term-sheet | 2 | 0 / 2 / 0 | keep | agg1 | 0.899 | 0.911 |
| tax/analyze-section-382-analysis | 2 | 2 / 0 / 0 | merge | agg1 | 0.000 | 0.804 |
| trusts-estates-private-client/extract-contested-divorce-asset-extraction | 2 | 0 / 2 / 0 | keep | agg1 | 0.915 | 0.901 |
| white-collar-defense-investigations/compare-document-production-set-against-subpoena-request-categories | 2 | 2 / 0 / 0 | merge | agg1 | 0.895 | 0.947 |

Budget used: 114 rollouts · 174 improver calls · 280,606,836 input / 11,377,445 output tokens

## Lessons in the library

- **banking-finance/extract-intercreditor-agreement-terms**: Inspect the tool's interface (--help or source) before first use, and after any traceback change strategy instead of retrying the identical command
- **bankruptcy-restructuring/compare-competing-bid-terms-against-stalking-horse-asset-purchase-agreement**: Extract to a persistent scratch file, record its full size, and read it in tracked line-range chunks with a grep-built index — never draft from a partially-read source, and confirm full coverage before writing the deliverable
- **capital-markets/compare-closing-documents-against-closing-checklist**: Require every discrepancy finding to cite both the controlling source and the deviating document at a specific location, and treat one-sided claims as unverified hypotheses rather than findings
- **corporate-governance/extract-key-changes-from-proposed-regulation**: Inspect the tool's interface (--help or head of source) before invoking, and if it tracebacks, change a flag or mode rather than retrying the identical command
- **corporate-governance/assess-impact-of-new-state-privacy-law-on-multi**: Enforce per-provision pin cites and explicit separation of sourced facts, analysis, and assumptions — content requirements, not formatting, are what fix citation defects
- **corporate-ma/draft-issues-list-for-restrictive-covenant-agreement**: Persist each source to a scratch file, read it fully in tracked chunks (coverage ledger), and confirm 100% coverage before drafting — never draft from partial or truncated tool output
- **corporate-ma/extract-payoff-and-release-requirements-from-credit-facilities**: Before drafting, verify complete coverage of every source document via a coverage ledger (source, extracted length, sections read), and never fill gaps with plausible-looking numbers — label derived amounts as computed, separate sourced facts from analysis and assumptions, and pin-cite every figure and legal conclusion
- **corporate-ma/analyze-qoe-reconciliation**: Require independent recomputation (re-footing) of any schedule before reporting a discrepancy, and pin-cite both source positions with the dollar delta — never conclude from eyeballed or truncated extractions
- **data-privacy-cybersecurity/identify-issues-in-transfer-impact-assessment**: Adopt the edit that directly mitigates the observed failure mechanism (here: source-discipline rules forcing pin cites, re-checked quotes, and facts/analysis/assumption separation) over domain-generic edits, even when the latter show neutral contrasts
- **diligence/gaming-strategic-acquisition**: Persist full listings/outputs to scratch files first and derive all counts and coverage claims from those files, never from partially-seen tool output
- **emerging-companies-venture-capital/analyze-counterparty-markup-of-stock-purchase-agreement**: Require per-finding pin-cites to both sides (controlling source and deviating document) plus a coverage ledger confirming full extraction reads before drafting; treat single-sided or memory-derived claims as unverified hypotheses
- **employment-labor/compare-employee-handbook-against-state-requirements**: Require dual pin cites plus recomputation of every count and figure before findings are reported — single-sided citations, paraphrased quotes, and summary counts that don't tie to the findings table are the dominant failure mode in truncated-extraction audits
- **energy-natural-resources/draft-markup-of-intercreditor-agreement**: Persist extractions to scratch files and start producing deliverables by a fixed budget midpoint, rather than iterating on analysis until the run ends with no output
- **environmental-esg/extract-reporting-obligations-from-consent-decree**: Persist every source extraction to a file and read it fully in recorded chunks with a coverage ledger before drafting; derive all quotes, counts, and citations from the persisted files, never from stream memory
- **funds-asset-management/analyze-fund-economics-comparison**: Verify extraction output by content and size (grep for Traceback, check wc) before using it; on failure, read the named cause and switch tools (harness read, pandoc, python-docx) rather than retrying the same failing command with cosmetic changes like a new filename, and keep scratch files inside workspace-relative paths
- **healthcare-life-sciences/draft-enterprise-saas-vendor-onboarding-due-diligence**: Persist all intermediate extractions to workspace-relative scratch files with stable names and verify their size/content before relying on them, rather than streaming one-shot tool output or writing outside the workspace
- **insurance/extract-insurance-policy-terms**: Persist every document extraction to a verified workspace scratch file and complete a full-read ledger before drafting; treat any claim not traceable to a verified extraction as unsupported
- **intellectual-property/identify-tech-license-term-sheet-issues**: Never draft from streamed extraction output or memory of partial reads: persist every extraction to a workspace file, verify it succeeded, and read it completely before citing or summarizing it
- **intellectual-property/compare-executed-supply-agreement-against-approved-template**: Persist every extraction to a workspace-relative scratch file, verify it by content, and read it fully before drafting findings — never analyze from streamed or partially-read output
- **intellectual-property/update-data-processing-agreement-template-for-new-gdpr-adequacy-decision**: Persist each document's full extraction to a workspace scratch file and verify it (size, no errors, tail landmark present) before analyzing; never draft from streamed or partially-read tool output
- **international-trade-sanctions/compare-ownership-structure-against-sanctioned-parties-list**: Persist every document extraction to a workspace file before analyzing, and draft only from the persisted copy — never from streamed tool output or repeated failed reads
- **litigation-dispute-resolution/draft-defective-industrial-equipment-product-liability**: Persist every extraction to disk with completeness checks (error grep, size, tail landmark) and read fully in chunks, drafting only from a verified coverage ledger — never from memory of streamed tool output
- **tax/analyze-section-382-analysis**: Merge complementary candidates rather than choosing one; disjoint changes capture all mitigations without conflict
- **white-collar-defense-investigations/compare-document-production-set-against-subpoena-request-categories**: Persist extractions to disk, verify completeness before citing, and build a request-by-request coverage matrix with recomputed arithmetic and pin cites before drafting prose
