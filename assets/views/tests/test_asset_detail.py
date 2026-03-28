from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from assets.models import Asset, AssetChoices

User = get_user_model()


class AssetDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")
        cls.other_user = User.objects.create_user(username="otheruser", password="pass")
        cls.asset = Asset.objects.create(
            name="Petrobras", user=cls.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        cls.other_asset = Asset.objects.create(
            name="Vale", user=cls.other_user, symbol="VALE3", type=AssetChoices.STOCK
        )
        cls.url = reverse("assets:detail", kwargs={"pk": cls.asset.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_returns_200_for_asset_owner(self):
        self.client.login(username="testuser", password="pass")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context["asset"], self.asset)

    def test_other_user_asset_returns_404(self):
        self.client.login(username="testuser", password="pass")
        url = reverse("assets:detail", kwargs={"pk": self.other_asset.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
