# Tax Issue Identification Report
## Review of Tax Structure Memorandum — Project Prism (Ridgeline Capital Partners Fund III, LP / Prism Health Analytics, Inc.)

**Prepared for:** Ridgeline Capital Partners Fund III, LP — Investment Committee
**Subject:** Issues, inconsistencies, and omissions identified in the Calloway, Stern & Whitaker LLP ("CSW") Tax Structure Memorandum dated February 10, 2025, reviewed against: the Agreement and Plan of Merger dated January 28, 2025 (excerpts); the Thornfield Accounting Group Tax Due Diligence Report (January 15, 2025); the Asset Valuation Summary / preliminary PPA (Thornfield, draft); the Prism capitalization table; and the Beacon Insights, LLC Amended and Restated Operating Agreement.
**Note:** The shareholder QSBS email thread (.eml) could not be opened/converted in this review environment; QSBS findings below are based on the diligence report and cap table.

---

## Executive Summary

The CSW memorandum correctly identifies the basic architecture of the transaction — a reverse triangular merger qualifying as a qualified stock purchase, a joint Section 338(h)(10) election, expiration of the Section 1374 built-in gains recognition period on December 31, 2021, and single-level taxation of deemed asset sale gain to the S corporation shareholders. However, the review identifies **material errors and omissions** that must be resolved before signing/closing and before filing Form 8023 and Form 8883:

1. **The memorandum's ADSP of $473,000,000 double-counts the $48,000,000 of funded debt.** Thornfield's computation supports an ADSP of $425,000,000 ($370M amount realized + $48M debt + $7M expenses). The error inflates Class VII goodwill by $48M (memo: $272.8M vs. Thornfield: $196.3M) and overstates buyer's amortization benefit by roughly $3.2M/year over 15 years — an IRS audit flag and a buyer/seller fairness issue.
2. **The S corporation election — the threshold requirement for the 338(h)(10) election — is not confirmed.** The cap table flags three restricted stock holders with unverified eligibility (Lin Wei Zhang, H-1B; Yusuf Al-Rashidi; Nina Petrova), and the diligence report identifies a possible 2021 transfer of restricted stock to a family LLC that would be an ineligible shareholder. The memo affirmatively (and inconsistently with the diligence record) states that "no events causing a termination of the S election have been identified."
3. **The memo's Class V allocation omits the $28.5M Beacon Insights partnership interest**, and the memo does not analyze the Beacon right of first refusal triggered by Prism's change of control, the advisability of a Beacon Section 754 election, or the non-transferable NC data processing license supporting ~$19M of government revenue.
4. **The memo omits analysis of:** QSBS (Section 1202) eligibility for the C-corporation-period shareholders; the rollover's interaction with the 338(h)(10) deemed sale and the qualified stock purchase tests; the likely permanent loss of $3.8M in suspended 2016 R&D credits; Section 482 exposure (~$6.3M) on under-market intercompany fees; and state tax conformity issues.

Severity is ranked Critical / High / Medium / Minor below. Recommended actions appear in the final section.

---

## Severity Framework

- **Critical:** Could invalidate the intended tax structure or produce a material, unrecoverable tax cost.
- **High:** Material dollar impact or closing-condition risk; must be resolved before closing.
- **Medium:** Material but manageable; requires analysis, documentation, or protective drafting.
- **Minor:** Clerical, citation, or disclosure-quality items.

---

## Critical Issues

### C-1. Unverified S corporation shareholder eligibility — S election validity is the foundation of the entire structure
- **Memo position:** "No events causing a termination of the S election have been identified. All shareholders of Prism are U.S. individuals, and we are not aware of any ineligible shareholders."
- **Contrary evidence:** (i) The cap table marks **three** restricted stock holders as unverified: **Lin Wei Zhang** (PRC citizen, H-1B visa; substantial presence not confirmed for all years since her 1/15/2021 grant), **Yusuf Al-Rashidi** (dual U.S./Jordan citizen; citizenship documentation not on file), and **Nina Petrova** (Bulgarian-born; green card status unconfirmed). (ii) The Thornfield report identifies a 2021 stock-ledger annotation referencing a **transfer to a family LLC** — an ineligible shareholder if it occurred — and notes company counsel has not responded to document requests. (iii) Two California angel shareholders have W-9 forms expired since 2019.
- **Consequence:** If any holder was ineligible in any year after 1/1/2017, the S election terminated under Section 1362(d)(2), Prism was a C corporation for all subsequent years (entity-level tax, penalties, and interest for open years), the Section 1374 analysis changes entirely, and **the Section 338(h)(10) election is unavailable**.
- **Note:** The memo says restricted stock holders are included in the "14 other shareholders," and SPA §2.5 contains a blanket representation that all restricted stock holders are U.S. citizens or residents — a representation currently unsupported by the diligence record. If inadvertent termination occurred, a Section 1362(f) relief application may be the only salvage path.
- **Action:** Do not close on the strength of the rep alone. Obtain immigration/residency documentation for Zhang, Al-Rashidi, and Petrova covering all years since grant; obtain the family LLC transfer documentation and the LLC's classification/member composition; refresh the two expired W-9s.

### C-2. ADSP overstated by $48,000,000 — double-count of funded debt
- **Memo position:** ADSP = $473,000,000 (enterprise value $425M + $48M liabilities).
- **Thornfield computation:** ADSP = amount realized on the stock ($370M = $333M cash + $37M rollover) + target liabilities ($48M debt + $7M seller transaction expenses) = **$425,000,000**.
- **Why the memo is wrong:** Enterprise value already embeds the debt (EV = equity + net debt). Starting from EV and adding debt back again double-counts the $48M. This overstates the residual Class VII goodwill (memo $272.8M vs. Thornfield $196.3M) and, if filed on Form 8883, would overstate the buyer's Section 197 amortization by ~$48M/15 = ~$3.2M per year — a high-exam-risk position and an economic windfall to the buyer at the sellers' expense.
- **Action:** Recompute ADSP under Treas. Reg. 1.338-4 before Form 8023/8883; reconcile the memo and the PPA; also resolve whether the $48M debt is "assumed" (memo) or "repaid at closing per payoff letters" (SPA §2.6(a)) — the liability-inclusion mechanics for ADSP differ.

---

## High-Severity Issues

### H-1. Class V allocation omits the $28.5M Beacon Insights partnership interest
- Memo Class V = $68.5M; Thornfield Class V = $97.0M. The entire $28.5M variance is the Beacon 80.5% interest (FMV $28.5M, outside basis $6.4M), properly a Class V asset. Combined with C-2, this drives the full $76.5M Class VII variance. **Action:** Correct the allocation; perform a look-through of Beacon's underlying assets; evaluate a Beacon **Section 754 election** and prepare §743(b) computations so the buyer actually obtains amortizable basis in Beacon's inside assets (absent it, a Class V step-up in a partnership interest generally yields **no** amortizable basis).

### H-2. Beacon right of first refusal triggered by the merger
- Beacon OA §8.03(a)(ii) makes a **Change of Control of any entity Member** a ROFR triggering event; §8.03(b) requires a ROFR Notice within 10 business days of signing (January 28, 2025 — notice timing has likely already lapsed), with a 45-day exercise period for Delano and Avesta. The merger is plainly a Change of Control of Prism (SPA §2.3(d)). The memo mentions only "customary transfer restrictions, including a right of first refusal" and provides no compliance analysis. Failure could invalidate the deemed transfer of Prism's interest or create litigation risk. **Action:** Confirm ROFR notice delivery/waivers immediately; consider a closing condition and a specific indemnity.

### H-3. Dr. Chandra's $37M rollover — interaction with 338(h)(10) and internal inconsistencies
- The memo states rollover equity will be contributed to "Newco" in exchange for "membership interests," while the SPA (§1.1, §2.4(b)) provides for equity interests in **Parent (Fund III, LP) or a designated acquisition vehicle**; the cap table notes rollover into "Ridgeline Acquisition Sub, Inc." These are inconsistent descriptions with different tax results.
- Substantively, the memo never analyzes: (i) whether the rollover shares count toward the 80% "purchase" requirement of §338(d)(3) (shares held by a continuing related person can taint the qualified stock purchase and, in turn, the 338(h)(10) election); (ii) whether the rollover is treated as part of the deemed asset sale (taxable at Dr. Chandra's 52% share of deemed gain) with reinvestment, or as a non-taxable exchange — a materially different after-tax outcome for the CEO; and (iii) gain recognition timing on the rollover interest in a partnership acquiror.
- **Action:** Re-paper the rollover structure, reconcile the memo/SPA/cap-table descriptions, and model the after-tax result for Dr. Chandra.

### H-4. NC Data Processing License (No. DIT-2019-04821) — non-transferable; supports ~$19M revenue
- The license is non-transferable and non-assignable (SPA §4.9(i); valuation summary asset A-008 assigns $0 FMV). Whether it survives a reverse triangular merger (legal continuity of Prism Data Services) versus being "deemed transferred" in the 338(h)(10) asset context must be confirmed; if terminated, ~$19M of annual government revenue is at risk, affecting both enterprise value and the PPA. The memo does not address this at all. **Action:** Legal opinion/confirmation from NC DIT; reallocate any embedded value to goodwill; consider value impairment and indemnity coverage.

### H-5. Suspended federal R&D credits ($3.8M) treated dismissively
- The memo notes the credits "will be addressed in the post-closing tax planning." Thornfield's analysis: under §1371(b) the credits cannot be used in S years; with no §1374 BIG tax (recognition period expired) and no C-corp tax from the deemed sale, the credits are at **significant risk of permanent loss** upon the deemed liquidation. **Action:** Counsel should analyze §§1371(b)/(e) and 338(h)(10) interactions for any salvage path; absent a path, treat as lost and reflect in price expectations.

---

## Medium-Severity Issues

### M-1. QSBS (Section 1202) analysis omitted
- The diligence report flags unresolved shareholder QSBS questions; the cap table shows most angels and both founders acquired stock **during the 2016 C corporation period** at original issuance (founders 6/14/2016; angels/employees 8/15/2016–11/1/2016), with 5-year holding periods satisfied — potentially substantial §1202 exclusion (subject to the $50M gross assets test and active business requirements, both unverified). Elena Vargas's 3/1/2017 stock is **not** QSBS (issued by an S corporation, §1202(c)(1)). The memo contains no §1202 discussion; shareholders are making decisions based on expected gain character. Note: a 338(h)(10) election generally does not convert shareholders' stock-sale gain into asset-sale character for §1202 purposes, but this should be confirmed and communicated.

### M-2. Section 482 transfer pricing exposure (~$6.3M cumulative)
- The memo describes the Beacon management fee ($850K/yr) and IP license fee ($400K/yr) neutrally. The Beacon OA itself states the management fee **has never been benchmarked**, does not vary with scope/cost of services, and caps annual increases at CPI/3%; the SPA rep (§4.9(h)) says "arm's length" while conceding **no transfer pricing study exists**; Thornfield estimates **~$6.3M of §482 exposure (2019–2024)** with fees apparently below arm's length. **Action:** Obtain a transfer pricing study pre-closing; assess buyer's successor exposure; address via indemnity/escrow.

### M-3. Escrow ($22M, 18 months) tax timing unaddressed
- The memo describes escrow mechanics but does not analyze open/closed transaction treatment, whether deemed asset sale gain is recognized in full at closing notwithstanding the escrow, or the character of later escrow releases/forfeitures (capital loss vs. ordinary claim-of-right) for shareholders. This materially affects shareholders' estimated-payment obligations for the 2025 deemed gain.

### M-4. State tax analysis is thin
- The memo promises detailed NC analysis and only "notes" California. Open items: NC conformity to the 338(h)(10) election (confirm the state form referenced in the SPA's "338(h)(10) Forms" definition is filed); California 1.5% entity-level S corp tax and CA-source pass-through gain for Muñoz and Yoon; NY fixed-dollar minimum tax and NY-resident (Okoye) consequences; and multi-state allocation of the deemed asset sale gain among shareholders.

### M-5. AAA / deemed liquidation characterization
- Thornfield reports AAA of ~$64.2M at 12/31/2023. The memo does not walk through AAA/distribution ordering in the deemed liquidation, which affects the character of deemed distributions (including any E&P from the 2016 C year) and shareholder-level outcomes. Confirm this analysis exists.

### M-6. 2024 Form 1120-S filing deadline coincides with closing
- The 2024 return is due March 15, 2025 — the expected Closing Date. An extension will be required; the memo does not address the final short-year return (SPA §7.1), estimated payments for the deemed sale gain, or K-1 timing.

---

## Minor Issues

1. **Citation error:** The memo cites "Treas. Reg. 1.301-7701-3" for disregarded-entity classification; the correct citation is **Treas. Reg. §301.7701-3** (cited correctly in SPA §4.9(k)).
2. **Shareholder-count presentation:** The memo's "14 angel investors and early employees" holding 20% conflates angels and the eight restricted stock holders; the cap table shows 18 holder lines / 16 unique individuals. The consent list for Form 8023 must match Schedule 1.1(a) exactly.
3. **Date inconsistencies:** The memo references the Thornfield report "dated January 10, 2025"; the report is dated **January 15, 2025**. The valuation summary references a "CSW memo dated 1/28/2025"; the memo is dated **February 10, 2025** — a version-control concern given the memo is the operative structuring document.
4. **Unreviewable QSBS email thread** (file conversion failure); shareholder §1202 communications may contain additional representations that should be reconciled with counsel's analysis before closing.
5. **Escrow pro rata funding:** escrow is drawn only from cash-receiving shareholders; the memo does not confirm Dr. Chandra's escrow share excludes rollover value (cap table confirms it does — $10.26M escrow on $155.4M cash); should be stated expressly.

---

## Issue Summary Table

| # | Issue | Severity | Source(s) | Est. Exposure / Impact |
|---|---|---|---|---|
| C-1 | S election validity — unverified holders; possible family LLC transfer | Critical | Cap table; DD report §III.B | Full structure failure; entity-level C corp tax, penalties, interest; loss of 338(h)(10) |
| C-2 | ADSP double-counts $48M debt ($473M vs. $425M) | Critical | Valuation summary; DD report | $48M PPA error; ~$3.2M/yr overstated amortization; audit risk |
| H-1 | Class V omits $28.5M Beacon interest; §754 decision unmade | High | Valuation summary; memo | Step-up may be non-amortizable without §754 |
| H-2 | Beacon ROFR triggered by change of control; notice clock likely expired | High | Beacon OA §8.03; SPA §2.3(d) | Transfer invalidity / litigation; closing condition |
| H-3 | Rollover structuring and 338(h)(10)/QSP interaction unanalyzed; inconsistent descriptions | High | Memo; SPA; cap table | Election validity; CEO after-tax outcome |
| H-4 | Non-transferable NC data processing license | High | SPA §4.9(i); valuation A-008 | ~$19M annual revenue at risk; PPA impact |
| H-5 | $3.8M suspended R&D credits likely permanently lost | High | DD report §IV.B | $3.8M |
| M-1 | QSBS §1202 analysis omitted | Medium | DD report §VIII.B; cap table | Potentially large shareholder exclusions |
| M-2 | §482 exposure ~$6.3M; no TP study; rep contradicted by OA | Medium | DD report §VII; Beacon OA §9.01; SPA §4.9(h) | ~$6.3M + penalties |
| M-3 | Escrow gain-recognition timing unaddressed | Medium | SPA §2.6(c); memo | Shareholder cash-tax timing |
| M-4 | State tax gaps (NC conformity, CA, NY) | Medium | DD report Art. V; memo | Multi-state exposure |
| M-5 | AAA/deemed liquidation characterization | Medium | DD report §IV.A | Shareholder-level character |
| M-6 | 2024 return due on closing date; final-year mechanics | Medium | DD report §IV.A; SPA §7.1 | Compliance/filing risk |
| — | Citation error; date inconsistencies; shareholder-count presentation; unreadable .eml | Minor | Multiple | Documentation quality |

---

## Recommended Action Plan (Pre-Closing)

1. **S election remediation (C-1):** Obtain immigration/residency documentation (Zhang, Al-Rashidi, Petrova) for all years since grant; resolve the 2021 family LLC transfer; refresh expired W-9s; if a defect is found, prepare a §1362(f) inadvertent-termination application before closing.
2. **Recompute ADSP and PPA (C-2, H-1):** Adopt $425M ADSP; add the Beacon interest to Class V; evaluate the Beacon §754 election and §743(b) computations; reconcile Form 8023/8883 packages.
3. **Beacon ROFR (H-2):** Deliver (or confirm delivery of) the ROFR Notice and obtain waivers from Delano and Avesta; add as a closing condition.
4. **Rollover (H-3):** Re-structure/re-paper consistently across the memo, SPA, and rollover agreement; confirm QSP testing excludes or properly treats rollover shares; model Dr. Chandra's after-tax result.
5. **License (H-4):** Obtain NC DIT confirmation or a legal opinion; adjust the PPA and consider a specific indemnity/insurance.
6. **R&D credits (H-5) and §482 (M-2):** Complete the §1371/§338(h)(10) credit analysis; commission a transfer pricing study; size escrow/indemnity accordingly.
7. **Shareholder communications (M-1, M-3, M-4):** Issue a shareholder tax letter covering QSBS status, estimated tax on deemed sale gain (including escrow timing), and state filing obligations (CA/NY residents in particular).
8. **Compliance calendar (M-6):** Extend the 2024 Form 1120-S; calendar state 338(h)(10) election forms and Form 8023 within the regulatory deadline.
9. **Documentation hygiene (Minor items):** Correct the regulatory citation; reconcile memo/report dates and versions; align the consent shareholder list with Schedule 1.1(a) and the cap table.

*This report is based solely on the documents identified above, portions of which were excerpted or truncated; the QSBS email thread could not be reviewed. Legal conclusions should be confirmed with tax counsel.*
