from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.views import APIView

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


class CalendarEventMyResponseView(APIView):
    def put(self, request, pk=None, format=None):
        event = CalendarEvent.objects.get(pk=pk)
        # Need to pass request (for CurrentUserDefault) and event (for the validator) in context to make this work
        event_response = CalendarEventResponse.objects.filter(calendar_event=event, user=request.user).first()
        print "response is ", event_response
        serializer = CalendarEventResponseSerializer(instance=event_response, data=request.data,
                                                     context={'request': request, 'event': event})
        if serializer.is_valid():
            serializer.save()
            if event_response:
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None, format=None):
        # TODO: test that only the currently selected event's response is deleted
        event = CalendarEvent.objects.get(pk=pk)
        response = CalendarEventResponse.objects.filter(calendar_event=event, user=request.user)
        response.delete()
        return Response(status=status.HTTP_200_OK)


class CalendarEventResponseViewSet(viewsets.ModelViewSet):
    queryset = CalendarEventResponse.objects.all()
    serializer_class = CalendarEventResponseSerializer
