from django import forms
from django.forms import Form


class GainMalignancyRollForm(Form):
    roll_result = forms.IntegerField(min_value=1, max_value=100, required=False,
                                     label=u'Результат броска на малигнацию')
