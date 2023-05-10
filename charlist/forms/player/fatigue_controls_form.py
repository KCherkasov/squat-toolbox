from django import forms
from django.forms import Form


class FatigueControlsForm(Form):
    amount = forms.IntegerField(min_value=1, max_value=20)
