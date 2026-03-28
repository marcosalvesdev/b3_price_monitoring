from django.contrib.auth import get_user_model
from django.test import TestCase

from assets.forms import AssetForm
from assets.models import Asset, AssetChoices

User = get_user_model()


class AssetFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")
        cls.other_user = User.objects.create_user(username="otheruser", password="pass")
        cls.existing_asset = Asset.objects.create(
            name="Petrobras", user=cls.user, symbol="PETR4", type=AssetChoices.STOCK
        )

    def _form_data(self, symbol="VALE3", asset_type=AssetChoices.STOCK):
        return {"name": "Vale", "symbol": symbol, "type": asset_type, "description": ""}

    def test_valid_form_with_new_symbol(self):
        form = AssetForm(data=self._form_data(symbol="VALE3"), user=self.user)
        self.assertTrue(form.is_valid())

    def test_duplicate_symbol_same_user_is_invalid(self):
        form = AssetForm(data=self._form_data(symbol="PETR4"), user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("symbol", form.errors)

    def test_duplicate_symbol_different_user_is_valid(self):
        form = AssetForm(data=self._form_data(symbol="PETR4"), user=self.other_user)
        self.assertTrue(form.is_valid())

    def test_update_same_symbol_on_own_asset_is_valid(self):
        form = AssetForm(
            data=self._form_data(symbol="PETR4"),
            user=self.user,
            instance=self.existing_asset,
        )
        self.assertTrue(form.is_valid())

    def test_without_user_skips_duplicate_check(self):
        form = AssetForm(data=self._form_data(symbol="PETR4"))
        self.assertTrue(form.is_valid())

    def test_missing_required_fields_returns_errors(self):
        form = AssetForm(data={}, user=self.user)
        self.assertFalse(form.is_valid())
        for field in ("name", "symbol", "type"):
            self.assertIn(field, form.errors)
