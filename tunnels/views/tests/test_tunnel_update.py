from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from assets.models import Asset
from tunnels.models import PriceTunnel


class TunnelUpdateViewTests(TestCase):
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
        cls.url = reverse("tunnels:update", kwargs={"pk": cls.tunnel.pk})

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)

    def test_update_get_returns_200_for_owner(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_update_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tunnels/tunnel_update.html")

    def test_update_context_contains_cancel_url(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        expected_url = reverse("tunnels:detail", kwargs={"pk": self.tunnel.pk})
        self.assertEqual(response.context["cancel_url"], expected_url)

    def test_update_context_contains_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.context["tunnel"], self.tunnel)

    def test_update_valid_post_updates_tunnel(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "upper_limit": "200.00",
            "lower_limit": "50.00",
            "check_interval_minutes": 20,
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tunnels:list"))
        self.tunnel.refresh_from_db()
        self.assertEqual(self.tunnel.upper_limit, 200.00)
        self.assertEqual(self.tunnel.lower_limit, 50.00)
        self.assertEqual(self.tunnel.check_interval_minutes, 20)

    def test_update_invalid_post_empty_values_returns_form_with_errors(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "upper_limit": "",
            "lower_limit": "",
            "check_interval_minutes": "",
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_update_invalid_post_lower_greater_than_upper_returns_errors(self):
        self.client.login(username="testuser", password="testpass123")
        data = {
            "upper_limit": "100.00",
            "lower_limit": "200.00",
            "check_interval_minutes": 10,
            "is_active": True,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)
