from django import forms
from django.forms import Form


class WoundControlsForm(Form):
    amount = forms.IntegerField(min_value=1, max_value=50)
