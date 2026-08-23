# CREDIT OPPORTUNITY MEMORANDUM

**Credit Suisse Group AG (CS)** | Financials — Global Systemically Important Bank (G-SIB)  
*Prepared using the Corporate Credit Risk Early-Warning System | Confidential — For Internal Discussion Purposes*

---

## Deal Context

This memorandum presents a retrospective credit risk assessment of Credit Suisse Group AG (“CS” or “the Bank”), evaluated through a proprietary composite early-warning model that combines bank-specific accounting ratios with a market-implied Merton distance-to-default measure. The purpose of this exercise is to demonstrate that CS's credit deterioration was observable and quantifiable well in advance of its emergency acquisition by UBS in March 2023 — the model's composite risk score crossed our defined distress threshold in 2022Q2, three quarters ahead of resolution, with the market-based signal (distance-to-default) providing the earliest confirmation.

---

## Executive Summary

- **Credit Suisse's composite credit risk score rose steadily from 57.1% (2022Q1) to 67.3%** in its final full trading quarter (2023Q1), crossing our 60% distress threshold in 2022Q2 — approximately three quarters before the UBS-brokered emergency rescue announced in March 2023.
- **Distance-to-default (Merton model) flagged the earliest and sharpest signal**: DD fell from 3.05 (2022Q1, baseline solvency) to 1.74 (2022Q2, implied PD 4.12%), well ahead of the accounting ratios' deterioration.
- **Peer comparison against JPMorgan Chase and Goldman Sachs** — both of which remained range-bound between 40–50% throughout the same period — confirms the deterioration was CS-specific, not sector-wide.
- **Recommendation / Rating: HIGH RISK — DISTRESS ZONE** (Composite Score 67.3%, pre-resolution). Consistent with the actual outcome of external resolution via UBS acquisition.

---

## Business & Industry Overview

Credit Suisse was a global systemically important bank headquartered in Zurich, operating across wealth management, investment banking, and Swiss universal banking. Heading into 2022, the Bank was already contending with a series of legacy risk-management and litigation issues (including the Archegos and Greensill episodes) that had eroded market confidence ahead of the period covered by this analysis.

The broader banking sector entered a period of acute stress in 2022–23 as aggressive central bank rate hikes compressed the value of fixed-income asset holdings and tightened funding conditions industry-wide, culminating in the March 2023 failures of Silicon Valley Bank and Signature Bank in the U.S. CS's collapse occurred within this same window but was driven primarily by idiosyncratic, CS-specific deposit flight rather than the asset-liability mismatch that drove the U.S. regional bank failures — a distinction this analysis supports through the deposit and funding data below.

---

## Credit Analysis

### Composite Risk Score Trajectory

The model's composite score, derived from a logistic regression fit against sector-appropriate bank signals (CET1 ratio, loan-to-deposit ratio, non-performing loan ratio, net interest margin) and distance-to-default, tracked a consistent upward trajectory through five quarters of active trading data:

| Quarter | CS Composite Score | JPM Composite Score | GS Composite Score |
| :--- | :--- | :--- | :--- |
| **2022Q1** | 57.1% | 45.0% | 45.1% |
| **2022Q2** | **61.4%** *(crosses 60% threshold)* | 44.9% | 49.6% |
| **2022Q3** | 63.7% | 43.6% | 48.6% |
| **2022Q4** | 65.2% | 40.2% | 48.4% |
| **2023Q1** | **67.3%** *(final active quarter — UBS rescue)* | 44.9% | 49.5% |

*Note: CS was delisted following the March 2023 UBS acquisition. Post-resolution quarters in the underlying dataset carry an imputed distress-floor value and are excluded from this table as they do not represent live market data.*

### Distance-to-Default: The Earliest Signal

The market-implied distance-to-default measure moved ahead of the accounting-based composite score, providing the earliest confirmation of deteriorating solvency:

| Quarter | Equity Volatility ($\sigma_E$) | Distance-to-Default ($DD$) | Implied PD (%) | Status / Milestone |
| :--- | :--- | :--- | :--- | :--- |
| **2022Q1** | 33.8% | 3.05 | 0.11% | Baseline solvency |
| **2022Q2** | 55.8% | **1.74** | **4.12%** | **Early warning triggered** |
| **2022Q3** | 76.5% | 1.00 | 15.84% | Accelerated distress |
| **2022Q4** | 98.2% | 0.55 | 29.11% | Severe deterioration |
| **2023Q1** | 135.4% | **-0.08** | **53.09%** | **UBS rescue quarter** |

### Deposit & Funding Stress

The most acute stress signal in the dataset is the deposit base itself. Total deposits fell from $390B to $180B — a **54% decline** — over five quarters, pushing the loan-to-deposit ratio from 76.9% to 144.4% over the same period:

| Quarter | Total Deposits | CET1 Capital | Loan-to-Deposit Ratio |
| :--- | :--- | :--- | :--- |
| **2022Q1** | $390B | $41.0B | 76.9% |
| **2022Q2** | $360B | $39.5B | 81.9% |
| **2022Q3** | $310B | $38.0B | 93.5% |
| **2022Q4** | $230B | $36.0B | 121.7% |
| **2023Q1** | $180B | $31.0B | 144.4% |

---

## Capital Structure

As a G-SIB, CS's capital structure included a substantial layer of Additional Tier 1 (AT1) contingent convertible bonds sitting subordinate to senior unsecured debt and senior to common equity in ordinary circumstances. A defining feature of the actual UBS resolution was that Swiss regulator FINMA exercised a full write-down of approximately CHF 16 billion in AT1 notes to zero as part of the rescue — while equity holders retained a residual (if severely diluted) recovery through UBS's stock-and-cash offer. This inverted the conventional capital structure waterfall (equity subordinate to AT1) and is a widely cited case study in contingent-capital risk. This analysis's declining CET1 trend (from $41.0B to $31.0B over the period, against broadly stable risk-weighted assets) is consistent with the capital erosion that ultimately triggered this outcome.

---

## Red Flags

- **CET1 capital declined from $41.0B to $31.0B (−24%)** over five quarters while risk-weighted assets remained broadly stable, signaling erosion of the Bank's core solvency buffer rather than balance-sheet shrinkage alone.
- **Loan-to-deposit ratio rose from 76.9% to 144.4%**, moving from a conservative funding profile to one indicating significant reliance on non-deposit funding — a classic precursor to a liquidity-driven crisis.
- **Equity volatility more than tripled (33.8% → 135.4%)**, directly compressing distance-to-default from a safe 3.05 to a negative reading (-0.08) by the final active quarter.
- **The composite score's deterioration was monotonic** across all five observed quarters with no quarter of improvement or stabilization — a pattern that, in hindsight, offered no false-recovery signal to mask the underlying trend.

---

## Peer Benchmarking

| Metric (2023Q1 / Latest Active) | Credit Suisse | JPMorgan Chase | Goldman Sachs |
| :--- | :--- | :--- | :--- |
| **Composite Risk Score** | **67.3%** | 44.9% | 49.5% |
| **Distance-to-Default** | **-0.08** | 6.70 | 5.30 |
| **Implied Probability of Default** | **53.09%** | < 0.0001% | < 0.0001% |
| **Loan-to-Deposit Ratio (2022Q1→Latest)** | **76.9% → 144.4%** | Stable, ~53–54% | N/A / stable |

---

## Downside Sensitivity

Had deposit outflows continued at the 2022Q4→2023Q1 run-rate (approximately $50B/quarter) for two additional quarters without external intervention, the loan-to-deposit ratio would have breached approximately 200%, and distance-to-default — already negative at -0.08 — would imply a probability of default approaching certainty on the model's logistic scale, underscoring why external resolution occurred when it did rather than the Bank stabilizing organically.

---

## Risk Factors

- **Model risk**: the composite score is derived from a 14-company sample (7 failures), a small dataset by conventional statistical standards; bank-sector coefficients in particular are based on only 4 companies and should be treated as directionally indicative rather than precisely calibrated.
- **The deposit flight captured here reflects reported quarterly balances**, not daily/weekly outflow velocity; the actual acute run in March 2023 occurred on a timescale faster than this quarterly framework can resolve.
- **No standalone funding-cost (e.g., interest expense/liabilities) metric was incorporated**; loan-to-deposit ratio serves as the model's sole funding-stress proxy.

---

## Recommendation / Rating

Based on the composite score of **67.3% (DISTRESS ZONE, >60% threshold)**, a negative and rapidly falling distance-to-default, and accelerating deposit attrition, this analysis would have assigned Credit Suisse a **HIGH RISK / DISTRESSED** rating as of 2023Q1 — consistent with, and in fact anticipating, the actual outcome of the Bank's emergency acquisition by UBS later that quarter. The earliest actionable signal in this framework (distance-to-default crossing into warning territory in 2022Q2) preceded the resolution event by approximately three quarters, which this analysis holds out as the model's central, defensible finding.
