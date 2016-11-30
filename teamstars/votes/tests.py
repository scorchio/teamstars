from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from models import VoteType, Vote
from django.contrib.auth.models import User


class VoteTestCase(TestCase):
    TEST_TITLE = "Test title"
    TEST_DESCRIPTION = "Test description"

    def test_user_creation_delete(self):
        """Should be able to create / delete users"""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        self.assertEqual(2, User.objects.count(), "Couldn't create users")
        user1.delete()
        user2.delete()
        self.assertEqual(0, User.objects.count(), "Couldn't delete users")

    def test_vote_type_creation_delete(self):
        """Should be able to create / delete vote types"""
        vote_type_1 = VoteType.objects.create(type="+")
        vote_type_2 = VoteType.objects.create(type="-")
        self.assertEqual(2, VoteType.objects.count(),
                         "Couldn't create vote types")
        vote_type_1.delete()
        vote_type_2.delete()
        self.assertEqual(0, VoteType.objects.count(),
                         "Couldn't delete vote types")

    def test_vote_creation_delete(self):
        """Should be able to create a vote"""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        VoteType.objects.create(type="+")

        with self.assertRaises(ObjectDoesNotExist,
                               msg="Did not raise exception as expected"):
            bogus_vote_type = VoteType.objects.get(type="-")

        working_vote_type = VoteType.objects.get(type="+")

        Vote.objects.create(sender=user1, recipient=user2,
                            type=working_vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        self.assertEqual(1, Vote.objects.count(), "Couldn't create vote")

        vote = Vote.objects.get()
        self.assertEqual(self.TEST_DESCRIPTION, vote.description,
                         "Vote description doesn't match")
        self.assertEqual("user1", vote.sender.username,
                         "Sender username doesn't match")
        self.assertEqual("user2", vote.recipient.username,
                         "Recipient username doesn't match")
