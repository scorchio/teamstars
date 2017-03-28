# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendstar', '0002_calendareventresponse'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='calendareventresponse',
            unique_together=set([('user', 'calendar_event')]),
        ),
    ]
