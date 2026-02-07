from tunnels.utils.validators.tunnel_validator import TunelValidator


class TunelExecutionValidator(TunelValidator):
    def __init__(self, current_asset_price: [float, int], associated_asset_is_active: bool,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_assert_price = current_asset_price
        self.associated_asset_is_active = associated_asset_is_active

    def is_ready_to_use(self) -> bool:
        return self.associated_asset_is_active and self.limits_are_valid and self.interval_is_valid

    def notify_user_to_buy_asset(self):
        return self.current_assert_price < self.lower_limit

    def notify_user_to_sell_asset(self):
        return self.current_assert_price > self.upper_limit
