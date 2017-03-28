# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('calendstar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CalendarEventResponse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', model_utils.fields.StatusField(default=b'status_yes', max_length=100, verbose_name='status', no_check_for_status=True, choices=[(b'status_yes', 'Yes'), (b'status_rather_yes', 'Likely yes'), (b'status_rather_no', 'Likely no'), (b'status_no', 'No')])),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, verbose_name='status changed', monitor='status')),
                ('comment', models.TextField(max_length=1000)),
                ('calendar_event', models.ForeignKey(to='calendstar.CalendarEvent')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
