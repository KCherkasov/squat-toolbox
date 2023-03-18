# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form
from django.forms import ValidationError

from charlist.constants import tags


class DoubleAptsChoiceForm(Form):
    def __init__(self, doubled, apts, flyweights, *args, **kwargs):
        super(DoubleAptsChoiceForm, self).__init__(*args, **kwargs)
        self.doubled = doubled
        choices = []
        for st_apt in tags.STAT_APTS:
            if st_apt not in apts:
                choices.append((st_apt, flyweights.aptitudes().get(st_apt).get_name_en()))
            if doubled > 0:
                self.fields['apt_choice'].choices = choices
                if doubled > 1:
                    self.fields['apt_choice2'] = forms.ChoiceField(label=u'Вторая склонность')
                    self.fields['apt_choice2'].choices = choices
            else:
                self.fields['apt_choice'].required = False
                self.fields['apt_choice'].widget = forms.Select(
                    {'class': 'form-control disabled'}, choices)
                self.fields['apt_choice2'].required = False
                self.fields['apt_choice2'].widget = forms.Select(
                    {'class': 'form-control disabled'}, choices)

    apt_choice = forms.ChoiceField(label=u'Первая склонность')
    # apt_choice2 = forms.ChoiceField(label=u'Вторая склонность')

    def clean(self):
        cd = self.cleaned_data
        if cd.get('apt_choice') is None:
            raise ValidationError('select first aptitude')
        if self.doubled > 1:
            if cd.get('apt_choice2') is None:
                raise ValidationError('select second aptitude')
            if (cd.get('apt_choice') == cd.get('apt_choice2')):
                raise ValidationError("aptitudes shall be different!")
        return cd
