from django import forms
from django.forms import Form


class EndSessionForm(Form):
    xp_amount = forms.IntegerField(min_value=1, max_value=10000, label=u'Опыт за сессию')
