from django import forms
from django.forms import Form


class WoundControlsForm(Form):
    amount = forms.IntegerField(min=1, max=50)
