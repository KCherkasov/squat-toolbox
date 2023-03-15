from django import forms
from django.forms import Form


class GainInsanityRollForm(Form):
    roll_value = forms.IntegerField(min_value=1, max_value=100, label=u'Очки Безумия')
