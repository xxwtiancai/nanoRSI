# Tax Issue Identification Report
## Review of Tax Structure Memorandum — Project Prism (Ridgeline Capital Partners Fund III, LP / Prism Health Analytics, Inc.)

**Prepared:** February 2025
**Subject:** Issues, inconsistencies, and omissions in the Calloway, Stern & Whitaker LLP ("CSW") Tax Structure Memorandum dated February 10, 2025, identified against the supporting deal documents.

---

## Executive Summary

The CSW memo concludes that the Section 338(h)(10) election for the acquisition of Prism Health Analytics, Inc. will (i) produce a basis step-up on an Aggregate Deemed Sale Price ("ADSP") of $473,000,000, (ii) avoid entity-level tax because the Section 1374 built-in gains recognition period expired December 31, 2021, and (iii) pass all gain through to eligible individual S corporation shareholders free of entity-level tax. Our cross-check against the supporting documents shows that each of these conclusions rests on computations or factual premises that are contradicted or unverified in the deal documents.

The most significant findings, in rank order:

1. **The ADSP is overstated by $48 million.** The memo computes ADSP as $425M enterprise value + $48M liabilities = $473M. Thornfield's reconciliation (asset-valuation-summary.xlsx) demonstrates this double-counts the funded debt: enterprise value already includes debt, and the amount realized by shareholders is $370M. Correct ADSP is $425M ($370M + $48M + $7M). This error inflates the memo's Class VII goodwill residual by $48M (memo: $272.8M vs. Thornfield: $196.3M) and would flow into an incorrect Form 8883.
2. **The memo's Class V allocation omits the $28.5M Beacon Insights partnership interest.** Combined with Issue 1, the memo's residual goodwill is overstated by $76.5M. The memo also never analyzes the §754/§743(b) implications of stepping up the Beacon interest.
3. **The memo asserts unqualified S corporation validity while three shareholders' eligibility is unverified** (per the cap table: Lin Wei Zhang, Yusuf Al-Rashidi, Nina Petrova) and an unresolved 2021 stock-ledger annotation suggests a possible transfer to a family LLC — any of which, if adverse, retroactively terminates the S election and destroys the foundation of the entire 338(h)(10) structure.
4. **The memo's Beacon discussion overlooks that the merger itself is a "Change of Control" that triggers the Beacon members' 45-day right of first refusal at undiscounted fair market value** — a closing-condition risk to acquiring the 80.5% interest the memo treats as a Class V asset.
5. **The memo omits or under-analyzes:** the non-transferable NC data processing license supporting ~$19M of government revenue; the ~$6.3M Section 482 transfer-pricing exposure on the Prism–Beacon intercompany fees; the likely permanent loss of the $3.8M suspended federal R&D credits; QSBS (Section 1202) issues raised by shareholders; and the tax mechanics of Dr. Chandra's $37M rollover within a 338(h)(10) transaction.

One source document, **shareholder-qsbs-email-thread.eml, could not be read** (conversion failed twice). QSBS findings in this report therefore rely on the Thornfield due diligence report and the cap table; the QSBS analysis is correspondingly incomplete (see "Sources").

---

## Severity-Ranked Findings

### CRITICAL

**C-1. ADSP overstated by $48 million; goodwill residual overstated by $48M.**
- Memo (Exec. Summary; §IV): ADSP = $473,000,000, allocated with $272.8M to Class VII goodwill.
- Thornfield allocation summary (Allocation Summary tab, Note 1): under Treas. Reg. §1.338-4, ADSP = amount realized on the stock ($370M = $333M cash + $37M rollover) + target liabilities ($48M funded debt + $7M seller transaction expenses) = **$425M**. The memo's method (enterprise value $425M + $48M debt) double-counts the funded debt already embedded in EV.
- Impact: memo goodwill is $272.8M vs. Thornfield's $196.3M on this item alone; depreciation/amortization projections, the PPA delivered under SPA §7.3(b), and Form 8883 would all be wrong if the memo's computation is used.
- Action: Reconcile ADSP before the SPA §7.3(b) allocation process begins; the memo should be corrected.

**C-2. S corporation eligibility unverified for three restricted stock holders; memo states no ineligible shareholders are known.**
- Memo (§III.A): "All shareholders of Prism are U.S. individuals, and we are not aware of any ineligible shareholders"; represents every 83(b) election was timely filed.
- Cap table (prism-cap-table.xlsx) flags **three** holders with unconfirmed eligibility: Lin Wei Zhang (H-1B, PRC citizen — "if nonresident alien, S election invalidated"), Yusuf Al-Rashidi (dual U.S./Jordan citizen; documentation not on file), Nina Petrova (green card holder; documentation not on file). Aggregate consideration to unverified holders: $2,775,000.
- Thornfield (§III.B) flags **two** holders: a Canadian national on an H-1B whose substantial-presence compliance is unverified, and a possible 2021 transfer to "Family Holdings, LLC" (an ineligible shareholder if a partnership or SMLLC owned by an ineligible person). **The two documents also conflict on the H-1B holder's nationality (Canadian vs. PRC citizen), which itself must be resolved.**
- Impact: If the S election terminated in any prior year, Prism was a C corporation for all subsequent years — entity-level tax for open years, penalties/interest, and **the 338(h)(10) election becomes unavailable**. SPA §4.9(a) reps would also be inaccurate.
- Action: Do not close until citizenship/residency documentation is obtained for every holder for every year since 1/1/2017, and the alleged family-LLC transfer is documented or disproven. Consider a corrective §1362(f) relief plan if an inadvertent termination is discovered.

**C-3. Memo's Class V allocation omits the $28.5M Beacon Insights interest (part of a $76.5M goodwill overstatement).**
- Memo Class V: $68.5M. Thornfield Class V: $97.0M, itemizing real property ($14.2M), FF&E ($6.8M), developed technology ($41.8M), government software licenses ($5.7M), NC license ($0), and the Beacon 80.5% interest ($28.5M) — which "does not appear to be included" in the memo's Class V (Allocation Summary, Note 2).
- Impact: misallocation between Class V and Class VII; and no analysis of whether Beacon should make a §754 election to give Prism's transferee the §743(b) step-up (the memo treats the interest as a Class V asset in one sentence and stops).

### HIGH

**H-1. Beacon ROFR triggered by the merger itself — unaddressed in the memo.**
- Beacon operating agreement §8.03(a)(ii): a "Change of Control of any Member that is an entity" is a Triggering Event; the merger (SPA §2.3(d) expressly a change of control) puts Prism — the Manager and 80.5% member — through a change of control. Non-transferring members (Delano 12%, Avesta 7.5%) have a 45-day ROFR at Fair Market Value determined **without discount for lack of control or marketability** (§8.04(d)).
- The memo mentions the ROFR only in passing ("customary transfer restrictions") and never analyzes it. Closing cannot be assured without ROFR waivers; the $28.5M Beacon valuation and PPA are at risk.

**H-2. Non-transferable NC data processing license — omitted from the memo.**
- Valuation summary (A-008, Note 3) and SPA §4.9(i): License No. DIT-2019-04821 is non-transferable and non-assignable; ~$19M of annual government revenue depends on it; $0 FMV assigned; legal confirmation of survival through the reverse triangular merger is outstanding. The memo describes the license (§II.A, §III.C) but never flags transferability or valuation consequences.

**H-3. Section 482 transfer-pricing exposure (~$6.3M) — memo treats the intercompany fees as unremarkable.**
- Thornfield (Exec. Summary; §VII): the $850K management fee and $400K IP license fee "appear to be below arm's-length pricing" with no benchmarking study ever performed (Beacon OA §9.01 confirms the fee has never been benchmarked and does not vary with services). SPA §4.9(h) concedes no transfer pricing study exists. Estimated cumulative exposure: $6.3M (2019–2024). The memo simply recites the fee amounts without risk analysis. Note also that the 338(h)(10) deemed sale price for the Beacon-dependent intangibles rests partly on an intercompany pricing structure the IRS could reallocate.

**H-4. Suspended $3.8M federal R&D credits likely permanently lost — memo defers.**
- Thornfield (§IV.B): credits from the 2016 C corp year are suspended under §1371(b)(1); with no BIG tax (recognition period expired) and no C corp tax anticipated, there is no apparent utilization vehicle; credits are lost on the deemed liquidation. The memo notes the credits "will be addressed in the post-closing tax planning" without acknowledging the material risk of permanent expiration or analyzing §§1371(b)/(e).

**H-5. Rollover equity mechanics within the 338(h)(10) structure — unanalyzed; descriptions inconsistent across documents.**
- $37M of consideration is Parent (or affiliate) equity, not cash. The memo does not analyze (a) the tax treatment of the rollover shares in a deemed-asset-sale framework, or (b) whether the non-cash component and any related-party acquisition jeopardize the "qualified stock purchase" under §338(d)(3). The cap table itself notes: "Memo does not address interaction of rollover with 338(h)(10) deemed sale."
- Documents describe the rollover destination inconsistently: memo says contributed to "Newco"; SPA §2.6(e) says equity in "Parent (or a designated acquisition vehicle)"; the cap table says "Ridgeline Acquisition Sub, Inc." These must be reconciled.

### MEDIUM

**M-1. QSBS (Section 1202) omitted from the memo entirely.**
- Thornfield (§VIII.B) flags unresolved QSBS questions raised by angel investors through Linden Rock; the cap table annotates most C-corp-period holders "Potential QSBS — not analyzed" and correctly notes Elena Vargas (issued 3/1/2017, S corp period) cannot qualify under §1202(c)(1). The memo contains no Section 1202 discussion at all, including the fundamental interaction issue: a 338(h)(10) election converts shareholders' stock sale into deemed asset-sale gain pass-through, with asset-level character (much of it ordinary/recapture and §197 gain) — potentially eliminating QSBS exclusion that an unelected stock sale might have provided. Affected shareholders should be advised before they consent to the election (a closing condition under SPA §7.3(a)). *Note: this analysis is incomplete because shareholder-qsbs-email-thread.eml was unreadable (see Sources).*

**M-2. Shareholder-count and factual inconsistencies between memo and cap table.**
- Memo: "Fourteen (14) angel investors and early employees hold the remaining 20%." Cap table: 12 non-restricted minority holders (10 angels/early employees + Derek Hawkins's two tranches) plus 8 restricted holders — 16 unique individuals outside the founders, 19-20 holders total. The counts do not reconcile; accurate shareholder counts matter for the §1361 100-shareholder limit and the Form 8023 consents.

**M-3. Date discrepancies.**
- Memo says the Thornfield report is "dated January 10, 2025"; the report itself is dated **January 15, 2025** (and states information only through January 10). The valuation summary references "Memo dated 1/28/2025," but the memo is dated **February 10, 2025**. Citation hygiene suggests version-control problems.

**M-4. CSW appears on both sides of the deal.**
- The memo lists CSW as tax and deal counsel to **Ridgeline (Buyer)**; SPA §2.6(b) pays $2.2M of seller transaction expenses to CSW "**as Company counsel**." This conflict (or drafting error) should be clarified; it also raises privilege/work-product questions about the memo's circulation.

**M-5. Final/2024 S corporation return timing.**
- The 2024 Form 1120-S is due March 15, 2025 — the same day as closing — and the final short-year return (SPA §7.1) must reflect the deemed sale. The memo (readable portion) does not flag the extension need or the mechanics of the final return with a 338(h)(10) deemed sale. Escrow of $22M/18 months also has estimated-tax implications for individuals that the memo's state discussion only gestures at ("consult your individual tax advisor").

**M-6. AAA and deemed-liquidation characterization.**
- Thornfield reports AAA of ~$64.2M (12/31/2023), relevant to characterizing deemed distributions in the deemed liquidation; the memo does not address it in the portions reviewed.

### LOW

**L-1.** Memo states restricted stock is "approximately 2.3% of the fully diluted equity" — cap table computes 2.26%; trivial, but precision matters in the consent-shareholder population.
**L-2.** Memo cites "Treas. Reg. 1.301-7701-3" for the check-the-box regulation; the correct citation is Treas. Reg. §301.7701-3 (cited correctly in the SPA and Beacon OA). Citation error recurring in the memo.
**L-3.** California entity-level S corp tax (1.5%/$800 minimum) and NY fixed-dollar minimum are represented as current (SPA §4.9(c)); memo "notes briefly" — acceptable, but CA-resident shareholders' pass-through gain from the deemed sale should be specifically flagged in the closing communications the memo recommends.

---

## Cross-Document Reconciliation Summary

| Item | Memo | Thornfield DD | Valuation Summary / Cap Table / SPA | Assessment |
|---|---|---|---|---|
| ADSP | $473M | $425M | $425M (valuation Note 1) | Memo wrong (double-count) |
| Class V | $68.5M | $97.0M | $97.0M incl. Beacon $28.5M | Memo omits Beacon |
| Class VII | $272.8M | $196.3M | $196.3M | Memo overstated $76.5M |
| BIG period expired 12/31/21 | Yes | Yes (verified) | SPA §4.9(f) | Consistent — conclusion sound *if* S election valid |
| Unverified S-eligible holders | None known | 2 | 3 (cap table) | Memo understates; DD vs. cap table conflict on nationality |
| Family LLC transfer | Not addressed | Open item | Not addressed | Omission |
| Beacon ROFR | Mentioned only | — | OA §8.03 triggered by CoC | Omission |
| NC license non-transferable | Not addressed | — | A-008 / SPA §4.9(i) | Omission |
| §482 exposure | Not addressed | ~$6.3M | SPA §4.9(h): no TP study | Omission |
| $3.8M R&D credits | Deferred | At risk of permanent loss | SPA §4.9(g) | Under-analyzed |
| QSBS | Omitted | Flagged | Cap table flags; eml unreadable | Omission |
| Rollover destination | "Newco" | — | Parent / Acquisition Sub | Inconsistent |

---

## Sources

**Reviewed:** transaction-structure-memo.docx (CSW memo, Feb 10, 2025; tail truncated but principal analysis sections read); purchase-agreement-excerpts.docx (Merger Agreement excerpts, Jan 28, 2025); tax-due-diligence-report.docx (Thornfield, Jan 15, 2025; portions truncated); beacon-operating-agreement.docx (excerpts); prism-cap-table.xlsx (3 tabs); asset-valuation-summary.xlsx (2 tabs).

**Not reviewed:** shareholder-qsbs-email-thread.eml — conversion failed on two attempts. Affected analysis: QSBS shareholder communications (Finding M-1) is based solely on the Thornfield report and cap table; shareholder-specific Section 1202 positions in the email thread could not be verified.

**Caveat:** Several documents were truncated at display limits (memo §IV mid-section; SPA Articles VII+ tail; Thornfield Sections V–XII tail). Findings reflect the readable portions; the truncated sections could contain additional analysis that would modify findings M-5/M-6 in particular.
