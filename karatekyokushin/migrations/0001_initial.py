# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(default=None, max_length=3, choices=[(b'KT', b'kata'), (b'KM', b'kumite')])),
                ('playerT_id', models.ManyToManyField(to='main.PlayerTournament', blank=True)),
                ('tournament_id', models.ForeignKey(to='main.Tournament', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('winner', models.IntegerField(null=True)),
                ('reason', models.CharField(default=b'arbiters', max_length=5, choices=[(b'knock', b'knockout'), (b'walko', b'walkover'), (b'arbit', b'arbiters'), (b'wazar', b'wazari')])),
                ('arbitersfor', models.IntegerField(null=True)),
                ('arbitersagainst', models.IntegerField(null=True)),
                ('arbitersdraw', models.IntegerField(null=True)),
                ('round', models.IntegerField()),
                ('category_id', models.ForeignKey(to='karatekyokushin.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FirstPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='main.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SecondPlayer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('player', models.ForeignKey(to='main.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fight',
            name='firstplayer',
            field=models.ForeignKey(to='karatekyokushin.FirstPlayer'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fight',
            name='secondplayer',
            field=models.ForeignKey(to='karatekyokushin.SecondPlayer', null=True),
            preserve_default=True,
        ),
    ]
