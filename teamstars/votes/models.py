from collections import defaultdict, Counter
from operator import itemgetter
import logging

from django.db import models, connection
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

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
            'sent': {vote['type']:
                     [{
                           "user_id": typed_vote['sender__id'],
                           "username": typed_vote['sender__username'],
                           "count": typed_vote['sent_count']
                       } for typed_vote in sent_votes
                     if typed_vote['type'] == vote['type']]
                     for vote in sent_votes},
            'received': {vote['type']:
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
        sent_query = "select sender_id, username, " \
                     "count(sender_id)*sender_points " \
                     "from votes_vote, votes_votetype, auth_user " \
                     "where votes_vote.type_id = votes_votetype.id and " \
                     "votes_vote.sender_id = auth_user.id " \
                     "group by type_id, sender_id"

        received_query = "select recipient_id, username, " \
                         "count(recipient_id)*recipient_points " \
                         "from votes_vote, votes_votetype, auth_user " \
                         "where votes_vote.type_id = votes_votetype.id and " \
                         "votes_vote.recipient_id = auth_user.id " \
                         "group by type_id, recipient_id"

        with connection.cursor() as cursor:
            cursor.execute(sent_query)
            sent_results = cursor.fetchall()
            cursor.execute(received_query)
            received_results = cursor.fetchall()

        # Sum the results using Counter, saving the usernames in the process
        usernames = dict()
        leaderboard = defaultdict(Counter)
        sent_points = [{"id": result[0],
                        "username": result[1],
                        "points": result[2]} for result in sent_results]
        for result in sent_results:
            usernames[result[0]] = result[1]
        for point in sent_points:
            leaderboard[point['id']].update({'points': point['points']})
        received_points = [{"id": result[0],
                            "username": result[1],
                            "points": result[2]}
                           for result in received_results]
        for result in received_results:
            usernames[result[0]] = result[1]
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
