from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from votes.models import Vote, VoteType
from serializers import LeaderboardSerializer, UserSerializer, VoteSerializer, VoteTypeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteTypeViewSet(viewsets.ModelViewSet):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer


class LeaderboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        # Do not use the queryset property instead of this, as that would cache
        # the results.
        return Vote.objects.leaderboard()
