from django import forms
from django.forms import Form


class InfluenceControlsForm(Form):
    amount = forms.IntegerField(min_value=1, max_value=100, label=u'Сколько?')
