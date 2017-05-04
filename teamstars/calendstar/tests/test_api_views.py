from django.test import TestCase
from mock import patch, Mock

from calendstar.api_views import CalendarEventViewSet


class CalendarEventViewSetTestCase(TestCase):

    @patch('calendstar.api_views.CalendarEventResponseSerializer')
    @patch('calendstar.api_views.CalendarEventResponse')
    @patch('calendstar.api_views.CalendarEvent')
    def test_get_response(self, mock_event, mock_event_response, mock_event_response_serializer):
        sample_data = {'this': 'that'}
        mock_event_response_serializer.return_value = Mock(data=sample_data)
        mock_request = Mock()

        viewset = CalendarEventViewSet()
        viewset.get_object = Mock()

        response = viewset.get_responses(mock_request)

        self.assertDictEqual(sample_data, response.data)
