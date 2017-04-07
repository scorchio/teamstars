from rest_framework import serializers

from common.api_serializers import UserSerializer
from models import VoteType, Vote


class VoteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteType
        fields = ('id', 'type', 'sender_points', 'recipient_points', 'created',
                  'modified')


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    type = VoteTypeSerializer()
    sender = UserSerializer()
    recipient = UserSerializer()

    class Meta:
        model = Vote
        fields = ('id', 'type', 'sender', 'recipient', 'title', 'description',
                  'created', 'modified')

    def validate(self, data):
        vote = Vote(**data)
        vote.clean()
        return data


class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)
