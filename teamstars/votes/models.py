from collections import defaultdict, Counter
from operator import itemgetter
import logging

from django.core.exceptions import ValidationError
from django.db import models, connection
from django.db.models import Count, F
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel

logger = logging.getLogger('votes')


@python_2_unicode_compatible
class VoteType(TimeStampedModel):
    type = models.CharField(max_length=255)
    sender_points = models.IntegerField(default=0)
    recipient_points = models.IntegerField(default=0)

    def __str__(self):
        return self.type


class VoteManager(models.Manager):
    def vote_statistics(self):
        sent_votes = Vote.objects.values('sender__id', 'sender__username',
                                         'type', 'type__type'). \
            annotate(sent_count=Count('sender_id'))
        received_votes = Vote.objects.values('recipient__id',
                                             'recipient__username',
                                             'type', 'type__type'). \
            annotate(received_count=Count('recipient_id'))

        # Get the sent and received votes together into a unified structure,
        # which can be passed to leaderboard calculation etc.
        votes = {
            'sent': {(vote['type'], vote['type__type']):
                     [{
                           "user_id": typed_vote['sender__id'],
                           "username": typed_vote['sender__username'],
                           "count": typed_vote['sent_count']
                       } for typed_vote in sent_votes
                     if typed_vote['type'] == vote['type']]
                     for vote in sent_votes},
            'received': {(vote['type'], vote['type__type']):
                         [{
                               "user_id": typed_vote['recipient__id'],
                               "username": typed_vote['recipient__username'],
                               "count": typed_vote['received_count']
                           } for typed_vote in received_votes
                         if typed_vote['type'] == vote['type']]
                         for vote in received_votes}
                 }

        return votes

    def leaderboard(self):
        """Generates leaderboard from the votes."""

        sender_points = Vote.objects\
            .values('type__id', 'sender__id', 'sender__username')\
            .annotate(points=Count('sender__id') * F('type__sender_points'))

        recipient_points = Vote.objects\
            .values('type__id', 'recipient__id', 'recipient__username') \
            .annotate(points=Count('recipient__id') * F('type__recipient_points'))

        # Sum the results using Counter, saving the usernames in the process
        usernames = dict()
        leaderboard = defaultdict(Counter)
        sent_points = [{"id": result['sender__id'],
                        "username": result['sender__username'],
                        "points": result['points']} for result in sender_points]
        for result in sender_points:
            usernames[int(result['sender__id'])] = result['sender__username']
        for point in sent_points:
            leaderboard[point['id']].update({'points': point['points']})
        received_points = [{"id": result['recipient__id'],
                            "username": result['recipient__username'],
                            "points": result['points']}
                           for result in recipient_points]
        for result in recipient_points:
            usernames[int(result['recipient__id'])] = result['recipient__username']
        for point in received_points:
            leaderboard[point['id']].update({'points': point['points']})

        # Transform the result back into a normal dict
        leaderboard = {
            key: {'user_id': key,
                  'points': value['points'],
                  'username': usernames[key]}
            for key, value in leaderboard.iteritems()}

        leaderboard = sorted(leaderboard.values(), key=itemgetter("points"),
                             reverse=True)
        return leaderboard


@python_2_unicode_compatible
class Vote(TimeStampedModel):
    type = models.ForeignKey(VoteType, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="sender_user")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name="recipient_user")
    title = models.CharField(max_length=255)
    description = models.TextField()
    objects = VoteManager()

    def __str__(self):
        return "[{0:%Y-%m-%d}] {1} -> {2}: {3}".format(
            self.created,
            self.sender.username,
            self.recipient.username, self.title)

    def clean(self):
        if self.sender_id == self.recipient_id:
            raise ValidationError(
                _('A user should not send votes to himself.'))
