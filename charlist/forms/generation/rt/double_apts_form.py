# -*- coding: utf-8 -*-

from typing import Dict, List

from django import forms
from django.forms import Form
from django.forms import ValidationError

from charlist.constants.tags import *
from charlist.flyweights.rt_flyweights import RTFacade
from charlist.character.rt_creation_data import RTCreationDataModel


class DoubleAptsForm(Form):
    def __init__(self, cd: RTCreationDataModel, flyweights: RTFacade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = list()
        for apt in cd.simplify_apts():
            self.current_apts = flyweights.aptitudes().get(apt).get_name('en')
        for apt in STAT_APTS:
            if apt not in cd.aptitudes:
                choices.append((apt, flyweights.aptitudes().get(apt).get_name('en')))
        for i in range(cd.count_doubles()):
            label = str('Choose doubled aptitude ').join(str(i + 1))
            name = str('apt-').join(str(i + 1))
            self.fields[name] = forms.ChoiceField(label=label)

    def clean(self):
        cd = self.cleaned_data
        for key_i, apt_i in cd.items():
            for key_j, apt_j in cd.items():
                if (key_j != key_i) and (apt_i == apt_j):
                    raise ValidationError('Aptitudes shall be different!')
        return cd
