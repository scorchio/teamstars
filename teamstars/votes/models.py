from django.db import models
from django.contrib.auth.models import User

from model_utils.models import TimeStampedModel


class VoteType(TimeStampedModel):
    type = models.CharField(max_length=255)


class Vote(TimeStampedModel):
    type = models.ForeignKey(VoteType, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_user")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipient_user")
    title = models.CharField(max_length=255)
    description = models.TextField()
