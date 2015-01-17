# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import main.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('acceptedbycoachteam', models.BooleanField(default=False)),
                ('acceptedbyplayer', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerTournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acceptedbymanager', models.BooleanField(default=False)),
                ('acceptedbycoach', models.BooleanField(default=False)),
                ('player_id', models.ForeignKey(to='main.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('coach', models.ForeignKey(to='main.Coach', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('start', models.DateField()),
                ('end', models.DateField()),
                ('type', models.CharField(default=None, max_length=3, null=True, choices=[(b'KYO', b'kyokushin'), (b'SHO', b'shotokan')])),
                ('file', models.FileField(upload_to=main.models.file, verbose_name=b'Nazwa pliku', blank=True)),
                ('description', models.TextField(max_length=500)),
                ('coaches', models.ManyToManyField(to='main.Coach', verbose_name=b'Lista trenerow', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('name', models.CharField(max_length=32)),
                ('surname', models.CharField(max_length=32)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tournament',
            name='username',
            field=models.ForeignKey(to='main.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='playertournament',
            name='tournament_id',
            field=models.ForeignKey(to='main.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='team_id',
            field=models.ForeignKey(to='main.Team', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='player',
            name='user_id',
            field=models.ForeignKey(to='main.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='manager',
            name='tournament',
            field=models.ForeignKey(to='main.Tournament'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='manager',
            name='user_id',
            field=models.ForeignKey(to='main.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='coach',
            name='user_id',
            field=models.ForeignKey(to='main.User', null=True),
            preserve_default=True,
        ),
    ]
