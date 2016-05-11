# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0009_auto_20160426_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmsearch',
            name='a120',
            field=models.CharField(default=datetime.datetime(2016, 4, 26, 14, 1, 50, 533944, tzinfo=utc), max_length=100, verbose_name=b'a120'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filmsearch',
            name='a35mm',
            field=models.CharField(default=datetime.datetime(2016, 4, 26, 14, 1, 59, 825713, tzinfo=utc), max_length=100, verbose_name=b'a35mm'),
            preserve_default=False,
        ),
    ]
