from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Generates authentication tokens for Django REST Framework.'

    def handle(self, *args, **options):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
