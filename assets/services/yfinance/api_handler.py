import logging

import yfinance as yf

from assets.services.yfinance.constants import SYMBOL_MAP as _SYMBOL_MAP
from assets.utils.handlers.asset_api_handler import AssetApiHandler
from globals.services.exchange_rate import get_usd_brl_rate

logger = logging.getLogger(__name__)


class YFinanceApiHandler(AssetApiHandler):
    """Fetches asset data from Yahoo Finance via the yfinance library."""

    SYMBOL_MAP = _SYMBOL_MAP

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
            # yfinance returns {"trailingPegRatio": None} for invalid/unlisted tickers
            if not info or len(info) <= 1:
                return None
            return info
        except Exception:
            logger.exception("Failed to fetch data from yfinance for %s", yf_symbol)
            return None

    def get_stock_data(self, symbol: str, **kwargs) -> dict | None:
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

    def get_fii_data(self, symbol: str, **kwargs) -> dict | None:
        """
        Fetches data for FIIs (Fundos de Investimento Imobiliário).

        dividend_yield is the primary return metric for FIIs and is included
        to support monitoring strategies based on yield rather than just price.
        """
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        return {
            "price": info.get("regularMarketPrice") or info.get("previousClose"),
            "previous_close": info.get("previousClose"),
            "dividend_yield": info.get("dividendYield"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
            "short_name": info.get("shortName"),
        }

    def get_etf_data(self, symbol: str, **kwargs) -> dict | None:
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        return {
            "price": info.get("regularMarketPrice") or info.get("previousClose"),
            "previous_close": info.get("previousClose"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
            "short_name": info.get("shortName"),
        }

    def get_bdr_data(self, symbol: str, **kwargs) -> dict | None:
        """
        Fetches data for BDRs (Brazilian Depositary Receipts).

        BDRs trade on B3 in BRL and represent shares of foreign companies.
        Price and volume behaviour mirrors regular stocks.
        """
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        return {
            "price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "previous_close": info.get("previousClose"),
            "volume": info.get("volume"),
            "currency": info.get("currency"),
            "short_name": info.get("shortName"),
        }

    def get_crypto_data(self, symbol: str, **kwargs) -> dict | None:
        """
        Fetches crypto price in USD from Yahoo Finance and converts to BRL.

        All prices in this system are stored in BRL, so the USD/BRL rate
        is applied here before returning.
        """
        info = self._fetch_ticker_info(symbol)
        if not info:
            return None
        usd_brl = self._get_usd_brl_rate()
        usd_price = info.get("regularMarketPrice")
        usd_previous_close = info.get("previousClose")
        return {
            "price": round(usd_price * usd_brl, 8) if usd_price else None,
            "previous_close": round(usd_previous_close * usd_brl, 8)
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
