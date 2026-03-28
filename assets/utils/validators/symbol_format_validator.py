import re

from django.core.exceptions import ValidationError

# All instruments traded on B3 (stocks, FIIs, ETFs, BDRs) follow the pattern:
# 4–5 uppercase letters + 1–2 digits
# Examples: PETR4, VALE3, BOVA11, HGLG11, AAPL34, GOOGL34
_B3_PATTERN = re.compile(r"^[A-Z]{4,5}[0-9]{1,2}$")

# Cryptocurrencies use only letters, no exchange suffix
# Examples: BTC, ETH, SOL, USDT
_CRYPTO_PATTERN = re.compile(r"^[A-Z]{2,10}$")

_B3_TYPES = {"stock", "fii", "etf", "bdr"}


class SymbolFormatValidator:
    """
    Validates that a symbol matches the expected format for its asset type.

    Called before any external API request so obviously malformed symbols
    are rejected immediately without consuming API quota.
    """

    def __init__(self, symbol: str, asset_type: str):
        self.symbol = symbol
        self.asset_type = asset_type

    def validate(self):
        if self.asset_type in _B3_TYPES:
            if not _B3_PATTERN.match(self.symbol):
                raise ValidationError(
                    f"'{self.symbol}' is not a valid B3 symbol. "
                    "Expected 4–5 uppercase letters followed by 1–2 digits "
                    "(e.g. PETR4, BOVA11, HGLG11, AAPL34)."
                )
        elif self.asset_type == "crypto" and not _CRYPTO_PATTERN.match(self.symbol):
            raise ValidationError(
                f"'{self.symbol}' is not a valid crypto symbol. "
                "Expected 2–10 uppercase letters with no digits (e.g. BTC, ETH, SOL)."
            )
