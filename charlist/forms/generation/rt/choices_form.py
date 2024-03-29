# -*- coding: utf-8 -*-

from typing import Dict, List

from django import forms
from django.forms import Form
from django.forms import ValidationError

import json

from charlist.flyweights.rt_flyweights import RTFacade
from charlist.character.rt_creation_data import RTCreationDataModel

STG_PREFIX = 'subtag-'


class RTChoicesForm(Form):
    def __init__(self, cd: RTCreationDataModel, facade: RTFacade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__facade = facade
        hw = facade.rt_homeworlds().get(cd.hw_id)
        birthright = facade.birthrights().get(cd.birthright_id)
        lure = facade.lures().get(cd.lure_id)
        trial = facade.trials().get(cd.trial_id)
        motive = facade.motivations().get(cd.motivation_id)
        career = facade.careers().get(cd.career_id)
        i = 0
        for grp in hw.get_skill_choices():
            i = parse_group(grp, i, 'Homeworld skill', self.fields, facade)
        for grp in hw.get_talent_choices():
            i = parse_group(grp, i, 'Homeworld talent', self.fields, facade)
        for grp in birthright.choices():
            i = parse_group(grp, i, "Birthright", self.fields, facade)
        birthright_apts = list()
        for apt in birthright.aptitude_choices():
            birthright_apts.append({'tag': apt})
        i = parse_group(birthright_apts, i, 'Birthright aptitude', self.fields, facade)
        for grp in lure.choices():
            i = parse_group(grp, i, 'Lure of the Void', self.fields, facade)
        for grp in trial.choices():
            i = parse_group(grp, i, 'Trial and Travail', self.fields, facade)
        for grp in motive.choices():
            i = parse_group(grp, i, 'Motivation', self.fields, facade)
        motivation_apts = list()
        for apt in motive.aptitudes():
            motivation_apts.append({'tag': apt})
        i = parse_group(motivation_apts, i, 'Motivation aptitude', self.fields, facade)
        for grp in career.choices():
            i = parse_group(grp, i, 'Career', self.fields, facade)


def parse_group(grp: List, i: int, prefix: str, fields, facade: RTFacade):
    j = i + 1
    choices = list()
    subtagged = False
    for choice in grp:
        name = parse_choice(choice, facade)
        choices.append((json.dumps(choice), name))
        if ('subtag' in choice.keys()) and (not subtagged):
            if (choice.get('subtag') == 'SK_ANY') or (choice.get('subtag') == 'TL_ANY'):
                subtagged = True
    fld_name = 'choice-' + str(i)
    label = str(prefix) + ' choice ' + str(j)
    fields[fld_name] = forms.ChoiceField(label=label)
    fields[fld_name].choices = choices
    if subtagged:
        stg_name = str(STG_PREFIX) + fld_name
        stg_label = 'Specialization:'
        fields[stg_name] = forms.CharField(label=stg_label, required=False)
    i += 1
    return i


def parse_choice(choice: Dict, facade: RTFacade):
    name = None
    if choice.get('tag')[:2] == 'A_':
        name = facade.aptitudes().get(choice.get('tag')).get_name('en')
    if choice.get('tag')[:2] == 'SK':
        name = facade.skill_descriptions().get(choice.get('tag')).get_name('en')
    if choice.get('tag')[:2] == 'TL':
        name = facade.talent_descriptions().get(choice.get('tag')).get_name('en')
    if 'subtag' in choice.keys():
        if (choice.get('subtag') == 'SK_ANY') or (choice.get('subtag') == 'TL_ANY'):
            name += '(any)'
        else:
            name += '(' + choice.get('subtag') + ')'
    if choice.get('tag') == 'GainInsanityRoll':
        name = 'Gain insanity (make roll according to the table)'
    if choice.get('tag') == 'GainCorruptionRoll':
        name = 'Gain corruption (make roll according to the table)'
    return name
