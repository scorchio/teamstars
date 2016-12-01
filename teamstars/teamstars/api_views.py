from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from votes.models import Vote
from serializers import LeaderboardSerializer


class LeaderboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        # Do not use the queryset property instead of this, as that would cache
        # the results.
        return Vote.objects.leaderboard()
