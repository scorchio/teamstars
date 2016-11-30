from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from votes.models import Vote
from serializers import LeaderboardSerializer


class LeaderboardView(ListAPIView):
    serializer_class = LeaderboardSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Vote.objects.leaderboard()


class LeaderboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Vote.objects.leaderboard()
    serializer_class = LeaderboardSerializer
