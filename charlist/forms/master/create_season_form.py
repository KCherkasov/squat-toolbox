from django import forms
from django.forms import Form


class CreateSeasonForm(Form):
    name = forms.CharField(label=u'Название кампании', max_length=100)
    description = forms.CharField(label=u'Краткое описание', max_length=500)
