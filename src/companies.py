"""
Companies Dataset for Credit Risk Analysis.
Contains metadata for 14 companies across Group A (distressed) and Group B (healthy).
"""

COMPANIES = [
    # Group A: Distressed Companies
    {
        "name": "Bed Bath & Beyond",
        "ticker": "BBBY",
        "sector": "retail",
        "group": "A",
    },
    {
        "name": "Party City",
        "ticker": "PRTY",
        "sector": "retail",
        "group": "A",
    },
    {
        "name": "Rite Aid",
        "ticker": "RAD",
        "sector": "retail",
        "group": "A",
    },
    {
        "name": "WeWork",
        "ticker": "WE",
        "sector": "baseline",
        "group": "A",
    },
    {
        "name": "Credit Suisse",
        "ticker": "CS",
        "sector": "bank",
        "group": "A",
    },
    {
        "name": "Silicon Valley Bank",
        "ticker": "SIVB",
        "sector": "bank",
        "group": "A",
    },
    {
        "name": "Venator Materials",
        "ticker": "VNTR",
        "sector": "chemical",
        "group": "A",
    },
    # Group B: Healthy Companies
    {
        "name": "Target",
        "ticker": "TGT",
        "sector": "retail",
        "group": "B",
    },
    {
        "name": "Costco",
        "ticker": "COST",
        "sector": "retail",
        "group": "B",
    },
    {
        "name": "JPMorgan Chase",
        "ticker": "JPM",
        "sector": "bank",
        "group": "B",
    },
    {
        "name": "Goldman Sachs",
        "ticker": "GS",
        "sector": "bank",
        "group": "B",
    },
    {
        "name": "Air Products and Chemicals",
        "ticker": "APD",
        "sector": "chemical",
        "group": "B",
    },
    {
        "name": "Microsoft",
        "ticker": "MSFT",
        "sector": "baseline",
        "group": "B",
    },
    {
        "name": "Apple",
        "ticker": "AAPL",
        "sector": "baseline",
        "group": "B",
    },
]


def get_distressed_companies():
    """Returns list of distressed companies (Group A)."""
    return [c for c in COMPANIES if c["group"] == "A"]


def get_healthy_companies():
    """Returns list of healthy companies (Group B)."""
    return [c for c in COMPANIES if c["group"] == "B"]


def get_companies_by_sector(sector: str):
    """Returns list of companies matching the given sector."""
    return [c for c in COMPANIES if c["sector"] == sector.lower()]
