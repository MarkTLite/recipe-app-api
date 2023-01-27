"""
Tests for the recipe models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models
from decimal import Decimal


class RecipeModelTests(TestCase):
    """Tests for recipe models"""

    def test_create_recipe_success(self):
        user = get_user_model().objects.create_user(
            "test@example.com",
            "Testdfdf",
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title="Sample Recipe name",
            time_minutes=5,
            price=Decimal("5.50"),
            description="Sample Recipe Description",
        )
        self.assertEqual(str(recipe), recipe.title)
