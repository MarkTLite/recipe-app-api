"""
Tests for the User API
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    """Helper fn for creating a user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Tests for the public features of the User API"""

    def setUp(self):
        self.client = APIClient()

    def test_user_create_success(self):
        """Test that the user is created well"""
        payload = {
            "email": "testUse@example.com",
            "password": "SampleTest12345*",
            "name": "Test User",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        # check first for status code
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # confirm user in database and password is right
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        # no passwords in response
        self.assertNotIn("password", res.data)

    def test_same_email_returns_error(self):
        """Test user creation attempt with same email fails"""
        payload = {
            "email": "testUse@example.com",
            "password": "SampleTest12345*",
            "name": "Different Name",
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_create_password_short_fails(self):
        """Test that the user cannot create with short password"""
        payload = {
            "email": "testUse@example.com",
            "password": "pw",
            "name": "Different Name",
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        # and then make sure user not in database
        user_exists = (
            get_user_model()
            .objects.filter(
                email=payload["email"],
            )
            .exists()
        )
        self.assertFalse(user_exists)

    def test_creates_token_for_user(self):
        """Test that a token is returned for a logged in user"""
        # create the user
        user_details = {
            "email": "test@example.com",
            "name": "Test User",
            "password": "Sample123",
        }
        create_user(**user_details)
        # login and test
        payload = {
            "email": user_details["email"],
            "password": user_details["password"],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_bad_creds_return_error(self):
        """Wrong logins return 400 bad request"""
        create_user(email="test@example.com", password="Pass")
        payload = {
            "email": "test@example.com",
            "password": "Sample USer",
            "name": "SAmple USer",
        }
        res = self.client.post(TOKEN_URL, **payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_pass_returns_error(self):
        """No password return 400 bad request"""
        payload = {"email": "test@example.com", "password": ""}
        res = self.client.post(TOKEN_URL, **payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
