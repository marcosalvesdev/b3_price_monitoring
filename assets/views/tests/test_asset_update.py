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


class AssetUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")

    def setUp(self):
        self.asset = Asset.objects.create(
            name="Petrobras", user=self.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        self.url = reverse("assets:update", kwargs={"pk": self.asset.pk})

    def tearDown(self):
        Asset.validator_class = None

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_get_returns_200_for_asset_owner(self):
        self.client.login(username="testuser", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_valid_post_updates_asset_and_redirects(self):
        Asset.validator_class = _make_validator_class(is_valid=True)
        self.client.login(username="testuser", password="pass")

        response = self.client.post(
            self.url,
            {
                "name": "Petrobras Updated",
                "symbol": "PETR4",
                "type": AssetChoices.STOCK,
                "description": "Updated",
            },
        )

        self.assertRedirects(response, reverse("assets:list"))
        self.asset.refresh_from_db()
        self.assertEqual(self.asset.name, "Petrobras Updated")
