# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myrobot', '0004_auto_20160424_0609'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Films',
        ),
    ]
