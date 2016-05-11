# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0011_auto_20160426_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmsearch',
            name='ASA_ISO',
            field=models.CharField(max_length=100, verbose_name=b'ASA/ISO', db_index=True),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='Developer',
            field=models.CharField(max_length=100, verbose_name=b'Developer', db_index=True),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='Dilution',
            field=models.CharField(max_length=100, verbose_name=b'Dilution', db_index=True),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='Film',
            field=models.CharField(max_length=100, verbose_name=b'Film', db_index=True),
        ),
    ]
