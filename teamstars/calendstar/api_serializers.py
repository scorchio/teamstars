from rest_framework import serializers

from calendstar.models import CalendarEvent
from teamstars.serializers import UserSerializer


class CalendarEventSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer()

    class Meta:
        model = CalendarEvent
        depth = 2
        fields = ('submitted_by', 'title', 'location',
                  'starts', 'ends', 'description', 'is_private')
