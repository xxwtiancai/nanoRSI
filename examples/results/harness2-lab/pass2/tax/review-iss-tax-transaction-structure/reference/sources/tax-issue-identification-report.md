# Tax Issue Identification Report
## Review of Tax Structure Memorandum — Project Prism (Ridgeline Capital Partners Fund III, LP / Prism Health Analytics, Inc.)

**Prepared for:** Ridgeline Capital Partners Fund III, LP — Investment Committee
**Subject:** Review of the Calloway, Stern & Whitaker LLP Tax Structure Memorandum dated February 10, 2025, against supporting deal documents
**Documents reviewed:** transaction-structure-memo.docx; purchase-agreement-excerpts.docx; tax-due-diligence-report.docx (Thornfield Accounting Group, LLP, January 15, 2025); asset-valuation-summary.xlsx (Thornfield preliminary PPA); prism-cap-table.xlsx; beacon-operating-agreement.docx; shareholder-qsbs-email-thread.eml (unreadable by review tool — see Section 4, Item 1)

---

## 1. Executive Summary

The CSW tax structure memorandum is internally coherent and well organized, but contains **one critical computational error, one critical unaddressed risk to the entire transaction structure, and several material inconsistencies and omissions** when tested against the supporting deal documents.

**Most consequential findings (Severity 1 — Critical):**

1. **ADSP overstatement of $48,000,000.** The memo computes the Aggregate Deemed Sale Price as $473,000,000 (enterprise value of $425M plus $48M of funded debt). This double-counts the funded debt: enterprise value already includes debt, and the equity value of $370M was derived by subtracting it. Thornfield's computation under Treas. Reg. §1.338-4 is $370M (cash $333M + rollover $37M) + $48M debt + $7M seller expenses = **$425,000,000**. The error inflates the Class VII goodwill residual by $48M and distorts the entire §1060 allocation and Form 8883.
2. **Unverified S corporation eligibility of restricted stock holders.** The memo asserts categorically that "no events causing a termination of the S election have been identified" and that all shareholders are eligible. The cap table and the Thornfield report contradict this: **three shareholders (Lin Wei Zhang — H-1B/PRC citizen; Yusuf Al-Rashidi — dual citizen, documentation missing; Nina Petrova — green card status unconfirmed) have unverified eligibility**, and Thornfield additionally identified a possible 2021 transfer of restricted stock to a family LLC (an ineligible shareholder if it occurred). If the S election terminated in a prior year, the §338(h)(10) election is unavailable and Prism would owe entity-level C corporation tax for all open years with penalties and interest.
3. **Beacon Insights 80.5% partnership interest omitted from the memo's Class V allocation.** The memo's Class V of $68.5M excludes the $28.5M Beacon interest that both Thornfield's valuation and the memo itself (Section III.C) identify as a Class V asset. Combined with the ADSP error, the memo's Class VII goodwill ($272.8M) is overstated by **$76.5M** versus Thornfield's $196.3M.

**Other significant findings:** the memo does not address the Beacon right of first refusal triggered by the change of control, the non-transferable NC data processing license (supporting ~$19M of government revenue), the §754 election decision for Beacon, QSBS/§1202 interaction with the deemed asset sale, the rollover-structure interaction with §338(h)(10), suspended C-corporation R&D credits ($3.8M at risk of permanent loss), §482 transfer pricing exposure (~$6.3M), and conflicting gain-character descriptions between the memo and cap table.

**Recommendation:** Do not rely on the memo's ADSP or allocation figures; require correction before Form 8023/Form 8883 preparation. Make shareholder eligibility verification (all restricted stock holders, all years since 1/1/2017) a closing condition, and resolve the Beacon ROFR and license issues before signing/closing.

---

## 2. Severity-Ranked Findings

### Severity 1 — Critical (transaction-structure or valuation-level impact)

**1.1 ADSP computed incorrectly — $48,000,000 overstatement.**
- Memo: ADSP = $425M enterprise value + $48M liabilities = $473M; Class VII goodwill = $272.8M.
- Thornfield allocation summary (Note 1): ADSP = $370M amount realized + $48M debt + $7M expenses = $425M; Class VII = $196.3M.
- Impact: Every downstream number in the memo's allocation, step-up, and depreciation/amortization benefit analysis is overstated; filing Form 8883 on the memo's figures would misstate the parties' tax returns.
- Action: Recompute ADSP per Treas. Reg. §1.338-4 and reissue the memo before the election is made.

**1.2 Memo's blanket assertion of valid S status conflicts with diligence.**
- Memo (Section III.A): "No events causing a termination of the S election have been identified... we are not aware of any ineligible shareholders."
- Cap table: three holders flagged "Unconfirmed"/"Not verified" (Zhang, Al-Rashidi, Petrova). Thornfield Section III.B: same three plus a possible 2021 transfer to "[name] Family Holdings, LLC"; company counsel non-responsive to document requests.
- Impact: An inadvertent termination under §1362(d)(2) would make the §338(h)(10) election unavailable (the target would not be a valid S corporation), trigger entity-level tax for open years, and undermine the SPA rep in Section 4.9(a). Unverified holders are receiving $2,775,000 in aggregate consideration per the cap table.
- Action: Obtain immigration/residency documentation for each restricted stock holder for every year since grant; obtain the family LLC transfer documentation and operating agreement; if an inadvertent termination is discovered, evaluate a §1362(f) relief application and revisit structure/pricing.

**1.3 Beacon Insights interest omitted from Class V allocation.**
- Memo Class V: $68.5M. Thornfield Class V: $97.0M, itemized as real property ($14.2M), FF&E ($6.8M), developed technology ($41.8M), government software licenses ($5.7M), NC license ($0), Beacon interest ($28.5M).
- The memo itself (Section III.C) states the Beacon interest "will be treated as an asset of Prism in the deemed asset sale... classified as a Class V asset" — yet the allocation omits it. Internal inconsistency within the memo.
- Action: Include the $28.5M interest in Class V; reconcile total allocation to corrected ADSP.

### Severity 2 — High (material tax or deal-execution risk)

**2.1 Beacon right of first refusal triggered by the transaction — not addressed in the memo.**
- Beacon Operating Agreement §8.03(a)(ii): a Change of Control of any entity Member triggers the ROFR for the other Members (Delano 12.0%, Avesta 7.5%). The Merger is expressly a "change of control" under SPA §2.3(d). A ROFR Notice is due within 10 business days of signing the definitive agreement (January 28, 2025 — the deadline appears to have already passed). The memo mentions the ROFR only in passing ("customary transfer restrictions") and never analyzes it.
- Action: Confirm a ROFR Notice was delivered; obtain waivers from Delano and Avesta as a closing condition.

**2.2 Non-transferable NC Data Processing License (No. DIT-2019-04821) — omitted from the memo.**
- SPA §4.9(i) and Thornfield (asset A-008): the license is non-transferable/non-assignable; ~$19M of annual government revenue partially depends on it; assigned $0 FMV. Legal confirmation of whether the license survives the reverse triangular merger is outstanding.
- Impact: If terminated, government business value migrates to (or impairs) goodwill; valuation and PPA impact.
- Action: Obtain NC DIT confirmation pre-closing; condition/reprice accordingly.

**2.3 Beacon §754 election decision not analyzed.**
- Thornfield Note 2: no look-through analysis of Beacon's underlying assets; the tax step-up on the partnership interest depends on a Beacon §754 election and §743(b) computations. The memo is silent on the mechanics and on who controls the decision (Prism is sole Manager and holds 80.5%, but approval of "any transaction with the Manager" requires Majority Interest under §4.03(e)).
- Action: Determine §754 advisability and prepare §743(b) computations before closing; the election is due with Beacon's return for the transaction year.

**2.4 QSBS / §1202 interaction unanalyzed.**
- Thornfield Finding 4 and the cap table flag QSBS questions from angel holders; Section 1202(c)(1) requires issuance by a C corporation (stock acquired during 2016 C corp period may qualify; Elena Vargas's 3/1/2017 shares likely do not). Critically, a §338(h)(10) deemed **asset** sale generally eliminates the capital-gain framework on which QSBS exclusion depends — the memo nowhere analyzes this, even though shareholder expectations (per the QSBS email thread referenced in diligence, which could not be read by this reviewer) may be misaligned.
- Action: Counsel should promptly analyze §1202 availability under the deemed asset sale and communicate to shareholders; consider disclosure in the shareholder consent process.

**2.5 Rollover equity mechanics inconsistent and unanalyzed against §338(h)(10).**
- Memo Section II.A: rollover into "the post-closing acquisition vehicle"; SPA definition: equity in "Parent (or a designated acquisition vehicle)"; cap table: "Ridgeline Acquisition Sub, Inc." — three different formulations. Memo Section II.B says the contribution goes to "Newco." The memo also does not address whether the rollover affects the ADSP/consideration computations, gain allocation among shareholders, or the qualified stock purchase analysis.
- Action: Specify the rollover vehicle definitively; analyze rollover interaction with the §338(h)(10) election and allocation of deemed sale gain.

**2.6 Suspended C-corporation R&D credits ($3.8M) — memo dismisses rather than analyzes.**
- Memo III.D: credits "noted and will be addressed in post-closing tax planning." Thornfield IV.B: under §1371(b) they cannot be used in S years; a §338(h)(10) deemed liquidation may permanently destroy them; structuring modifications could potentially preserve value. Given the 2016 C corp year generated only ~$408,000 of tax and no BIG tax applies, realistic salvage paths are limited — but the memo's treatment is an unanalyzed omission.
- Action: Complete the §§1371(b)/(e), 1374, 338(h)(10) interaction analysis and reflect any value impact in pricing.

### Severity 3 — Medium (compliance, exposure, or consistency items)

**3.1 Gain character inconsistency between memo and cap table.**
- Cap table "Gain Character" column labels all shareholder gains "Capital gain (per memo)" while simultaneously flagging that the §338(h)(10) deemed asset sale produces pass-through **asset-sale** character (potentially ordinary income on receivables, §1231 gains, recapture). The memo (truncated portion) does not appear to reconcile character at the shareholder level. Shareholders may face ordinary income on AR/recovery property items.
- Action: Model shareholder-level character; correct the cap table characterization.

**3.2 §482 transfer pricing exposure (~$6.3M, 2019–2024) understated in memo.**
- Memo describes the $850K management fee and $400K IP license fee as described in the agreements and moves on. Thornfield estimates cumulative exposure of ~$6,300,000; the Beacon operating agreement itself discloses the fee has never been benchmarked and does not vary with services. Exposure runs to the pre-closing period (seller risk) but also affects post-closing deductible basis for the ongoing arrangements.
- Action: Quantify indemnity/escrow coverage; consider repricing the intercompany agreements at closing.

**3.3 2024 Form 1120-S filing deadline coincides with closing.**
- Due March 15, 2025 — the Closing Date. Final short-year return (through 3/15/2025) also required under SPA §7.1 with 30-day buyer review. Extension should be filed; memo is silent.
- Action: Calendar extensions; coordinate SPA §7.1 review workflow.

**3.4 Memo cites incorrect regulation reference.**
- Sections II.A and III.C cite "Treas. Reg. 1.301-7701-3" for disregarded-entity classification; the correct cite is Treas. Reg. §301.7701-3 (the SPA cites it correctly). Minor, but flags citation quality control.

**3.5 Shareholder-count and "other shareholders" composition inconsistencies.**
- Memo: "Fourteen (14) angel investors and early employees hold the remaining 20%." Cap table: the minority block comprises 10 angel/early-employee common holders plus 8 restricted stock holders (16 unique individuals; 18 holder lines). Also, memo waterfall percentages (52/28/20 basic) do not tie to fully diluted percentages (50.83%/27.37%) used in the cap table's escrow computations — the SPA's "Pro Rata Share" definition (Schedule 1.1(a), not produced) determines which controls. The memo's "$74,000,000 to Other Shareholders" vs. the cap table's $74,999,231 + $1,110,769 (Hawkins) subtotals require reconciliation.
- Action: Confirm the definitive shareholder schedule and pro rata definitions; reconcile escrow math.

**3.6 AAA balance ($64.2M as of 12/31/2023) not addressed.**
- Thornfield flags the AAA as relevant to characterizing deemed distributions in the deemed liquidation; the memo (as produced) does not analyze it. Affects shareholder-level distribution/EBP characterization.

**3.7 State tax items underdeveloped.**
- CA shareholders (Muñoz, Yoon) and CA entity-level S tax (1.5%/$800 minimum — rep'd paid at SPA 4.9(c)); CA does not conform to §338(h)(10) in all cases — state-level deemed-sale treatment and filing obligations for NC/CA/NY/VA shareholders need shareholder-level guidance. The memo defers this to individual advisors; acceptable, but the memo should at least flag nonconformity risk.

### Severity 4 — Low (documentation/process)

**4.1 Supporting document could not be reviewed.** The shareholder QSBS email thread (shareholder-qsbs-email-thread.eml) could not be converted for review; QSBS findings above rely on Thornfield and the cap table. Recommend the email thread be reviewed by counsel directly.

**4.2 Memo dated February 10, 2025 but references its own PPA as "dated 1/28/2025."** Thornfield's allocation summary refers to a CSW memo dated 1/28/2025 — either an earlier draft exists or a date error; confirm which memo version is operative.

**4.3 Escrow release date arithmetic.** 18 months from 3/15/2025 is 9/15/2026 — consistent across documents; no issue, noted as verified.

---

## 3. Reconciled Key Figures

| Item | Memo | Thornfield/Docs | Correct/Action |
|---|---|---|---|
| ADSP | $473,000,000 | $425,000,000 | Use $425M |
| Class V | $68,500,000 | $97,000,000 | Include Beacon $28.5M |
| Classes I–IV | $36,700,000 | $36,700,000 | Agreed |
| Class VI | $95,000,000 | $95,000,000 | Agreed |
| Class VII (goodwill) | $272,800,000 | $196,300,000 | Use $196.3M |
| Equity value / cash / rollover | $370M / $333M / $37M | Same | Agreed |
| Escrow | $22M / 18 mo. | Same | Agreed |
| S election validity | Asserted clean | 3 unverified holders + possible LLC transfer | Verify pre-closing |
| BIG tax (§1374) | None (period expired 12/31/2021) | Same | Agreed |

## 4. Recommended Closing Conditions / Next Steps

1. Corrected memo reissuing ADSP and allocation (Severity 1.1, 1.3).
2. Documentary confirmation of S eligibility for all 8 restricted stock holders, all years since 1/1/2017, plus resolution of the family LLC transfer allegation (1.2).
3. Beacon ROFR waivers from Delano and Avesta; Beacon §754 decision and §743(b) computations (2.1, 2.3).
4. NC DIT confirmation on license survivability (2.2).
5. Shareholder-level §1202 and gain-character analysis and communications (2.4, 3.1).
6. Rollover vehicle documentation (2.5) and R&D credit salvage analysis (2.6).
7. Transfer pricing exposure quantification and indemnity coverage check (3.2); extension of the 2024/final returns (3.3).

---
*This report is based solely on the documents listed above; the QSBS email thread could not be read and should be reviewed separately. Legal conclusions rest with tax counsel.*
