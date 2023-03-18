# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

from charlist.constants import tags


class DoubleAptsChoiceForm(Form):
    def __init__(self, doubled, apts, flyweights, *args, **kwargs):
        super(DoubleAptsChoiceForm, self).__init__(*args, **kwargs)
        self.__doubled = doubled
        choices = []
        for st_apt in tags.STAT_APTS:
            if st_apt not in apts:
                choices.append((st_apt, flyweights.aptitudes().get(st_apt).get_name_en()))
            if doubled > 0:
                self.fields['apt_choice'].choices = choices
                if doubled > 1:
                    self.fields['apt_choice2'].choice = choices
                else:
                    self.fields['apt_choice2'].required = False
                    self.fields['apt_choice2'].widget = forms.Select(
                        {'class': 'form-control disabled'}, choices)
            else:
                self.fields['apt_choice'].required = False
                self.fields['apt_choice'].widget = forms.Select(
                    {'class': 'form-control disabled'}, choices)
                self.fields['apt_choice2'].required = False
                self.fields['apt_choice2'].widget = forms.Select(
                    {'class': 'form-control disabled'}, choices)

    apt_choice = forms.ChoiceField(label=u'Первая склонность')
    apt_choice2 = forms.ChoiceField(label=u'Вторая склонность')

    def is_valid(self):
        if self.__doubled > 1:
            return super().is_valid() and (self.apt_choice != self.apt_choice2)
        else:
            return self.apt_choice is not None
