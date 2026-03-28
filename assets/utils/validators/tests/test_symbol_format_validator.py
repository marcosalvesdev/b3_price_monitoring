from django.core.exceptions import ValidationError
from django.test import TestCase

from assets.utils.validators.symbol_format_validator import SymbolFormatValidator


class SymbolFormatValidatorB3Tests(TestCase):
    """
    B3-traded instruments (stocks, FIIs, ETFs, BDRs) must follow the pattern:
    4–5 uppercase letters + 1–2 digits.
    """

    def _valid(self, symbol, asset_type):
        SymbolFormatValidator(symbol=symbol, asset_type=asset_type).validate()

    def _invalid(self, symbol, asset_type):
        with self.assertRaises(ValidationError):
            SymbolFormatValidator(symbol=symbol, asset_type=asset_type).validate()

    # --- Stocks ---

    def test_stock_valid_four_letters_one_digit(self):
        self._valid("PETR4", "stock")

    def test_stock_valid_on_shares_digit_3(self):
        self._valid("VALE3", "stock")

    def test_stock_invalid_lowercase(self):
        self._invalid("petr4", "stock")

    def test_stock_invalid_no_digits(self):
        self._invalid("PETRO", "stock")

    def test_stock_invalid_only_digits(self):
        self._invalid("12345", "stock")

    def test_stock_invalid_too_short(self):
        self._invalid("PET4", "stock")

    # --- FIIs ---

    def test_fii_valid_four_letters_two_digits(self):
        self._valid("HGLG11", "fii")

    def test_fii_valid_different_fund(self):
        self._valid("KNRI11", "fii")

    def test_fii_invalid_lowercase(self):
        self._invalid("hglg11", "fii")

    def test_fii_invalid_no_digits(self):
        self._invalid("HGLGXX", "fii")

    # --- ETFs ---

    def test_etf_valid_ibovespa(self):
        self._valid("BOVA11", "etf")

    def test_etf_valid_sp500_brl(self):
        self._valid("IVVB11", "etf")

    def test_etf_invalid_too_long(self):
        self._invalid("BOVESPA11", "etf")

    # --- BDRs ---

    def test_bdr_valid_four_letters(self):
        self._valid("AAPL34", "bdr")

    def test_bdr_valid_five_letters(self):
        self._valid("GOOGL34", "bdr")

    def test_bdr_invalid_no_digits(self):
        self._invalid("AAPL", "bdr")

    def test_bdr_invalid_too_many_letters(self):
        self._invalid("AMAZON34", "bdr")


class SymbolFormatValidatorCryptoTests(TestCase):
    """Crypto symbols must be 2–10 uppercase letters with no digits."""

    def _valid(self, symbol):
        SymbolFormatValidator(symbol=symbol, asset_type="crypto").validate()

    def _invalid(self, symbol):
        with self.assertRaises(ValidationError):
            SymbolFormatValidator(symbol=symbol, asset_type="crypto").validate()

    def test_crypto_valid_btc(self):
        self._valid("BTC")

    def test_crypto_valid_eth(self):
        self._valid("ETH")

    def test_crypto_valid_sol(self):
        self._valid("SOL")

    def test_crypto_valid_usdt(self):
        self._valid("USDT")

    def test_crypto_invalid_with_digits(self):
        self._invalid("BTC1")

    def test_crypto_invalid_lowercase(self):
        self._invalid("btc")

    def test_crypto_invalid_too_short(self):
        self._invalid("B")

    def test_crypto_invalid_too_long(self):
        self._invalid("TOOLONGSYMBOL")
