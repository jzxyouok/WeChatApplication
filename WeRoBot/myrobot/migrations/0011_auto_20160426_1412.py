# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0010_auto_20160426_1401'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmsearch',
            name='_120',
        ),
        migrations.RemoveField(
            model_name='filmsearch',
            name='_35mm',
        ),
    ]
