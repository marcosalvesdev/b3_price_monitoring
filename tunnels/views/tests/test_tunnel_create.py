from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from assets.models import Asset
from globals.http_helpers import status_codes
from tunnels.models import PriceTunnel


class TunnelCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.other_user = User.objects.create_user(username="otheruser", password="testpass123")

        cls.asset = Asset.objects.create(
            name="Test Asset",
            user=cls.user,
            symbol="TEST1",
            type="stock",
            is_active=True,
        )
        cls.other_asset = Asset.objects.create(
            name="Other Asset",
            user=cls.other_user,
            symbol="OTHR1",
            type="stock",
            is_active=True,
        )
        cls.url = reverse("tunnels:create")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_302_FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_create_get_returns_200_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)

    def test_create_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tunnels/tunnel_create.html")

    def test_create_context_contains_cancel_url(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["cancel_url"], reverse("tunnels:list"))

    def test_create_form_only_shows_user_assets(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        form = response.context["form"]
        asset_queryset = form.fields["asset"].queryset
        self.assertIn(self.asset, asset_queryset)
        self.assertNotIn(self.other_asset, asset_queryset)

    def test_create_valid_post_creates_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "asset": self.asset.pk,
            "upper_limit": "150.00",
            "lower_limit": "100.00",
            "check_interval_minutes": 10,
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status_codes.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("tunnels:list"))
        self.assertEqual(PriceTunnel.objects.count(), 1)
        tunnel = PriceTunnel.objects.first()
        self.assertEqual(tunnel.asset, self.asset)

    def test_create_invalid_post_empty_values_returns_form_with_errors(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "asset": self.asset.pk,
            "upper_limit": "",
            "lower_limit": "",
            "check_interval_minutes": "",
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)
        self.assertTrue(response.context["form"].errors)

    def test_create_invalid_post_lower_greater_than_upper_returns_errors(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "asset": self.asset.pk,
            "upper_limit": "100.00",
            "lower_limit": "200.00",
            "check_interval_minutes": 10,
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)
        self.assertTrue(response.context["form"].errors)

    def test_create_duplicate_tunnel_shows_error(self):
        PriceTunnel.objects.create(
            asset=self.asset,
            upper_limit=150.00,
            lower_limit=100.00,
            check_interval_minutes=10,
        )

        self.client.login(username="testuser", password="testpass123")
        data = {
            "asset": self.asset.pk,
            "upper_limit": "150.00",
            "lower_limit": "100.00",
            "check_interval_minutes": 10,
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)
        self.assertTrue(response.context["form"].errors)
