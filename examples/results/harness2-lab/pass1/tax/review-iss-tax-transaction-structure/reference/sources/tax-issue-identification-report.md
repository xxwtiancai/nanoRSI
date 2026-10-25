# Tax Issue Identification Report
## Review of Transaction Structure Memorandum — Project Prism
### Acquisition of Prism Health Analytics, Inc. by Ridgeline Capital Partners Fund III, LP

**Prepared for:** Deal Team / Investment Committee
**Subject:** Review of the Calloway, Stern & Whitaker LLP Tax Structure Memorandum (Feb. 10, 2025) against supporting deal documents
**Documents reviewed:** transaction-structure-memo.docx; purchase-agreement-excerpts.docx; tax-due-diligence-report.docx (Thornfield, Jan. 15, 2025); asset-valuation-summary.xlsx (Thornfield PPA); prism-cap-table.xlsx; beacon-operating-agreement.docx
**Document not reviewed:** shareholder-qsbs-email-thread.eml (file could not be converted/read; QSBS issues below are sourced from the Thornfield report and cap table)

---

## 1. Executive Summary

The transaction structure memo is well-organized but contains material errors and omissions that must be resolved before closing (expected March 15, 2025) and before any Form 8023 or Form 8883 is filed.

The most significant issues are:

1. **Critical — ADSP appears overstated by $48 million.** The memo computes an Aggregate Deemed Sale Price of $473M (enterprise value $425M plus $48M of funded debt). Thornfield's analysis demonstrates this double-counts the funded debt: under Treas. Reg. 1.338-4, ADSP should be built from the amount realized on the stock ($370M, including the $37M rollover) plus target liabilities, i.e., approximately $425M. The $48M overstatement flows directly into an inflated Class VII goodwill residual ($272.8M vs. Thornfield's $196.3M — a $76.5M variance once the Beacon classification error is also included).
2. **Critical — S corporation eligibility of restricted stock holders is unconfirmed, and the memo overstates comfort.** The memo states that "no events causing a termination of the S election have been identified" and that all shareholders are U.S. individuals. In fact, the cap table and Thornfield report identify **three** holders with unverified eligibility (an H-1B/PRC-national holder, a dual U.S./Jordan citizen without documentation on file, and a Bulgarian-born holder whose green card is not documented), plus a possible historical transfer to a family LLC referenced in the 2021 stock ledger, and two California shareholders with expired W-9s. A valid S election is a threshold requirement for the 338(h)(10) election; inadvertent termination would trigger entity-level tax for open years and eliminate the election.
3. **High — The memo misstates key facts about the Beacon Insights interest and ignores the ROFR.** The memo's Class V allocation ($68.5M) does not include the $28.5M Beacon partnership interest, contrary to Treas. Reg. 1.338-6 classification and Thornfield's PPA. The memo mentions the Beacon ROFR only in passing and does not analyze that the merger itself is a "Change of Control" Triggering Event under Section 8.03(a)(ii) of the Beacon operating agreement, requiring a ROFR Notice within 10 business days of signing (the agreement was signed January 28, 2025 — this deadline has likely already passed, and non-compliance risk should be assessed).
4. **High — Suspended $3.8M federal R&D credits.** The memo notes the credits but does not analyze whether the 338(h)(10) deemed liquidation and post-termination transition period offer any utilization; Thornfield flags them as at significant risk of permanent loss.
5. **High — Section 482 transfer pricing exposure (~$6.3M cumulative).** The Beacon operating agreement itself confirms the $850K management fee has never been benchmarked and does not vary with services — yet the purchase agreement contains a flat representation that the fees are "at arm's length."
6. **High — QSBS (Section 1202) analysis is omitted entirely.** Multiple C-corporation-period shareholders hold potentially QSBS-eligible stock; the memo does not address the interaction of QSBS exclusion with the 338(h)(10) deemed asset sale (an issue on which shareholders have actively inquired via their advisor).
7. **Medium/High — Rollover equity treatment.** The memo does not analyze the tax treatment of Dr. Chandra's $37M rollover within the 338(h)(10) framework (the deemed asset sale/liquidation affects the exchange treatment of rollover shares).
8. **Medium — NC data processing license (non-transferable).** Roughly $19M of annual government revenue depends on a license that is non-transferable and non-assignable; the deemed asset sale framing heightens the risk that value attributed to it and the underlying revenue are impaired. The memo does not address this.
9. **Medium — Beacon §754 election / §743(b) step-up.** The memo classifies the Beacon interest as Class V but does not address the §754 election needed to obtain inside basis step-up; Thornfield has not performed a look-through analysis.
10. **Medium — Date and citation inconsistencies** (memo dated Feb. 10 vs. Thornfield report cited as Jan. 10 and referenced elsewhere as Jan. 15; the memo mis-cites Treas. Reg. "1.301-7701-3" instead of 301.7701-3; the memo's assertion that all restricted stock holders are confirmed eligible conflicts with the cap table).

**Recommended immediate actions:** (a) recompute ADSP and reissue the memo with corrected allocation; (b) obtain definitive residency/citizenship documentation for all shareholders and investigate the 2021 family-LLC transfer entry before closing (consider a Section 1362(f) inadvertent-termination remediation plan as a fallback); (c) deliver a compliant ROFR Notice to Beacon members and obtain waivers; (d) complete QSBS, rollover, R&D credit, and §754 analyses; (e) resolve the NC license status with counsel and DIT.

---

## 2. Severity Framework

- **Critical** — Could invalidate the transaction's core tax structure, materially change the price allocation, or expose the parties to significant entity-level tax.
- **High** — Material dollar exposure or closing-mechanics risk requiring resolution before or at closing.
- **Medium** — Compliance, documentation, or accuracy issues that should be corrected but are not deal-breaking.
- **Low** — Drafting/consistency items.

---

## 3. Critical Issues

### Issue C-1. ADSP Overstated by $48 Million; Goodwill Allocation Inflated by $76.5 Million
- **Memo position (Sec. I, IV):** ADSP = $473,000,000 (enterprise value $425M + $48M funded debt); Class VII goodwill = $272.8M.
- **Supporting documents:** Thornfield asset-valuation-summary.xlsx (Allocation Summary, Notes 1–2); Treas. Reg. 1.338-4.
- **Issue:** Enterprise value already includes the debt component (EV = equity + net debt). The memo derives equity value ($370M) by subtracting the $48M debt and $7M expenses, then adds the $48M debt back to EV to reach ADSP — double-counting the debt. Correct ADSP ≈ $370M (cash $333M + rollover $37M) + $48M debt + $7M liabilities ≈ $425M. The error inflates the memo's Class VII residual goodwill by $48M; combined with the Beacon classification omission (H-1), total Class VII variance is $76.5M (memo $272.8M vs. Thornfield $196.3M). Note the corrected total allocation equals $425M — coincidentally the same figure as enterprise value, which may mask the error on casual review.
- **Consequence:** Incorrect Forms 8023/8883; overstated 15-year §197 amortization; shareholder/buyer gain mismatch; audit exposure.
- **Recommendation:** Recompute ADSP per Treas. Reg. 1.338-4 and reissue the memo and allocation before filing.

### Issue C-2. Unverified S Corporation Shareholder Eligibility; Memo Overstates Comfort
- **Memo position (Sec. III.A):** "No events causing a termination of the S election have been identified. All shareholders of Prism are U.S. individuals, and we are not aware of any ineligible shareholders."
- **Supporting documents:** Thornfield report Sec. III.B (critical finding); prism-cap-table.xlsx (three holders flagged "Unconfirmed": Lin Wei Zhang — H-1B, PRC citizen, substantial presence unverified; Yusuf Al-Rashidi — dual U.S./Jordan citizen, no documentation; Nina Petrova — Bulgarian-born, green card not documented); 2021 stock ledger annotation re "transfer to [name] Family Holdings, LLC."
- **Issue:** If any holder was an ineligible shareholder in any year since January 1, 2017, the S election terminated under §1362(d)(2), retroactively converting Prism to a C corporation — eliminating the 338(h)(10) election and triggering entity-level tax, penalties, and interest for open years. The memo's flat assertion conflicts with its own diligence provider's "critical open item" designation. Separately, two California shareholders have W-9s expired since 2019.
- **Recommendation:** Obtain immigration/residency documentation for all years for Zhang; citizenship documentation for Al-Rashidi; green card documentation for Petrova; investigate and document the 2021 family-LLC transfer (operating agreement, classification, member list). Consider closing conditions, specific indemnity/escrow, and a §1362(f) inadvertent-termination relief plan as fallback. Address the 2024 Form 1120-S extension (due March 15, 2025 — the closing date).

---

## 4. High-Severity Issues

### Issue H-1. Beacon Insights Interest Omitted from Class V Allocation
- **Memo (Sec. III.C, IV.C):** Class V = $68.5M; Beacon interest described as a $28.5M FMV / $6.4M basis Class V asset.
- **Supporting documents:** Thornfield PPA (Class V = $97.0M including Beacon at $28.5M; variance $28.5M / 41.6%).
- **Issue:** The memo's own narrative says Beacon is Class V, but its allocation omits it. This misallocates $28.5M between Class V and Class VII residual, affecting amortization profiles.
- **Recommendation:** Correct the allocation; decide whether Beacon makes a §754 election and prepare §743(b) computations; consider a look-through analysis of Beacon's assets (receivables would carry ordinary-income character under Beacon's character-preservation provision, Sec. 6.05 of the operating agreement).

### Issue H-2. Beacon ROFR Triggered by the Merger; Timing Likely Lapsed
- **Memo:** Mentions "customary transfer restrictions, including a right of first refusal" with no analysis.
- **Supporting documents:** Beacon operating agreement §8.03(a)(ii) — a Change of Control of any entity Member is a Triggering Event; ROFR Notice due within **10 business days of execution of the definitive agreement** (signed January 28, 2025); 45-day exercise period; Delano and Avesta could elect to purchase Prism's interest at FMV (no minority discounts, per §8.04(d)).
- **Issue:** No evidence a ROFR Notice was delivered. If the ROFR was not validly noticed or waived, closing could be challenged; if exercised, up to $28.5M of value (and ~$3.2M EBITDA) could exit the acquired group.
- **Recommendation:** Confirm notice status immediately; deliver/cure ROFR notice; obtain written waivers from Delano and Avesta as a closing deliverable.

### Issue H-3. Suspended Federal R&D Credits ($3.8M) — Utilization Unanalyzed
- **Memo (Sec. III.D):** Credits are "noted and will be addressed in the post-closing tax planning."
- **Supporting documents:** Thornfield report Sec. IV.B — credits suspended under §1371(b)(1); possible interaction with the post-termination transition period under §1371(e); at significant risk of permanent expiration upon deemed liquidation.
- **Issue:** The memo defers analysis that may affect structuring decisions. Under the corrected ADSP there is no §1374 tax to absorb the credits.
- **Recommendation:** Complete the §1371(b)/(e)/§1374/§338(h)(10) interaction analysis now; if unsalvageable, reflect in price/indemnity discussions.

### Issue H-4. Section 482 Transfer Pricing Exposure (~$6.3M) Contradicted by Documents
- **Memo:** Describes the management fee ($850K) and IP license fee ($400K) neutrally.
- **Supporting documents:** Thornfield report Sec. VII (cumulative §482 exposure est. $6.3M for 2019–2024; fees appear below arm's-length); Beacon operating agreement §9.01 (fee never benchmarked; CPI-capped at 3%; does not vary with volume, scope, or cost); Purchase Agreement §4.9(h) (Company represents fees are arm's length while admitting no transfer pricing study exists).
- **Issue:** The memo omits a material diligence finding; the SPA representation is internally inconsistent. Post-closing, buyer inherits exposure on the Prism side; pre-closing exposure is an indemnity matter.
- **Recommendation:** Quantify exposure; address via special indemnity/escrow; benchmark the fees and paper corrected terms at or before closing.

### Issue H-5. QSBS (§1202) Omitted Despite Active Shareholder Inquiries
- **Memo:** No Section 1202 analysis.
- **Supporting documents:** Thornfield report Sec. VIII.B (shareholders raised QSBS questions through Linden Rock; interaction with 338(h)(10) unanalyzed); cap table (founders and 2016-period angels acquired stock during the C corporation period — potentially QSBS-eligible; Elena Vargas's 3/1/2017 stock is ineligible under §1202(c)(1) because issued by an S corporation); shareholder-qsbs-email-thread.eml (not readable — should be reviewed to capture any commitments made to shareholders).
- **Issue:** Under the 338(h)(10) election, gain flows through as deemed asset-sale gain; whether §1202 exclusion remains available to shareholders in this framework is uncertain. Shareholder expectations of full exclusion may be wrong, creating closing-consent and dispute risk (all shareholders must consent to the election as a closing condition).
- **Recommendation:** Prepare a §1202 analysis (gross assets testing, active business requirements, character of pass-through gain under 338(h)(10)); communicate to shareholders before they execute consents.

### Issue H-6. Chandra Rollover ($37M) — Tax Treatment Unanalyzed; Entity Descriptions Inconsistent
- **Memo (Sec. II.B):** Rollover described as a contribution to "Newco" in exchange for membership interests.
- **Supporting documents:** SPA §2.4(b)-(c), §2.6(e) (rollover into Parent or a designated acquisition vehicle); cap table notes ("Memo does not address interaction of rollover with 338(h)(10) deemed sale") and references rollover into Ridgeline Acquisition Sub, Inc.
- **Issue:** The rollover amount is correctly included in the amount realized/ADSP ($37M within the $370M), but the memo does not analyze gain recognition on the exchange of rollover shares for acquiror interests, nor the deemed-liquidation interaction. Inconsistent entity descriptions across the memo, SPA, and cap table suggest the rollover structure is not finalized.
- **Recommendation:** Specify the rollover vehicle definitively; document the federal and state tax treatment of the rollover exchange; align memo, SPA, and subscription documents.

---

## 5. Medium-Severity Issues

### Issue M-1. NC Data Processing License (DIT-2019-04821) — Non-Transferable; ~$19M Revenue at Risk
- **Facts:** License held by Prism Data Services, LLC; non-transferable/non-assignable per its terms (SPA §4.9(i); Thornfield PPA A-008 assigns $0 FMV). The memo does not mention the transferability restriction.
- **Issue:** If the license is deemed terminated on the deemed asset sale (or even on the actual merger), ~$19M of annual government revenue and related asset values (A-007 $5.7M government software licenses; goodwill) may be impaired. The memo's Class V "software" lines may embed value attributable to the license.
- **Recommendation:** Legal opinion on license survival under DGCL §259 (merger continuity) and under the deemed-asset-sale framing; confirm with NC DIT; reallocate any embedded value to goodwill or reduce value.

### Issue M-2. Beacon §754 Election / §743(b) Step-Up Omitted
- The memo classifies Beacon as a Class V asset but never addresses that buyer's economic step-up inside Beacon requires a §754 election and §743(b) computation; Thornfield expressly flagged this as undecided (PPA Note 2). Decide and calendar the election before Beacon's filing deadline for the closing year.

### Issue M-3. State Tax Gaps
- **California:** 12 employees/SF office; CA imposes a 1.5% entity-level S corp tax and $800 minimum franchise tax (SPA §4.9(c)). The memo notes CA only "briefly" — no analysis of CA conformity to the 338(h)(10) election or of CA-source pass-through gain for Muñoz and Yoon (CA residents; ~$12.95M combined consideration).
- **New York:** NY resident shareholder (Okoye, ~$3.7M) and NY office; memo is silent on NY filing/withholding on pass-through gain.
- **2024 return timing:** Form 1120-S due March 15, 2025 — the Closing Date; SPA §7.1 requires Parent's 30-day draft review, which the memo does not address.
- **Recommendation:** Expand state analysis; ensure the SPA §7.1 timeline works with the closing date.

### Issue M-4. Escrow and Payment Mechanics — Consistency Check
- Escrow $22M / 18 months / release 9/15/2026 is consistent across memo, SPA, and cap table ($311M net cash at closing). No issue; confirm pro-rata escrow withholding in the flow of funds.

### Issue M-5. Facts Asserted Without Support / Memo–Document Conflicts
- The memo asserts "all holders are individuals" and all eligible, conflicting with the cap table and Thornfield (see C-2).
- Memo cites the Thornfield report as "dated January 10, 2025"; the report is dated January 15, 2025. Fix citations.
- The Thornfield PPA references a CSW memo "dated 1/28/2025"; the reviewed memo is dated Feb. 10, 2025 — confirm which version the PPA reconciles against.
- Memo mis-cites "Treas. Reg. 1.301-7701-3" (twice); correct citation is Treas. Reg. §301.7701-3 (the SPA cites it correctly).

---

## 6. Low-Severity Issues

- **L-1.** The memo's shareholder split (52/28/20) uses basic ownership; the cap table's fully diluted split is 50.83%/27.37%. The SPA's "Pro Rata Share" definition should be confirmed (basic vs. fully diluted) to avoid a consideration mismatch — the cap table shows the minority block at $74,999,231 fully diluted vs. $74,000,000 per the memo/SPA, adjusted ad hoc. Reconcile Schedule 1.1(a).
- **L-2.** Escrow release date (September 15, 2026) matches across documents; no issue.
- **L-3.** Restricted stock 83(b) elections: memo, Thornfield, SPA, and cap table all confirm timely filings; consistent. No issue.
- **L-4.** Financing math in the memo (equity contribution $143M) is internally consistent.

---

## 7. Summary Table

| # | Issue | Severity | Source / Conflict | Action Before Closing |
|---|---|---|---|---|
| C-1 | ADSP overstated $48M; goodwill inflated $76.5M | Critical | Memo vs. Thornfield PPA / Reg. 1.338-4 | Recompute ADSP; reissue memo & allocation |
| C-2 | S corp eligibility unverified (3 holders + family-LLC transfer + expired W-9s) | Critical | Memo Sec. III.A vs. Thornfield III.B, cap table | Documentation; §1362(f) contingency; escrow/indemnity |
| H-1 | Beacon $28.5M interest omitted from Class V | High | Memo allocation vs. PPA | Correct PPA |
| H-2 | Beacon ROFR triggered; 10-business-day notice likely missed | High | Memo vs. Beacon OA §8.03 | Deliver/cure notice; obtain waivers |
| H-3 | $3.8M suspended R&D credits — utilization unanalyzed | High | Memo III.D vs. Thornfield IV.B | Complete §1371 analysis |
| H-4 | §482 exposure ~$6.3M; SPA rep contradicted by OA §9.01 | High | Thornfield VII; SPA §4.9(h) | Quantify; special indemnity; re-paper fees |
| H-5 | QSBS §1202 omitted despite shareholder inquiries | High | Memo (silent) vs. Thornfield VIII.B, cap table | Analysis + shareholder communication |
| H-6 | $37M rollover treatment unanalyzed; entity descriptions inconsistent | High | Memo II.B vs. SPA §2.6(e), cap table | Finalize structure; document tax treatment |
| M-1 | NC data processing license non-transferable; ~$19M revenue at risk | Medium | PPA A-008; SPA §4.9(i) | Legal opinion; DIT confirmation |
| M-2 | Beacon §754/§743(b) election undecided | Medium | PPA Note 2 | Decide and calendar election |
| M-3 | CA/NY state tax and 2024 return timing gaps | Medium | Memo vs. SPA §4.9(c), §7.1 | Expand state analysis; extension |
| M-5 | Citation/date/reg-cite inconsistencies | Medium/Low | Various | Correct in reissued memo |
| L-1 | Basic vs. fully diluted pro-rata ambiguity | Low | Memo vs. cap table | Confirm Schedule 1.1(a) |

---

## 8. Scope and Limitations

This report is based solely on the documents listed above. The shareholder QSBS email thread (.eml) could not be read due to a file conversion failure and should be reviewed separately — it may contain advisor statements or expectations regarding Section 1202 that create additional risk. The Thornfield PPA is marked DRAFT and subject to revision. Nothing herein constitutes legal or tax advice to any shareholder; all shareholders should consult their own advisors.
