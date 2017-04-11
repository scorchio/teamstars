from rest_framework import serializers

from calendstar.models import CalendarEvent, CalendarEventResponse
from common.api_serializers import UserSerializer


class CalendarEventResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer(default=serializers.CurrentUserDefault())

    def validate(self, data):
        if 'calendar_event' not in data:
            data['calendar_event'] = self.context['event']
        return data

    class Meta:
        model = CalendarEventResponse
        fields = ('id', 'user', 'status', 'comment')


class CalendarEventSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer()
    responses = CalendarEventResponseSerializer(many=True)

    class Meta:
        model = CalendarEvent
        depth = 2
        fields = ('id', 'submitted_by', 'title', 'location',
                  'starts', 'ends', 'description', 'is_private',
                  'response_stats', 'responses')
