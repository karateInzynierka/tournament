# -*- coding: utf-8 -*-
from django.db import models

from main.models import Tournament
from main.models import PlayerTournament
from main.models import Player
from main.models import Team
from main.models import User
from main.models import Coach
from main.models import Manager

class ShotokanPlayersCategory(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

    MLODZIK = 'MLODZIK'
    JUNIOR_MLODSZY = 'JUNIOR MLODSZY'
    JUNIOR = 'JUNIOR'
    SENIOR = 'SENIOR'

    TYPE_CHOICES = (
        (MLODZIK, 'MLODZIK'),
        (JUNIOR_MLODSZY, 'JUNIOR MLODSZY'),
        (JUNIOR, 'JUNIOR'),
        (SENIOR, 'SENIOR')
    )
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=None)
    team = models.ManyToManyField(Team, null=True)

    def __unicode__(self):
        return self.name + " " + self.surname

class ShotokanCategory(models.Model):
    name = models.CharField(max_length=50)
    tournament_id = models.ForeignKey(Tournament, null = True)
    playerT_id = models.ManyToManyField(PlayerTournament, blank=True)

    MALE1 = '-60 kg'
    MALE2 = '-67 kg'
    MALE3 = '-75 kg'
    MALE4 = '-84 kg'
    MALE5 = '+84 kg'

    FEMALE1 = '-55 kg'
    FEMALE2 = '-61 kg'
    FEMALE3 = '-68 kg'
    FEMALE4 = '+68 kg'

    WEIGHT_CHOICES = (
        (MALE1, '-60 kg'),
        (MALE2, '-67 kg'),
        (MALE3, '-75 kg'),
        (MALE4, '-84 kg'),
        (MALE5, '+84 kg'),
        (FEMALE1, '-55 kg'),
        (FEMALE2, '-61 kg'),
        (FEMALE3, '-68 kg'),
        (FEMALE4, '+68 kg'),
    )

    KATA = 'KATA'
    KUMITE = 'KUMITE'

    TYPE_FIGHT_CHOICES = (
        (KATA, 'KATA'),
        (KUMITE, 'KUMITE')
    )

    M = 'MALE'
    F = 'FEMALE'

    SEX_CHOICES = (
        (M, 'Male'),
        (F, 'Female')
    )

    MLODZIK = 'MLODZIK'
    JUNIOR_MLODSZY = 'JUNIOR MLODSZY'
    JUNIOR = 'JUNIOR'
    SENIOR = 'SENIOR'

    weight = models.CharField(max_length=50, choices=WEIGHT_CHOICES, blank=True)
    TYPE_AGE_CHOICES = (
        (MLODZIK, 'MLODZIK'),
        (JUNIOR_MLODSZY, 'JUNIOR MLODSZY'),
        (JUNIOR, 'JUNIOR'),
        (SENIOR, 'SENIOR')
    )
    type_age = models.CharField(max_length=16, choices=TYPE_AGE_CHOICES, blank=True, null=True)
    type_fight = models.CharField(max_length=16, choices=TYPE_FIGHT_CHOICES, default=None)
    sex = models.CharField(max_length=16, choices=SEX_CHOICES, default=None)

    def __unicode__(self):
        return self.name


class Round(models.Model):
    category = models.ForeignKey(ShotokanCategory, verbose_name=u'Kategoria')
    number = models.PositiveIntegerField(u'Numer rundy', default=1)
    playerT_first = models.ForeignKey(PlayerTournament, verbose_name=u'AKA', blank=True, null=True, related_name='first_fighter')
    playerT_second = models.ForeignKey(PlayerTournament, verbose_name=u'AO', blank=True, null=True, related_name='second_fighter')
    who_win = models.PositiveIntegerField(u'Wygrany', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.category.name + " " + str(self.number))

    def who_fight(self):
        if self.playerT_first and self.playerT_second:
            return self.playerT_first, self.playerT_second
        elif not self.playerT_first and self.playerT_second:
            return None. self.playerT_second
        elif self.playerT_first and not self.playerT_second:
            return self.playerT_first, None