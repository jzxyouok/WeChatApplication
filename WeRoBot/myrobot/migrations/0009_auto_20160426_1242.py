# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0008_auto_20160426_1239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmsearch',
            name='a120',
        ),
        migrations.RemoveField(
            model_name='filmsearch',
            name='a35mm',
        ),
    ]
