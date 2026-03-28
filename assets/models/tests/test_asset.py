from decimal import Decimal
from unittest.mock import MagicMock, PropertyMock

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from assets.models import Asset, AssetChoices, AssetPrice
from assets.utils.validators.base_asset_validator import BaseAssetValidator

User = get_user_model()


def _make_validator(is_valid: bool) -> BaseAssetValidator:
    mock = MagicMock(spec=BaseAssetValidator)
    type(mock).is_valid = PropertyMock(return_value=is_valid)
    return mock


class AssetChoicesTests(TestCase):
    def test_stock_value(self):
        self.assertEqual(AssetChoices.STOCK, "stock")

    def test_fii_value(self):
        self.assertEqual(AssetChoices.FII, "fii")

    def test_etf_value(self):
        self.assertEqual(AssetChoices.ETF, "etf")

    def test_bdr_value(self):
        self.assertEqual(AssetChoices.BDR, "bdr")

    def test_crypto_value(self):
        self.assertEqual(AssetChoices.CRYPTO, "crypto")

    def test_stock_label(self):
        self.assertEqual(AssetChoices.STOCK.label, "Ação")

    def test_fii_label(self):
        self.assertEqual(AssetChoices.FII.label, "FII")

    def test_bdr_label(self):
        self.assertEqual(AssetChoices.BDR.label, "BDR")

    def test_crypto_label(self):
        self.assertEqual(AssetChoices.CRYPTO.label, "Cripto")


class AssetModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")
        cls.other_user = User.objects.create_user(username="otheruser", password="pass")

    def tearDown(self):
        Asset.validator_class = None

    def test_str_shows_name_and_symbol(self):
        asset = Asset(name="Petrobras", user=self.user, symbol="PETR4", type=AssetChoices.STOCK)
        self.assertEqual(str(asset), "Petrobras (PETR4)")

    def test_save_uppercases_symbol(self):
        asset = Asset.objects.create(
            name="Petrobras", user=self.user, symbol="petr4", type=AssetChoices.STOCK
        )
        self.assertEqual(asset.symbol, "PETR4")

    def test_unique_together_user_symbol_raises_integrity_error(self):
        Asset.objects.create(
            name="Petrobras", user=self.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        with self.assertRaises(IntegrityError):
            Asset.objects.create(
                name="Petrobras dup", user=self.user, symbol="PETR4", type=AssetChoices.STOCK
            )

    def test_same_symbol_different_users_is_allowed(self):
        Asset.objects.create(
            name="Petrobras", user=self.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        # Should not raise
        Asset.objects.create(
            name="Petrobras", user=self.other_user, symbol="PETR4", type=AssetChoices.STOCK
        )

    def test_clean_uppercases_symbol_before_validation(self):
        Asset.validator_class = MagicMock(return_value=_make_validator(is_valid=True))
        asset = Asset(name="Vale", user=self.user, symbol="vale3", type=AssetChoices.STOCK)
        asset.clean()
        self.assertEqual(asset.symbol, "VALE3")

    def test_clean_raises_for_invalid_symbol_format(self):
        asset = Asset(name="Bad", user=self.user, symbol="INVALID", type=AssetChoices.STOCK)
        with self.assertRaises(ValidationError):
            asset.clean()

    def test_assert_validation_passes_when_external_validator_is_valid(self):
        asset = Asset(name="Vale", user=self.user, symbol="VALE3", type=AssetChoices.STOCK)
        asset.assert_validation(external_validator=_make_validator(is_valid=True))

    def test_assert_validation_raises_when_external_validator_is_invalid(self):
        asset = Asset(name="Invalid", user=self.user, symbol="VALE3", type=AssetChoices.STOCK)
        with self.assertRaises(ValidationError):
            asset.assert_validation(external_validator=_make_validator(is_valid=False))

    def test_assert_validation_skips_when_symbol_and_type_unchanged(self):
        asset = Asset.objects.create(
            name="Petrobras2", user=self.user, symbol="BRFS3", type=AssetChoices.STOCK
        )
        validator = _make_validator(is_valid=False)
        # Validation is skipped — no exception even though the validator would fail
        asset.assert_validation(external_validator=validator)

    def test_assert_validation_runs_when_symbol_changes(self):
        asset = Asset.objects.create(
            name="Petrobras3", user=self.user, symbol="LREN3", type=AssetChoices.STOCK
        )
        asset.symbol = "VALE3"
        with self.assertRaises(ValidationError):
            asset.assert_validation(external_validator=_make_validator(is_valid=False))

    def test_fii_asset_can_be_created(self):
        asset = Asset.objects.create(
            name="Kinea Renda Imobiliária", user=self.user, symbol="KNRI11", type=AssetChoices.FII
        )
        self.assertEqual(asset.type, AssetChoices.FII)

    def test_bdr_asset_can_be_created(self):
        asset = Asset.objects.create(
            name="Apple Inc.", user=self.user, symbol="AAPL34", type=AssetChoices.BDR
        )
        self.assertEqual(asset.type, AssetChoices.BDR)

    def test_create_asset_price_returns_asset_price_instance(self):
        asset = Asset.objects.create(
            name="Petrobras4", user=self.user, symbol="MGLU3", type=AssetChoices.STOCK
        )
        price = asset.create_asset_price(42.50)
        self.assertIsInstance(price, AssetPrice)
        self.assertEqual(price.asset, asset)
        self.assertEqual(price.price, Decimal("42.50"))


class AssetPriceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username="priceuser", password="pass")
        cls.asset = Asset.objects.create(
            name="Petrobras", user=user, symbol="PETR4", type=AssetChoices.STOCK
        )

    def test_str_contains_symbol_brl_and_date(self):
        price = AssetPrice.objects.create(asset=self.asset, price=Decimal("38.90"))
        self.assertIn("PETR4", str(price))
        self.assertIn("R$", str(price))

    def test_prices_related_name_returns_all_prices(self):
        AssetPrice.objects.create(asset=self.asset, price=Decimal("38.90"))
        AssetPrice.objects.create(asset=self.asset, price=Decimal("39.10"))
        self.assertEqual(self.asset.prices.count(), 2)

    def test_cascade_delete_removes_prices(self):
        asset = Asset.objects.create(
            name="Temp", user=self.asset.user, symbol="TEMP3", type=AssetChoices.STOCK
        )
        asset_id = asset.pk
        AssetPrice.objects.create(asset=asset, price=Decimal("10.00"))
        asset.delete()
        self.assertEqual(AssetPrice.objects.filter(asset_id=asset_id).count(), 0)
