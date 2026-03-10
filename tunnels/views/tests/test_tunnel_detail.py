from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from assets.models import Asset
from globals.http_helpers import status_codes
from tunnels.models import PriceTunnel


class TunnelDetailViewTests(TestCase):
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
        cls.tunnel = PriceTunnel.objects.create(
            asset=cls.asset,
            upper_limit=150.00,
            lower_limit=100.00,
            check_interval_minutes=10,
        )
        cls.other_tunnel = PriceTunnel.objects.create(
            asset=cls.other_asset,
            upper_limit=200.00,
            lower_limit=50.00,
            check_interval_minutes=5,
        )
        cls.url = reverse("tunnels:detail", kwargs={"pk": cls.tunnel.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_302_FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_detail_returns_200_for_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)

    def test_detail_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tunnels/tunnel_detail.html")

    def test_detail_context_contains_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["tunnel"], self.tunnel)

    def test_detail_returns_404_for_other_users_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("tunnels:detail", kwargs={"pk": self.other_tunnel.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_codes.HTTP_404_NOT_FOUND)

    def test_detail_returns_404_for_nonexistent_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        url = reverse("tunnels:detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status_codes.HTTP_404_NOT_FOUND)
