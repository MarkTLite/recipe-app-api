"""
Tests for admin modifications
"""
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for Django admin"""

    def setUp(self) -> None:
        """Create user and Admin test Client"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="TestAdmin@example.com",
            password="Sample189*",
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="AnyTEst3454", name="Test USer"
        )

    def test_users_list(self):
        """Test user is in list when logged as admin"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.email)
        self.assertContains(res, self.user.name)

    def test_users_change_page(self):
        """Test the users change page works due to custom user admin"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_add_user(self):
        """Test that admin add users page works due to custom user admin"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
