# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_player_user_id'),
        ('karateshotokan', '0002_auto_20150114_2113'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(default=1, verbose_name='Numer rundy')),
                ('who_win', models.PositiveIntegerField(verbose_name='Wygrany', choices=[(1, b'AKA'), (2, b'AO')])),
                ('category', models.ForeignKey(verbose_name='Kategoria', to='karateshotokan.ShotokanCategory')),
                ('playerT_first', models.ForeignKey(related_name='first_fighter', verbose_name='AKA', blank=True, to='main.PlayerTournament', null=True)),
                ('playerT_second', models.ForeignKey(related_name='second_fighter', verbose_name='AO', blank=True, to='main.PlayerTournament', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
