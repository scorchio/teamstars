from django.contrib.auth.models import User

from rest_framework import serializers

from common.models import Profile
from votes.models import Vote, VoteType


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        depth = 1
        fields = ('fb_link', 'location', 'birth_date', 'photo')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'is_active', 'is_staff', 'date_joined', 'last_login', 'profile')


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'type', 'sender', 'recipient', 'title', 'description',
                  'created', 'modified')

    def validate(self, data):
        vote = Vote(**data)
        vote.clean()
        return data


class VoteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteType
        fields = ('id', 'type', 'sender_points', 'recipient_points', 'created',
                  'modified')


class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)
