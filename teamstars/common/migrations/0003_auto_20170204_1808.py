# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_profile_fb_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.FileField(null=True, upload_to=b''),
        ),
        migrations.AlterField(
            model_name='profile',
            name='fb_link',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
