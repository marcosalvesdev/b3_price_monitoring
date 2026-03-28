from http import HTTPStatus
from unittest.mock import MagicMock, PropertyMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from assets.models import Asset, AssetChoices
from assets.utils.validators.base_asset_validator import BaseAssetValidator

User = get_user_model()


def _make_validator_class(is_valid: bool):
    """Returns a validator class whose instances report the given is_valid value."""
    mock_instance = MagicMock(spec=BaseAssetValidator)
    type(mock_instance).is_valid = PropertyMock(return_value=is_valid)

    validator_class = MagicMock(return_value=mock_instance)
    return validator_class


class AssetCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")
        cls.existing_asset = Asset.objects.create(
            name="Petrobras", user=cls.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        cls.url = reverse("assets:create")

    def tearDown(self):
        # Reset class-level validator so it doesn't leak between tests
        Asset.validator_class = None

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_get_returns_200_for_authenticated_user(self):
        self.client.login(username="testuser", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_valid_post_creates_asset_and_redirects(self):
        Asset.validator_class = _make_validator_class(is_valid=True)
        self.client.login(username="testuser", password="pass")

        response = self.client.post(
            self.url,
            {"name": "Vale", "symbol": "VALE3", "type": AssetChoices.STOCK, "description": ""},
        )

        self.assertRedirects(response, reverse("assets:list"))
        self.assertTrue(Asset.objects.filter(user=self.user, symbol="VALE3").exists())

    def test_duplicate_symbol_returns_form_error_without_creating_asset(self):
        self.client.login(username="testuser", password="pass")

        response = self.client.post(
            self.url,
            {
                "name": "Petrobras dup",
                "symbol": "PETR4",
                "type": AssetChoices.STOCK,
                "description": "",
            },
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFormError(
            response.context["form"], "symbol", "An asset with this symbol already exists."
        )
        self.assertEqual(Asset.objects.filter(user=self.user, symbol="PETR4").count(), 1)
