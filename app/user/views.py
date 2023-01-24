"""
Views for the User API
"""
from rest_framework import generics
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
