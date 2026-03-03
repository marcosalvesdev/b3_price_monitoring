from core import celery_app
from tunnels.utils.handlers import asset_api_handler
from tunnels.utils.tunnel_manager import TunnelManager


@celery_app.task()
def tunnel_asset_price_check(*args, **kwargs):
    """
    Task to check the price of assets and update the asset price
    in the database and notify users if there are significant changes.
    """

    symbol = kwargs.get("asset_symbol")
    asset_id = kwargs.get("asset_id")
    asset_type = kwargs.get("asset_type")
    tunnel_upper_limit = kwargs.get("tunnel_upper_limit")
    tunnel_lower_limit = kwargs.get("tunnel_lower_limit")

    api_handler = asset_api_handler(symbol=symbol, asset_type=asset_type)
    asset_price = api_handler.asset_price()

    if not asset_price:
        raise ValueError(
            {
                "message": f"Could not retrieve price for {symbol} of type {asset_type}.",
                "asset": symbol,
                "api_response": api_handler.data,
            }
        )

    tunnel = TunnelManager(
        asset_current_price=asset_price,
        tunnel_upper_limit=tunnel_upper_limit,
        tunnel_lower_limit=tunnel_lower_limit,
    )

    tunnel.create_asset_price(asset_id=asset_id)

    # TODO: Next step is to implement a notification system to alert users
    #  when the price is above or below the limits. This can be done using email, SMS,
    #  or push notifications depending on the user's preferences.

    if tunnel.asset_price_is_above_upper_limit(asset_price):
        return {
            "message": f"Price of {tunnel.asset.name} is above the upper limit of {tunnel.upper_limit}. Current price: {asset_price}",  # noqa: E501
            "asset": tunnel.asset.name,
            "price": asset_price,
            "upper_limit": tunnel.upper_limit,
        }
    elif tunnel.asset_price_is_below_lower_limit(asset_price):
        return {
            "message": f"Price of {tunnel.asset.name} is below the lower limit of {tunnel.lower_limit}. Current price: {asset_price}",  # noqa: E501
            "asset": tunnel.asset.name,
            "price": asset_price,
            "lower_limit": tunnel.lower_limit,
        }

    return {
        "message": f"Price of {tunnel.asset.name} is within the limits. Current price: {asset_price}",  # noqa: E501
        "asset": tunnel.asset.name,
        "price": asset_price,
        "lower_limit": tunnel.lower_limit,
        "upper_limit": tunnel.upper_limit,
    }
