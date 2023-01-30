"""
Tests of the recipe API
"""
from decimal import Decimal

from rest_framework.test import APIClient
from rest_framework import status

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
)

from core.models import Recipe

RECIPES_URL = reverse("recipe:recipe-list")


def create_user(**params):
    """Helper to create and return new user"""
    return get_user_model().objects.create_user(**params)


def create_url(recipe_id):
    """Create Recipe Detail URL from id"""
    return reverse("recipe:recipe-detail", args=[recipe_id])


def create_recipe(user, **params):
    """Helper to create and return a sample recipe"""
    defaults = {
        "title": "Sample recipe title",
        "time_minutes": 22,
        "price": Decimal("5.50"),
        "description": "Sample recipee description",
        "link": "http://example.com/recipe.pdf",
    }
    defaults.update(params)

    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    """Tests for unprotected recipe endpoints"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test that auth is required for the recipe"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Tests for protected recipe endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            email="test@example.com",
            password="TestPass3434",
        )
        self.client.force_authenticate(self.user)

    def test_get_recipe_list(self):
        """Test retrieve of all the recipes"""
        create_recipe(self.user)
        create_recipe(self.user, title="Test Recipe")

        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.all().order_by("-id")  # reverse order
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_list_limited_to_user(self):
        """Confirm users see only their recipes"""
        other_user = create_user(
            email="other@example.com",
            password="TestedOther232",
        )
        # different users create recipes
        create_recipe(self.user)
        create_recipe(other_user)

        res = self.client.get(RECIPES_URL)
        # then get only for user and test
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_recipe_detail(self):
        """Test get recipe detail"""
        recipe = create_recipe(user=self.user)
        url = create_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe"""
        payload = {
            "title": "Sample Recipe",
            "time_minutes": 30,
            "price": Decimal("5.99"),
        }
        res = self.client.post(RECIPES_URL, payload)
        # confirm creation, then check the db
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data["id"])
        # first confirm it is the current user's
        self.assertEqual(recipe.user, self.user)
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_partial_update(self):
        """Test partial change to recipe"""
        original_link = "https://example.com/recipe.pdf"
        recipe = create_recipe(
            user=self.user,
            title="Sample REcipe",
            link=original_link,
        )
        payload = {"title": "New REcipe Tuitle"}
        url = create_url(recipe.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)
        # ensure only fields in payload were changed
        self.assertEqual(recipe.link, original_link)
        self.assertEqual(recipe.title, payload["title"])

    def test_full_recipe_update(self):
        """Test a full recipe update"""
        recipe = create_recipe(
            user=self.user,
            title="New Put Recipe",
            link="http",
            description="Description",
        )
        payload = {
            "title": "Updated Put Tilt",
            "price": Decimal("5.50"),
            "description": "Changed",
            "time_minutes": 10,
            "link": "https:/",
        }
        url = create_url(recipe.id)
        res = self.client.put(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(recipe.user, self.user)
        # check that eth changed
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_recipe_user_update_fails(self):
        """Security check that user in recipe cant be updated"""
        other_user = create_user(
            email="teast@exam.com",
            password="TESTS Fsf",
        )
        recipe = create_recipe(user=self.user)
        payload = {"user": other_user.id}
        url = create_url(recipe.id)
        self.client.patch(url, payload)

        recipe.refresh_from_db()
        self.assertEqual(recipe.user, self.user)

    def test_delete_recipe(self):
        """Deleting recipe by it's user successful"""
        recipe = create_recipe(user=self.user)
        url = create_url(recipe.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        # also confirm no longer in database
        self.assertFalse(Recipe.objects.filter(id=recipe.id).exists())

    def test_delete_other_users_recipe_fail(self):
        """Deleting another user's recipe shd fail"""
        other_user = create_user(
            email="test@exam.com",
            password="TEKDSds",
        )
        recipe = create_recipe(user=other_user)

        url = create_url(recipe.id)
        res = self.client.delete(url)
        # check also recipe still in db
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Recipe.objects.filter(id=recipe.id).exists())
