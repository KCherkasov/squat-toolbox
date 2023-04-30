# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

from charlist.flyweights.rt_flyweights import RTFacade
from charlist.character.rt_creation_data import RTCreationDataModel


class DivinationForm(Form):
    def __init__(self, flyweights: RTFacade, cd: RTCreationDataModel, *args, **kwargs):
        super(DivinationForm, self).__init__(*args, **kwargs)
        self.default_wounds = flyweights.rt_homeworlds().get(cd.hw_id).get_wounds()
        self.min_blessing = flyweights.rt_homeworlds().get(cd.hw_id).get_blessing()

    divination_roll = forms.IntegerField(label=u'Divination (roll 1d100)', min_value=1, max_value=100)
    wound_roll = forms.IntegerField(label=u'Wounds (roll 1d5)', min_value=1, max_value=5)
    fate_roll = forms.IntegerField(label=u'Emperor\'s blessing (roll 1d10)', min_value=1, max_value=10)