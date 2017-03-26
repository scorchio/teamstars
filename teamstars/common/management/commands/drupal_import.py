from datetime import datetime

from django.core.management.base import BaseCommand
from django.db import connections


class Command(BaseCommand):
    help = 'Imports the entities from the legacy Drupal database.'

    def handle(self, *args, **options):
        with connections['legacy'].cursor() as cursor:
            cursor.execute("select u.uid, u.name, u.mail, u.created, u.status, "
                           "r.name as role, "
                           "fn.field_user_full_name_value as fullname, "
                           "fm.filename as picture "
                           "from users u left join field_data_field_user_full_name fn on u.uid = fn.entity_id "
                           "left join (users_roles ur left join role r on ur.rid=r.rid) on u.uid=ur.uid "
                           "left join file_managed fm on u.picture = fm.fid"
                           )
            columns = [col[0] for col in cursor.description]
            result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            for user in result:
                # Let's ignore Drupal root, as we shouldn't move that user
                if user['uid'] != 0:
                    self.stdout.write(u'User: {name} ({fullname}) <{mail}> - {created} - {role} - {picture} - {status}'.format(
                        mail=user['mail'],
                        created=datetime.utcfromtimestamp(user['created']),
                        name=user['name'],
                        fullname=user['fullname'],
                        role=user['role'],
                        picture=user['picture'],
                        status=user['status']
                    ))

        # TODO: upgrade to Django 1.9+ to support styling in management commands
        self.stdout.write('Successfully run command')
