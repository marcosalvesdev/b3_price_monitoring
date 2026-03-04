from unittest.mock import MagicMock, patch

from django.test import TestCase

from tunnels.tasks.tunnel_asset_price_check import price_check


class TunnelAssetPriceCheckTestCase(TestCase):
    """Test suite for price_check Celery task

    This test class covers:
    - Mocking the external API handler to isolate the task logic
    - Testing all possible price scenarios (within limits, above, below)
    - Verifying proper initialization of dependencies
    - Testing error handling when API fails
    """

    def setUp(self):
        """Set up standard test data for each test"""
        self.test_kwargs = {
            "asset_symbol": "PETR4",
            "asset_id": 1,
            "asset_type": "stock",
            "asset_name": "Petrobras",
            "tunnel_upper_limit": 30.0,
            "tunnel_lower_limit": 20.0,
            "emails_to_notification": ["user@example.com"],
            "user_name": "user_example",
        }

    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_price_within_limits(self, mock_asset_handler_func, mock_tunnel_manager_class):
        """Test when asset price is within tunnel limits"""
        # Arrange
        asset_price = 25.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        result = price_check(**self.test_kwargs)

        # Assert
        self.assertIn("within the limits", result["message"])
        self.assertEqual(result["asset"], "Petrobras")
        self.assertEqual(result["price"], 25.0)
        self.assertEqual(result["lower_limit"], 20.0)
        self.assertEqual(result["upper_limit"], 30.0)
        mock_tunnel.create_asset_price.assert_called_once_with(asset_id=1)

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_price_above_upper_limit(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test when asset price exceeds upper limit"""
        # Arrange
        asset_price = 35.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = True
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        result = price_check(**self.test_kwargs)

        # Assert
        self.assertIn("above the upper limit", result["message"])
        self.assertEqual(result["asset"], "Petrobras")
        self.assertEqual(result["price"], 35.0)
        self.assertEqual(result["upper_limit"], 30.0)
        mock_tunnel.create_asset_price.assert_called_once_with(asset_id=1)

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_price_below_lower_limit(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test when asset price falls below lower limit"""
        # Arrange
        asset_price = 15.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = True
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        result = price_check(**self.test_kwargs)

        # Assert
        self.assertIn("below the lower limit", result["message"])
        self.assertEqual(result["asset"], "Petrobras")
        self.assertEqual(result["price"], 15.0)
        self.assertEqual(result["lower_limit"], 20.0)
        mock_tunnel.create_asset_price.assert_called_once_with(asset_id=1)

    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_api_handler_returns_none(self, mock_asset_handler_func):
        """Test when API handler returns None (API failure)"""
        # Arrange
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = None
        mock_api_handler.data = {"error": "API not available"}
        mock_asset_handler_func.return_value = mock_api_handler

        # Act & Assert
        with self.assertRaises(ValueError) as context:
            price_check(**self.test_kwargs)

        error_data = context.exception.args[0]
        self.assertIn("Could not retrieve price", error_data["message"])
        self.assertEqual(error_data["asset"], "PETR4")
        self.assertEqual(error_data["api_response"], {"error": "API not available"})

    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_api_handler_returns_zero(self, mock_asset_handler_func):
        """Test when API handler returns 0 or falsy value"""
        # Arrange
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = 0
        mock_api_handler.data = {}
        mock_asset_handler_func.return_value = mock_api_handler

        # Act & Assert
        with self.assertRaises(ValueError):
            price_check(**self.test_kwargs)

    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_tunnel_manager_initialized_correctly(
        self, mock_asset_handler_func, mock_tunnel_manager_class
    ):
        """Test that TunnelManager is initialized with correct parameters"""
        # Arrange
        asset_price = 25.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        price_check(**self.test_kwargs)

        # Assert - Verify TunnelManager was initialized with correct params
        mock_tunnel_manager_class.assert_called_once_with(
            asset_current_price=asset_price,
            tunnel_upper_limit=30.0,
            tunnel_lower_limit=20.0,
        )

    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_asset_api_handler_called_with_correct_params(
        self, mock_asset_handler_func, mock_tunnel_manager_class
    ):
        """Test that asset_api_handler is called with correct symbol and asset_type"""
        # Arrange
        asset_price = 25.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        price_check(**self.test_kwargs)

        # Assert - Verify asset_api_handler was instantiated correctly
        mock_asset_handler_func.assert_called_once_with(symbol="PETR4", asset_type="stock")

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_create_asset_price_called_regardless_of_limits(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test that create_asset_price is called regardless of price limits"""
        # Arrange
        asset_price = 35.0  # above limits
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = True
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Act
        price_check(**self.test_kwargs)

        # Assert - create_asset_price should always be called
        mock_tunnel.create_asset_price.assert_called_once_with(asset_id=1)

    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_float_price_values(self, mock_asset_handler_func, mock_tunnel_manager_class):
        """Test with float price values"""
        # Arrange
        asset_price = 25.50
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        # Override limits in kwargs to float values
        test_kwargs = {
            **self.test_kwargs,
            "tunnel_upper_limit": 30.50,
            "tunnel_lower_limit": 20.50,
        }

        # Act
        result = price_check(**test_kwargs)

        # Assert
        self.assertEqual(result["price"], 25.50)
        self.assertEqual(result["lower_limit"], 20.50)
        self.assertEqual(result["upper_limit"], 30.50)

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_email_sent_above_upper_limit(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test that e-mail is sent when price is above upper limit"""
        asset_price = 35.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = True
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        price_check(**self.test_kwargs)

        email_instance = mock_email_service_class.return_value
        email_instance.send_email_with_html_content.assert_called_once()

        _, kwargs = email_instance.send_email_with_html_content.call_args
        self.assertEqual(
            kwargs["template_name"], "tunnels/notifications/opportunity_notification.html"
        )
        self.assertEqual(kwargs["subject"], "Price Alert: Petrobras has exceeded the upper limit!")
        self.assertEqual(kwargs["recipient_list"], ["user@example.com"])

        context = kwargs["context"]
        self.assertEqual(context["action"], "sell")
        self.assertEqual(context["action_cap"], "Sell")
        self.assertEqual(context["asset_symbol"], "PETR4")
        self.assertEqual(context["asset_name"], "Petrobras")
        self.assertEqual(context["current_price"], asset_price)
        self.assertEqual(context["lower_limit"], 20.0)
        self.assertEqual(context["upper_limit"], 30.0)

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_email_sent_below_lower_limit(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test that e-mail is sent when price is below lower limit"""
        asset_price = 15.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = True
        mock_tunnel_manager_class.return_value = mock_tunnel

        price_check(**self.test_kwargs)

        email_instance = mock_email_service_class.return_value
        email_instance.send_email_with_html_content.assert_called_once()

        _, kwargs = email_instance.send_email_with_html_content.call_args
        self.assertEqual(
            kwargs["template_name"], "tunnels/notifications/opportunity_notification.html"
        )
        self.assertEqual(
            kwargs["subject"], "Price Alert: Petrobras has fallen below the lower limit!"
        )
        self.assertEqual(kwargs["recipient_list"], ["user@example.com"])

        context = kwargs["context"]
        self.assertEqual(context["action"], "buy")
        self.assertEqual(context["action_cap"], "Buy")
        self.assertEqual(context["asset_symbol"], "PETR4")
        self.assertEqual(context["asset_name"], "Petrobras")
        self.assertEqual(context["current_price"], asset_price)
        self.assertEqual(context["lower_limit"], 20.0)
        self.assertEqual(context["upper_limit"], 30.0)

    @patch("tunnels.tasks.tunnel_asset_price_check.EmailNotificationService")
    @patch("tunnels.tasks.tunnel_asset_price_check.TunnelManager")
    @patch("tunnels.tasks.tunnel_asset_price_check.asset_api_handler")
    def test_email_not_sent_within_limits(
        self, mock_asset_handler_func, mock_tunnel_manager_class, mock_email_service_class
    ):
        """Test that e-mail is NOT sent when price is within limits"""
        asset_price = 25.0
        mock_api_handler = MagicMock()
        mock_api_handler.asset_price.return_value = asset_price
        mock_asset_handler_func.return_value = mock_api_handler

        mock_tunnel = MagicMock()
        mock_tunnel.asset.name = "Petrobras"
        mock_tunnel.upper_limit = 30.0
        mock_tunnel.lower_limit = 20.0
        mock_tunnel.asset_price_is_above_upper_limit.return_value = False
        mock_tunnel.asset_price_is_below_lower_limit.return_value = False
        mock_tunnel_manager_class.return_value = mock_tunnel

        price_check(**self.test_kwargs)

        mock_email_service_class.return_value.send_email_with_html_content.assert_not_called()
