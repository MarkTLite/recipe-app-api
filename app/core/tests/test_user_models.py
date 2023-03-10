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

    def test_normalise_email_successful(self):
        """Test whether poorly input emails are normalized"""
        sample_inputs = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]
        for given_email, expected in sample_inputs:
            user = get_user_model().objects.create_user(
                given_email, "Sample123")
            self.assertEqual(user.email, expected)

    def test_no_email_raises_exception(self):
        """Test that email is required"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "Sample123")

    def test_create_superuser_success(self):
        """Test that super user is created well"""
        user = get_user_model().objects.create_superuser(
            email="test@example.com",
            password="Admin123",
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
