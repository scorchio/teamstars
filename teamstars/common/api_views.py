from django.contrib.auth.models import User
from rest_framework import viewsets

from common.api_serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('profile')
    serializer_class = UserSerializer
