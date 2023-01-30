"""
Tests for the Tag models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Tag


def create_user(email="user@example.com", password="testpass!@#"):
    """Helper to create and return user"""
    return get_user_model().objects.create(
        email=email,
        password=password,
    )


class TagModelTests(TestCase):
    """Tag model tests"""

    def test_tag_create(self):
        """Test creating a tag is successful"""
        user = create_user()
        tag = Tag.objects.create(user=user, name="Tag1")

        self.assertEqual(str(tag), tag.name)
