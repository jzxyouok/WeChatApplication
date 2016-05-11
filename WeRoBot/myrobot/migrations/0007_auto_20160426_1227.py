# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0006_films'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmsearch',
            name='Sheet',
            field=models.CharField(max_length=100, verbose_name=b'Sheet'),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='Temp',
            field=models.CharField(max_length=100, verbose_name=b'Temp'),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='_120',
            field=models.CharField(max_length=100, verbose_name=b'120'),
        ),
        migrations.AlterField(
            model_name='filmsearch',
            name='_35mm',
            field=models.CharField(max_length=100, verbose_name=b'35mm'),
        ),
        migrations.AlterField(
            model_name='notes',
            name='Remark',
            field=models.CharField(max_length=200, verbose_name=b'Remark'),
        ),
    ]
