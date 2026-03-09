from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from assets.models import Asset


class TunnelListViewTests(TestCase):
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
        cls.url = reverse("tunnels:list")

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)
        self.assertIn("/accounts/login/", response.url)

    def test_list_returns_200_for_authenticated_user(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_list_uses_correct_template(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "tunnels/tunnel_list.html")

    def test_list_shows_only_user_tunnels(self):
        from tunnels.models import PriceTunnel

        user_tunnel = PriceTunnel.objects.create(
            asset=self.asset,
            upper_limit=150.00,
            lower_limit=100.00,
            check_interval_minutes=10,
        )
        PriceTunnel.objects.create(
            asset=self.other_asset,
            upper_limit=200.00,
            lower_limit=50.00,
            check_interval_minutes=5,
        )

        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        tunnels = response.context["tunnels"]
        self.assertEqual(len(tunnels), 1)
        self.assertEqual(tunnels[0].pk, user_tunnel.pk)

    def test_list_empty_when_user_has_no_tunnels(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        tunnels = response.context["tunnels"]
        self.assertEqual(len(tunnels), 0)

    def test_list_context_name_is_tunnels(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertIn("tunnels", response.context)
