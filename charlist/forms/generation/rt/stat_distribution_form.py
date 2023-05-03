# -*- coding: utf-8 -*-


from django import forms
from django.forms import Form

from charlist.constants.tags import *
from charlist.character.rt_creation_data import RTCreationDataModel
from charlist.flyweights.rt_flyweights import RTFacade


class RTStatDistributionForm(Form):
    def __init__(self, facade: RTFacade, *args, **kwargs):
        super(RTStatDistributionForm, self).__init__(*args, **kwargs)
        for stat in RT_STAT_TAGS:
            self.fields[stat] = forms.IntegerField(
                label=facade.stat_descriptions().get(stat).name().get('en'),
                min_value=2, max_value=20, required=True)
