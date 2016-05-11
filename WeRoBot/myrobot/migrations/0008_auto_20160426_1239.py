# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0007_auto_20160426_1227'),
    ]

    operations = [
        migrations.AddField(
            model_name='filmsearch',
            name='a120',
            field=models.CharField(default=datetime.datetime(2016, 4, 26, 12, 39, 47, 167520, tzinfo=utc), max_length=100, verbose_name=b'a120'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='filmsearch',
            name='a35mm',
            field=models.CharField(default=datetime.datetime(2016, 4, 26, 12, 39, 59, 14676, tzinfo=utc), max_length=100, verbose_name=b'a35mm'),
            preserve_default=False,
        ),
    ]
