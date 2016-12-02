from django.contrib.auth.models import User

from rest_framework import serializers, viewsets

from votes.models import Vote, VoteType


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'type', 'sender', 'recipient', 'title', 'description',
                  'created', 'modified')

    def validate(self, data):
        vote = Vote(**data)
        vote.clean()
        return data


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteType
        fields = ('id', 'type', 'sender_points', 'recipient_points', 'created',
                  'modified')


class VoteTypeViewSet(viewsets.ModelViewSet):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer


class LeaderboardSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    points = serializers.IntegerField(read_only=True)

