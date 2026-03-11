import logging

import yfinance as yf

from assets.utils.validators.base_asset_validator import BaseAssertValidator

logger = logging.getLogger(__name__)

B3_SUFFIX = ".SA"

SYMBOL_MAP = {
    "stock": lambda s: f"{s}{B3_SUFFIX}",
    "etf": lambda s: f"{s}{B3_SUFFIX}",
    "crypto": lambda s: f"{s}-USD",
}


class YFinanceAssetValidator(BaseAssertValidator):
    def __init__(self, symbol: str, asset_type: str, *args, **kwargs):
        self.symbol = symbol
        self.asset_type = asset_type

    def _build_symbol(self) -> str:
        formatter = SYMBOL_MAP.get(self.asset_type)
        if formatter is None:
            return self.symbol
        return formatter(self.symbol)

    @property
    def is_valid(self) -> bool:
        yf_symbol = self._build_symbol()
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            return not (not info or info.get("regularMarketPrice") is None)
        except Exception:
            logger.exception("Validation failed for symbol %s", yf_symbol)
            return False
