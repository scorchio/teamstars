import datetime

import pytz
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from calendstar.models import CalendarEvent, CalendarEventResponse
from common.tests.api.test_api_auth import TEST_USER, TEST_PASSWORD


class CalendstarTestCase(APITestCase):
    token = None
    event1, event2 = None, None

    def setUp(self):
        user = User.objects.create_user(username=TEST_USER, password=TEST_PASSWORD)
        token_response = self.client.post('/api/v1/token-auth/', {
            'username': TEST_USER,
            'password': TEST_PASSWORD,
        }, format='json')
        self.token = token_response.data.get('token')

        tz = pytz.timezone("Europe/Budapest")
        self.event1 = CalendarEvent.objects.create(
            submitted_by=user,
            title='Test event 1',
            location='Test location',
            starts=tz.localize(datetime.datetime.utcnow()),
            ends=tz.localize(datetime.datetime.utcnow() + datetime.timedelta(hours=2)),
            description='Test description',
            is_private=False,
        )

        self.event2 = CalendarEvent.objects.create(
            submitted_by=user,
            title='Test event 2',
            location='Test location',
            starts=tz.localize(datetime.datetime.utcnow()),
            ends=tz.localize(datetime.datetime.utcnow() + datetime.timedelta(hours=4)),
            description='Test description',
            is_private=False,
        )

    def _respond_to_event(self, event_id, status, comment):
        return self.client.put('/api/v1/events/{event_id}/responses/mine/'.format(event_id=event_id), {
            'status': status,
            'comment': comment,
        }, format='json')

    def test_response_flow(self):
        response = self._respond_to_event(self.event1.id, 'status_yes', 'I think so')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self._respond_to_event(self.event1.id, 'status_yes', 'I think so')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CalendarEventResponse.objects.count(), 1)

        response = self._respond_to_event(self.event2.id, 'status_yes', 'I think so')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CalendarEventResponse.objects.count(), 2)

        response = self._respond_to_event(self.event1.id, 'status_no', 'Whoops, not yet')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CalendarEventResponse.objects.count(), 2)

        response = self.client.delete('/api/v1/events/{event_id}/responses/mine/'.format(event_id=self.event1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CalendarEventResponse.objects.count(), 1)

        response = self.client.delete('/api/v1/events/{event_id}/responses/mine/'.format(event_id=self.event2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CalendarEventResponse.objects.count(), 0)

    # TODO: response stat?
