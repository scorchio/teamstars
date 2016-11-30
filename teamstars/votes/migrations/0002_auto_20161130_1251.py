# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='votetype',
            name='type',
            field=models.CharField(max_length=255),
            preserve_default=True,
        ),
    ]
