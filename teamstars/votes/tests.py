from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from models import VoteType, Vote
from django.contrib.auth.models import User


class VoteTestCase(TestCase):
    """Test case for checking the voting mechanism"""

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
        vote_type_1 = VoteType.objects.create(type="+", sender_points=2,
                                              recipient_points=10)
        vote_type_2 = VoteType.objects.create(type="-", sender_points=-10,
                                              recipient_points=-5)
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
        VoteType.objects.create(type="+", sender_points=2, recipient_points=10)

        with self.assertRaises(ObjectDoesNotExist,
                               msg="Did not raise exception as expected"):
            VoteType.objects.get(type="-")

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

    def test_vote_creation_same_user(self):
        user1 = User.objects.create_user(username="user1")
        vote_type = VoteType.objects.create(type="+", sender_points=2,
                                            recipient_points=10)

        with self.assertRaises(ValidationError,
                               msg="A self-vote did not raise exception as "
                                   "expected"):
            vote = Vote(sender=user1, recipient=user1,
                        type=vote_type,
                        title=self.TEST_TITLE,
                        description=self.TEST_DESCRIPTION)
            vote.clean()

    def test_leaderboard(self):
        """Asking for a leaderboard after a vote should return the correct
        results"""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        vote_type = VoteType.objects.create(type="+", sender_points=2,
                                            recipient_points=10)

        Vote.objects.create(sender=user1, recipient=user2,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        leaderboard = Vote.objects.leaderboard()
        self.assertTrue(type(leaderboard) is list,
                        "Vote.leaderboard() should return a list")
        self.assertListEqual(leaderboard,
                             [{"user_id": user2.id, "username":
                                 user2.username, "points": 10},
                              {"user_id": user1.id, "username":
                                  user1.username, "points": 2}],
                             "The points are not calculated correctly after "
                             "the first vote")

        Vote.objects.create(sender=user1, recipient=user2,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        leaderboard = Vote.objects.leaderboard()
        self.assertListEqual(leaderboard,
                             [{"user_id": user2.id, "username":
                                 user2.username, "points": 20},
                              {"user_id": user1.id, "username":
                                  user1.username, "points": 4}],
                             "The points are not calculated correctly after "
                             "the second vote")

        Vote.objects.create(sender=user2, recipient=user1,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        leaderboard = Vote.objects.leaderboard()
        self.assertListEqual(
            [{"user_id": user2.id, "username": user2.username, "points": 22},
             {"user_id": user1.id, "username": user1.username, "points": 14}],
            leaderboard,
            "The points are not calculated correctly after the third "
            "(reverse) vote")

    def test_leaderboard_multitype(self):
        """Asking for the leaderboard should return the correct results even
        when multiple vote types are used."""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        normal_vote_type = VoteType.objects.create(type="+", sender_points=2,
                                                   recipient_points=10)
        huge_vote_type = VoteType.objects.create(type="+", sender_points=2,
                                                 recipient_points=333)
        Vote.objects.create(sender=user1, recipient=user2,
                            type=normal_vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        Vote.objects.create(sender=user1, recipient=user2,
                            type=normal_vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        Vote.objects.create(sender=user2, recipient=user1,
                            type=huge_vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        leaderboard = Vote.objects.leaderboard()
        self.assertListEqual([{"user_id": user1.id, "username":
                              user1.username, "points": 337},
                              {"user_id": user2.id, "username":
                                  user2.username, "points": 22}], leaderboard,
                             "The points are not calculated correctly for "
                             "multiple vote types.")

    def test_vote_statistics(self):
        """Asking for the vote statistics should return the correct results"""
        user1 = User.objects.create_user(username="user1")
        user2 = User.objects.create_user(username="user2")
        vote_type = VoteType.objects.create(type="+", sender_points=2,
                                            recipient_points=10)

        Vote.objects.create(sender=user1, recipient=user2,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        Vote.objects.create(sender=user1, recipient=user2,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        Vote.objects.create(sender=user2, recipient=user1,
                            type=vote_type,
                            title=self.TEST_TITLE,
                            description=self.TEST_DESCRIPTION)
        stats = Vote.objects.vote_statistics()
        self.assertDictEqual({
                'received': {
                    vote_type.id: [
                        {
                            'user_id': user1.id,
                            'username': user1.username,
                            'count': 1,
                        },
                        {
                            'user_id': user2.id,
                            'username': user2.username,
                            'count': 2,
                        }
                    ]
                },
                'sent': {
                    vote_type.id: [
                        {
                            'user_id': user1.id,
                            'username': user1.username,
                            'count': 2,
                        },
                        {
                            'user_id': user2.id,
                            'username': user2.username,
                            'count': 1,
                        }
                    ]
                }
            },
            stats,
            "The points are not calculated correctly after the third "
            "(reverse) vote")
