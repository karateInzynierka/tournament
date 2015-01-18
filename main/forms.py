from django import forms
from django.forms.models import ModelForm

from main.models import *


class UserFormSignUp(ModelForm):
    class Meta:
        model = User
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }


class UserFormSignIn(ModelForm):
    class Meta:
        model = User
        exclude = ('surname', 'name', 'email')
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }


class CreateTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name',)


class EditTeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ('name',)


class ManageTeamForm(ModelForm):
    class Meta:
        model = Player
        fields = ('name', 'surname', )


class CreateTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'type', 'file', 'description', )
        widgets = {
            'start': forms.DateInput(format=('%m.%d.%Y'), attrs={'class': 'datepicker'}),
            'end': forms.DateInput(format=('%m.%d.%Y'), attrs={'class': 'datepicker'})
        }

class UpdateTournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ('name', 'start', 'end', 'description',)
        widgets = {
            'start': forms.DateInput(format=('%m.%d.%Y'), attrs={'class': 'datepicker'}),
            'end': forms.DateInput(format=('%m.%d.%Y'), attrs={'class': 'datepicker'})
        }


class SelectArtsTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ('type',)


# update profile
class UserFormUpdateProfile(ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname')
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }


def clean_email(self):
    email = self.cleaned_data.get('email')
    password = self.cleaned_data.get('password')

    if email and User.objects.filter(email=email).exclude(password=password).count():
        raise forms.ValidationError('Ten login juz istnieje w bazie!')
    return email


def save(self, commit=True):
    user = super(UserFormSignUp, self).save(commit=False)
    user.email = self.cleaned_data['email']

    if commit:
        user.save()

    return user