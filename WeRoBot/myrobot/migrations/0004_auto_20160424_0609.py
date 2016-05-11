# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0003_notes_notes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Developer', models.CharField(max_length=100, verbose_name=b'Developer')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Developers',
                'verbose_name_plural': 'Developers',
            },
        ),
        migrations.CreateModel(
            name='Films',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Film', models.CharField(max_length=100, verbose_name=b'Film')),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('last_update_timestamp', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Films',
                'verbose_name_plural': 'Films',
            },
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='Developer',
            field=models.CharField(max_length=100, verbose_name=b'Developer'),
        ),
    ]
