# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FightersPair',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('winner', models.IntegerField(default=None, unique=True)),
                ('name', models.ForeignKey(to='main.PlayerTournament')),
                ('tournament_id', models.ForeignKey(to='main.Tournament', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShotokanCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('weight', models.CharField(blank=True, max_length=50, choices=[(b'-60 kg', b'-60 kg'), (b'-67 kg', b'-67 kg'), (b'-75 kg', b'-75 kg'), (b'-84 kg', b'-84 kg'), (b'+84 kg', b'+84 kg'), (b'-55 kg', b'-55 kg'), (b'-61 kg', b'-61 kg'), (b'-68 kg', b'-68 kg'), (b'+68 kg', b'+68 kg')])),
                ('type', models.CharField(default=None, max_length=16, choices=[(b'KATA', b'KATA'), (b'KUMITE', b'KUMITE')])),
                ('sex', models.CharField(default=None, max_length=16, choices=[(b'MALE', b'Male'), (b'FEMALE', b'Female')])),
                ('playerT_id', models.ManyToManyField(to='main.PlayerTournament', blank=True)),
                ('tournament_id', models.ForeignKey(to='main.Tournament', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ShotokanPlayersCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('type', models.CharField(default=None, max_length=16, choices=[(b'MLODZIK', b'MLODZIK'), (b'JUNIOR MLODSZY', b'JUNIOR MLODSZY'), (b'JUNIOR', b'JUNIOR'), (b'SENIOR', b'SENIOR')])),
                ('team', models.ManyToManyField(to='main.Team', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
