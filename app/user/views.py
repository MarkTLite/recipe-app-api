"""
Views for the User API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.serializers import (
    UserSerializers,
    AuthTokenSerializer,
)


class CreateUserView(generics.CreateAPIView):
    """Creating a User"""

    serializer_class = UserSerializers


class CreateAuthTokenView(ObtainAuthToken):
    """Obtains the user's auth token"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manages the authenticated user"""

    serializer_class = UserSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the updated user"""
        return self.request.user
