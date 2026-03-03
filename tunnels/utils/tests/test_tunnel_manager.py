from unittest.mock import patch

from django.test import TestCase

from tunnels.utils.tunnel_manager import TunnelManager


class TunnelManagerTestCase(TestCase):
    def test_price_is_above_tunnel_limit_returns_true_when_price_exceeds_upper_limit(self):
        tunnel_manager = TunnelManager(
            asset_current_price=25,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        self.assertTrue(tunnel_manager.price_is_above_tunnel_limit())

    def test_price_is_above_tunnel_limit_returns_false_when_price_is_within_limits(self):
        tunnel_manager = TunnelManager(
            asset_current_price=15,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        self.assertFalse(tunnel_manager.price_is_above_tunnel_limit())

    def test_price_is_below_tunnel_limit_returns_true_when_price_is_below_lower_limit(self):
        tunnel_manager = TunnelManager(
            asset_current_price=5,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        self.assertTrue(tunnel_manager.price_is_below_tunnel_limit())

    def test_price_is_below_tunnel_limit_returns_false_when_price_is_within_limits(self):
        tunnel_manager = TunnelManager(
            asset_current_price=15,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        self.assertFalse(tunnel_manager.price_is_below_tunnel_limit())

    def test_notify_user_returns_sell_suggestion_when_price_is_above_upper_limit(self):
        tunnel_manager = TunnelManager(
            asset_current_price=25,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        notification = tunnel_manager.notify_user()
        self.assertIsNotNone(notification)
        self.assertIn("risen above", notification["message"])
        self.assertIn("selling", notification["suggestion"])

    def test_notify_user_returns_buy_suggestion_when_price_is_below_lower_limit(self):
        tunnel_manager = TunnelManager(
            asset_current_price=5,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        notification = tunnel_manager.notify_user()
        self.assertIsNotNone(notification)
        self.assertIn("fallen below", notification["message"])
        self.assertIn("buying", notification["suggestion"])

    def test_notify_user_returns_none_when_price_is_within_limits(self):
        tunnel_manager = TunnelManager(
            asset_current_price=15,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        notification = tunnel_manager.notify_user()
        self.assertIsNone(notification)

    @patch("tunnels.utils.external_models.AssetPrice")
    def test_create_asset_price_creates_price_record(self, mock_asset_price):
        tunnel_manager = TunnelManager(
            asset_current_price=15.5,
            tunnel_upper_limit=20,
            tunnel_lower_limit=10,
        )
        asset_id = 1
        tunnel_manager.create_asset_price(asset_id)

        mock_asset_price.objects.create.assert_called_once_with(
            asset_id=asset_id,
            price=15.5,
        )
