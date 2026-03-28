B3_SUFFIX = ".SA"

# All instruments traded on B3 — stocks, FIIs, ETFs, and BDRs — use the .SA
# suffix on Yahoo Finance. Crypto prices are fetched in USD then converted to BRL.
SYMBOL_MAP = {
    "stock": lambda s: f"{s}{B3_SUFFIX}",
    "fii": lambda s: f"{s}{B3_SUFFIX}",
    "etf": lambda s: f"{s}{B3_SUFFIX}",
    "bdr": lambda s: f"{s}{B3_SUFFIX}",
    "crypto": lambda s: f"{s}-USD",
}
