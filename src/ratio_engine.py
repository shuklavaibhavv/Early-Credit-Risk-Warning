"""
Ratio Engine Module for Credit Risk Analysis.

Calculates key financial ratios and risk signals for both non-bank (standard) 
and bank financial institutions. Handles missing data, zero/negative denominators, and edge cases.
"""

import math
from typing import Any, Dict, Optional, Union


def safe_divide(
    numerator: Any,
    denominator: Any,
    default: Optional[float] = None,
    allow_non_positive_denominator: bool = True,
) -> Optional[float]:
    """
    Safely divides numerator by denominator handling None, NaN, zero division, Inf, and non-positive denominators.

    Args:
        numerator: Numerator value.
        denominator: Denominator value.
        default: Fallback value returned if division fails or denominator is invalid.
        allow_non_positive_denominator: If False, returns default when denominator <= 0.

    Returns:
        Divided float result or default fallback.
    """
    if numerator is None or denominator is None:
        return default
    try:
        num = float(numerator)
        den = float(denominator)
        if den == 0.0 or (not allow_non_positive_denominator and den <= 0.0):
            return default
        res = num / den
        if math.isinf(res) or math.isnan(res):
            return default
        return res
    except (ValueError, TypeError, ZeroDivisionError, OverflowError):
        return default


def calculate_standard_signals(
    company_data: Union[Dict[str, Any], Any]
) -> Dict[str, Any]:
    """
    Calculates standard credit risk signals for non-bank companies.

    Ratios Computed:
    1. Altman Z-Score: Z = 1.2*(WC/TA) + 1.4*(RE/TA) + 3.3*(EBIT/TA) + 0.6*(MVE/TL) + 1.0*(Sales/TA)
       - X1 (WC/TA): Working Capital to Total Assets (liquidity measure).
       - X2 (RE/TA): Retained Earnings to Total Assets (cumulative profitability).
       - X3 (EBIT/TA): EBIT to Total Assets (asset productivity).
       - X4 (MVE/TL): Market Value of Equity to Total Liabilities (solvency/leverage).
       - X5 (Sales/TA): Sales to Total Assets (asset turnover).
       - Standard Interpretation: Z > 2.99 (Safe), 1.81 <= Z <= 2.99 (Grey Zone), Z < 1.81 (Distress).
    2. Debt to EBITDA: Total Debt / EBITDA
       - Measures leverage and debt repayment capacity in years of cash earnings.
       - Returns None if EBITDA <= 0 (distressed or non-earning company).
    3. Interest Coverage Ratio: EBIT / Interest Expense
       - Measures ability to service debt interest payments from operating profits.
       - Returns None if Interest Expense <= 0.
    4. Current Ratio: Current Assets / Current Liabilities
       - Measures short-term liquidity and ability to cover short-term obligations.
    5. Cash Burn Rate: Cash(t) - Cash(t-1) (Quarter-over-Quarter Change in Cash)
       - Sign Convention: NEGATIVE when cash decreases (cash burn/consumption), POSITIVE when cash increases.

    Args:
        company_data: Dictionary or Series containing financial metrics.

    Returns:
        Structured dictionary containing signal_1 to signal_5 and metadata labels.
    """
    get_val = (
        lambda key: company_data.get(key)
        if isinstance(company_data, dict)
        else getattr(company_data, key, None)
    )

    total_assets = get_val("total_assets")
    total_liabilities = get_val("total_liabilities")
    current_assets = get_val("current_assets")
    current_liabilities = get_val("current_liabilities")
    retained_earnings = get_val("retained_earnings")
    ebit = get_val("ebit")
    ebitda = get_val("ebitda")
    sales = get_val("sales")
    market_value_equity = get_val("market_value_equity")
    total_debt = get_val("total_debt")
    interest_expense = get_val("interest_expense")
    cash = get_val("cash")
    cash_prev = get_val("cash_prev")

    # 1. Altman Z-Score Components
    working_capital = (
        (current_assets - current_liabilities)
        if (current_assets is not None and current_liabilities is not None)
        else None
    )

    x1 = safe_divide(working_capital, total_assets)
    x2 = safe_divide(retained_earnings, total_assets)
    x3 = safe_divide(ebit, total_assets)
    x4 = safe_divide(market_value_equity, total_liabilities)
    x5 = safe_divide(sales, total_assets)

    if all(param is not None for param in [x1, x2, x3, x4, x5]):
        altman_z = (1.2 * x1) + (1.4 * x2) + (3.3 * x3) + (0.6 * x4) + (1.0 * x5)
    else:
        altman_z = None

    # 2. Debt / EBITDA (EBITDA must be > 0)
    debt_to_ebitda = safe_divide(
        total_debt, ebitda, allow_non_positive_denominator=False
    )

    # 3. Interest Coverage Ratio (Interest Expense must be > 0)
    interest_coverage = safe_divide(
        ebit, interest_expense, allow_non_positive_denominator=False
    )

    # 4. Current Ratio
    current_ratio = safe_divide(current_assets, current_liabilities)

    # 5. Cash Burn Rate (QoQ Cash Change: cash_t - cash_t-1)
    # Negative when cash decreases, Positive when cash increases
    cash_burn = (
        (cash - cash_prev)
        if (cash is not None and cash_prev is not None)
        else None
    )

    return {
        "signal_1": altman_z,
        "signal_2": debt_to_ebitda,
        "signal_3": interest_coverage,
        "signal_4": current_ratio,
        "signal_5": cash_burn,
        "labels": {
            "signal_1": "Altman Z-Score",
            "signal_2": "Debt / EBITDA",
            "signal_3": "Interest Coverage Ratio",
            "signal_4": "Current Ratio",
            "signal_5": "Cash Burn Rate",
        },
    }


def calculate_bank_signals(
    company_data: Union[Dict[str, Any], Any]
) -> Dict[str, Any]:
    """
    Calculates credit risk signals tailored specifically for bank/financial institutions.

    Ratios Computed:
    1. CET1 Ratio: CET1 Capital / Risk-Weighted Assets
    2. Loan-to-Deposit Ratio: Total Loans / Total Deposits
    3. Non-Performing Loan (NPL) Ratio: Non-Performing Loans / Total Loans
    4. Net Interest Margin (NIM): Net Interest Income / Interest-Earning Assets
    5. Bank Leverage Ratio: CET1 Capital / Total Assets

    Args:
        company_data: Dictionary or Series containing bank metrics.

    Returns:
        Structured dictionary containing signal_1 to signal_5 and metadata labels.
    """
    get_val = (
        lambda key: company_data.get(key)
        if isinstance(company_data, dict)
        else getattr(company_data, key, None)
    )

    cet1_capital = get_val("cet1_capital")
    risk_weighted_assets = get_val("risk_weighted_assets")
    total_loans = get_val("total_loans")
    total_deposits = get_val("total_deposits")
    non_performing_loans = get_val("non_performing_loans")
    net_interest_income = get_val("net_interest_income")
    interest_earning_assets = get_val("interest_earning_assets")
    total_assets = get_val("total_assets")

    # 1. CET1 Ratio
    cet1_ratio = safe_divide(cet1_capital, risk_weighted_assets)

    # 2. Loan-to-Deposit Ratio
    loan_to_deposit = safe_divide(total_loans, total_deposits)

    # 3. Non-Performing Loan Ratio
    npl_ratio = safe_divide(non_performing_loans, total_loans)

    # 4. Net Interest Margin
    net_interest_margin = safe_divide(
        net_interest_income, interest_earning_assets
    )

    # 5. Bank Leverage Ratio
    bank_leverage = safe_divide(cet1_capital, total_assets)

    return {
        "signal_1": cet1_ratio,
        "signal_2": loan_to_deposit,
        "signal_3": npl_ratio,
        "signal_4": net_interest_margin,
        "signal_5": bank_leverage,
        "labels": {
            "signal_1": "CET1 Ratio",
            "signal_2": "Loan-to-Deposit Ratio",
            "signal_3": "Non-Performing Loan Ratio",
            "signal_4": "Net Interest Margin",
            "signal_5": "Bank Leverage Ratio",
        },
    }


def get_risk_signals(
    company_data: Union[Dict[str, Any], Any], sector: str
) -> Dict[str, Any]:
    """
    Router function to calculate appropriate credit risk signals based on sector.

    Args:
        company_data: Dictionary or Series with financial metrics.
        sector: Sector name (e.g. 'bank', 'retail', 'chemical', 'baseline').

    Returns:
        Structurally comparable dictionary with keys signal_1 through signal_5 and labels.
    """
    if str(sector).lower().strip() == "bank":
        return calculate_bank_signals(company_data)
    else:
        return calculate_standard_signals(company_data)
