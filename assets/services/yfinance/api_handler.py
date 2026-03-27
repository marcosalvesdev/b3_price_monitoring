import logging

import yfinance as yf

from assets.utils.handlers.asset_api_handler import AssetApiHandler
from globals.services.exchange_rate import get_usd_brl_rate

logger = logging.getLogger(__name__)

B3_SUFFIX = ".SA"


class YFinanceApiHandler(AssetApiHandler):
    """Fetches asset data from Yahoo Finance via the yfinance library."""

    SYMBOL_MAP = {
        "stock": lambda s: f"{s}{B3_SUFFIX}",
        "etf": lambda s: f"{s}{B3_SUFFIX}",
        "crypto": lambda s: f"{s}-USD",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _get_usd_brl_rate(self) -> float:
        return get_usd_brl_rate()

    def _build_symbol(self, symbol: str) -> str:
        formatter = self.SYMBOL_MAP.get(self.asset_type)
        if formatter is None:
            return symbol
        return formatter(symbol)

    def _fetch_ticker_info(self, symbol: str) -> dict | None:
        yf_symbol = self._build_symbol(symbol)
        try:
            ticker = yf.Ticker(yf_symbol)
            info = ticker.info
            if not info or info.get("trailingPegRatio") is None and len(info) <= 1:
                return None
            return info
        except Exception:
            logger.exception("Failed to fetch data from yfinance for %s", yf_symbol)
            return None

    def get_stock_data(self, symbol: str, **kwargs) -> dict:
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "market_cap": info.get("marketCap"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
            "short_name": info.get("shortName"),
        }

    def get_etf_data(self, symbol: str, **kwargs) -> dict:
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        return {
            "price": info.get("previousClose") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
            "short_name": info.get("shortName"),
        }

    def get_crypto_data(self, symbol: str, **kwargs) -> dict:
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        usd_brl = self._get_usd_brl_rate()
        usd_price = info.get("regularMarketPrice")
        usd_previous_close = info.get("previousClose")
        return {
            "price": round(usd_price * usd_brl, 2) if usd_price else None,
            "previous_close": round(usd_previous_close * usd_brl, 2)
            if usd_previous_close
            else None,
            "volume": info.get("volume24Hr") or info.get("volume"),
            "market_cap": info.get("marketCap"),
            "currency": "BRL",
            "short_name": info.get("shortName"),
        }

    def asset_price(self):
        if not self.data:
            raise ValueError(f"No price data found for {self.symbol} of type {self.asset_type}.")
        return self.data.get("price")
