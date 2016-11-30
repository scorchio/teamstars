from django.contrib.auth.models import User

from rest_framework import serializers, viewsets

from votes.models import Vote, VoteType


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class VoteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vote
        fields = ('id', 'type', 'sender', 'recipient', 'title', 'description',
                  'created', 'modified')


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class VoteTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = VoteType
        fields = ('id', 'type', 'created', 'modified')


class VoteTypeViewSet(viewsets.ModelViewSet):
    queryset = VoteType.objects.all()
    serializer_class = VoteTypeSerializer
