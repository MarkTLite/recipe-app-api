"""
Serializer for the Recipe API data
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


class RecipeSerializer(serializers.ModelSerializer):
    """Parsing the recipe api data"""

    class Meta:
        model = Recipe
        fields = [
            "id",
            "title",
            "time_minutes",
            "price",
            # "description",
            "link",
        ]
        read_only_fields = ["id"]


class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail Endpoint"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]


class TagSerializer(serializers.ModelSerializer):
    """Tag Endpoint CRUD"""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
