import logging

from celery import shared_task

from globals.services.exchange_rate import update_cached_rate

logger = logging.getLogger(__name__)


@shared_task()
def refresh_usd_brl_rate():
    """Periodic task to refresh the cached USD/BRL exchange rate."""
    try:
        rate = update_cached_rate()
        return {"status": "ok", "rate": rate}
    except Exception:
        logger.exception("Failed to refresh USD/BRL rate")
        raise
