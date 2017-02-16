from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import connections


class Command(BaseCommand):
    help = 'Imports the entities from the legacy Drupal database.'

    def handle(self, *args, **options):
        with connections['legacy'].cursor() as cursor:
            cursor.execute("select u.name, u.mail, u.created, "
                           "fn.field_user_full_name_value as fullname "
                           "from users u left join field_data_field_user_full_name fn "
                           "on u.uid = fn.entity_id")
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            for user in result:
                self.stdout.write(u'User: {name} ({fullname}) <{mail}> - {created}'.format(
                    mail=user['mail'],
                    created=datetime.utcfromtimestamp(user['created']),
                    name=user['name'],
                    fullname=user['fullname']
                ))

        # TODO: upgrade to Django 1.9+ to support styling in management commands
        self.stdout.write('Successfully run command')
