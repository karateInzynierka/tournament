# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True),
            preserve_default=True,
        ),
    ]
