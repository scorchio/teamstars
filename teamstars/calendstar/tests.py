from django.utils import timezone
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from models import CalendarEvent


class CalendarEventTestCase(TestCase):
    def test_create_event(self):
        creator = User.objects.create_user(username="user1")
        CalendarEvent.objects.create(
            submitted_by=creator,
            title="Test event",
            location="Test location with a really nice description of the place",
            description="Bla bla",
            is_private=False,
            starts=timezone.now(),
            ends=timezone.now() + timedelta(hours=2)
        )
        self.assertEqual(1, CalendarEvent.objects.count())
