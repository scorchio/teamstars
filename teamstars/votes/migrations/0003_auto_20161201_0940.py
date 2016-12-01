# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0002_auto_20161130_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='votetype',
            name='recipient_points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='votetype',
            name='sender_points',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
