# Tax Issue Identification Report
## Review of Tax Structure Memorandum — Project Prism (Ridgeline Capital Partners Fund III, LP / Prism Health Analytics, Inc.)

**Prepared:** February 2025
**Subject documents:** Tax Structure Memorandum (Calloway, Stern & Whitaker LLP, dated Feb. 10, 2025); Agreement and Plan of Merger (excerpts, dated Jan. 28, 2025); Thornfield Accounting Group Tax Due Diligence Report (Jan. 15, 2025); Beacon Insights, LLC Amended & Restated Operating Agreement; Prism Capitalization Table (as of 12/31/2024); Thornfield Preliminary Asset Valuation Summary / Purchase Price Allocation.
**Note on document availability:** The shareholder QSBS email thread (`shareholder-qsbs-email-thread.eml`) could not be opened/converter errors prevented reading; QSBS findings below rely on the due diligence report and capitalization table, which reference those shareholder inquiries.

---

## I. Executive Summary

The Tax Structure Memorandum is generally well organized and reaches a defensible headline conclusion (no Section 1374 built-in gains tax; Section 338(h)(10) election available for an S corporation target). However, our cross-check against the supporting deal documents identified **one critical computational error, one critical unresolved eligibility risk, and several material omissions** that must be resolved before signing/closing and before filing Form 8023/Form 8883:

1. **Critical — ADSP double-count.** The memo states an Aggregate Deemed Sale Price of $473,000,000. Thornfield's reconciliation shows the correct ADSP under Treas. Reg. 1.338-4 is $425,000,000 ($370M amount realized on the stock + $48M funded debt + $7M seller transaction expenses). The memo's figure double-counts the $48M funded debt (already netted out of equity value, then added back on top of enterprise value), overstating ADSP — and goodwill — by $48M.
2. **Critical — Class V omission of Beacon interest.** The memo's $68.5M Class V allocation appears to exclude the $28.5M Beacon Insights, LLC 80.5% partnership interest; combined with the ADSP error, the memo's Class VII goodwill ($272.8M) is overstated by $76.5M versus Thornfield's $196.3M.
3. **Critical — S corporation eligibility unresolved.** The memo asserts "we are not aware of any ineligible shareholders," but both the cap table and the Thornfield report flag **three unverified shareholders** (an H-1B holder, a dual citizen without documentation, and a green-card holder without documentation) plus a possible 2021 transfer to a family LLC. If the S election terminated inadvertently, the Section 338(h)(10) election is unavailable and Prism would owe entity-level tax for all open years.
4. **High — QSBS/Section 1202 analysis omitted.** Despite flagged shareholder inquiries, the memo contains no Section 1202 analysis, even though most founder/angel stock was issued during the 2016 C corporation period and could qualify — materially affecting after-tax proceeds and shareholder consent dynamics.
5. **High — Suspended $3.8M federal R&D credits.** The memo notes the credits but defers analysis; Thornfield warns they are at significant risk of permanent expiration upon the deemed liquidation.
6. **High — Section 482 transfer pricing exposure (~$6.3M).** Intercompany management fee ($850K/yr) and IP license fee ($400K/yr) lack any transfer pricing study and appear below arm's length (per the Beacon operating agreement, the fee has never been benchmarked and does not vary with services).
7. **Medium/High — Beacon ROFR triggered by Change of Control.** The merger is a "Change of Control" of Prism (the Manager-member) and triggers the Beacon members' 45-day right of first refusal; the memo mentions the ROFR only in passing and does not address timing/waiver mechanics against a March 15, 2025 closing.
8. **Medium — Rollover/338(h)(10) interaction unaddressed.** The memo does not analyze whether Dr. Chandra's $37M rollover into a Fund III vehicle satisfies the QSP/consent requirements or its effect on ADSP (Thornfield includes the $37M rollover in the amount realized).
9. **Medium — NC data processing license (DIT-2019-04821).** Non-transferable license supporting ~$19M of government revenue; memo does not address whether the license survives the deemed asset sale. Valued at $0 in the PPA.
10. **Medium — Other items:** escrow-indemnity tax treatment, California/NY state filings for nonresident shareholders, 2024 Form 1120-S due on the closing date, AAA ($64.2M) characterization of deemed distributions, and the memo's reliance on a draft (Jan. 10/15, 2025) Thornfield report.

Issues are ranked Critical / High / Medium below with document citations and recommended actions.

---

## II. Severity-Ranked Findings

### CRITICAL

**C-1. ADSP overstated by $48 million (double-count of funded debt).**
- **Memo (§ I, § IV):** ADSP stated as $473,000,000.
- **Valuation summary (Allocation Summary, Note 1):** Correct ADSP = $370M (amount realized: $333M cash + $37M rollover) + $48M funded debt + $7M seller transaction expenses = **$425,000,000**. The memo starts from enterprise value ($425M, which already embeds debt) and adds $48M again.
- **Impact:** $48M overstatement of ADSP flows entirely to Class VII goodwill; all preliminary allocation figures, Form 8883, and buyer's amortization modeling are wrong. Seller-side deemed-sale gain could also be misstated.
- **Action:** Recompute ADSP per Treas. Reg. 1.338-4 before Form 8023/8883; reconcile with Thornfield.

**C-2. Class V allocation omits Beacon Insights interest; goodwill overstated $76.5M in aggregate.**
- **Valuation summary:** Thornfield Class V = $97.0M (including the $28.5M Beacon 80.5% interest, a Class V asset per Treas. Reg. 1.338-6(b)(2)(v)); memo Class V = $68.5M — a $28.5M variance "attributable entirely" to the Beacon interest. Combined with C-1, memo Class VII goodwill ($272.8M) exceeds Thornfield's ($196.3M) by $76.5M.
- **Related omission:** No analysis of whether Beacon should make a **Section 754 election** / Section 743(b) step-up computations; Thornfield performed no look-through of Beacon's underlying assets (valuation summary, Note 2).
- **Action:** Include Beacon interest in Class V; decide on Beacon §754 election and prepare §743(b) computations.

**C-3. S corporation shareholder eligibility unverified — threshold risk to the entire structure.**
- **Memo (§ III.A):** "No events causing a termination of the S election have been identified… we are not aware of any ineligible shareholders."
- **Thornfield report (§ III.B, Finding #1):** unable to confirm eligibility for restricted stock holders, including a possible Canadian national on an H-1B (substantial presence unverified) and a possible 2021 transfer to a "Family Holdings, LLC" (company counsel unresponsive).
- **Cap table:** flags **three** unverified holders — Lin Wei Zhang (H-1B, PRC citizen), Yusuf Al-Rashidi (U.S./Jordan dual citizen, documentation not on file), Nina Petrova (green card status unconfirmed) — holding in aggregate $2,775,000 of consideration. Also, both California angel investors have expired W-9s (2019).
- **Note discrepancy:** The memo describes "fourteen (14) angel investors and early employees" holding 20%; the cap table shows 16 unique individuals (including 8 restricted stock holders) and a fully diluted total of 1,995,000 shares with founders at 78.20% fully diluted vs. 80% basic — the memo's ownership table uses basic percentages and does not reconcile to fully diluted.
- **Impact:** Inadvertent termination under §1362(d)(2) would make Prism a C corporation — §338(h)(10) unavailable, entity-level tax for open years, penalties/interest, and potential SPA rep breach (SPA §4.9(a)).
- **Action:** Obtain immigration/residency documentation for all three unverified holders for every year since grant; resolve the family-LLC transfer; consider reliance on the §4.9(a) rep and inadvertent-termination relief under §1362(f) as a fallback; refresh W-9s.

### HIGH

**H-1. QSBS / Section 1202 analysis omitted despite flagged shareholder inquiries.**
- **Thornfield report (Finding #4):** angels have raised §1202 eligibility questions; interaction with the 338(h)(10) deemed asset sale "has not been analyzed." (The QSBS email thread itself was unreadable in this review.)
- **Cap table:** founders, angels, and early employees acquired stock 6/14/2016–11/1/2016 — during the C corporation period with a 5-year holding period satisfied by closing (potential QSBS exclusion); Elena Vargas (3/1/2017, S corp-period issuance) is **not** eligible under §1202(c)(1); restricted stock (2020–2023 grants) is also S corp-period issuance.
- **Impact:** Exclusion of up to the greater of $10M or 10x basis could materially change shareholders' after-tax outcomes and their willingness to consent to the 338(h)(10) election; note that a 338(h)(10) election generally converts stock-sale gain into pass-through deemed-asset-sale gain, putting QSBS capital-gain treatment at risk — this tension is nowhere analyzed in the memo.
- **Action:** Prepare a shareholder-by-shareholder §1202 analysis (gross assets test, active business test, original issuance, holding periods) and quantify the cost/benefit of the 338(h)(10) election for QSBS-eligible holders.

**H-2. Suspended $3.8M federal R&D credits — expiration risk unanalyzed.**
- **Memo (§ III.D):** credits "noted and will be addressed in post-closing tax planning."
- **Thornfield report (§ IV.B):** credits suspended under §1371(b)(1); likely permanently lost upon deemed liquidation; recommends counsel analyze §§1371(b)/(e), 1374, 338(h)(10) for salvage/structuring options.
- **Action:** Complete that analysis before closing; consider indemnity or purchase-price adjustment if value is lost.

**H-3. Section 482 transfer pricing exposure (~$6.3M cumulative, 2019–2024).**
- **SPA §4.9(h):** fees represented as arm's length; **"No formal transfer pricing study has been prepared."**
- **Beacon operating agreement §9.01:** management fee never benchmarked since 2018 and does not adjust with actual volume/scope/cost of services — corroborating Thornfield's below-arm's-length conclusion.
- **Impact:** Pre-closing tax exposure for an S corporation flows through to selling shareholders; also affects post-closing intercompany pricing and Beacon's value.
- **Action:** Quantify exposure, address via indemnity/escrow or pre-closing true-up; commission a benchmarking study.

**H-4. Beacon ROFR triggered by the Change of Control — timing risk to closing.**
- **Beacon operating agreement §§8.03(a)(ii), (b)–(e):** a Change of Control of any entity member triggers the ROFR; Prism must deliver a ROFR Notice within 10 business days of signing the SPA (executed Jan. 28, 2025); Delano/Avesta then have a 45-day exercise period. The memo mentions the ROFR only as a "customary transfer restriction."
- **Impact:** If not waived, members could seek to purchase Prism's 80.5% interest at Fair Market Value, jeopardizing the acquisition of a $28.5M asset.
- **Action:** Confirm ROFR Notice was timely delivered and obtain written waivers from Delano and Avesta as a closing deliverable.

### MEDIUM

**M-1. Rollover equity / 338(h)(10) interaction not analyzed.**
- **Memo (§ II.B):** Dr. Chandra contributes $37M to "Newco"/Parent vehicle; cap table notes "Memo does not address interaction of rollover with 338(h)(10) deemed sale." Issues include whether the rollover is part of the QSP consideration (Thornfield includes it in amount realized), boot/SOEI characterization, and the correct rollover vehicle (memo references both "Newco" and Parent/SPA-defined "Rollover Equity" in Parent or a designated vehicle — internally inconsistent). Also note cap table says rollover is into "Ridgeline Acquisition Sub, Inc." (which ceases to exist in the merger), an apparent drafting error.

**M-2. NC Data Processing License (DIT-2019-04821) treatment unresolved.**
- **SPA §4.9(i) / valuation summary A-008, Note 3:** license is non-transferable/non-assignable; supports ~$19M annual government revenue; $0 FMV in PPA; memo is silent on whether it survives the merger/deemed asset sale and on value reallocation if terminated.

**M-3. Escrow/indemnity tax treatment omitted.**
- **SPA §§2.6(c)–(d), Escrow Release Date 9/15/2026; cap table** shows $22M pro rata holdback. The memo does not address whether escrow amounts are amounts realized at closing (open transaction/closed transaction characterization) or indemnity payment consequences for buyer and sellers.

**M-4. State tax gaps.**
- Nonresident shareholders (2 CA, 1 NY, plus a VA Beacon member) will have pass-through deemed-sale gain sourced to CA/NY; memo "notes briefly" CA entity-level tax and defers individual advice. CA entity-level 1.5% S tax and NY fixed dollar minimum are represented as paid (SPA §4.9(c)) but not independently verified. NC conformity to the 338(h)(10) election should be confirmed (memo asserts "applicable state" treatment without analysis).

**M-5. 2024 Form 1120-S timing conflict.**
- **Thornfield report (§ IV.A):** 2024 return due March 15, 2025 — the same day as closing; extension "will likely be required." Memo does not address the final short-year return coordination with SPA §7.1 (30-day buyer review right) and §7.2 closing-of-the-books straddle method.

**M-6. AAA / deemed liquidation characterization not analyzed.**
- **Thornfield report (§ IV.A):** AAA balance $64.2M (12/31/2023) "will be relevant for the characterization of deemed distributions" — the memo's (truncated) liquidation discussion does not address AAA/OAA ordering, which affects whether distributions are tax-free to shareholders.

**M-7. Memo factual discrepancies / dating.**
- Memo says it relies on the Thornfield report "dated January 10, 2025," while the report is dated January 15, 2025 (and marked **CONFIDENTIAL — DRAFT**); the memo also refers to a "Stock Purchase Agreement" while the operative document is an "Agreement and Plan of Merger" (reverse triangular merger). Memo cites the wrong regulation reference ("Treas. Reg. 1.301-7701-3" for check-the-box). Memo's "20% other shareholders / 14 individuals" does not tie to the cap table's 16 individuals / 19.92–20% fully diluted detail. The memo's §338(h)(10) reference to "Section 7.04 of the Stock Purchase Agreement" for consents does not match the SPA's numbering (election provisions are in §7.3(a)).
- The memo's consideration table allocates per **basic** percentages while the cap table's fully diluted percentages differ (e.g., Chandra 50.83% FD); confirm the intended allocation basis (the SPA uses "Pro Rata Share," schedule not provided).

### LOW

**L-1.** Beacon management fee CPI escalation (3% cap, operating agreement §9.01) and the IP License Agreement terms are not reflected in the memo's intercompany discussion; confirm post-closing treatment.
**L-2.** Prism Data Services EIN presentation (memo lists its own EIN 86-5512340 while noting it uses Prism's EIN) — minor, but should be conformed for Form 8883 schedules.
**L-3.** The memo's escrow "anticipated release date: September 15, 2026" matches the SPA — no issue; noted as verified. Several other figures verified as consistent: equity value waterfall ($370M totals), NUBIG ($46.5M), BIG recognition period expiration (12/31/2021), 45,000 restricted shares with 83(b) elections, Beacon ownership 80.5/12.0/7.5.

---

## III. Verified Consistencies (no issue)

- Equity value build: $425M − $48M − $7M = $370M; cash/rollover split $333M/$37M; per-shareholder totals tie to SPA §2.6(f).
- Built-in gains: recognition period expired 12/31/2021; NUBIG $46.5M ($78M − $31.5M) — memo, SPA §4.9(f), and Thornfield all agree.
- Restricted stock: 45,000 shares / ~2.3% fully diluted, 8 holders, timely 83(b) elections — memo, SPA §2.5, Thornfield, cap table all agree.
- Class III and Class VI allocations agree between the memo and Thornfield ($24.3M and $95.0M respectively).

## IV. Recommended Action Plan (Priority Order)

1. Reissue corrected ADSP/PPA ($425M ADSP; Beacon interest in Class V; §754 decision for Beacon) before Form 8023/8883 (C-1, C-2).
2. Close out S eligibility documentation for Zhang, Al-Rashidi, Petrova, the alleged family-LLC transfer, and expired CA W-9s; make closing condition (C-3).
3. Complete §1202 QSBS shareholder analysis and quantify election cost for eligible holders (H-1).
4. Analyze §1371(b)/(e) salvage of the $3.8M R&D credits pre-closing (H-2).
5. Address §482 exposure via study, true-up, or indemnity (H-3).
6. Deliver/obtain Beacon ROFR notice and waivers; confirm license (DIT-2019-04821) survival (H-4, M-2).
7. Supplement memo on rollover mechanics, escrow tax treatment, AAA ordering, straddle/final-return logistics, and state conformity (M-1, M-3–M-6).
8. Correct the memo's cross-references, document names/dates, and ownership-table basis (M-7).

*This report is based solely on the documents listed above; the QSBS email thread could not be reviewed and its contents should be separately confirmed.*
