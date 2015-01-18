# -*- coding: utf-8 -*-

import os

from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.conf import settings


class User(models.Model):
    user = models.ForeignKey(DjangoUser, blank=True, null=True)
    email = models.EmailField(unique=True)
    # password = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name + " " + self.surname

class Coach(models.Model):
    user_id = models.ForeignKey(User, null=True)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name + " " + self.surname

class Team(models.Model):
    name = models.CharField(max_length=32)
    coach = models.ForeignKey(Coach, null=True)

    def __unicode__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    team_id = models.ForeignKey(Team, null=True)
    acceptedbycoachteam = models.BooleanField(default=False)
    acceptedbyplayer = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.name + " " + self.surname)

def file(self, filename):
    url = "users/%s %s/%s" % (self.username.name, self.username.surname, filename)
    return url

class Tournament(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateField(null=True, blank=True)
    end = models.DateField(null=True, blank=True)
    username = models.ForeignKey(User, null=True)

    KYOKUSHIN = 'KYO'
    SHOTOKAN = 'SHO'
    TYPE_CHOICES = (
        (KYOKUSHIN, 'kyokushin'),
        (SHOTOKAN, 'shotokan')
    )
    type = models.CharField(max_length=3,
                            choices=TYPE_CHOICES,
                            default=None,
                            null=True)
    coaches = models.ManyToManyField(Coach, verbose_name="Lista trenerow", blank=True)
    file = models.FileField(upload_to=file, verbose_name="Nazwa pliku", blank=True)
    description = models.TextField(max_length=500)

    @property
    def relative_path(self):
        return os.path.relpath(self.path, settings.MEDIA_ROOT)

    def __unicode__(self):
        return unicode(self.name + " " + self.start.strftime('%Y-%m-%d') + " " + self.end.strftime('%Y-%m-%d'))


class PlayerTournament(models.Model):
    player_id = models.ForeignKey(Player)
    tournament_id = models.ForeignKey(Tournament) 
    acceptedbymanager = models.BooleanField(default=False)
    acceptedbycoach = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.player_id)

    def return_full_name(self):
        return u"%s %s" % (
            self.player_id.name.replace(u'Ł', 'L').replace(u'ł', 'l'),
            self.player_id.surname.replace(u'Ł', 'L').replace(u'ł', 'l')
        )


class Manager(models.Model):
    user_id = models.ForeignKey(User)
    tournament = models.ForeignKey(Tournament)