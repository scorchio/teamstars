from rest_framework import viewsets
from rest_framework import mixins

from models import Vote, VoteType
from api_serializers import LeaderboardSerializer, VoteSerializer, VoteTypeSerializer


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all().prefetch_related('type',
                                                   'sender',
                                                   'recipient',
                                                   'sender__profile',
                                                   'recipient__profile')
    serializer_class = VoteSerializer


class VoteTypeViewSet(viewsets.ModelViewSet):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer


class LeaderboardViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = LeaderboardSerializer

    def get_queryset(self):
        # Do not use the queryset property instead of this, as that would cache
        # the results.
        return Vote.objects.leaderboard()
