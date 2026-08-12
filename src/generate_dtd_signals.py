"""
Distance-to-Default (DD) Generator & Validation Script.

Computes Merton Distance-to-Default (DD) and Probability of Default (PD)
for Target, JPMorgan Chase, Credit Suisse, and the full 14-company cohort across 8 quarters.
Exports the combined output to data/merton_dtd_signals.csv.
"""

import csv
from pathlib import Path
from companies import COMPANIES
from fetch_data import get_quarterly_financial_data, get_stock_price_history
from distance_to_default import calculate_dtd_for_company, get_equity_volatility


def run_dtd_analysis():
    raw_data = get_quarterly_financial_data()
    company_map = {c["ticker"]: c for c in COMPANIES}

    rows = []

    for entry in raw_data:
        ticker = entry["ticker"]
        quarter = entry["quarter"]

        if ticker not in company_map:
            continue

        comp = company_map[ticker]
        company_name = comp["name"]
        sector = comp["sector"]
        group = comp["group"]

        # Extract market value of equity and total debt
        equity_val = entry.get("market_value_equity")
        total_debt = entry.get("total_debt") or entry.get("total_liabilities")

        # Get price history
        price_hist = get_stock_price_history(ticker, quarter)

        # Compute Merton DD & PD
        dtd_res = calculate_dtd_for_company(
            ticker=ticker,
            quarter=quarter,
            price_history=price_hist,
            total_debt=total_debt,
            equity_value=equity_val,
            risk_free_rate=0.04,
            time_horizon=1.0,
        )

        eq_vol = dtd_res["equity_volatility"]
        dd = dtd_res["distance_to_default"]
        pd_val = dtd_res["probability_of_default"]

        row = {
            "company": company_name,
            "ticker": ticker,
            "quarter": quarter,
            "sector": sector,
            "group": group,
            "equity_value_M": equity_val,
            "total_debt_M": total_debt,
            "equity_volatility": eq_vol,
            "distance_to_default": dd,
            "probability_of_default": pd_val,
        }
        rows.append(row)

    rows.sort(key=lambda r: (r["ticker"], r["quarter"]))

    # Save to data/merton_dtd_signals.csv
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "merton_dtd_signals.csv"

    fieldnames = [
        "company",
        "ticker",
        "quarter",
        "sector",
        "group",
        "equity_value_M",
        "total_debt_M",
        "equity_volatility",
        "distance_to_default",
        "probability_of_default",
    ]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} rows of Merton DD signals in: {output_csv}")
    return rows


if __name__ == "__main__":
    rows = run_dtd_analysis()

    # 1. Target (TGT) Test
    tgt_rows = [r for r in rows if r["ticker"] == "TGT"]
    print("\n=== 1. TARGET (TGT) MERTON DD RESULTS ===")
    for r in tgt_rows:
        dd_str = f"{r['distance_to_default']:.3f}" if r["distance_to_default"] is not None else "None"
        pd_str = f"{r['probability_of_default']*100:.4f}%" if r["probability_of_default"] is not None else "None"
        vol_str = f"{r['equity_volatility']*100:.2f}%" if r["equity_volatility"] is not None else "None"
        print(f"  {r['quarter']}: EqVol = {vol_str:<7} | DD = {dd_str:<6} | PD = {pd_str}")

    # 2. JPMorgan Chase (JPM) Test
    jpm_rows = [r for r in rows if r["ticker"] == "JPM"]
    print("\n=== 2. JPMORGAN CHASE (JPM) MERTON DD RESULTS ===")
    for r in jpm_rows:
        dd_str = f"{r['distance_to_default']:.3f}" if r["distance_to_default"] is not None else "None"
        pd_str = f"{r['probability_of_default']*100:.4f}%" if r["probability_of_default"] is not None else "None"
        vol_str = f"{r['equity_volatility']*100:.2f}%" if r["equity_volatility"] is not None else "None"
        print(f"  {r['quarter']}: EqVol = {vol_str:<7} | DD = {dd_str:<6} | PD = {pd_str}")

    # 3. Credit Suisse (CS) Key Comparison
    cs_rows = [r for r in rows if r["ticker"] == "CS"]
    print("\n=== 3. CREDIT SUISSE (CS) MERTON DD EARLY WARNING ANALYSIS ===")
    print(f"{'QUARTER':<8} | {'EQ VOLATILITY':<14} | {'DISTANCE TO DEFAULT':<20} | {'IMPLIED PD':<12}")
    print("-" * 65)
    for r in cs_rows:
        vol_str = f"{r['equity_volatility']*100:.2f}%" if r["equity_volatility"] is not None else "Delisted/None"
        dd_str = f"{r['distance_to_default']:.4f}" if r["distance_to_default"] is not None else "None"
        pd_str = f"{r['probability_of_default']*100:.2f}%" if r["probability_of_default"] is not None else "None"
        print(f"{r['quarter']:<8} | {vol_str:<14} | {dd_str:<20} | {pd_str:<12}")

    # 4. Summary Table across 14 Companies for 2022Q2 and 2022Q4
    print("\n=== 4. 14-COMPANY COHORT MERTON DD COMPARISON (2022Q2 & 2022Q4) ===")
    print(f"{'TICKER':<6} | {'GROUP':<5} | {'2022Q2 DD':<10} | {'2022Q2 PD':<10} | {'2022Q4 DD':<10} | {'2022Q4 PD':<10}")
    print("-" * 65)
    tickers = [c["ticker"] for c in COMPANIES]
    for t in tickers:
        r_q2 = next((r for r in rows if r["ticker"] == t and r["quarter"] == "2022Q2"), None)
        r_q4 = next((r for r in rows if r["ticker"] == t and r["quarter"] == "2022Q4"), None)
        group = next(c["group"] for c in COMPANIES if c["ticker"] == t)

        q2_dd = f"{r_q2['distance_to_default']:.2f}" if r_q2 and r_q2["distance_to_default"] is not None else "None"
        q2_pd = f"{r_q2['probability_of_default']*100:.2f}%" if r_q2 and r_q2["probability_of_default"] is not None else "None"
        q4_dd = f"{r_q4['distance_to_default']:.2f}" if r_q4 and r_q4["distance_to_default"] is not None else "None"
        q4_pd = f"{r_q4['probability_of_default']*100:.2f}%" if r_q4 and r_q4["probability_of_default"] is not None else "None"

        print(f"{t:<6} | {group:<5} | {q2_dd:<10} | {q2_pd:<10} | {q4_dd:<10} | {q4_pd:<10}")
