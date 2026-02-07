from django.test import TestCase
from tunnels.utils.validators.tunnel_execution_validator import TunelExecutionValidator


class TunelExecutionValidatorTestCase(TestCase):

    def test_is_ready_to_use_when_all_conditions_are_met(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=15, associated_asset_is_active=True
        )
        self.assertTrue(validator.is_ready_to_use())

    def test_is_not_ready_to_use_when_asset_is_inactive(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=15, associated_asset_is_active=False
        )
        self.assertFalse(validator.is_ready_to_use())

    def test_is_not_ready_to_use_when_limits_are_invalid(self):
        validator = TunelExecutionValidator(
            lower_limit=20, upper_limit=10, interval=5,
            current_asset_price=15, associated_asset_is_active=True
        )
        self.assertFalse(validator.is_ready_to_use())

    def test_is_not_ready_to_use_when_interval_is_invalid(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=-5,
            current_asset_price=15, associated_asset_is_active=True
        )
        self.assertFalse(validator.is_ready_to_use())

    def test_notify_user_to_buy_asset_when_price_is_below_lower_limit(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=5, associated_asset_is_active=True
        )
        self.assertTrue(validator.notify_user_to_buy_asset())

    def test_do_not_notify_user_to_buy_asset_when_price_is_above_lower_limit(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=15, associated_asset_is_active=True
        )
        self.assertFalse(validator.notify_user_to_buy_asset())

    def test_notify_user_to_sell_asset_when_price_is_above_upper_limit(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=25, associated_asset_is_active=True
        )
        self.assertTrue(validator.notify_user_to_sell_asset())

    def test_do_not_notify_user_to_sell_asset_when_price_is_below_upper_limit(self):
        validator = TunelExecutionValidator(
            lower_limit=10, upper_limit=20, interval=5,
            current_asset_price=15, associated_asset_is_active=True
        )
        self.assertFalse(validator.notify_user_to_sell_asset())
