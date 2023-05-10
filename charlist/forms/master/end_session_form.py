from django import forms
from django.forms import Form


class EndSessionForm(Form):
    xp_amount = forms.IntegerField(min=1, max=10000, label=u'Опыт за сессию')
