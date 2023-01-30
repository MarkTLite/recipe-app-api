"""
Tests for Tag API
"""

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from recipe.serializers import TagSerializer
from core.models import Tag

TAGS_URL = reverse("recipe:tag-list")


def create_user(email="test@example.com", password="TEsre434"):
    """Helper for creating and returning a user"""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagAPITests(TestCase):
    """For tag api tests not requiring auth"""

    def setUp(self):
        self.client = APIClient()

    def test_tag_req_authentication(self):
        """Auth requierd to retrieve tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagAPITests(TestCase):
    """For tag api tests requiring auth"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_tags(self):
        """Test retrieves all tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_to_user(self):
        """Test tags list is only for user authenticated"""
        other_user = create_user("other@example.com")
        Tag.objects.create(user=other_user, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort Food")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "Comfort Food")
        self.assertEqual(res.data[0]["id"], tag.id)
