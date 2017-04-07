from django.contrib.auth.models import User

from rest_framework import serializers

from models import Profile


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
