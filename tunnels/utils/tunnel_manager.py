class TunnelManager:
    def __init__(
        self,
        asset_current_price: float,
        tunnel_upper_limit: float,
        tunnel_lower_limit: float,
    ):
        self.asset_current_price = asset_current_price
        self.tunnel_upper_limit = tunnel_upper_limit
        self.tunnel_lower_limit = tunnel_lower_limit

    def price_is_above_tunnel_limit(self):
        return self.asset_current_price > self.tunnel_upper_limit

    def price_is_below_tunnel_limit(self):
        return self.asset_current_price < self.tunnel_lower_limit

    def notify_user(self):
        if self.price_is_above_tunnel_limit():
            return {
                "message": f"Alert: The price of the asset has risen above the upper limit of {self.tunnel_upper_limit}.",  # noqa: E501
                "suggestion": "Consider selling the asset at this price.",
            }
        elif self.price_is_below_tunnel_limit():
            return {
                "message": f"Alert: The price of the asset has fallen below the lower limit of {self.tunnel_lower_limit}.",  # noqa: E501
                "suggestion": "Consider buying the asset at this price.",
            }

    def create_asset_price(self, asset_id: int):
        from tunnels.utils.external_models import AssetPrice

        AssetPrice.objects.create(
            asset_id=asset_id,
            price=self.asset_current_price,
        )
