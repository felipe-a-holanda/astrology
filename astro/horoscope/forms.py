__author__ = 'fholanda'

from django import forms
from .models import Event

class yourForm(forms.ModelForm):
    class Meta:
        model = Event
        widgets = {
            #Use localization and bootstrap 3
            'datetime': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True, bootstrap_version=3)
        }

