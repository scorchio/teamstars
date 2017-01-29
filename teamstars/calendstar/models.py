from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class CalendarEvent(TimeStampedModel):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    location = models.TextField(max_length=1000)
    starts = models.DateTimeField()
    ends = models.DateTimeField()
    description = models.TextField()
    is_private = models.BooleanField()

    def __str__(self):
        return self.title
