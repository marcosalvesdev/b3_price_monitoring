from django.utils import timezone

from core import celery_app
from globals.services.notifications.email import EmailNotificationService
from tunnels.utils.handlers import asset_api_handler
from tunnels.utils.tunnel_manager import TunnelManager


@celery_app.task()
def price_check(*args, **kwargs):
    """
    Task to check the price of assets and update the asset price
    in the database and notify users if there are significant changes.
    """

    asset_symbol = kwargs.get("asset_symbol")
    asset_id = kwargs.get("asset_id")
    asset_name = kwargs.get("asset_name")
    asset_type = kwargs.get("asset_type")
    tunnel_upper_limit = kwargs.get("tunnel_upper_limit")
    tunnel_lower_limit = kwargs.get("tunnel_lower_limit")
    emails_to_notification = kwargs.get("emails", [])
    template_name = kwargs.get("template_name", "notifications/opportunity_notification.html")

    api_handler = asset_api_handler(symbol=asset_symbol, asset_type=asset_type)
    asset_price = api_handler.asset_price()

    if not asset_price:
        raise ValueError(
            {
                "message": f"Could not retrieve price for {asset_symbol} of type {asset_type}.",
                "asset": asset_symbol,
                "api_response": api_handler.data,
            }
        )

    tunnel = TunnelManager(
        asset_current_price=asset_price,
        tunnel_upper_limit=tunnel_upper_limit,
        tunnel_lower_limit=tunnel_lower_limit,
    )

    tunnel.create_asset_price(asset_id=asset_id)

    if tunnel.asset_price_is_above_upper_limit(asset_price):
        EmailNotificationService().send_email_with_html_content(
            template_name=template_name,
            context={
                "action": "sell",
                "action_cap": "Sell",
                "asset_symbol": asset_symbol,
                "asset_name": asset_name,
                "current_price": asset_price,
                "lower_limit": tunnel_lower_limit,
                "upper_limit": tunnel_upper_limit,
                "date": timezone.now(),
            },
            subject=f"Price Alert: {asset_name} has exceeded the upper limit!",
            recipient_list=emails_to_notification,
        )
        return {
            "message": f"Price of {asset_name} is above the upper limit. Current price: {asset_price}",  # noqa: E501
            "asset": asset_name,
            "price": asset_price,
            "lower_limit": tunnel_lower_limit,
            "upper_limit": tunnel_upper_limit,
        }

    if tunnel.asset_price_is_below_lower_limit(asset_price):
        EmailNotificationService().send_email_with_html_content(
            template_name=template_name,
            context={
                "asset_symbol": asset_symbol,
                "asset_name": asset_name,
                "current_price": asset_price,
                "action": "buy",
                "action_cap": "Buy",
                "lower_limit": tunnel_lower_limit,
                "upper_limit": tunnel_upper_limit,
                "date": timezone.now(),
            },
            subject=f"Price Alert: {asset_name} has fallen below the lower limit!",
            recipient_list=emails_to_notification,
        )
        return {
            "message": f"Price of {asset_name} is below the lower limit. Current price: {asset_price}",  # noqa: E501
            "asset": asset_name,
            "price": asset_price,
            "lower_limit": tunnel_lower_limit,
            "upper_limit": tunnel_upper_limit,
        }

    return {
        "message": f"Price of {asset_name} is within the limits. Current price: {asset_price}",  # noqa: E501
        "asset": asset_name,
        "price": asset_price,
        "lower_limit": tunnel_lower_limit,
        "upper_limit": tunnel_upper_limit,
    }
