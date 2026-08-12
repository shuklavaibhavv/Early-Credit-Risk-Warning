"""
Merton Distance-to-Default (DD) Engine.

Implements Merton's (1974) structural model of default.
Estimates market value of firm assets (V_A) and asset volatility (sigma_A)
by solving the non-linear Merton system (Equity = Black-Scholes call option on assets).
Calculates Distance-to-Default (DD) and implied Probability of Default (PD).
"""

import math
from typing import Dict, List, Optional, Tuple, Union, Any

try:
    from scipy.stats import norm
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


def norm_cdf(x: float) -> float:
    """
    Standard normal cumulative distribution function (CDF).
    Uses scipy.stats.norm if available, otherwise built-in math.erf.
    """
    if HAS_SCIPY:
        return float(norm.cdf(x))
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def get_equity_volatility(
    price_history: Union[List[float], Any], window_days: int = 252
) -> Optional[float]:
    """
    Calculates annualized equity volatility from a series of daily stock prices.

    Args:
        price_history: List or Series of daily closing prices.
        window_days: Number of trading days in a year (default 252).

    Returns:
        Annualized equity volatility as float, or None if invalid.
    """
    if price_history is None:
        return None

    # Handle pandas Series or list
    if hasattr(price_history, "tolist"):
        prices = [p for p in price_history.tolist() if p is not None and not math.isnan(p)]
    else:
        prices = [p for p in price_history if p is not None and not math.isnan(p)]

    if len(prices) < 2:
        return None

    # Calculate daily log returns
    log_returns = []
    for i in range(1, len(prices)):
        if prices[i - 1] > 0 and prices[i] > 0:
            log_returns.append(math.log(prices[i] / prices[i - 1]))

    if len(log_returns) < 2:
        return None

    # Calculate sample variance
    mean_ret = sum(log_returns) / len(log_returns)
    var = sum((r - mean_ret) ** 2 for r in log_returns) / (len(log_returns) - 1)

    if var <= 0:
        return None

    daily_vol = math.sqrt(var)
    annualized_vol = daily_vol * math.sqrt(window_days)
    return annualized_vol


def calculate_dtd(
    equity_value: float,
    equity_volatility: float,
    total_debt: float,
    risk_free_rate: float = 0.04,
    time_horizon: float = 1.0,
    max_iter: int = 100,
    tol: float = 1e-5,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Calculates Merton Distance-to-Default (DD) and Probability of Default (PD).

    Solves the Merton non-linear equations iteratively:
    1. E = V_A * N(d1) - D * exp(-r*T) * N(d2)
    2. sigma_E * E = N(d1) * sigma_A * V_A

    Args:
        equity_value (E): Market value of equity ($M).
        equity_volatility (sigma_E): Annualized equity volatility.
        total_debt (D): Total liabilities / face value of debt ($M).
        risk_free_rate (r): Risk-free interest rate (annualized).
        time_horizon (T): Time horizon in years (default 1.0).
        max_iter: Maximum solver iterations.
        tol: Tolerance for convergence.

    Returns:
        Tuple of (Distance-to-Default, Probability-of-Default) or (None, None) if solution fails.
    """
    # Guard clauses for invalid inputs
    if (
        equity_value is None
        or equity_volatility is None
        or total_debt is None
        or equity_value <= 0
        or equity_volatility <= 0
        or total_debt <= 0
        or time_horizon <= 0
    ):
        return None, None

    E = float(equity_value)
    sigma_E = float(equity_volatility)
    D = float(total_debt)
    r = float(risk_free_rate)
    T = float(time_horizon)

    # Initial guesses
    V_A = E + D
    sigma_A = sigma_E * (E / V_A)

    sqrt_T = math.sqrt(T)

    # Iterative solver for Merton system
    converged = False
    for _ in range(max_iter):
        if sigma_A <= 0 or V_A <= 0:
            return None, None

        d1 = (math.log(V_A / D) + (r + 0.5 * sigma_A**2) * T) / (sigma_A * sqrt_T)
        d2 = d1 - sigma_A * sqrt_T

        N_d1 = norm_cdf(d1)
        N_d2 = norm_cdf(d2)

        if N_d1 <= 1e-12:
            return None, None

        # Update V_A and sigma_A
        V_A_new = (E + D * math.exp(-r * T) * N_d2) / N_d1
        sigma_A_new = (sigma_E * E) / (N_d1 * V_A_new)

        if abs(V_A_new - V_A) < tol and abs(sigma_A_new - sigma_A) < tol:
            V_A = V_A_new
            sigma_A = sigma_A_new
            converged = True
            break

        V_A = V_A_new
        sigma_A = sigma_A_new

    if not converged or V_A <= 0 or sigma_A <= 0:
        # Fallback to single-step estimation if iteration doesn't converge
        V_A = E + D
        sigma_A = sigma_E * (E / V_A)

    d1 = (math.log(V_A / D) + (r + 0.5 * sigma_A**2) * T) / (sigma_A * sqrt_T)
    d2 = d1 - sigma_A * sqrt_T

    # Distance-to-Default (DD)
    # DD = [ln(V_A / D) + (r - 0.5 * sigma_A^2) * T] / (sigma_A * sqrt_T)
    dd = (math.log(V_A / D) + (r - 0.5 * sigma_A**2) * T) / (sigma_A * sqrt_T)

    # Probability of Default (PD) = N(-DD)
    pd = norm_cdf(-dd)

    return dd, pd


def calculate_dtd_for_company(
    ticker: str,
    quarter: str,
    price_history: Union[List[float], Any],
    total_debt: float,
    equity_value: float,
    risk_free_rate: float = 0.04,
    time_horizon: float = 1.0,
) -> Dict[str, Optional[float]]:
    """
    Wrapper function to compute DD and PD for a given company quarter.

    Args:
        ticker: Company ticker.
        quarter: Quarter string (e.g. '2022Q1').
        price_history: Daily stock price history.
        total_debt: Total debt / liabilities ($M).
        equity_value: Market capitalization ($M).
        risk_free_rate: Risk-free rate (default 0.04).
        time_horizon: Time horizon in years (default 1.0).

    Returns:
        Dictionary with keys: ticker, quarter, distance_to_default, probability_of_default.
    """
    sigma_E = get_equity_volatility(price_history)

    if sigma_E is None or equity_value is None or total_debt is None:
        return {
            "ticker": ticker,
            "quarter": quarter,
            "equity_volatility": None,
            "distance_to_default": None,
            "probability_of_default": None,
        }

    dd, pd = calculate_dtd(
        equity_value=equity_value,
        equity_volatility=sigma_E,
        total_debt=total_debt,
        risk_free_rate=risk_free_rate,
        time_horizon=time_horizon,
    )

    return {
        "ticker": ticker,
        "quarter": quarter,
        "equity_volatility": sigma_E,
        "distance_to_default": dd,
        "probability_of_default": pd,
    }
