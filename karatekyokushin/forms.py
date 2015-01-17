from django import forms
from django.forms.models import ModelForm
from main.models import *
from karatekyokushin.models import *
from django.core import validators
from django.utils import dateformat


class KyoCreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields= ('name', 'type',)
     
