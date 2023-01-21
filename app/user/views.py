"""
Views for the User API
"""
from rest_framework import generics
from user.serializers import UserSerializers


class CreateUserView(generics.CreateAPIView):
    """View that connects to the UserSerializer"""

    serializer_class = UserSerializers
