# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karateshotokan', '0004_auto_20150114_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='who_win',
            field=models.PositiveIntegerField(null=True, verbose_name='Wygrany', blank=True),
            preserve_default=True,
        ),
    ]
