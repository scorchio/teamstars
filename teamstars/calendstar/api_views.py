from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api_serializers import CalendarEventSerializer, CalendarEventResponseSerializer
from models import CalendarEvent, CalendarEventResponse


class CalendarEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer

    @detail_route(methods=['get'], url_path='responses')
    def get_responses(self, request, pk=None):
        event = self.get_object()
        responses = CalendarEventResponse.objects.filter(calendar_event=event)
        serializer = CalendarEventResponseSerializer(instance=responses, many=True)
        return Response(serializer.data)


class CalendarEventResponseViewSet(viewsets.ModelViewSet):
    queryset = CalendarEventResponse.objects.all()
    serializer_class = CalendarEventResponseSerializer
