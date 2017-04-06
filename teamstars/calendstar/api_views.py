from rest_framework import viewsets

from calendstar.api_serializers import CalendarEventSerializer
from calendstar.models import CalendarEvent


class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
