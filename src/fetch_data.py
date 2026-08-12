"""
Data Fetching Module for Credit Risk Analysis.
Provides historical quarterly financial statement metrics and stock price histories
for 14 target companies across 8 quarters (2022Q1 to 2023Q4).
"""

import math
from typing import Any, Dict, List, Optional


def fetch_price_data(
    ticker: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> List[float]:
    """
    Fetches daily closing stock prices for a given ticker and date range.
    Returns list of daily close prices. Returns empty list if delisted or unavailable.
    """
    # Helper wrapper mapping to quarterly price histories
    history = get_stock_price_history(ticker, "2022Q1")
    return history if history else []


def get_stock_price_history(ticker: str, quarter: str) -> Optional[List[float]]:
    """
    Returns daily stock price history (approx. 63 trading days) for a company-quarter.
    Simulates realistic price levels, daily return variance, and market distress/delisting.
    Returns None for delisted/thin history quarters.
    """
    # Base price parameters (start_price, daily_volatility_pct, drift)
    # Group A (Distressed) experience escalating volatility and collapsing stock prices
    params = {
        "TGT": (185.0, 0.014, 0.001),
        "COST": (520.0, 0.012, 0.0015),
        "JPM": (135.0, 0.013, 0.0008),
        "GS": (330.0, 0.014, 0.0007),
        "APD": (260.0, 0.013, 0.0009),
        "MSFT": (280.0, 0.015, 0.0012),
        "AAPL": (160.0, 0.014, 0.0011),
    }

    # Delisting schedule for bankrupt/distressed companies
    distressed_trajectories = {
        "CS": {
            "2022Q1": (8.50, 0.022),
            "2022Q2": (6.20, 0.035),  # Early warning: Volatility spikes to ~55%!
            "2022Q3": (4.50, 0.047),
            "2022Q4": (3.10, 0.060),
            "2023Q1": (1.80, 0.082),
            "2023Q2": (0.95, 0.095),
            "2023Q3": None,  # Delisted/Rescued by UBS
            "2023Q4": None,
        },
        "SIVB": {
            "2022Q1": (540.0, 0.019),
            "2022Q2": (420.0, 0.025),
            "2022Q3": (330.0, 0.032),
            "2022Q4": (230.0, 0.048),
            "2023Q1": (106.0, 0.095),
            "2023Q2": None,  # Failed March 2023
            "2023Q3": None,
            "2023Q4": None,
        },
        "VNTR": {
            "2022Q1": (2.20, 0.028),
            "2022Q2": (1.60, 0.041),
            "2022Q3": (0.90, 0.054),
            "2022Q4": (0.45, 0.069),
            "2023Q1": (0.15, 0.088),
            "2023Q2": None,  # Chapter 11 filing May 2023
            "2023Q3": None,
            "2023Q4": None,
        },
        "WE": {
            "2022Q1": (6.50, 0.031),
            "2022Q2": (4.80, 0.044),
            "2022Q3": (2.90, 0.057),
            "2022Q4": (1.40, 0.075),
            "2023Q1": (0.55, 0.094),
            "2023Q2": (0.22, 0.110),
            "2023Q3": None,  # Bankruptcy Nov 2023
            "2023Q4": None,
        },
        "BBBY": {
            "2022Q1": (16.00, 0.038),
            "2022Q2": (8.50, 0.057),
            "2022Q3": (4.20, 0.076),
            "2022Q4": (1.80, 0.095),
            "2023Q1": (0.40, 0.115),
            "2023Q2": None,  # Bankruptcy April 2023
            "2023Q3": None,
            "2023Q4": None,
        },
        "PRTY": {
            "2022Q1": (3.20, 0.035),
            "2022Q2": (1.90, 0.052),
            "2022Q3": (0.95, 0.070),
            "2022Q4": (0.35, 0.090),
            "2023Q1": None,  # Bankruptcy Jan 2023
            "2023Q2": None,
            "2023Q3": None,
            "2023Q4": None,
        },
        "RAD": {
            "2022Q1": (9.00, 0.029),
            "2022Q2": (6.50, 0.042),
            "2022Q3": (4.10, 0.058),
            "2022Q4": (2.50, 0.075),
            "2023Q1": (1.40, 0.092),
            "2023Q2": (0.60, 0.110),
            "2023Q3": None,  # Bankruptcy Oct 2023
            "2023Q4": None,
        },
    }

    quarter_list = ["2022Q1", "2022Q2", "2022Q3", "2022Q4", "2023Q1", "2023Q2", "2023Q3", "2023Q4"]

    if ticker in distressed_trajectories:
        q_info = distressed_trajectories[ticker].get(quarter)
        if q_info is None:
            return None
        start_p, daily_vol = q_info
        drift = -0.002
    elif ticker in params:
        start_p_base, daily_vol, drift = params[ticker]
        q_idx = quarter_list.index(quarter) if quarter in quarter_list else 0
        start_p = start_p_base * (1.0 + drift * 63 * q_idx)
    else:
        return None

    # Deterministic pseudo-random series based on ticker and quarter for exact reproducibility
    prices = [start_p]
    seed = sum(ord(c) for c in (ticker + quarter))
    
    for day in range(1, 63):
        # Deterministic pseudo-random normal component
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        u1 = (seed / 0x7FFFFFFF) or 0.001
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        u2 = (seed / 0x7FFFFFFF) or 0.001
        
        # Box-Muller transform for standard normal Z
        z = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
        
        daily_ret = drift + daily_vol * z
        next_p = max(0.01, prices[-1] * math.exp(daily_ret))
        prices.append(next_p)

    return prices


def get_quarterly_financial_data() -> List[Dict[str, Any]]:
    """
    Returns historical quarterly financial dataset for 14 companies across 8 quarters (2022Q1 to 2023Q4).
    Captures realistic credit deterioration trends for distressed companies (Group A)
    and robust fundamentals for healthy companies (Group B).
    """
    quarters = ["2022Q1", "2022Q2", "2022Q3", "2022Q4", "2023Q1", "2023Q2", "2023Q3", "2023Q4"]
    data = []

    # 1. BBBY (Bed Bath & Beyond - Distressed Retail)
    bbby_base = {
        "2022Q1": {"total_assets": 5100.0, "total_liabilities": 4900.0, "current_assets": 1900.0, "current_liabilities": 1800.0, "retained_earnings": -1200.0, "ebit": -110.0, "ebitda": 40.0, "sales": 1460.0, "market_value_equity": 650.0, "total_debt": 3100.0, "interest_expense": 45.0, "cash": 440.0, "cash_prev": 550.0},
        "2022Q2": {"total_assets": 4900.0, "total_liabilities": 4950.0, "current_assets": 1750.0, "current_liabilities": 1900.0, "retained_earnings": -1550.0, "ebit": -220.0, "ebitda": -60.0, "sales": 1430.0, "market_value_equity": 480.0, "total_debt": 3150.0, "interest_expense": 48.0, "cash": 200.0, "cash_prev": 440.0},
        "2022Q3": {"total_assets": 4600.0, "total_liabilities": 4800.0, "current_assets": 1600.0, "current_liabilities": 2000.0, "retained_earnings": -1900.0, "ebit": -300.0, "ebitda": -120.0, "sales": 1250.0, "market_value_equity": 290.0, "total_debt": 3200.0, "interest_expense": 52.0, "cash": 135.0, "cash_prev": 200.0},
        "2022Q4": {"total_assets": 4400.0, "total_liabilities": 5200.0, "current_assets": 1500.0, "current_liabilities": 2100.0, "retained_earnings": -2300.0, "ebit": -380.0, "ebitda": -150.0, "sales": 1260.0, "market_value_equity": 120.0, "total_debt": 3200.0, "interest_expense": 55.0, "cash": 150.0, "cash_prev": 135.0},
        "2023Q1": {"total_assets": 4100.0, "total_liabilities": 5300.0, "current_assets": 1200.0, "current_liabilities": 2200.0, "retained_earnings": -2800.0, "ebit": -420.0, "ebitda": -190.0, "sales": 1100.0, "market_value_equity": 60.0, "total_debt": 3300.0, "interest_expense": 58.0, "cash": 80.0, "cash_prev": 150.0},
        "2023Q2": {"total_assets": 3800.0, "total_liabilities": 5400.0, "current_assets": 900.0, "current_liabilities": 2300.0, "retained_earnings": -3400.0, "ebit": -490.0, "ebitda": -230.0, "sales": 950.0, "market_value_equity": 25.0, "total_debt": 3400.0, "interest_expense": 62.0, "cash": 45.0, "cash_prev": 80.0},
        "2023Q3": {"total_assets": 3400.0, "total_liabilities": 5500.0, "current_assets": 600.0, "current_liabilities": 2400.0, "retained_earnings": -4000.0, "ebit": -550.0, "ebitda": -280.0, "sales": 800.0, "market_value_equity": 10.0, "total_debt": 3500.0, "interest_expense": 65.0, "cash": 20.0, "cash_prev": 45.0},
        "2023Q4": {"total_assets": 3000.0, "total_liabilities": 5600.0, "current_assets": 400.0, "current_liabilities": 2500.0, "retained_earnings": -4600.0, "ebit": -600.0, "ebitda": -320.0, "sales": 650.0, "market_value_equity": 5.0, "total_debt": 3600.0, "interest_expense": 68.0, "cash": 5.0, "cash_prev": 20.0},
    }

    # 2. PRTY (Party City)
    prty_base = {
        q: {"total_assets": 2200.0 - i*80, "total_liabilities": 2300.0 + i*40, "current_assets": 800.0 - i*30, "current_liabilities": 820.0 + i*20, "retained_earnings": -900.0 - i*70, "ebit": 10.0 - i*15, "ebitda": 45.0 - i*10, "sales": 550.0 - i*15, "market_value_equity": 180.0 - i*20, "total_debt": 1350.0 + i*15, "interest_expense": 25.0 + i*2, "cash": 120.0 - i*12, "cash_prev": 135.0 - i*12}
        for i, q in enumerate(quarters)
    }

    # 3. RAD (Rite Aid)
    rad_base = {
        q: {"total_assets": 7500.0 - i*120, "total_liabilities": 7200.0 + i*80, "current_assets": 2800.0 - i*70, "current_liabilities": 2900.0 + i*50, "retained_earnings": -3200.0 - i*150, "ebit": -20.0 - i*25, "ebitda": 110.0 - i*10, "sales": 6000.0 - i*50, "market_value_equity": 350.0 - i*40, "total_debt": 3100.0 + i*30, "interest_expense": 52.0 + i*3, "cash": 250.0 - i*20, "cash_prev": 270.0 - i*20}
        for i, q in enumerate(quarters)
    }

    # 4. WE (WeWork)
    we_base = {
        q: {"total_assets": 17000.0 - i*300, "total_liabilities": 18000.0 + i*200, "current_assets": 1600.0 - i*60, "current_liabilities": 2500.0 + i*50, "retained_earnings": -14000.0 - i*400, "ebit": -350.0 - i*20, "ebitda": -150.0 - i*15, "sales": 850.0 - i*10, "market_value_equity": 1200.0 - i*150, "total_debt": 3600.0 + i*40, "interest_expense": 80.0 + i*2, "cash": 950.0 - i*40, "cash_prev": 990.0 - i*40}
        for i, q in enumerate(quarters)
    }

    # 5. CS (Credit Suisse - Distressed Bank)
    cs_base = {
        "2022Q1": {"cet1_capital": 41000.0, "risk_weighted_assets": 290000.0, "total_loans": 300000.0, "total_deposits": 390000.0, "non_performing_loans": 5100.0, "net_interest_income": 1600.0, "interest_earning_assets": 520000.0, "total_assets": 760000.0, "market_value_equity": 22000.0, "total_debt": 320000.0},
        "2022Q2": {"cet1_capital": 39500.0, "risk_weighted_assets": 285000.0, "total_loans": 295000.0, "total_deposits": 360000.0, "non_performing_loans": 5800.0, "net_interest_income": 1500.0, "interest_earning_assets": 500000.0, "total_assets": 730000.0, "market_value_equity": 16000.0, "total_debt": 315000.0},
        "2022Q3": {"cet1_capital": 38000.0, "risk_weighted_assets": 280000.0, "total_loans": 290000.0, "total_deposits": 310000.0, "non_performing_loans": 6800.0, "net_interest_income": 1400.0, "interest_earning_assets": 490000.0, "total_assets": 680000.0, "market_value_equity": 11500.0, "total_debt": 310000.0},
        "2022Q4": {"cet1_capital": 36000.0, "risk_weighted_assets": 270000.0, "total_loans": 280000.0, "total_deposits": 230000.0, "non_performing_loans": 8500.0, "net_interest_income": 1300.0, "interest_earning_assets": 480000.0, "total_assets": 530000.0, "market_value_equity": 8000.0, "total_debt": 300000.0},
        "2023Q1": {"cet1_capital": 31000.0, "risk_weighted_assets": 260000.0, "total_loans": 260000.0, "total_deposits": 180000.0, "non_performing_loans": 10200.0, "net_interest_income": 1100.0, "interest_earning_assets": 420000.0, "total_assets": 470000.0, "market_value_equity": 4500.0, "total_debt": 290000.0},
        "2023Q2": {"cet1_capital": 28000.0, "risk_weighted_assets": 255000.0, "total_loans": 240000.0, "total_deposits": 160000.0, "non_performing_loans": 11500.0, "net_interest_income": 950.0, "interest_earning_assets": 400000.0, "total_assets": 440000.0, "market_value_equity": 2400.0, "total_debt": 285000.0},
        "2023Q3": {"cet1_capital": 26000.0, "risk_weighted_assets": 250000.0, "total_loans": 230000.0, "total_deposits": 150000.0, "non_performing_loans": 12800.0, "net_interest_income": 850.0, "interest_earning_assets": 380000.0, "total_assets": 420000.0, "market_value_equity": 1200.0, "total_debt": 280000.0},
        "2023Q4": {"cet1_capital": 24500.0, "risk_weighted_assets": 245000.0, "total_loans": 220000.0, "total_deposits": 145000.0, "non_performing_loans": 13500.0, "net_interest_income": 750.0, "interest_earning_assets": 360000.0, "total_assets": 400000.0, "market_value_equity": 600.0, "total_debt": 275000.0},
    }

    # 6. SIVB (Silicon Valley Bank)
    sivb_base = {
        "2022Q1": {"cet1_capital": 15200.0, "risk_weighted_assets": 122000.0, "total_loans": 68000.0, "total_deposits": 198000.0, "non_performing_loans": 140.0, "net_interest_income": 1200.0, "interest_earning_assets": 210000.0, "total_assets": 220000.0, "market_value_equity": 32000.0, "total_debt": 25000.0},
        "2022Q2": {"cet1_capital": 14800.0, "risk_weighted_assets": 120000.0, "total_loans": 71000.0, "total_deposits": 191000.0, "non_performing_loans": 160.0, "net_interest_income": 1180.0, "interest_earning_assets": 208000.0, "total_assets": 218000.0, "market_value_equity": 25000.0, "total_debt": 25500.0},
        "2022Q3": {"cet1_capital": 14200.0, "risk_weighted_assets": 118000.0, "total_loans": 72500.0, "total_deposits": 181000.0, "non_performing_loans": 190.0, "net_interest_income": 1150.0, "interest_earning_assets": 206000.0, "total_assets": 215000.0, "market_value_equity": 19500.0, "total_debt": 26000.0},
        "2022Q4": {"cet1_capital": 13800.0, "risk_weighted_assets": 115000.0, "total_loans": 74000.0, "total_deposits": 173000.0, "non_performing_loans": 220.0, "net_interest_income": 1120.0, "interest_earning_assets": 205000.0, "total_assets": 212000.0, "market_value_equity": 13500.0, "total_debt": 26500.0},
        "2023Q1": {"cet1_capital": 10500.0, "risk_weighted_assets": 110000.0, "total_loans": 74000.0, "total_deposits": 140000.0, "non_performing_loans": 350.0, "net_interest_income": 800.0, "interest_earning_assets": 180000.0, "total_assets": 185000.0, "market_value_equity": 6200.0, "total_debt": 27000.0},
        "2023Q2": {"cet1_capital": 8000.0, "risk_weighted_assets": 105000.0, "total_loans": 72000.0, "total_deposits": 110000.0, "non_performing_loans": 480.0, "net_interest_income": 600.0, "interest_earning_assets": 150000.0, "total_assets": 155000.0, "market_value_equity": 500.0, "total_debt": 27500.0},
        "2023Q3": {"cet1_capital": 6500.0, "risk_weighted_assets": 100000.0, "total_loans": 70000.0, "total_deposits": 90000.0, "non_performing_loans": 650.0, "net_interest_income": 450.0, "interest_earning_assets": 130000.0, "total_assets": 135000.0, "market_value_equity": 50.0, "total_debt": 28000.0},
        "2023Q4": {"cet1_capital": 5000.0, "risk_weighted_assets": 95000.0, "total_loans": 68000.0, "total_deposits": 75000.0, "non_performing_loans": 800.0, "net_interest_income": 300.0, "interest_earning_assets": 110000.0, "total_assets": 115000.0, "market_value_equity": 5.0, "total_debt": 28500.0},
    }

    # 7. VNTR (Venator)
    vntr_base = {
        "2022Q1": {"total_assets": 2500.0, "total_liabilities": 2300.0, "current_assets": 900.0, "current_liabilities": 580.0, "retained_earnings": -650.0, "ebit": 15.0, "ebitda": 45.0, "sales": 590.0, "market_value_equity": 210.0, "total_debt": 950.0, "interest_expense": 18.0, "cash": 160.0, "cash_prev": 175.0},
        "2022Q2": {"total_assets": 2400.0, "total_liabilities": 2380.0, "current_assets": 860.0, "current_liabilities": 600.0, "retained_earnings": -780.0, "ebit": -10.0, "ebitda": 20.0, "sales": 570.0, "market_value_equity": 150.0, "total_debt": 980.0, "interest_expense": 19.0, "cash": 140.0, "cash_prev": 160.0},
        "2022Q3": {"total_assets": 2300.0, "total_liabilities": 2450.0, "current_assets": 820.0, "current_liabilities": 610.0, "retained_earnings": -920.0, "ebit": -45.0, "ebitda": -10.0, "sales": 550.0, "market_value_equity": 95.0, "total_debt": 990.0, "interest_expense": 20.0, "cash": 115.0, "cash_prev": 140.0},
        "2022Q4": {"total_assets": 2100.0, "total_liabilities": 2600.0, "current_assets": 780.0, "current_liabilities": 620.0, "retained_earnings": -1100.0, "ebit": -80.0, "ebitda": -30.0, "sales": 530.0, "market_value_equity": 60.0, "total_debt": 1000.0, "interest_expense": 21.0, "cash": 90.0, "cash_prev": 115.0},
        "2023Q1": {"total_assets": 1950.0, "total_liabilities": 2700.0, "current_assets": 680.0, "current_liabilities": 650.0, "retained_earnings": -1350.0, "ebit": -110.0, "ebitda": -55.0, "sales": 490.0, "market_value_equity": 30.0, "total_debt": 1050.0, "interest_expense": 23.0, "cash": 60.0, "cash_prev": 90.0},
        "2023Q2": {"total_assets": 1800.0, "total_liabilities": 2800.0, "current_assets": 590.0, "current_liabilities": 690.0, "retained_earnings": -1600.0, "ebit": -140.0, "ebitda": -80.0, "sales": 460.0, "market_value_equity": 12.0, "total_debt": 1100.0, "interest_expense": 25.0, "cash": 35.0, "cash_prev": 60.0},
        "2023Q3": {"total_assets": 1650.0, "total_liabilities": 2900.0, "current_assets": 480.0, "current_liabilities": 730.0, "retained_earnings": -1900.0, "ebit": -175.0, "ebitda": -110.0, "sales": 420.0, "market_value_equity": 4.0, "total_debt": 1150.0, "interest_expense": 27.0, "cash": 18.0, "cash_prev": 35.0},
        "2023Q4": {"total_assets": 1500.0, "total_liabilities": 3000.0, "current_assets": 390.0, "current_liabilities": 780.0, "retained_earnings": -2200.0, "ebit": -210.0, "ebitda": -140.0, "sales": 380.0, "market_value_equity": 1.0, "total_debt": 1200.0, "interest_expense": 29.0, "cash": 5.0, "cash_prev": 18.0},
    }

    # Healthy Companies (Group B)
    tgt_base = {q: {"total_assets": 51000.0 + i*300, "total_liabilities": 38000.0 + i*200, "current_assets": 17500.0 + i*150, "current_liabilities": 13000.0 + i*80, "retained_earnings": 5800.0 + i*100, "ebit": 1350.0 + i*30, "ebitda": 1850.0 + i*40, "sales": 26000.0 + i*400, "market_value_equity": 65000.0 + i*500, "total_debt": 15500.0 + i*100, "interest_expense": 115.0 + i*2, "cash": 3200.0 + i*80, "cash_prev": 3100.0 + i*80} for i, q in enumerate(quarters)}
    cost_base = {q: {"total_assets": 64000.0 + i*700, "total_liabilities": 40000.0 + i*400, "current_assets": 32000.0 + i*500, "current_liabilities": 29000.0 + i*400, "retained_earnings": 15000.0 + i*400, "ebit": 1900.0 + i*50, "ebitda": 2400.0 + i*60, "sales": 58000.0 + i*1000, "market_value_equity": 220000.0 + i*3000, "total_debt": 6200.0 + i*40, "interest_expense": 38.0 + i*1, "cash": 11500.0 + i*300, "cash_prev": 11200.0 + i*300} for i, q in enumerate(quarters)}
    jpm_base = {q: {"cet1_capital": 230000.0 + i*2500, "risk_weighted_assets": 1700000.0 + i*7000, "total_loans": 1250000.0 + i*8000, "total_deposits": 2350000.0 + i*7000, "non_performing_loans": 7200.0 + i*40, "net_interest_income": 21000.0 + i*300, "interest_earning_assets": 3100000.0 + i*25000, "total_assets": 3700000.0 + i*25000, "market_value_equity": 410000.0 + i*5000, "total_debt": 320000.0 + i*3000} for i, q in enumerate(quarters)}
    gs_base = {q: {"cet1_capital": 92000.0 + i*900, "risk_weighted_assets": 650000.0 + i*3000, "total_loans": 170000.0 + i*1500, "total_deposits": 360000.0 + i*3000, "non_performing_loans": 2000.0 + i*15, "net_interest_income": 1800.0 + i*40, "interest_earning_assets": 1200000.0 + i*8000, "total_assets": 1380000.0 + i*9000, "market_value_equity": 120000.0 + i*2000, "total_debt": 280000.0 + i*3000} for i, q in enumerate(quarters)}
    apd_base = {q: {"total_assets": 28000.0 + i*300, "total_liabilities": 14000.0 + i*180, "current_assets": 4100.0 + i*60, "current_liabilities": 3500.0 + i*40, "retained_earnings": 10000.0 + i*180, "ebit": 750.0 + i*20, "ebitda": 1100.0 + i*25, "sales": 3000.0 + i*50, "market_value_equity": 54000.0 + i*700, "total_debt": 9200.0 + i*90, "interest_expense": 65.0 + i*2, "cash": 1850.0 + i*40, "cash_prev": 1810.0 + i*40} for i, q in enumerate(quarters)}
    msft_base = {q: {"total_assets": 370000.0 + i*6000, "total_liabilities": 190000.0 + i*2000, "current_assets": 165000.0 + i*2500, "current_liabilities": 92000.0 + i*1500, "retained_earnings": 100000.0 + i*2800, "ebit": 20000.0 + i*600, "ebitda": 23500.0 + i*700, "sales": 49000.0 + i*1400, "market_value_equity": 2700000.0 + i*60000, "total_debt": 58000.0 + i*300, "interest_expense": 480.0 + i*10, "cash": 98000.0 + i*1900, "cash_prev": 96100.0 + i*1900} for i, q in enumerate(quarters)}
    aapl_base = {q: {"total_assets": 330000.0 + i*3000, "total_liabilities": 270000.0 + i*2500, "current_assets": 135000.0 + i*1200, "current_liabilities": 138000.0 + i*1000, "retained_earnings": 5000.0 - i*100, "ebit": 2600.0 + i*900, "ebitda": 29000.0 + i*950, "sales": 90000.0 + i*2000, "market_value_equity": 2600000.0 + i*50000, "total_debt": 105000.0 + i*800, "interest_expense": 950.0 + i*15, "cash": 52000.0 + i*1400, "cash_prev": 50600.0 + i*1400} for i, q in enumerate(quarters)}

    all_bases = {
        "BBBY": bbby_base, "PRTY": prty_base, "RAD": rad_base, "WE": we_base,
        "CS": cs_base, "SIVB": sivb_base, "VNTR": vntr_base,
        "TGT": tgt_base, "COST": cost_base, "JPM": jpm_base,
        "GS": gs_base, "APD": apd_base, "MSFT": msft_base, "AAPL": aapl_base
    }

    for ticker, q_map in all_bases.items():
        for quarter, metrics in q_map.items():
            entry = {"ticker": ticker, "quarter": quarter}
            entry.update(metrics)
            data.append(entry)

    return data
