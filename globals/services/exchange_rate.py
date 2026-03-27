import logging

import yfinance as yf
from decouple import config
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_KEY = "usd_brl_rate"
CACHE_TTL = config("USD_BRL_CACHE_TTL", default=600, cast=int)  # 10 minutes


def fetch_usd_brl_rate() -> float:
    """Fetch the current USD/BRL exchange rate from yfinance."""
    ticker = yf.Ticker("USDBRL=X")
    rate = ticker.info.get("regularMarketPrice")
    if not rate:
        raise ValueError("yfinance returned no price for USDBRL=X")
    return float(rate)


def update_cached_rate() -> float:
    """Fetch the USD/BRL rate and store it in cache. Returns the rate."""
    rate = fetch_usd_brl_rate()
    cache.set(CACHE_KEY, rate, timeout=CACHE_TTL)
    logger.info("USD/BRL rate cached: %s", rate)
    return rate


def get_usd_brl_rate() -> float:
    """Read USD/BRL rate from cache. If missing, fetch and cache it."""
    rate = cache.get(CACHE_KEY)
    if rate is not None:
        return rate
    logger.warning("USD/BRL rate not in cache, fetching now")
    return update_cached_rate()
