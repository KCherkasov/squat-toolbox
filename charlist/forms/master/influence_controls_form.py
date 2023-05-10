from django import forms
from django.forms import Form


class InfluenceControlsForm(Form):
    amount = forms.IntegerField(min=1, max=100)
