# Quantitative Credit Risk & Solvency Engine

### 🌐 [**Live Interactive Dashboard →**](https://shuklavaibhavv.github.io/Early-Credit-Risk-Warning/)

I built this project to test a simple question: **could we have predicted major corporate bankruptcies and bank collapses (like Credit Suisse, SVB, WeWork, and Bed Bath & Beyond) months before they actually happened?**

Standard financial ratios like Altman Z-Score work well for normal retail or chemical companies, but they break down when you try to apply them to banks — or when financial statements are filed with a 45-day SEC lag. To solve this, I combined sector-tailored accounting ratios with Merton's structural Distance-to-Default model (which uses daily stock market prices to estimate firm solvency in real time).

---

## 🚀 Key Highlights & Results

- **13.7 Months (4.57 Quarters) Average Early Warning**: Across 7 distressed companies that failed or needed emergency rescue in 2023, the composite model flagged a high-risk warning score (>60%) an average of nearly 14 months before collapse.
- **Zero False Positives (0.0%)**: None of the 7 healthy control companies (JPMorgan, Goldman Sachs, Apple, Microsoft, Costco, Target, Air Products) ever crossed the warning threshold.
- **Credit Suisse Case Study**: While Credit Suisse's accounting CET1 ratio looked safe in early 2022, market equity volatility exploded. The Merton Distance-to-Default metric dropped to **1.74** in **2022Q2** (implied default probability of 4.12%), giving a **3-quarter advance warning** before the UBS rescue in March 2023.

---

## 📋 Credit Opportunity Memo

As a follow-on deliverable, I synthesized this model's quantitative findings on Credit Suisse into a formal investment-banking-style credit memo. The memorandum translates raw model signals into an institutional credit report covering business & industry overview, capital structure (including Swiss regulator FINMA's AT1 bond write-down), balance-sheet red flags, peer benchmarking against JPMorgan Chase and Goldman Sachs, and a quantified rating recommendation.

📄 **[View Full Credit Opportunity Memo (PDF)](reports/Credit_Opportunity_Memo_CreditSuisse.pdf)**

---

## 🛠️ How It Works

### 1. Dual-Path Ratio Engine
Different industries need different financial metrics:
- **Non-Banks (Retail, Chemical, etc.)**: Calculates Altman Z-Score, Debt/EBITDA, Interest Coverage (EBIT / Interest Expense), Current Ratio, and quarter-over-quarter Cash Burn Rate (negative values mean burning cash).
- **Banks**: Swaps out non-applicable ratios for regulatory capital and liquidity metrics — CET1 Capital Ratio, Loan-to-Deposit Ratio, Non-Performing Loans (NPL %), Net Interest Margin (NIM), and Bank Leverage.

### 2. Merton Distance-to-Default (DD)
Treats a company's equity as a European call option on its underlying asset value ($V_A$), with the total debt face value ($D$) as the strike price:
$$\text{Equity } E = V_A \Phi(d_1) - D e^{-r T} \Phi(d_2)$$
$$\sigma_E E = \Phi(d_1) \sigma_A V_A$$
It iteratively solves for asset value ($V_A$) and asset volatility ($\sigma_A$) to calculate Distance-to-Default ($DD$) and implied default probability ($PD = \Phi(-DD)$).

### 3. Logistic Regression Scoring Model
Combines the 5 ratio signals plus Merton DD into a single risk probability (0 to 100%):

$$\text{Risk Score } P(\text{Default} = 1) = \frac{1}{1 + e^{-(\beta_0 + \boldsymbol{\beta}^T \mathbf{z})}}$$

- **Top Risk Reducer**: Merton Distance-to-Default ($\beta = -1.0049$) — high DD means strong market solvency buffer.
- **Top Risk Increase**: Debt / EBITDA ($\beta = +0.6342$) — heavy leverage drives default risk up.
- **Other Weights**: Solvency/Z-Score ($\beta = -0.4707$), Coverage ($\beta = -0.3776$), Cash Flow ($\beta = -0.1844$), Liquidity ($\beta = -0.0412$), Intercept ($\beta_0 = -0.2737$).

---

## 📁 Project Structure

```
credit_risk_project/
├── start.py                        # Main launcher script
├── docs/
│   └── index.html                  # GitHub Pages live dashboard (deployed)
├── src/
│   ├── companies.py                # 14-company cohort metadata (Group A Distressed vs Group B Healthy)
│   ├── ratio_engine.py             # Ratio calculation logic with safe division handlers
│   ├── distance_to_default.py      # Merton DD non-linear solver
│   ├── composite_score.py          # Logistic regression model trainer & dataset scorer
│   ├── backtest.py                 # Advance warning lead time & false positive calculator
│   └── run_pipeline.py             # Pipeline orchestrator script
├── dashboard/
│   ├── index.html                  # Standalone interactive dark-theme HTML/JS dashboard
│   ├── app.py                      # Streamlit interactive dashboard
│   └── .streamlit/config.toml      # Dark navy visual theme config
├── reports/
│   ├── Credit_Opportunity_Memo_CreditSuisse.pdf  # Investment-banking-style Credit Memo (PDF)
│   └── Credit_Opportunity_Memorandum_CS.md       # Markdown version of Credit Memo
├── data/                           # Generated CSV signals, JSON models & backtest results
└── research_note.md                # Quantitative methodology writeup & mathematical breakdown
```

---

## 💻 Quick Start

Run the entire pipeline and open the dashboard with a single command:

```bash
python3 start.py
```

This will run all 4 pipeline stages (ratios $\rightarrow$ Merton DD $\rightarrow$ composite scoring $\rightarrow$ backtesting), check that output files exist, and open the interactive dashboard directly in your default browser.

You can also view the HTML dashboard directly by opening `dashboard/index.html` in Chrome or Safari.
