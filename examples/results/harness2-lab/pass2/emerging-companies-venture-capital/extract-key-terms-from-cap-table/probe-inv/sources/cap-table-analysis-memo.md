# CAP TABLE ANALYSIS MEMORANDUM

**Proposed Series C Preferred Stock Financing — Cascade Robotics, Inc.**

| | |
|---|---|
| **Company** | Cascade Robotics, Inc. (Delaware C-corp; EIN 83-4127650) |
| **Transaction** | $45,000,000 Series C Preferred Stock financing led by Ridgeline Growth Partners Fund VI, L.P. |
| **Term Sheet Date** | November 8, 2024 |
| **Target Closing** | On or before December 31, 2024 |
| **Cap Table Date** | October 15, 2024 (as referenced in Term Sheet §1.11); spreadsheet prepared as of November 8, 2024 |
| **Sources Reviewed** | Series C Term Sheet; Cap Table Spreadsheet; Convertible Note Purchase Agreement (1/15/2021); Amended & Restated COI (8/12/2022); 2019 Equity Incentive Plan; 409A Valuation Report (Valiant Appraisals, 9/30/2024); Amended & Restated Investors' Rights Agreement (8/12/2022); Amended & Restated Voting Agreement (8/12/2022) |

---

## 1. EXECUTIVE SUMMARY

Cascade Robotics proposes to raise **$45,000,000** at a **$180,000,000 pre-money / $225,000,000 post-money** valuation, issuing approximately **5,500,000 shares of Series C Preferred at $8.18 per share** (1.5x non-participating liquidation preference; full ratchet anti-dilution). Ridgeline would invest $35,000,000 (~4,278,973 shares) and existing preferred holders $10,000,000 (~1,221,027 shares) via pro rata rights, giving Series C holders ~20.0% of the post-money fully diluted capitalization (computed below).

**Key findings requiring resolution before closing:**

1. **Series A share count discrepancy.** The Amended & Restated Certificate of Incorporation (COI §4.2(b), §5A.1) states **3,820,616** shares of Series A Preferred are outstanding — 3,500,000 purchased plus **320,616 shares issued on conversion of the Firstvale convertible note** — while the cap table, term sheet, and 409A all show only **3,500,000**. The cap table's own footnote concedes the note conversion shares are "not reflected." This is a **320,616-share understatement** in the term sheet's fully diluted denominator.
2. **Fully diluted denominator inconsistencies.** The term sheet's 22,004,000-share denominator (i) **excludes the 150,000-share Pinnacle warrant**, contradicting Term Sheet §1.5 which states fully diluted is inclusive of all warrants; (ii) **excludes the 450,000 shares of common issued on option exercises** (the cap table shows 10,450,000 shares of common outstanding vs. 10,000,000 used in the denominator); and (iii) uses an available pool of **1,204,000** while the Option Grants tab computes **1,275,000** (5,000,000 authorized − 3,725,000 granted).
3. **Option pool increase math conflict.** Term Sheet §1.10 requires a pre-closing pool increase from 5,000,000 to 7,500,000 shares (+2,500,000) and states the increase "shall be included in the pre-money Fully Diluted Capitalization" — but the §1.6 denominator of 22,004,000 does not reflect it. If included, the denominator rises to 24,504,000 (term sheet basis) and the price falls to ~$7.34.
4. **Warrant terms conflict.** COI §4.2(e): Pinnacle National Bank warrant dated **March 10, 2022, exercise price $3.50**; cap table, 409A report, and note agreement context: dated **June 22, 2021, exercise price $3.00**, expiring June 22, 2031.
5. **Founder name discrepancy.** "Raj Venkatesh" (term sheet, 409A, cap table) vs. "Raj Subramanian" (COI, Voting Agreement, Note Purchase Agreement) for the same 3,500,000-share co-founder.
6. **Board designee discrepancies.** Cap table lists the Firstvale Series A designee as **Thomas Aldridge** and Summit Arc's designee as **Victoria Langford**; the IRA, Voting Agreement, and 409A identify **Allison Trang** (Firstvale) and **Derek Hollowell** (Summit Arc).
7. **409A common FMV ($8.75) exceeds the Series C preferred price ($8.18)** — economically anomalous (illiquid common should value below senior preferred in the same period) and a tax-pricing flag for new option grants.
8. **Investor-favorable/unusual Series C terms:** full ratchet anti-dilution, 1.5x preference, and a protective provision (§2.5(b)) requiring Series C majority consent for **any** equity issuance including previously Board-approved option grants under the 2019 EIP — in tension with the EIP/COI framework under which routine grants within the reserve require no separate preferred consent.

---

## 2. CURRENT CAPITALIZATION (AS OF NOVEMBER 8, 2024)

### 2.1 Per the Cap Table Spreadsheet (Summary tab)

| Category | Holder | Shares | % FD (22,004,000 basis) |
|---|---|---:|---:|
| Founders' Common | Maya Chen | 5,000,000 | 22.72% |
| Founders' Common | Raj Venkatesh | 3,500,000 | 15.91% |
| Founders' Common | Lena Ostrowski | 1,500,000 | 6.82% |
| Common — exercised options | Various employees ($0.50 tranche) | 450,000 | (in common outstanding; excluded from FD build) |
| Series A Preferred | Firstvale Ventures | 3,500,000 | 15.91% |
| Series B Preferred | Summit Arc Capital | 4,200,000 | 19.09% |
| Options outstanding (unexercised) | 20 grantees, 4 price tranches | 3,100,000 | 14.09% |
| Available option pool | 2019 EIP | 1,275,000 (Summary line) / 1,204,000 (FD build & term sheet) | 5.79% |
| Warrant | Pinnacle National Bank | 150,000 | 0.68% |
| **Total common outstanding** | | **10,450,000** | |
| **Total outstanding (excl. options/pool)** | | **18,300,000** | |
| **Fully diluted per spreadsheet build** | | **22,004,000** | 100.00% |

### 2.2 Reconciliation of the Fully Diluted Buildup

The spreadsheet's FD buildup (10,000,000 + 3,500,000 + 4,200,000 + 3,100,000 + 1,204,000 = 22,004,000) omits three items visible elsewhere in the same workbook:

- **Exercised-option common (450,000)** — counted in the 18,300,000 outstanding total but not in the FD buildup;
- **Warrant shares (150,000)** — shown in the Warrants tab and Summary as 0.68% of FD, yet excluded from the FD buildup (internally inconsistent percentages);
- **71,000-share pool difference** (1,275,000 per Option Grants tab vs. 1,204,000 used in the buildup).

**Corrected fully diluted count (before pool increase), using cap table Series A of 3,500,000:** 10,000,000 + 450,000 + 3,500,000 + 4,200,000 + 3,100,000 + 1,275,000 + 150,000 = **22,675,000**.

**Using the COI's Series A figure of 3,820,616:** 22,675,000 + 320,616 = **22,995,616**.

**Including the §1.10 pool increase (+2,500,000):** up to **25,175,000 – 25,495,616** depending on Series A resolution.

### 2.3 Convertible Note History

Per the Convertible Note Purchase Agreement (Jan 15, 2021) and COI §5A.1: $750,000 principal, 6% simple interest, 20% discount, $25M cap, maturity January 15, 2023. The note converted at the Series A closing (June 22, 2021) into **320,616 Series A shares at a $2.40 conversion price** (the 20%-of-$3.00 discount price; the $25M cap was not binding), representing principal plus accrued interest of **$769,479.45** (check: $769,479.45 ÷ $2.40 = 320,616.4, rounded down per §2.5). The note is no longer outstanding and does not affect the Series C cap table — but its conversion shares do (see §4.1).

### 2.4 Option Pool Detail (2019 EIP)

Reserve history: 2,000,000 (2019) → 3,500,000 (Series A, 2021) → 5,000,000 (Series B, 2022). Activity per Option Grants tab:

| Tranche | Granted | Forfeited | Exercised | Outstanding | Vested (11/8/24) |
|---|---:|---:|---:|---:|---:|
| $0.50 | 1,200,000 | 0 | 450,000 | 750,000 | 750,000 |
| $1.25 | 800,000 | 100,000 | 0 | 700,000 | 700,000 |
| $3.50 | 925,000 | 75,000 | 0 | 850,000 | 745,833 |
| $6.50 | 800,000 | 0 | 0 | 800,000 | 297,916 |
| **Total** | **3,725,000** | **175,000** | **450,000** | **3,100,000** | **3,043,749** |

Available pool: 5,000,000 − 3,725,000 = **1,275,000** (formula check confirmed in workbook). Note: under EIP §2.3, forfeited shares revert to the reserve; the 1,275,000 figure per the workbook already nets forfeitures against the granted total, consistent with 3,725,000 granted (gross) less 175,000 forfeited = 3,550,000 net granted, implying 1,450,000 available — the workbook's own arithmetic (3,725,000 + 1,275,000 = 5,000,000) treats forfeitures as still encumbering the reserve; this should be clarified with the transfer agent since it changes the available pool by 175,000 shares.

---

## 3. SERIES C TERMS SUMMARY (TERM SHEET, NOVEMBER 8, 2024)

| Term | Value |
|---|---|
| Aggregate proceeds | $45,000,000 ($35M Ridgeline; $10M existing preferred pro rata) |
| Pre-money / Post-money | $180,000,000 / $225,000,000 |
| Pre-money FD denominator | 22,004,000 shares (§1.6) — see discrepancies, §4 |
| Price per share | $8.18 ($180,000,000 ÷ 22,004,000) |
| Shares issued | ~5,500,000 (Ridgeline ~4,278,973; existing holders ~1,221,027) |
| Dividends | 8% non-cumulative, when declared ($0.6544/share/yr) |
| Liquidation preference | 1.5x non-participating ($12.27/share), senior to Series A/B and Common; Series A (1x, $3.00) and Series B (1x, $6.00) pari passu behind Series C |
| Conversion | 1:1 initial; auto-conversion on ≥$50M IPO at ≥$16.36/share (2x OIP) or majority Series C consent |
| Anti-dilution | **Full ratchet** (vs. broad-based weighted average for Series A/B) |
| Voting | As-converted, with Common |
| Protective provisions | Series C-majority consent required for, inter alia, any equity issuance (including EIP grants), charter/bylaw amendments, debt >$5M, dividends, budget approval, board size, and hiring/terminating/compensating C-level officers |
| Pool increase | Pre-closing increase to 7,500,000 reserved shares (+2,500,000), dilution borne by existing holders |

### 3.1 Pro Forma Post-Money Cap Table (Term Sheet Basis; 27,504,000 FD)

| Holder/Class | Shares | % FD |
|---|---:|---:|
| Maya Chen (Common) | 5,000,000 | 18.18% |
| Raj Venkatesh (Common) | 3,500,000 | 12.73% |
| Lena Ostrowski (Common) | 1,500,000 | 5.45% |
| Firstvale — Series A | 3,500,000 | 12.73% |
| Summit Arc — Series B | 4,200,000 | 15.27% |
| Options outstanding | 3,100,000 | 11.27% |
| Available pool | 1,204,000 | 4.38% |
| Ridgeline — Series C | 4,278,973 | 15.56% |
| Existing preferred — Series C | 1,221,027 | 4.44% |
| **Total** | **27,504,000** | **100.00%** |

(Founders' aggregate dilution: 45.45% → 36.36%.) **If the corrected denominator of 22,995,616 (COI Series A, actual pool, warrants, exercised common) and the +2,500,000 pool increase are used, the price falls to approximately $180,000,000 ÷ 25,495,616 = $7.06 per share and Series C shares rise to ~6.4 million (~20.4% post-money** if the $45M raises at the corrected price; note the investors would still hold ~20% by construction). Any change in the denominator changes the price and share count under the term sheet's own mechanics.

### 3.2 Liquidation Preference Stack (Post-Series C)

| Series | Shares | Per-share preference | Aggregate |
|---|---:|---:|---:|
| Series C (1.5x, senior) | 5,500,000 | $12.27 | $67,485,000 |
| Series A (1x, pari passu w/ B) | 3,500,000 (or 3,820,616 per COI) | $3.00 | $10,500,000 (COI basis: $11,461,848) |
| Series B (1x, pari passu w/ A) | 4,200,000 | $6.00 | $25,200,000 |
| **Total stack** | | | **~$103.2M (cap table basis) / ~$104.1M (COI basis)** |

Non-participating throughout; holders may convert to Common instead where as-converted value exceeds the preference.

### 3.3 409A Valuation Cross-Check

Valiant Appraisals (as of 9/30/2024, report 10/18/2024): Common FMV **$8.75/share** via OPM; total equity value ~$145,000,000; volatility 65%; risk-free rate 4.52%; 3.0-year horizon; 25% DLOM. **Flag:** $8.75 common FMV exceeds the $8.18 Series C preferred price. A preferred share with a 1.5x preference should not price below contemporaneous illiquid common; either the Series C pricing (denominator error suppressing price) or the 409A inputs warrant re-examination. Note also the 409A total equity value ($145M) is below the Series C pre-money ($180M) — plausible for an option-pricing framework but worth noting for grant pricing.

---

## 4. DISCREPANCIES AND ISSUES LIST

### 4.1 Series A Share Count — 3,500,000 vs. 3,820,616 (HIGH)
COI §4.2(b)/§5A.1 and Exhibit A: 3,820,616 Series A shares outstanding including 320,616 note-conversion shares at $2.40. Cap table (Series A tab, own footnote), term sheet §1.6(iii), and 409A: 3,500,000. Because the term sheet makes cap table accuracy a closing condition (§1.11, §5.6), this must be reconciled — likely by amending/restating the cap table and adjusting the fully diluted denominator, price, and share count.

### 4.2 Fully Diluted Denominator Errors (HIGH)
§1.5 defines pre-money FD as inclusive of **all** outstanding options and warrants and the Available Option Pool, yet §1.6's 22,004,000 omits (a) the 150,000 warrant shares, (b) the 450,000 exercised-option common shares, and (c) 71,000 pool shares. Corrected figure: 22,675,000 (or 22,995,616 with the COI Series A count).

### 4.3 Pool Increase Not in Denominator (HIGH)
§1.10 mandates a +2,500,000 pool increase "included in the pre-money Fully Diluted Capitalization for purposes of calculating the Series C Original Issue Price," but §1.6 does not include it. With all corrections, the denominator approaches ~25.5M and the price ~$7.06, materially below $8.18.

### 4.4 Warrant Terms Conflict (MEDIUM)
Pinnacle National Bank warrant: COI says issued **March 10, 2022 at $3.50**; cap table/Warrants tab, 409A §3, and the venture-debt timeline say **June 22, 2021 at $3.00**, expiring June 22, 2031. Confirm the operative warrant document.

### 4.5 Founder Name (MEDIUM — corporate records)
"Raj Venkatesh" vs. "Raj Subramanian" across documents; confirm legal name for the Restated Charter, Series C purchase agreement, and stock ledger (cert. CS-002).

### 4.6 Board Designees (MEDIUM)
Cap table Series A/Series B tabs list Thomas Aldridge (Firstvale) and Victoria Langford (Summit Arc); the IRA, Voting Agreement §2.1, and 409A list Allison Trang and Derek Hollowell. Also, the Series C term sheet contemplates a Series C director (§2.5(b) references a Series C designee approving EIP issuances) but does not, in the portions reviewed, specify the expanded board composition; the Voting Agreement fixes the Board at five and requires amendment with preferred-class consents to change it.

### 4.7 409A FMV vs. Series C Price (MEDIUM)
See §3.3. Additionally, post-closing, a new 409A will be needed; the full ratchet and 1.5x preference will factor into the OPM breakpoints.

### 4.8 Protective Provision vs. EIP/COI (MEDIUM)
Series C §2.5(b) requires Series C majority consent for any equity issuance "including any... option... granted under any equity incentive plan, whether or not previously approved by the Board." This conflicts with the EIP (§3.2, §6.1: routine grants within the reserve need no separate preferred consent) and with the Series A/B COI excluded-issuance regimes. It would effectively give Ridgeline a consent right over every future hire grant — company should negotiate for a standard EIP carve-out (e.g., up to the increased 7,500,000 reserve).

### 4.9 Forfeiture Accounting in Pool (LOW)
1,275,000 "available pool" computed off gross grants (3,725,000) rather than net (3,550,000 after 175,000 forfeitures), notwithstanding EIP §2.3 reversion. 175,000-share difference; clarify with transfer agent (Ashford Financial Services).

### 4.10 Full Ratchet Anti-Dilution (deal-term flag)
A step change from the Series A/B broad-based weighted average; full ratchet with no tiered or time-limited fallback is highly investor-favorable and will compound any down-round; founders/Common bear the dilution.

---

## 5. GOVERNANCE AND RIGHTS CONTEXT

- **Board (current, per Voting Agreement §2.1/IRA §1.2):** Maya Chen (Common), Allison Trang (Series A/Firstvale), Derek Hollowell (Series B/Summit Arc), Dr. Samuel Otieno and Karen Lindqvist (Independent). Fixed at five; drag-along available on Board + majority Preferred + majority Common approval (Voting Agreement §3).
- **Pro rata participation:** The $10M existing-holder tranche is to be allocated per pro rata rights under the IRA (Term Sheet §1.4); each of Firstvale and Summit Arc is a "Major Investor" (≥1,000,000 preferred shares; IRA §1.14). Note that Firstvale's pro rata base may be understated if its true Series A holding is 3,820,616 (§4.1).
- **Registration rights:** Demand (2, after Aug 12, 2027 or post-IPO; ≥$15M), piggyback, and S-3 rights under the IRA; Ridgeline will presumably become a party via joinder/amendment at closing.
- **Authorization capacity:** 30,000,000 common authorized; current reservations (10,450,000 outstanding + 5,000,000 pool + 150,000 warrant + conversion reserves for 7,700,000 preferred) leave ample but not unlimited headroom; the pool increase to 7,500,000 and Series C issuance will require a charter amendment (new preferred designation from the 9,000,000 undesignated preferred shares is available for Series C — 5,500,000 fits within that reserve).

---

## 6. RECOMMENDATIONS

1. **Reconcile the Series A ledger** to 3,820,616 (or document the retirement/ cancellation of the 320,616 note-conversion shares if they were never issued) before signing definitive documents; cap table accuracy is a closing condition.
2. **Restate the fully diluted denominator** to include warrants, exercised common, the correct pool figure, the COI Series A count, and the §1.10 pool increase; recompute price and share count (~$7.06 / ~6.4M shares on fully corrected basis vs. $8.18 / 5.5M as drafted). Note that as drafted the errors run in the investors' favor (higher price, fewer shares), which the Company should surface now.
3. **Confirm the Pinnacle warrant's** issue date and exercise price against the executed warrant and Loan and Security Agreement.
4. **Resolve the founder-name and board-designee inconsistencies** in the cap table and corporate records before the Restated Charter is filed.
5. **Negotiate the §2.5(b) protective provision** to carve out EIP grants within the (increased) approved reserve, and align Series C anti-dilution toward broad-based weighted average or a time-limited ratchet.
6. **Commission a fresh 409A valuation promptly after closing**, and reconcile the current $8.75 common FMV vs. $8.18 preferred price anomaly with Valiant.
7. **Confirm pool availability accounting** (gross vs. net of forfeitures) with Ashford Financial Services.

---

*Prepared from the eight deal documents listed above. Figures labeled "COI basis" come from the Amended and Restated Certificate of Incorporation; "term sheet basis" from the Series C Term Sheet; cap table figures from the November 8, 2024 spreadsheet. Where documents conflict, both values are presented rather than silently selected. Items marked as flags/assumptions should be verified against executed instruments.*
