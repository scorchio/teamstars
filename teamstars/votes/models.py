from collections import defaultdict
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
    POINTS_FOR_SENDING = 2
    POINTS_FOR_RECEIVING = 10

    def vote_statistics(self):
        sent_votes = Vote.objects.values('sender__id', 'sender__username'). \
            annotate(sent_count=Count('sender_id'))
        received_votes = Vote.objects.values('recipient__id',
                                             'recipient__username'). \
            annotate(received_count=Count('recipient_id'))
        logger.info("Vote statistics queries sent: {0}".format(
            connection.queries))

        sent_votes = [{
                          "user_id": vote['sender__id'],
                          "username": vote['sender__username'],
                          "sent_count": vote['sent_count']
                      } for vote in sent_votes]
        received_votes = [{
                              "user_id": vote['recipient__id'],
                              "username": vote['recipient__username'],
                              "received_count": vote['received_count']
                          } for vote in received_votes]

        # Join the two lists of dicts based on user_id
        votes = defaultdict(dict)
        for l in (sent_votes, received_votes):
            for elem in l:
                votes[elem['user_id']].update(elem)
        return votes

    def leaderboard(self):
        """Generates leaderboard from the votes."""
        sent_votes = Vote.objects.values('sender__id', 'sender__username').\
            annotate(sent_count=Count('sender_id'))
        received_votes = Vote.objects.values('recipient__id',
                                             'recipient__username').\
            annotate(received_count=Count('recipient_id'))
        logger.info("Leaderboard queries sent: \n    {0}\n    {1}".format(
            sent_votes.query, received_votes.query))

        votes = {vote['sender__id']:{
                        "user_id": vote['sender__id'],
                        "username": vote['sender__username'],
                        "points": vote['sent_count'] * self.POINTS_FOR_SENDING
                     } for vote in sent_votes}
        received_votes = {vote['recipient__id']:{
                  "user_id": vote['recipient__id'],
                  "username": vote['recipient__username'],
                  "points": vote['received_count'] * self.POINTS_FOR_RECEIVING
              } for vote in received_votes}

        # Merge the two dicts, summing the points
        for recipient_id, vote in received_votes.iteritems():
            if recipient_id in votes:
                votes[recipient_id]['points'] += vote['points']
            else:
                votes[recipient_id] = vote

        leaderboard = sorted(votes.values(), key=itemgetter("points"),
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
