"""
Tests for Models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Tests the Models"""

    def test_user_creation_with_email_successful(self):
        """Can user created with email using custom user model succeed"""
        email = "test@example.com"
        password = "Test123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
