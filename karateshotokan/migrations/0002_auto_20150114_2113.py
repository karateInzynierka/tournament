# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('karateshotokan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fighterspair',
            name='name',
        ),
        migrations.RemoveField(
            model_name='fighterspair',
            name='tournament_id',
        ),
        migrations.DeleteModel(
            name='FightersPair',
        ),
        migrations.RenameField(
            model_name='shotokancategory',
            old_name='type',
            new_name='type_fight',
        ),
        migrations.AddField(
            model_name='shotokancategory',
            name='type_age',
            field=models.CharField(blank=True, max_length=16, null=True, choices=[(b'MLODZIK', b'MLODZIK'), (b'JUNIOR MLODSZY', b'JUNIOR MLODSZY'), (b'JUNIOR', b'JUNIOR'), (b'SENIOR', b'SENIOR')]),
            preserve_default=True,
        ),
    ]
