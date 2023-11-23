from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для пользователей.
    """

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
