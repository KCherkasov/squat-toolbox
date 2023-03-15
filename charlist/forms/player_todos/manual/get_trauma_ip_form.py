from django import forms
from django.forms import Form


class GetTraumaIPForm(Form):
    roll_result = forms.IntegerField(min_value=1, max_value=210, required=False,
                                     label=u'Результат броска на психическую травму')
