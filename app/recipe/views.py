"""
Views for the recipe api
"""

from rest_framework import (
    viewsets,
    mixins,
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    TagSerializer,
)
from core.models import (
    Recipe,
    Tag,
)


class RecipeViewset(viewsets.ModelViewSet):
    """Manages the recipe endpoints"""

    serializer_class = RecipeDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = Recipe.objects.all()

    def get_queryset(self):
        """Retrieve updates for the authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    def get_serializer_class(self):
        """Choose the serializer class for the request"""
        if self.action == "list":
            return RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """While creating the recipe"""
        serializer.save(user=self.request.user)


class TagViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Tags endpoints for CRUD"""

    serializer_class = TagSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()

    def get_queryset(self):
        """Return tags dependent on user and ordered"""
        return self.queryset.filter(user=self.request.user).order_by("name")
