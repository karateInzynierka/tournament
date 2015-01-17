# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karateshotokan', '0003_round'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='who_win',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Wygrany', choices=[(1, b'AKA'), (2, b'AO')]),
            preserve_default=True,
        ),
    ]
