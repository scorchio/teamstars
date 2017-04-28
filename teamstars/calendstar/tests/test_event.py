from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from calendstar.models import CalendarEvent, CalendarEventResponse


class CalendarEventTestCase(TestCase):
    def setUp(self):
        creator = User.objects.create_user(username="user_creator")
        CalendarEvent.objects.create(
            submitted_by=creator,
            title="Test event",
            location="Test location with a really nice description of the place",
            description="Bla bla",
            is_private=False,
            starts=timezone.now(),
            ends=timezone.now() + timedelta(hours=2)
        )

    def test_create_event(self):
        self.assertEqual(1, CalendarEvent.objects.count())

    def test_create_event_with_responses(self):
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        event = CalendarEvent.objects.all().first()
        CalendarEventResponse.objects.create(
            user=user1,
            calendar_event=event,
            status=CalendarEventResponse.STATUS.status_yes,
            comment="I'm going to be there for sure"
        )
        CalendarEventResponse.objects.create(
            user=user2,
            calendar_event=event,
            status=CalendarEventResponse.STATUS.status_rather_no,
            comment="I won't be there most likely, but who knows..."
        )
        self.assertEqual(1, CalendarEventResponse.status_yes.count())
        self.assertEqual(0, CalendarEventResponse.status_rather_yes.count())
        self.assertEqual(1, CalendarEventResponse.status_rather_no.count())
        self.assertEqual(0, CalendarEventResponse.status_no.count())

    def test_single_response_per_user_only(self):
        user1 = User.objects.create_user(username="user1")
        event = CalendarEvent.objects.all().first()
        CalendarEventResponse.objects.create(
            user=user1,
            calendar_event=event,
            status=CalendarEventResponse.STATUS.status_yes,
            comment="I'm going to be there for sure"
        )
        with self.assertRaises(IntegrityError):
            CalendarEventResponse.objects.create(
                user=user1,
                calendar_event=event,
                status=CalendarEventResponse.STATUS.status_no,
                comment="I won't be able to make it unfortunately :("
            )

    def test_response_update(self):
        user1 = User.objects.create_user(username="user1")
        event = CalendarEvent.objects.all().first()
        response = CalendarEventResponse.objects.create(
            user=user1,
            calendar_event=event,
            status=CalendarEventResponse.STATUS.status_yes,
            comment="I'm going to be there for sure"
        )
        response.status = CalendarEventResponse.STATUS.status_no
        response.comment = "I won't be able to make it :("
        response.save()
        self.assertEqual(0, CalendarEventResponse.status_yes.count())
        self.assertEqual(1, CalendarEventResponse.status_no.count())
