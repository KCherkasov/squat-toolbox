from django import forms
from django.forms import Form


class FatigueControlsForm(Form):
    amount = forms.IntegerField(min=1, max=20)
