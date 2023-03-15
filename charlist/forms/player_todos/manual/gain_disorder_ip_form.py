from django import forms
from django.forms import Form


class GainDisorderIPForm(Form):
    disorder_description = forms.CharField(max_length=1000, required=False, label=u'Описание психического расстройства')
