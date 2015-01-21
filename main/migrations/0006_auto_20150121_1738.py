# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_player_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='description',
            field=models.TextField(max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='end',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tournament',
            name='start',
            field=models.DateTimeField(),
            preserve_default=True,
        ),
    ]
