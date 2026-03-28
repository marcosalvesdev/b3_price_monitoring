from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from assets.models import Asset, AssetChoices

User = get_user_model()


class AssetDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="pass")

    def setUp(self):
        self.asset = Asset.objects.create(
            name="Petrobras", user=self.user, symbol="PETR4", type=AssetChoices.STOCK
        )
        self.url = reverse("assets:delete", kwargs={"pk": self.asset.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_deletes_asset_and_redirects(self):
        self.client.login(username="testuser", password="pass")

        response = self.client.post(self.url)

        self.assertRedirects(response, reverse("assets:list"))
        self.assertFalse(Asset.objects.filter(pk=self.asset.pk).exists())
