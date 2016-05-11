# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0002_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='Notes',
            field=models.CharField(default=datetime.datetime(2016, 4, 23, 17, 55, 55, 669074, tzinfo=utc), max_length=100, verbose_name=b'Notes'),
            preserve_default=False,
        ),
    ]
