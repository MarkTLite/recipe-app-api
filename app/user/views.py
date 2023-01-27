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
    """View that connects to the UserSerializer"""

    serializer_class = UserSerializers


class CreateAuthTokenView(ObtainAuthToken):
    """View that Obtains the user auth token"""

    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """View that manages the authenticated user"""

    serializer_class = UserSerializers
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the updated user"""
        return self.request.user
