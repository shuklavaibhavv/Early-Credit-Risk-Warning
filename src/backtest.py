"""
Backtest & Model Validation Engine.

Formally quantifies model performance across historical quarters:
1. Calculates exact 'Quarters of Advance Warning' for Group A distressed companies
   at 60% and 70% composite risk score thresholds.
2. Checks Group B healthy companies for false positives (false alarm rate).
"""

import csv
import json
from pathlib import Path
from typing import Any, Dict, List, Tuple
from companies import COMPANIES


# Actual collapse / bankruptcy / emergency rescue quarters for Group A companies
COLLAPSE_QUARTERS = {
    "BBBY": "2023Q2",  # Chapter 11 filing April 2023
    "PRTY": "2023Q1",  # Chapter 11 filing Jan 2023
    "RAD": "2023Q4",   # Chapter 11 filing Oct 2023
    "WE": "2023Q4",    # Chapter 11 filing Nov 2023
    "CS": "2023Q1",    # UBS Emergency Rescue March 2023
    "SIVB": "2023Q1",  # FDIC Receivership March 2023
    "VNTR": "2023Q2",  # Chapter 11 filing May 2023
}

QUARTER_ORDER = [
    "2022Q1",
    "2022Q2",
    "2022Q3",
    "2022Q4",
    "2023Q1",
    "2023Q2",
    "2023Q3",
    "2023Q4",
]


def get_quarter_index(q_str: str) -> int:
    """Returns 0-indexed position of a quarter string."""
    return QUARTER_ORDER.index(q_str) if q_str in QUARTER_ORDER else -1


def load_scored_dataset() -> List[Dict[str, Any]]:
    """Loads scored company quarterly observations from CSV."""
    csv_path = Path(__file__).parent.parent / "data" / "composite_credit_scores.csv"
    rows = []
    with open(csv_path, mode="r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["composite_credit_score"] = float(r["composite_credit_score"])
            r["composite_pd"] = float(r["composite_pd"])
            rows.append(r)
    return rows


def run_backtest(thresholds: List[float] = [60.0, 70.0]):
    """
    Executes backtest quantification.

    Calculates advance warning quarters for Group A and evaluates false positive rates for Group B.
    """
    rows = load_scored_dataset()
    company_name_map = {c["ticker"]: c["name"] for c in COMPANIES}

    # Group observations by ticker
    company_data = {}
    for r in rows:
        t = r["ticker"]
        if t not in company_data:
            company_data[t] = []
        company_data[t].append(r)

    # Sort each company's quarters chronologically
    for t in company_data:
        company_data[t].sort(key=lambda x: get_quarter_index(x["quarter"]))

    print("=" * 95)
    print("FORMAL MODEL BACKTEST & ADVANCE WARNING QUANTIFICATION")
    print("=" * 95)

    # 1. Evaluate Group A Distressed Companies
    print("\n--- 1. GROUP A DISTRESSED COMPANIES — ADVANCE WARNING METRICS ---")
    print(
        f"{'COMPANY':<22} | {'TICKER':<6} | {'COLLAPSE':<8} | "
        f"{'60% CROSS':<9} | {'60% ADV (Q)':<11} | "
        f"{'70% CROSS':<9} | {'70% ADV (Q)':<11}"
    )
    print("-" * 95)

    adv_warnings_60 = []
    adv_warnings_70 = []

    group_a_tickers = [t for t in COLLAPSE_QUARTERS.keys()]

    for ticker in group_a_tickers:
        comp_rows = company_data[ticker]
        company_name = company_name_map.get(ticker, ticker)
        collapse_q = COLLAPSE_QUARTERS[ticker]
        collapse_idx = get_quarter_index(collapse_q)

        # Helper to find first sustained threshold crossing
        def find_first_crossing(thresh):
            for r in comp_rows:
                q_idx = get_quarter_index(r["quarter"])
                if q_idx > collapse_idx:
                    break
                if r["composite_credit_score"] >= thresh:
                    return r["quarter"], collapse_idx - q_idx
            return "None", None

        cross_60_q, adv_60 = find_first_crossing(60.0)
        cross_70_q, adv_70 = find_first_crossing(70.0)

        if adv_60 is not None:
            adv_warnings_60.append(adv_60)
        if adv_70 is not None:
            adv_warnings_70.append(adv_70)

        adv_60_str = f"{adv_60} Qtrs" if adv_60 is not None else "N/A"
        adv_70_str = f"{adv_70} Qtrs" if adv_70 is not None else "N/A"

        print(
            f"{company_name:<22} | {ticker:<6} | {collapse_q:<8} | "
            f"{cross_60_q:<9} | {adv_60_str:<11} | "
            f"{cross_70_q:<9} | {adv_70_str:<11}"
        )

    print("-" * 95)

    avg_adv_60 = sum(adv_warnings_60) / len(adv_warnings_60) if adv_warnings_60 else 0
    avg_adv_70 = sum(adv_warnings_70) / len(adv_warnings_70) if adv_warnings_70 else 0

    print(f"Average Advance Warning at 60% Threshold: {avg_adv_60:.2f} Quarters ({avg_adv_60*3:.1f} Months)")
    print(f"Average Advance Warning at 70% Threshold: {avg_adv_70:.2f} Quarters ({avg_adv_70*3:.1f} Months)")

    # 2. Evaluate Group B Healthy Companies (False Positive Check)
    print("\n--- 2. GROUP B HEALTHY COMPANIES — FALSE POSITIVE CHECK ---")
    print(f"{'COMPANY':<26} | {'TICKER':<6} | {'MAX RISK SCORE':<14} | {'FALSE POSITIVE (>=60%)':<22} | {'FALSE POSITIVE (>=70%)':<22}")
    print("-" * 95)

    group_b_tickers = [
        t for t, rows in company_data.items() if rows[0]["group"] == "B"
    ]
    fp_count_60 = 0
    fp_count_70 = 0

    for ticker in group_b_tickers:
        comp_rows = company_data[ticker]
        company_name = company_name_map.get(ticker, ticker)

        max_score = max(r["composite_credit_score"] for r in comp_rows)
        max_q = next(r["quarter"] for r in comp_rows if r["composite_credit_score"] == max_score)

        fp_60 = max_score >= 60.0
        fp_70 = max_score >= 70.0

        if fp_60:
            fp_count_60 += 1
        if fp_70:
            fp_count_70 += 1

        fp_60_str = f"YES ({max_q})" if fp_60 else "NO (Passed Clean)"
        fp_70_str = f"YES ({max_q})" if fp_70 else "NO (Passed Clean)"

        print(
            f"{company_name:<26} | {ticker:<6} | {max_score:.1f}% ({max_q})   | "
            f"{fp_60_str:<22} | {fp_70_str:<22}"
        )

    print("-" * 95)
    fp_rate_60 = (fp_count_60 / len(group_b_tickers)) * 100.0
    fp_rate_70 = (fp_count_70 / len(group_b_tickers)) * 100.0

    print(f"Group B False Positive Rate (>=60% Threshold): {fp_count_60}/{len(group_b_tickers)} ({fp_rate_60:.1f}%)")
    print(f"Group B False Positive Rate (>=70% Threshold): {fp_count_70}/{len(group_b_tickers)} ({fp_rate_70:.1f}%)")
    print("=" * 95)

    # 3. Save Backtest Results Summary to JSON
    backtest_summary = {
        "group_a_advance_warning": {
            "threshold_60_pct": {
                "average_quarters_warning": round(avg_adv_60, 2),
                "average_months_warning": round(avg_adv_60 * 3, 1),
            },
            "threshold_70_pct": {
                "average_quarters_warning": round(avg_adv_70, 2),
                "average_months_warning": round(avg_adv_70 * 3, 1),
            },
        },
        "group_b_false_positives": {
            "threshold_60_pct": {
                "false_positive_count": fp_count_60,
                "total_healthy_companies": len(group_b_tickers),
                "false_positive_rate_pct": round(fp_rate_60, 1),
            },
            "threshold_70_pct": {
                "false_positive_count": fp_count_70,
                "total_healthy_companies": len(group_b_tickers),
                "false_positive_rate_pct": round(fp_rate_70, 1),
            },
        },
    }

    output_path = Path(__file__).parent.parent / "data" / "backtest_summary.json"
    with open(output_path, mode="w", encoding="utf-8") as f:
        json.dump(backtest_summary, f, indent=2)

    print(f"\nBacktest summary exported to: {output_path}")


if __name__ == "__main__":
    run_backtest()
