from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from model_utils import Choices

from model_utils.models import TimeStampedModel, StatusModel


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

    def _get_response_stats(self):
        return CalendarEventResponse.objects\
                    .filter(calendar_event=self)\
                    .values('status').annotate(count=Count('status'))

    response_stats = property(_get_response_stats)

    def _get_responses(self):
        return CalendarEventResponse.objects.filter(calendar_event=self)

    responses = property(_get_responses)


class CalendarEventResponse(StatusModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    calendar_event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    STATUS = Choices(
        ('status_yes', _('Yes')),
        ('status_rather_yes', _('Likely yes')),
        ('status_rather_no', _('Likely no')),
        ('status_no', _('No'))
    )
    comment = models.TextField(max_length=1000)

    class Meta:
        unique_together = ('user', 'calendar_event')
