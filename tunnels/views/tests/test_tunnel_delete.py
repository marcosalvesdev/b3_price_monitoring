from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from assets.models import Asset
from globals.http_helpers import status_codes
from tunnels.models import PriceTunnel


class TunnelDeleteViewTests(TestCase):
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
        cls.url = reverse("tunnels:delete", kwargs={"pk": cls.tunnel.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_302_FOUND)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_delete_get_returns_200_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_200_OK)

    def test_delete_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tunnels/tunnel_delete.html")

    def test_delete_context_contains_cancel_url(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        expected_url = reverse("tunnels:detail", kwargs={"pk": self.tunnel.pk})
        self.assertEqual(response.context["cancel_url"], expected_url)

    def test_delete_context_contains_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["tunnel"], self.tunnel)

    def test_delete_post_removes_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status_codes.HTTP_302_FOUND)
        self.assertRedirects(response, reverse("tunnels:list"))
        self.assertFalse(PriceTunnel.objects.filter(pk=self.tunnel.pk).exists())

    def test_delete_does_not_remove_other_tunnels(self):
        self.client.login(username="testuser", password="testpass123")
        self.client.post(self.url)
        self.assertTrue(PriceTunnel.objects.filter(pk=self.other_tunnel.pk).exists())

    def test_delete_other_user_tunnel_returns_404(self):
        self.client.login(username="testuser", password="testpass123")
        other_url = reverse("tunnels:delete", kwargs={"pk": self.other_tunnel.pk})
        response = self.client.get(other_url)
        self.assertEqual(response.status_code, status_codes.HTTP_404_NOT_FOUND)
        self.assertTrue(PriceTunnel.objects.filter(pk=self.other_tunnel.pk).exists())

    def test_delete_post_other_user_tunnel_returns_404(self):
        self.client.login(username="testuser", password="testpass123")
        other_url = reverse("tunnels:delete", kwargs={"pk": self.other_tunnel.pk})
        response = self.client.post(other_url)
        self.assertEqual(response.status_code, status_codes.HTTP_404_NOT_FOUND)
        self.assertTrue(PriceTunnel.objects.filter(pk=self.other_tunnel.pk).exists())
