# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form


class DivinationForm(Form):
    divination_roll = forms.IntegerField(label=u'Прорицание (от 1 до 100)', min_value=1, max_value=100)
    wound_roll = forms.IntegerField(label=u'Раны (от 1 до 5)', min_value=1, max_value=5)
    fate_roll = forms.IntegerField(label=u'Благословение Императора (от 1 до 10)', min_value=1, max_value=10)
