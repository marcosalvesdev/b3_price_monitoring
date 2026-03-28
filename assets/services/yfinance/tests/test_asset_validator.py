from unittest.mock import patch

from django.test import TestCase

from assets.services.yfinance.asset_validator import YFinanceAssetValidator


class YFinanceAssetValidatorTests(TestCase):
    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_true_for_valid_stock(self, MockTicker):
        MockTicker.return_value.info = {"regularMarketPrice": 38.90, "shortName": "PETR4"}

        validator = YFinanceAssetValidator(symbol="PETR4", asset_type="stock")

        self.assertTrue(validator.is_valid)

    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_true_for_valid_fii(self, MockTicker):
        MockTicker.return_value.info = {"regularMarketPrice": 112.50, "shortName": "KNRI11"}

        validator = YFinanceAssetValidator(symbol="KNRI11", asset_type="fii")

        self.assertTrue(validator.is_valid)

    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_true_for_valid_bdr(self, MockTicker):
        MockTicker.return_value.info = {"regularMarketPrice": 850.00, "shortName": "AAPL34"}

        validator = YFinanceAssetValidator(symbol="AAPL34", asset_type="bdr")

        self.assertTrue(validator.is_valid)

    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_false_when_regular_market_price_is_none(self, MockTicker):
        MockTicker.return_value.info = {"regularMarketPrice": None}

        validator = YFinanceAssetValidator(symbol="INVALID", asset_type="stock")

        self.assertFalse(validator.is_valid)

    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_false_on_empty_info(self, MockTicker):
        MockTicker.return_value.info = {}

        validator = YFinanceAssetValidator(symbol="INVALID", asset_type="stock")

        self.assertFalse(validator.is_valid)

    @patch("assets.services.yfinance.asset_validator.yf.Ticker")
    def test_is_valid_returns_false_on_exception(self, MockTicker):
        MockTicker.side_effect = Exception("network error")

        validator = YFinanceAssetValidator(symbol="PETR4", asset_type="stock")

        self.assertFalse(validator.is_valid)

    def test_build_symbol_adds_sa_suffix_for_stock(self):
        validator = YFinanceAssetValidator(symbol="PETR4", asset_type="stock")
        self.assertEqual(validator._build_symbol(), "PETR4.SA")

    def test_build_symbol_adds_sa_suffix_for_fii(self):
        validator = YFinanceAssetValidator(symbol="HGLG11", asset_type="fii")
        self.assertEqual(validator._build_symbol(), "HGLG11.SA")

    def test_build_symbol_adds_sa_suffix_for_etf(self):
        validator = YFinanceAssetValidator(symbol="BOVA11", asset_type="etf")
        self.assertEqual(validator._build_symbol(), "BOVA11.SA")

    def test_build_symbol_adds_sa_suffix_for_bdr(self):
        validator = YFinanceAssetValidator(symbol="AAPL34", asset_type="bdr")
        self.assertEqual(validator._build_symbol(), "AAPL34.SA")

    def test_build_symbol_adds_usd_suffix_for_crypto(self):
        validator = YFinanceAssetValidator(symbol="BTC", asset_type="crypto")
        self.assertEqual(validator._build_symbol(), "BTC-USD")

    def test_build_symbol_returns_raw_symbol_for_unknown_type(self):
        validator = YFinanceAssetValidator(symbol="XYZ", asset_type="unknown")
        self.assertEqual(validator._build_symbol(), "XYZ")
