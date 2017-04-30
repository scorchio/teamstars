from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

from rest_framework.authtoken.models import Token


class GenerateAuthTokensTestCase(TestCase):
    def test_generate(self):
        User.objects.create_user(username="user1")
        User.objects.create_user(username="user2")
        Token.objects.all().delete()
        call_command('generate_auth_tokens')
        self.assertEquals(2, Token.objects.count())
