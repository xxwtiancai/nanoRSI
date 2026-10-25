# TAX ISSUE IDENTIFICATION REPORT
## Review of Tax Structure Memorandum (Calloway, Stern & Whitaker LLP, Feb. 10, 2025) — Project Prism / Ridgeline Acquisition of Prism Health Analytics, Inc.

**PRIVILEGED AND CONFIDENTIAL — ATTORNEY WORK PRODUCT**
*Prepared for Ridgeline Capital Partners Fund III, LP*

---

## Sources Reviewed

| Document | Status |
|---|---|
| transaction-structure-memo.docx (CSW tax structure memo, 2/10/2025) | Reviewed |
| purchase-agreement-excerpts.docx (Agreement and Plan of Merger, 1/28/2025) | Reviewed |
| tax-due-diligence-report.docx (Thornfield Accounting Group, 1/15/2025 — DRAFT) | Reviewed |
| prism-cap-table.xlsx (as of 12/31/2024) | Reviewed |
| asset-valuation-summary.xlsx (Thornfield preliminary PPA) | Reviewed |
| beacon-operating-agreement.docx (A&R Operating Agreement, eff. 8/1/2018, excerpts) | Reviewed |
| shareholder-qsbs-email-thread.eml | **UNREADABLE** — conversion failed after two attempts. Findings that depend on this source (shareholder QSBS representations, Section 1202 positions) are **preliminary and subject to confirmation**. QSBS-related themes are corroborated in part by the Thornfield report (§ VIII.B) and the cap table notes. |

---

## I. Executive Summary

The CSW tax structure memorandum recommends a Section 338(h)(10) election in connection with Ridgeline Fund III's $425,000,000 acquisition of Prism Health Analytics, Inc. Our review identifies **material errors and omissions** that, if uncorrected, would affect the validity of the election, the purchase price allocation filed on Form 8883, and shareholder-level tax outcomes:

1. **CRITICAL — ADSP computed incorrectly; $48,000,000 double-count.** The memo computes Aggregate Deemed Sale Price as $473,000,000 (enterprise value $425M + $48M funded debt). Because enterprise value already includes the debt component, this double-counts the funded debt. The correct ADSP under Treas. Reg. 1.338-4, starting from the $370,000,000 amount realized on the stock plus target liabilities ($48M debt + $7M seller expenses), is **$425,000,000**. The memo's error inflates Class VII goodwill by $76,500,000 ($48M ADSP overstatement + $28.5M Beacon omission — see items 2 and 3 below). (Asset-Valuation Summary, Allocation Summary tab, Note 1.)

2. **CRITICAL — S corporation validity unconfirmed for three shareholders; the memo asserts eligibility without qualification.** The cap table flags **three** restricted stock holders with unverified eligibility (Lin Wei Zhang — H-1B/PRC citizen; Yusuf Al-Rashidi — dual citizen, documentation missing; Nina Petrova — green card status unconfirmed), and Thornfield flags a possible 2021 transfer to a "Family Holdings, LLC" that would be an ineligible shareholder. The memo states "we are not aware of any ineligible shareholders" — contradicted by the diligence record. If the S election was inadvertently terminated, the Section 338(h)(10) election is unavailable and entity-level C corporation tax applies for all open years.

3. **HIGH — Beacon Insights interest ($28,500,000) omitted from Class V allocation.** The memo's Class V of $68,500,000 excludes the 80.5% Beacon partnership interest (Thornfield FMV $28.5M), misdirecting that value into the Class VII goodwill residual and affecting amortization treatment (§197 15-year vs. look-through/§754 analysis).

4. **HIGH — Beacon right of first refusal triggered by the merger; no waiver/consent addressed.** Beacon OA § 8.03(a)(ii) triggers the ROFR upon a Change of Control of any entity Member. The merger is expressly a "change of control" (Merger Agreement § 2.3(d)). Neither the memo nor the diligence summary addresses delivery of a ROFR Notice or waivers from Marcus Delano and Shirin Avesta. The memo mentions the ROFR only in passing and takes no position.

5. **HIGH — Non-transferable NC Data Processing License (DIT-2019-04821).** The license supporting ~$19M of annual government-sector revenue is non-transferable/non-assignable (Merger Agreement § 4.9(i); Valuation Summary A-008). The memo does not analyze whether the license survives the reverse triangular merger or is terminated by the deemed asset sale; value and revenue are at risk.

6. **MEDIUM/HIGH — QSBS (Section 1202) analysis omitted.** The memo does not address QSBS at all, despite shareholder inquiries (Thornfield § VIII.B; cap table notes; unreadable email thread). Most shareholders acquired stock from the C corporation in 2016 and could claim up to $10M–$50M of gain exclusion each; a 338(h)(10) election converts stock-sale capital gain into pass-through deemed-asset-sale gain, potentially destroying QSBS eligibility. Quantifiable shareholder-level impact is potentially tens of millions of dollars; analysis must be confirmed against the unreadable email thread.

7. **MEDIUM — Rollover equity ($37,000,000) interaction with 338(h)(10) not analyzed.** Chandra's rollover into a Fund III vehicle raises qualification issues for the 100%-acquisition requirement (Treas. Reg. 1.338-2(c)) and gain-recognition mechanics; the memo defers entirely to the (unreviewed) Chandra Rollover Agreement. The cap table flags this same omission.

8. **MEDIUM — Suspended C corporation R&D credits ($3,800,000) likely permanently lost; memo defers.** Memo § III.D "notes" the credits; Thornfield concludes utilization is unclear and the credits are at significant risk of permanent expiration upon deemed liquidation (Thornfield § IV.B).

9. **MEDIUM — Section 482 transfer pricing exposure (~$6,300,000, 2019–2024) understated in the memo.** The memo repeats the SPA rep that intercompany fees ($850K management; $400K IP license) are arm's length; Thornfield estimates $6.3M cumulative exposure, and the Beacon OA § 9.01 confirms no benchmarking study has ever been performed.

10. **LOW/MEDIUM — Diligence documents relied on are DRAFTS; memo dates and characterizations are loose.** The memo is dated 2/10/2025 but cites a Thornfield report "dated January 10, 2025" (actual: January 15, 2025, marked CONFIDENTIAL — DRAFT); the memo also cites "Section 7.04" of the SPA for the 338(h)(10) consent covenant, while the excerpted agreement places the election provisions in **Section 7.3**. The memo mis-cites the check-the-box regulation as "Treas. Reg. 1.301-7701-3" (correct: § 301.7701-3).

**Recommended immediate actions** are set out in Section IV.

---

## II. Ranked Findings

### CRITICAL

**C-1. ADSP overstated by $48,000,000 due to double-counting of funded debt.**
- *Memo says:* ADSP is $473,000,000, derived from the $425,000,000 enterprise value plus $48,000,000 of liabilities (Memo § I; Allocation table).
- *Supporting documents say:* Thornfield's valuation summary (Allocation Summary tab, Note 1) computes ADSP = $370,000,000 (amount realized on stock: $333M cash + $37M rollover) + $48,000,000 funded debt + $7,000,000 seller transaction expenses = **$425,000,000**. Enterprise value already embeds the debt (EV = equity + net debt), so adding $48M again double-counts.
- *Consequence:* Form 8883 allocation as drafted would be wrong on its face; Class VII goodwill overstated (see C-2/H-1); seller/shareholder pass-through gain misstated by up to $48M; risk of IRS examination adjustment and valuation-penalty exposure.
- *Action:* Recompute ADSP per Treas. Reg. 1.338-4 from the $370M amount realized; reconcile the $7M seller expense treatment (liability of old target vs. shareholder-borne cost) before filing.

**C-2. Class VII goodwill overstated by $76,500,000 in the memo's allocation.**
- *Memo says:* Goodwill/going concern residual = $272,800,000 ($473M − $200.2M Classes I–VI).
- *Supporting documents say:* Thornfield computes $196,300,000 ($425M − $228.7M). Variance of $76.5M = $48M ADSP error (C-1) + $28.5M Beacon Class V omission (H-1). (Valuation Summary, Allocation Summary tab.)
- *Consequence:* Misstated §197 amortization schedule (~$5.1M/year delta at 15-year amortization), affecting buyer's post-closing tax returns and the purchase price allocation delivered under SPA § 7.3(b).
- *Action:* Restate allocation before the 90-day post-closing Allocation process under SPA § 7.3(b).

**C-3. S corporation shareholder eligibility unverified for three restricted stock holders; possible 2021 transfer to a family LLC.**
- *Memo says:* "All shareholders of Prism are U.S. individuals, and we are not aware of any ineligible shareholders" (Memo § III.A).
- *Supporting documents say:* Cap table flags **Lin Wei Zhang** (H-1B, PRC citizen — substantial presence not verified), **Yusuf Al-Rashidi** (dual U.S./Jordanian; documentation not on file), **Nina Petrova** (Bulgarian-born; green card not confirmed). Thornfield § III.B flags the H-1B holder and an annotated 2021 "transfer to [name] Family Holdings, LLC," with no response from Company counsel. The SPA rep (§ 4.9(a)) that all shareholders are eligible is a representation, not verified fact.
- *Consequence:* If the S election terminated in any year since 1/1/2017, the 338(h)(10) election is unavailable (an S corporation is a prerequisite), entity-level C corporation tax applies for open years with interest and penalties, and the entire transaction structure fails. Unverified holders are receiving $2,775,000 in aggregate consideration (cap table, Consideration Waterfall).
- *Action:* Make closing conditional on definitive eligibility documentation for all three holders and written resolution of the alleged family-LLC transfer; prepare a Section 1362(f) inadvertent-termination relief strategy as a fallback.

### HIGH

**H-1. Beacon Insights 80.5% interest ($28,500,000) omitted from Class V.**
- *Memo says:* Class V = $68,500,000, "as described in Section IV.C," with the Beacon interest stated (Memo § III.C) to be a Class V asset but not reflected in the allocation.
- *Supporting documents say:* Thornfield's Class V totals $97,000,000, including the Beacon interest at $28,500,000 (Asset A-009; Valuation Summary Note 2).
- *Consequence:* $28.5M of value misclassified into 15-year §197 goodwill rather than the partnership-interest class; buyer forgoes correct basis/amortization analysis; §754 election decision for Beacon unaddressed.
- *Action:* Restate Class V to include the Beacon interest; determine whether Beacon should make a §754 election and prepare §743(b) computations (Valuation Summary Note 2).

**H-2. Beacon ROFR triggered by the merger; consent/waiver path unaddressed.**
- *Documents:* Beacon OA §§ 8.03(a)(ii) (ROFR on Change of Control of an entity Member), 8.03(b)–(f) (10-business-day notice, 45-day exercise, cash closing). Merger Agreement § 2.3(d) states the Merger constitutes a change of control "under any... operating agreement." Memo § III.C notes the ROFR exists "including a right of first refusal" but takes no position.
- *Consequence:* If notice is not given and waivers not obtained, Delano (12.0%) and Avesta (7.5%) could exercise the ROFR over Prism's 80.5% interest at "Fair Market Value" without minority discounts (OA § 8.04(d)) — a direct threat to deal structure and to the $28.5M valuation.
- *Action:* Deliver a ROFR Notice now (the 10-business-day window from signing on 1/28/2025 has already lapsed if measured from execution — obtain waivers immediately) and build ROFR expiry/waiver into closing conditions.

**H-3. Non-transferable NC Data Processing License (DIT-2019-04821).**
- *Documents:* Merger Agreement § 4.9(i) (license "non-transferable and non-assignable"); Valuation Summary A-008 ($0 FMV assigned; ~$19M annual government revenue partially dependent; survival must be legally confirmed).
- *Memo:* Silent on license survival/termination under the deemed asset sale.
- *Consequence:* If the license does not survive the merger or is deemed transferred in the 338(h)(10) deemed asset sale, government-sector revenue is impaired and PPA values (and enterprise value support) must be revisited.
- *Action:* Obtain NC DIT confirmation or re-issuance commitment pre-closing; confirm SPA treatment.

**H-4. QSBS / Section 1202 analysis entirely omitted.**
- *Documents:* Thornfield § VIII.B (QSBS questions raised through Linden Rock; interaction with 338(h)(10) "not analyzed"); cap table notes (most shareholders acquired stock 8/15/2016–11/1/2016 during the C corporation window; Elena Vargas's 3/1/2017 stock is ineligible under §1202(c)(1)); shareholder email thread (unreadable — content unverified).
- *Memo:* No mention of Section 1202.
- *Consequence:* A 338(h)(10) election generally causes gain to arise from a deemed asset sale at the entity level, passing through as ordinary/§1231/ordinary-recapture character items rather than stock-sale gain — likely eliminating QSBS exclusion for eligible shareholders (potentially up to $10M of gain exclusion per eligible non-corporate shareholder, plus possible triple exemption under §1202(b)(2) for joint filers). Shareholders consenting to the election under Treas. Reg. 1.338(h)(10)-1(c)(3) without this analysis face material, quantifiable tax detriment; seller-side consent to the election (a closing condition under SPA § 7.3(a)) is at risk.
- *Action:* Perform a full §1202 analysis (active business, $50M gross assets test at and after issuance, original issuance, 5-year holding — all 2016 issuers satisfy holding by closing) and communicate consequences to shareholders before consents are executed. **Confirm against the unreadable email thread.**

**H-5. Memo asserts no entity-level tax and clean eligibility while relying on DRAFT diligence.**
- *Documents:* Thornfield report is marked "CONFIDENTIAL — DRAFT" and disclaims independent verification; the memo treats its conclusions as settled.
- *Consequence:* Overstated comfort to the Investment Committee; the memo should carry equivalent qualifications.
- *Action:* Revise memo to reflect draft-status reliance and open items.

### MEDIUM

**M-1. Rollover equity ($37,000,000) mechanics unanalyzed.**
- *Documents:* Memo § II.B defers to "the Stock Purchase Agreement and related subscription documents"; the Chandra Rollover Agreement (Exhibit C) is not in the record; cap table notes flag the omission. The rollover buyer is stated inconsistently — "Parent (or a designated acquisition vehicle)" (SPA) vs. "Newco" (memo § II.B) vs. "Ridgeline Acquisition Sub, Inc." (cap table).
- *Consequence:* The qualified stock purchase requirement (acquisition of 100% of stock, Treas. Reg. 1.338-2(c)) and gain-recognition treatment of the rollover depend on structure; inconsistency in the identity of the rollover vehicle must be resolved.
- *Action:* Analyze rollover against §338(h)(10) mechanics; obtain and review the Chandra Rollover Agreement; conform entity references.

**M-2. Suspended federal R&D credits ($3,800,000) — utilization unresolved.**
- *Documents:* Memo § III.D (credits "noted"); Thornfield § IV.B (§1371(b) suspension; PTTP under §1371(e); permanent-loss risk; recommendation that counsel analyze §§1371(b)/(e)/1374/338(h)(10)).
- *Consequence:* Up to $3.8M of credits permanently lost on deemed liquidation; memo performs none of the recommended analysis.
- *Action:* Complete the §1371 interaction analysis pre-closing and reflect any value in the price.

**M-3. Section 482 transfer pricing exposure (~$6,300,000, 2019–2024).**
- *Documents:* Thornfield Exec. Summary item 3 and § VII (fees "appear to be below arm's-length"; no transfer pricing study); Beacon OA § 9.01 (fee never benchmarked, CPI-capped, volume-independent). Memo § III.C repeats the arm's-length rep without flagging the exposure.
- *Consequence:* Pre-closing tax exposure that flows through to the deemed sale basis/gain computations; indemnity/escrow coverage should be confirmed.
- *Action:* Quantify exposure; confirm escrow/indemnity allocation for pre-closing periods.

**M-4. Escrow-funded deemed-sale gain timing not addressed.**
- *Documents:* SPA §§ 1.1 (Escrow Amount $22M; release 9/15/2026), 2.6(c)–(d). Memo states the escrow mechanics but does not address whether the full $370M (including escrowed amounts) is included in amount realized/ADSP at closing under the 338(h)(10) regime, or open-transaction treatment.
- *Action:* State the memo's position on escrow inclusion in ADSP and shareholder gain.

**M-5. AAA / deemed liquidation characterization omitted.**
- *Documents:* Thornfield § IV.A (AAA balance $64,200,000 at 12/31/2023, "relevant for characterization of deemed distributions"); memo does not address AAA, E&P from the 2016 C year, or §1368/distribution ordering in the deemed liquidation.
- *Action:* Add analysis of distribution characterization (AAA vs. E&P) in the deemed liquidation.

### LOW

**L-1. Citation errors.** Memo cites "Treas. Reg. 1.301-7701-3" (should be § 301.7701-3) (Memo §§ II.A, III.C) and "Section 7.04 of the Stock Purchase Agreement" for the 338(h)(10) consent condition; the excerpted agreement contains the covenant at **§ 7.3(a)**. Memo cites a Thornfield report "dated January 10, 2025"; the report is dated January 15, 2025 (and its own limitations section references information through January 10, 2025 — likely the source of the error). The valuation summary likewise labels the memo "dated 1/28/2025" though the memo is dated 2/10/2025.

**L-2. California/NY nonresident shareholder filing exposure noted only generically.** Two CA-resident shareholders (Muñoz $7.4M; Yoon $5.55M) bear CA tax on pass-through deemed-sale gain (cap table notes); the memo defers entirely to individual advisors. Consider a supplemental state sourcing discussion.

**L-3. 2024 Form 1120-S due date (3/15/2025) coincides with Closing Date** (Thornfield § IV.A); extension mechanics acknowledged only implicitly. Confirm extension and final-return coordination with SPA § 7.1.

---

## III. Cross-Verification Notes (Computations Recomputed)

- **Equity value:** $425,000,000 − $48,000,000 − $7,000,000 = $370,000,000 — memo, SPA § 1.1, and cap table agree. ✓
- **Consideration waterfall:** $155.4M + $37M + $103.6M + $74M = $370M — consistent across memo § II.C, SPA § 2.6(f), cap table. ✓ (Cap table fully-diluted percentages produce $74,999,231 for the "other" block, adjusted to $74M — immaterial rounding of Priya Srinivasan's line; per-share figures $189.74 basic / $185.46 fully diluted.) ✓
- **ADSP:** Memo $473M vs. Thornfield $425M — memo in error ($48M double-count). ✗
- **Class totals:** Classes I, II, III, IV, VI agree; Class V differs by $28.5M (Beacon); Class VII differs by $76.5M. ✗
- **NUBIG:** $78M − $31.5M = $46.5M; recognition period 1/1/2017–12/31/2021 — memo, SPA § 4.9(f), and Thornfield § III.C agree. ✓ (Conclusion that no §1374 tax applies is contingent on S election validity — see C-3.)
- **Financing:** $190M term loan drawn; Fund III equity $370M − $37M − $190M = $143M — memo internally consistent. ✓

---

## IV. Recommended Actions (Keyed to Findings)

1. **Before signing any Form 8023:** recompute ADSP at $425,000,000 and restate the §1060 allocation (C-1, C-2, H-1).
2. **Immediately** obtain eligibility documentation for Zhang, Al-Rashidi, and Petrova; resolve the alleged family-LLC transfer; condition closing on resolved status (C-3).
3. **Immediately** deliver the Beacon ROFR Notice / obtain written waivers from Delano and Avesta; add ROFR clearance as a closing condition (H-2).
4. Obtain NC DIT written confirmation on license survival or a re-issuance covenant from the Seller (H-3).
5. Complete the §1202 QSBS analysis and disclose consequences to all shareholders **before** collecting 338(h)(10) consents; obtain and review the unreadable shareholder email thread (H-4).
6. Revise the memo to flag draft-diligence reliance (H-5); correct citations (L-1).
7. Analyze the Chandra rollover structure against §338 qualified stock purchase requirements and conform the identity of the rollover vehicle across documents (M-1).
8. Complete the §1371 R&D credit and AAA/deemed-liquidation analyses; take a position on escrow inclusion in ADSP (M-2, M-4, M-5).
9. Quantify §482 exposure and confirm escrow/indemnity coverage for pre-closing tax liabilities (M-3).
10. Confirm extension for the 2024 Form 1120-S and coordinate the final short-year return under SPA § 7.1 (L-3).

---

*This report carries the confidentiality legend of its sources (Privileged & Confidential — Attorney Work Product). One source document (shareholder-qsbs-email-thread.eml) could not be read; all QSBS-related findings are preliminary pending review of that document.*
