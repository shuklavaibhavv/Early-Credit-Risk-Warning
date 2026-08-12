"""
Generate Ratio Signals Script.
Loops over all 14 companies and historical quarters, calculates risk signals,
and exports the combined output to data/ratio_signals.csv.
"""

import csv
from pathlib import Path
from companies import COMPANIES
from fetch_data import get_quarterly_financial_data
from ratio_engine import get_risk_signals


def generate_ratio_signals():
    """Generates quarterly ratio signals for all companies and exports to CSV."""
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

        # Compute risk signals using router function
        signals = get_risk_signals(entry, sector)

        row = {
            "company": company_name,
            "ticker": ticker,
            "quarter": quarter,
            "sector": sector,
            "group": group,
            "signal_1": signals.get("signal_1"),
            "signal_2": signals.get("signal_2"),
            "signal_3": signals.get("signal_3"),
            "signal_4": signals.get("signal_4"),
            "signal_5": signals.get("signal_5"),
        }
        rows.append(row)

    # Sort rows by ticker and quarter
    rows.sort(key=lambda r: (r["ticker"], r["quarter"]))

    # Output CSV path
    output_dir = Path(__file__).parent.parent / "data"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_csv = output_dir / "ratio_signals.csv"

    fieldnames = [
        "company",
        "ticker",
        "quarter",
        "sector",
        "group",
        "signal_1",
        "signal_2",
        "signal_3",
        "signal_4",
        "signal_5",
    ]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Successfully generated {len(rows)} rows of ratio signals in: {output_csv}")
    return rows


if __name__ == "__main__":
    generate_ratio_signals()
