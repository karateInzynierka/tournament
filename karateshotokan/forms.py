# -*- coding: utf-8 -*-

from django import forms
from django.forms.models import ModelForm

from main.models import Tournament, Team
from karateshotokan.models import ShotokanCategory


class ShotokanTournamentsForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'type', )


class ShotokanCategoryCreateForm(ModelForm):
    class Meta:
        model = ShotokanCategory
        fields = ('name', 'type_age', 'type_fight', 'sex', 'weight', )


# Tworzenie zawodnika
class ShotokanPlayerCreateForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "title": u"Imię",
            }
        )
    )
    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "title": u"Nazwisko",
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super(ShotokanPlayerCreateForm, self).__init__(*args, **kwargs)

        self.fields["teams"] = forms.ModelChoiceField(
            Team.objects.all(),
            required=True
        )