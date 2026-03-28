import logging

import yfinance as yf

from assets.services.yfinance.constants import SYMBOL_MAP
from assets.utils.validators.base_asset_validator import BaseAssetValidator

logger = logging.getLogger(__name__)


class YFinanceAssetValidator(BaseAssetValidator):
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
            return bool(info and info.get("regularMarketPrice") is not None)
        except Exception:
            logger.exception("Validation failed for symbol %s", yf_symbol)
            return False
