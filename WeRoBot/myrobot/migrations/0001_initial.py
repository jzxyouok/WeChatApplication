# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FilmSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Film', models.CharField(max_length=100, verbose_name=b'Film')),
                ('Developer', models.CharField(max_length=100, verbose_name=b'Film')),
                ('Dilution', models.CharField(max_length=100, verbose_name=b'Dilution')),
                ('ASA_ISO', models.CharField(max_length=100, verbose_name=b'ASA/ISO')),
                ('_35mm', models.CharField(max_length=100, verbose_name=b'35mm', blank=True)),
                ('_120', models.CharField(max_length=100, verbose_name=b'120', blank=True)),
                ('Sheet', models.CharField(max_length=100, verbose_name=b'Sheet', blank=True)),
                ('Temp', models.CharField(max_length=100, verbose_name=b'Temp', blank=True)),
                ('Notes', models.CharField(max_length=100, verbose_name=b'Notes')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Massive Dev Chart',
                'verbose_name_plural': 'Massive Dev Chart',
            },
        ),
    ]
