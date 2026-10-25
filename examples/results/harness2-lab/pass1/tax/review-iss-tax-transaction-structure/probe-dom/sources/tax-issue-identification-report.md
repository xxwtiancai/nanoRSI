# Tax Issue Identification Report
## Review of Transaction Structure Memorandum — Acquisition of Prism Health Analytics, Inc. by Ridgeline Capital Partners Fund III, LP

**Prepared for:** Deal Team / Investment Committee
**Date of review:** February 2025
**Documents reviewed:** transaction-structure-memo.docx (Calloway, Stern & Whitaker LLP ("CSW"), 2/10/2025); purchase-agreement-excerpts.docx (Agreement and Plan of Merger, 1/28/2025); tax-due-diligence-report.docx (Thornfield Accounting Group, LLP, 1/15/2025); asset-valuation-summary.xlsx (Thornfield draft PPA); prism-cap-table.xlsx; beacon-operating-agreement.docx.

**Document not reviewed:** `shareholder-qsbs-email-thread.eml` could not be read or converted. Its contents are **not** reflected in this report; QSBS-related findings below rely on the tax due diligence report and cap table, which reference shareholder QSBS questions. No facts from the email are inferred.

---

## Executive Summary — Top Issues

1. **CRITICAL — S corporation eligibility of at least three restricted stock holders is unverified**, including an H-1B visa holder and a possible transfer of shares to a family LLC. If the S election was terminated in any prior year, the Section 338(h)(10) election is unavailable and entity-level C corporation tax applies for all open years. The memo states categorically that "no events causing a termination of the S election have been identified," which is inconsistent with the Thornfield report and the cap table. (Findings 1, 2)
2. **CRITICAL — The memo's Aggregate Deemed Sale Price (ADSP) of $473,000,000 double-counts the $48,000,000 of funded debt.** Thornfield computes ADSP of $425,000,000 ($370M stock consideration + $48M debt + $7M expenses). The memo inflates Class VII goodwill by $76.5M ($48M ADSP error + $28.5M omitted Beacon interest). (Findings 3, 4)
3. **HIGH — Beacon Insights ROFR is triggered by the merger.** Beacon Operating Agreement §8.03(a)(ii) makes a Change of Control of a member a ROFR triggering event; the merger is expressly a change of control under Merger Agreement §2.3(d). The 19.5% minority members (Delano/Avesta) could exercise a 45-day purchase right over Prism's 80.5% interest at "Fair Market Value" determined without minority discounts (§8.04(d)). The memo mentions the ROFR only in passing and does not address it as a closing risk or waiver condition. (Finding 6)
4. **HIGH — $3.8M of suspended C-corporation R&D credits are likely permanently lost** under the 338(h)(10) structure; the memo dismisses them as "addressed in the post-closing tax planning" without analysis. (Finding 7)
5. **HIGH — Transfer pricing exposure of ~$6.3M** on the Prism–Beacon intercompany management fee ($850K) and IP license fee ($400K); Beacon OA §9.01 confirms no benchmarking or transfer pricing study ever performed and the fee does not vary with services. (Finding 8)
6. **HIGH — QSBS analysis is omitted.** Cap table holders acquired ~$70M of stock during the 2016 C corporation period; §1202 interaction with the 338(h)(10) deemed asset sale (character of pass-through gain) is unaddressed. The QSBS email thread could not be read. (Finding 9)
7. **MEDIUM/HIGH — NC Data Processing License (non-transferable) may not survive** the deemed asset sale/reverse merger, jeopardizing ~$19M of government-sector revenue; valued at $0 in the PPA. (Finding 10)
8. Additional issues: memo miscitations (Treas. Reg. "1.301-7701-3" for 301.7701-3; wrong §338(h)(10) consent cross-reference — SPA §7.3(a) vs. memo's "Section 7.04"; mischaracterization of rollover as gain-free), rollover/338(h)(10) interaction unanalyzed, 2024 Form 1120-S due on the closing date, Beacon §754/§743(b) step-up decision open, AAA ($64.2M) not addressed in deemed-liquidation analysis, and two California-resident shareholders with expired W-9s. (Findings 11–17)

---

## Cross-Document Reconciliation of Key Facts

| Fact | Structure Memo (CSW) | Merger Agreement | Thornfield DD Report | Valuation Summary | Cap Table | Flag |
|---|---|---|---|---|---|---|
| Enterprise value | $425,000,000 | $425,000,000 (§1.1) | $425,000,000 | $425,000,000 (EV) | — | Consistent |
| Equity value | $370,000,000 | $370,000,000 | $370,000,000 | $370,000,000 | $370,000,000 | Consistent |
| **ADSP** | **$473,000,000** | Per §7.3(b), per Treas. Reg. 1.338-4 (no figure in excerpts) | — (see PPA) | **$425,000,000** | — | **Mismatch — memo double-counts $48M debt** |
| Class V allocation | $68,500,000 | — | — | $97,000,000 (includes $28.5M Beacon interest) | — | **Mismatch — memo omits Beacon interest** |
| Class VII goodwill | $272,800,000 | — | — | $196,300,000 | — | **Mismatch ($76.5M)** |
| Classes I, III, VI | $12.4M / $24.3M / $95.0M | — | — | Identical | — | Consistent |
| S election validity | "No events causing a termination... identified"; all shareholders eligible individuals | §4.9(a) reps valid S status | **Critical open items: H-1B holder; family LLC transfer** | — | 3 holders "Unconfirmed"/not verified | **Memo inconsistent with DD** |
| Restricted stock holders eligible | 8 of 8, implied | §2.5 reps all eligible individuals | 2 of 8 unconfirmed | — | 3 unverified (Zhang, Al-Rashidi, Petrova) | **Inconsistent (see Finding 2)** |
| Big (recognition period expired 12/31/2021; NUBIG $46.5M) | Yes | §4.9(f) | Yes | — | — | Consistent |
| Suspended federal R&D credits | $3.8M "noted; post-closing planning" | §4.9(g) | $3.8M; utilization unclear; likely lost | — | — | Memo understated |
| Intercompany fees | $850K mgmt + $400K IP; "customary" | §4.9(h): arm's length rep, **no TP study** | Below arm's length; ~$6.3M §482 exposure | — | — | Memo omits exposure |
| Beacon interest FMV / basis | $28.5M / $6.4M; Class V asset | §4.9(j) same | Same | Same | — | Values consistent; but memo PPA omits it |
| Rollover | $37M to "Newco"/Parent; treated as part of $370M | $37M to Parent or designated vehicle | — | Amount realized includes $37M rollover | $37M | Consistent amount; **tax treatment unanalyzed (Finding 12)** |
| Escrow | $22M / 18 months / release 9/15/2026 | Same | — | — | Same | Consistent |
| Shareholders | 18 holders incl. 8 restricted | Schedule 1.1(a) (not reproduced) | 3 principal blocks | — | 16 unique individuals / 18 lines | Consistent in substance |
| Shareholder count for §1361(c) purposes | ≤100 asserted | §4.9(a) | — | — | 18 lines incl. possible family LLC transfer | Unverified pending Finding 1 |

---

## Detailed Findings (Severity-Ranked)

### CRITICAL

**1. S corporation election validity is a threshold open item, but the memo treats it as resolved.**
- Source: Thornfield report §III.B ("Critical Finding — Restricted Stock Holders"); memo §III.A.
- Thornfield could not confirm eligibility for restricted stock holders including (a) a Canadian-national H-1B holder whose substantial-presence-test compliance (§7701(b)(3)) is unverified for all years since grant and (b) an annotation in Prism's 2021 stock ledger of a "transfer to [name] Family Holdings, LLC," which, if a partnership or LLC owned by an ineligible person, would be an ineligible shareholder under §1361(b)(1) and terminate the S election retroactively under §1362(d)(2).
- Why it matters: If the S election terminated in a prior year, (i) the §338(h)(10) election is unavailable (it requires a valid S corporation target), (ii) entity-level C corp tax, penalties, and interest apply for all open years on $87M/year of revenue and the ~$330M+ of S-period income, and (iii) the entire memo's analysis fails.
- Recommended action: Do not rely on the memo's conclusion. Obtain immigration/residency documentation for all unverified holders for every year since grant; obtain the family LLC transfer documentation (operating agreement, classification, members); if an inadvertent termination occurred, evaluate a §1362(f) relief application **before** closing. Make resolution a closing condition. Note the SPA's §4.9(a) representation provides only contractual (indemnity/escrow) recourse, not tax cure.

**2. Memo's affirmative statements on shareholder eligibility are contradicted by the cap table and DD report.**
- Source: Memo §III.A ("All shareholders of Prism are U.S. individuals, and we are not aware of any ineligible shareholders"); cap table (Lin Wei Zhang — H-1B, PRC citizen; Yusuf Al-Rashidi — dual citizen, documentation missing; Nina Petrova — green card status unconfirmed; combined consideration ~$2.775M); Thornfield §III.B.
- Why it matters: The memo's own diligence standard requires verification, not awareness. Note also the cap table identifies the H-1B holder as a PRC citizen while Thornfield's report describes a Canadian national — the discrepancy between these two descriptions of the same apparent issue should be reconciled. Additionally, Thornfield found two California-resident shareholders with W-9s expired since 2019.
- Recommended action: Correct the memo; obtain current W-9s/citizenship documentation for all holders; reconcile the nationality discrepancy.

**3. ADSP overstated by $48,000,000 — funded debt double-counted.**
- Source: Memo §I ("ADSP is $473,000,000"); Valuation Summary, Allocation Summary tab, Note 1; Merger Agreement §7.3(b) (ADSP "determined in accordance with Treasury Regulation Section 1.338-4").
- Arithmetic check: Under Treas. Reg. 1.338-4, ADSP starts from the amount realized on the stock ($370M = $333M cash + $37M rollover) plus target liabilities ($48M debt; conservatively $7M seller expenses): **$425M**. The memo instead starts from enterprise value ($425M, which already includes debt) and adds $48M again, yielding $473M. Variance: **$48M (memo $473M vs. correct $425M)**.
- Why it matters: An overstated ADSP overstates the buyer's amortizable basis (duplicated deduction exposure on audit), misstates the sellers' deemed sale gain, and would produce an incorrect Form 8883.
- Recommended action: Recompute ADSP from stock consideration plus liabilities; reconcile with Thornfield before filing Form 8023/8883; also resolve whether the $7M seller transaction expenses are target liabilities for ADSP purposes (memo omits them entirely; Thornfield includes them "for conservatism").

**4. Class V / Class VII allocation variances of $28.5M / $76.5M.**
- Source: Valuation Summary Allocation Summary; memo §IV (allocation of $473M).
- Memo Class V $68.5M omits the $28.5M Beacon Insights 80.5% interest (a Class V asset per Treas. Reg. 1.338-6(b)(2)(v)); Class VII residual $272.8M vs. Thornfield $196.3M. Combined variance ($48M ADSP error + $28.5M Beacon omission = $76.5M) verified.
- Recommended action: Restate the PPA at the corrected ADSP; include the Beacon interest in Class V (or perform the §754/§743(b) look-through analysis — see Finding 13); confirm no value is buried in Class V for the non-transferable NC license (Finding 10).

### HIGH

**5. (Reserved — see Finding 1/3 severity consolidation.)**

**6. Beacon Insights ROFR is triggered by the merger and is unaddressed.**
- Source: Beacon Operating Agreement §8.03(a)(ii) (Change of Control of an entity member is a Triggering Event), §8.03(b)–(f) (10-business-day ROFR notice; 45-day exercise period; all-or-nothing purchase at FMV), §8.04(d) (FMV **without** minority/marketability discounts); Merger Agreement §2.3(d) (merger is a change of control "for all purposes... including any operating agreement").
- Why it matters: Prism (the transferring/change-of-control member) must deliver a ROFR Notice within 10 business days of signing the definitive agreement (i.e., by early February 2025 — the deadline may already have passed or is imminent as of the memo date). If Delano (12.0%) and/or Avesta (7.5%) exercise, Prism's 80.5% interest (~$28.5M undiscounted) could be purchased away from the buyer post-signing, unwinding ~$28.5M of the acquired value and changing the deemed-sale asset pool.
- Recommended action: Confirm whether a ROFR Notice was delivered; obtain ROFR waivers from Delano and Avesta as a closing condition; quantify breach exposure under §8.01 (purported transfers in violation are void).

**7. $3.8M suspended federal R&D credits likely forfeited; memo defers without analysis.**
- Source: Thornfield §IV.B; memo §III.D ("noted and will be addressed in the post-closing tax planning"); Merger Agreement §4.9(g).
- Under §1371(b)(1) the credits cannot be used in S years; with no §1374 BIG tax (recognition period expired) and a deemed liquidation under 338(h)(10), the credits are expected to be permanently lost (Thornfield's conclusion; attributed to Thornfield, not verified). Neither the memo nor the SPA allocates this value or prices it.
- Recommended action: Tax counsel analysis of §§1371(b)/(e), 1374, 338(h)(10) interactions; consider purchase price adjustment or indemnity; do not assume any credit value in the model.

**8. Transfer pricing / §482 exposure of ~$6.3M on Prism–Beacon intercompany fees.**
- Source: Thornfield §VII (est. cumulative §482 exposure ~$6.3M, 2019–2024); Merger Agreement §4.9(h) (fees represented arm's length; no TP study); Beacon OA §9.01 (fee fixed since 2018, never benchmarked, no CPI catch-up adjustment applied, does not vary with scope/cost).
- Why it matters: Pre-closing exposure runs with the target under the deemed asset sale/indemnity structure; secondary effect on Beacon's value and the PPA. The memo describes the arrangements as "customary" and does not mention the exposure.
- Recommended action: Quantify and allocate exposure (escrow/specific indemnity); commission a benchmarking study and reset fees at closing; verify whether the CPI escalator in §9.01 was ever applied (apparent non-compliance with the OA's own terms).

**9. QSBS (§1202) analysis omitted; large amounts at stake.**
- Source: Thornfield §VIII.B (angel investors raised QSBS questions via Linden Rock; interaction with 338(h)(10) "not analyzed"); cap table (founders and ~8 angel/early holders acquired stock 6/14/2016–11/1/2016 during the C corp window — combined consideration for C-corp-period common holders other than founders ~$70M; Elena Vargas (3/1/2017) is noted as not QSBS-eligible because Prism was then an S corporation).
- Note: the shareholder QSBS email thread could not be read; its contents are unknown and this finding should be revisited once it is available.
- Why it matters: Under 338(h)(10), shareholders recognize deemed **asset sale** gain passed through on K-1s, generally ordinary/§1231/§1250 character — not the capital gain from a stock sale that §1202 excludes. Shareholders expecting 100% QSBS exclusion (potential federal savings up to ~$20M+ at 23.8% on $70M–$296M of eligible gain) may face a materially worse result than a straight stock sale without the election. This affects shareholder consent to the election (a closing condition) and creates advisor-malpractice/consent-dispute risk.
- Recommended action: Prepare a §1202 eligibility and quantification memo for each C-corp-period holder (including $50M gross-asset test during holding period and active-business requirements); model the after-tax outcome with vs. without the election; disclose to shareholders before consents are collected.

**10. NC Data Processing License (No. DIT-2019-04821) is non-transferable and may not survive the transaction.**
- Source: Valuation Summary asset A-008 (notes: non-transferable/non-assignable; $0 FMV; ~$19M annual government revenue partially depends on it); Merger Agreement §4.9(i) (license non-transferable/non-assignable).
- Why it matters: In a 338(h)(10) deemed asset sale the license arguably cannot be "transferred"; even in the actual reverse merger, legal continuity should be confirmed with NC DIT. If terminated, up to ~$19M of revenue and the related customer-relationship value in the PPA (Class VI) is impaired.
- Recommended action: Obtain NC DIT confirmation or re-issuance commitment pre-closing; make it a closing condition; confirm no license value was embedded in the memo's software/technology line ($47.5M per Thornfield Note 3).

### MEDIUM

**11. Legal citation errors in the memo.**
- Memo §II.A and §III.C cite "Treas. Reg. 1.301-7701-3" — the correct citation is **Treas. Reg. §301.7701-3** (the check-the-box regulation). Beacon OA §2.05 and Merger Agreement §4.9(k) cite it correctly.
- Memo §II.B says the shareholder-consent requirement is "reflected in Section 7.04 of the Stock Purchase Agreement"; the reproduced agreement addresses the 338(h)(10) election and consent condition in **Section 7.3(a)** (Article VII). No §7.04 appears in the excerpts.
- The memo also describes the restricted stock as "approximately 2.3% of the fully diluted equity" — cap table computes 2.26% (45,000/1,995,000); immaterial but should be conformed.
- Recommended action: Correct citations before the memo is circulated/relied upon; confirm the correct SPA section against the full agreement.

**12. Rollover equity treatment under 338(h)(10) is unanalyzed.**
- Source: Memo §II.B (rollover to "Newco" for membership interests; rollover "expected to be completed in connection with the closing"); Merger Agreement §§1.1, 2.4(c), 6.2(e) (rollover into Parent or a designated acquisition vehicle — note the memo says Dr. Chandra receives equity in "Newco"/an LLC, while the cap table notes rollover into **Ridgeline Acquisition Sub, Inc.**, a corporation; the rollover vehicle's form and identity are inconsistent across documents).
- Why it matters: Under 338(h)(10), 100% of each shareholder's stock (including rollover shares, valued at $37M) is deemed sold; Dr. Chandra would recognize deemed asset-sale gain on his full 52% share with cash to pay tax on only ~81% of his consideration. Gain recognition vs. nonrecognition (e.g., §351/721 contribution structuring, "waters-edge" election mechanics) must be analyzed; the memo's cap table column labels his $192.4M as "capital gain (per memo)" which conflicts with the memo's own deemed-asset-sale analysis.
- Recommended action: Specify the rollover vehicle and analyze tax-free contribution mechanics; reconcile the inconsistent vehicle descriptions; disclose cash-tax shortfall issue to Dr. Chandra before consents.

**13. Beacon §754/§743(b) step-up decision open.**
- Source: Valuation Summary Note 2 / asset A-009 ("Thornfield has not performed a look-through analysis... §754 election implications").
- Why it matters: Without a Beacon §754 election, the $22.1M step-up on the Beacon interest ($28.5M FMV vs. $6.4M basis) may not generate amortizable basis inside Beacon, materially reducing the buyer's expected deductions from the PPA.
- Recommended action: Determine whether Beacon can/must make a §754 election (note: as a non-partner transferee via asset purchase treatment, mechanics require structuring attention); perform look-through valuation of Beacon assets.

**14. Final-year tax compliance timing: 2024 Form 1120-S due March 15, 2025 — the Closing Date.**
- Source: Thornfield §IV.A; Merger Agreement §7.1 (final short-year 1120-S through Closing Date; 30-day Parent review right).
- Why it matters: Both the 2024 calendar-year return and the final short-year return (1/1/2025–3/15/2025) must be handled; the 30-day pre-filing review right in §7.1 is inconsistent with a 3/15/2025 closing for any return due that day; extensions will be required. The deemed-sale gain must be reported on the final short-year return and K-1s delivered promptly so shareholders can pay estimated tax.
- Recommended action: Plan extensions (Forms 7004 and, for shareholders, 4868 with estimated payments); build the §7.1 review timeline into the closing calendar.

**15. AAA balance ($64.2M) and deemed-liquidation characterization not addressed in the memo (memo truncated before full treatment; flagged to extent visible).**
- Source: Thornfield §IV.A (AAA $64.2M at 12/31/2023, "relevant for the characterization of deemed distributions in connection with the deemed liquidation").
- Recommended action: Memo should analyze AAA/distribution ordering (§1368) effects for shareholders, including the escrow ($22M funded pro rata from cash recipients) and its character.

**16. State tax gaps: CA entity-level tax and non-resident shareholders.**
- Source: Merger Agreement §4.9(c) (1.5% CA S corp tax / $800 minimum; NY fixed dollar minimum); cap table (Muñoz, Yoon — CA residents; Okoye — NY); memo defers state-specific advice to individual advisors.
- Why it matters: CA will tax the deemed asset-sale gain apportioned to CA at the entity level notwithstanding the S election; the 338(h)(10) election must also be evaluated for CA/NY conformity (CA does not conform to 338(h)(10) for state purposes in the same manner — state ADSP recomputation needed). VA (Avesta) filing obligations for Beacon also unaddressed.
- Recommended action: Quantify CA entity-level tax on the deemed gain and address who bears it under the SPA; prepare state ADSP/PPA computations; NC 338(h)(10) conformity confirmation.

### LOW

**17. Minor reconciliation items.**
- Memo describes Thornfield DD report as "dated January 10, 2025"; the report itself is dated **January 15, 2025** (and relies on information through January 10, 2025). Conform the reference.
- Memo states escrow is "funded pro rata from all cash-receiving shareholders"; Merger Agreement §2.6(d) deducts escrow pro rata from each recipient — consistent, but note Dr. Chandra's escrow share (~$10.26M per cap table) reduces his net cash to ~$145.1M, which the memo's consideration table does not show.
- Memo/advisor role: Merger Agreement §2.6(b) lists Calloway, Stern & Whitaker LLP as **Company counsel** receiving $2.2M of seller transaction expenses, while the memo presents CSW as tax/deal counsel to **Ridgeline**. This dual-role presentation should be clarified (potential conflict/disclosure point).
- Restricted stock acceleration: memo/SPA §2.5 accelerate vesting at closing; because 83(b) elections were filed, full consideration is capital in character — consistent across documents; no issue beyond confirmation of grant-date ordinary income already recognized (cap table notes agree).

---

## Verification Notes

- Consideration arithmetic verified: $155.4M + $37M + $103.6M + $74M = $370M; $333M + $37M = $370M; escrow $333M − $22M = $311M net closing cash.
- ADSP variance verified: memo $473M vs. Thornfield $425M = $48M double-count; Class V variance $28.5M; Class VII variance $76.5M ($48M + $28.5M). Both totals foot (each equals its stated ADSP).
- NUBIG verified: $78M − $31.5M = $46.5M (consistent in memo, SPA §4.9(f), and Thornfield, the latter independently verified against the 2017 opening balance sheet and a December 2016 appraisal).
- Attribution: conclusions regarding S election risk, R&D credit loss, and §482 exposure are Thornfield's (advisor conclusions), not independently verified facts; ADSP/PPA discrepancies are our analysis of the two documents' computations; the memo's own statements are characterized as the drafting firm's conclusions.
