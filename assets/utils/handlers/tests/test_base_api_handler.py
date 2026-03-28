from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase

from assets.utils.handlers.base_api_handler import BaseApiHandler
from globals.http_helpers import status_codes


class ConcreteHandler(BaseApiHandler):
    """Minimal concrete subclass used only in tests."""


class BaseApiHandlerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = "http://example.com/api"
        cls.symbol = "PETR4"

    def setUp(self):
        self.handler = ConcreteHandler(api_name="TestAPI")

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_json_on_200(self, mock_get):
        mock_get.return_value.status_code = status_codes.HTTP_200_OK
        mock_get.return_value.json.return_value = {"data": "value"}

        result = self.handler.get(self.url, symbol=self.symbol)

        self.assertEqual(result, {"data": "value"})

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_empty_dict_on_404(self, mock_get):
        mock_get.return_value.status_code = status_codes.HTTP_404_NOT_FOUND

        result = self.handler.get(self.url, symbol=self.symbol)

        self.assertEqual(result, {})

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_empty_dict_on_400(self, mock_get):
        mock_get.return_value.status_code = status_codes.HTTP_400_BAD_REQUEST
        mock_get.return_value.json.return_value = {"error": "bad request"}

        result = self.handler.get(self.url, symbol=self.symbol)

        self.assertEqual(result, {})

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_empty_dict_on_402(self, mock_get):
        mock_get.return_value.status_code = status_codes.HTTP_402_PAYMENT_REQUIRED

        result = self.handler.get(self.url, symbol=self.symbol)

        self.assertEqual(result, {})

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_retries_on_timeout_and_returns_successful_response(self, mock_get):
        success_response = MagicMock()
        success_response.status_code = status_codes.HTTP_200_OK
        success_response.json.return_value = {"price": 42}
        mock_get.side_effect = [requests.Timeout(), success_response]

        result = self.handler.get(self.url, symbol=self.symbol, retry=1)

        self.assertEqual(result, {"price": 42})
        self.assertEqual(mock_get.call_count, 2)

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_empty_dict_after_max_retries_exceeded(self, mock_get):
        mock_get.side_effect = requests.Timeout()

        result = self.handler.get(self.url, symbol=self.symbol, retry=0)

        self.assertEqual(result, {})

    @patch("assets.utils.handlers.base_api_handler.requests.get")
    def test_returns_empty_dict_on_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("connection refused")

        result = self.handler.get(self.url, symbol=self.symbol)

        self.assertEqual(result, {})
