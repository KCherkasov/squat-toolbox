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
    def __init__(self, facade: RTFacade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__facade = facade

    def parse(self, cd: RTCreationDataModel):
        hw = self.__facade.rt_homeworlds().get(cd.hw_id)
        birthright = self.__facade.birthrights().get(cd.birthright_id)
        lure = self.__facade.lures().get(cd.lure_id)
        trial = self.__facade.trials().get(cd.trial_id)
        motive = self.__facade.motivations().get(cd.motivation_id)
        career = self.__facade.careers().get(cd.career_id)
        i = 0
        for grp in hw.get_skill_choices():
            i = self.parse_group(grp, i, 'Homeworld skill')
        for grp in hw.get_talent_choices():
            i = self.parse_group(grp, i, 'Homeworld talent')
        for grp in birthright.choices():
            i = self.parse_group(grp, i, "Birthright")
        birthright_apts = list()
        for apt in birthright.aptitude_choices():
            birthright_apts.append({'tag': apt})
        i = self.parse_group(birthright_apts, i, 'Birthright aptitude')
        for grp in lure.choices():
            i = self.parse_group(grp, i, 'Lure of the Void')
        for grp in trial.choices():
            i = self.parse_group(grp, i, 'Trial and Travail')
        for grp in motive.choices():
            i = self.parse_group(grp, i, 'Motivation')
        motivation_apts = list()
        for apt in motive.aptitudes():
            motivation_apts.append({'tag': apt})
        i = self.parse_group(motivation_apts, i, 'Motivation aptitude')
        for grp in career.choices():
            i = self.parse_group(grp, i, 'Career')

    def parse_group(self, grp: List, i: int, prefix: str):
        j = i + 1
        choices = list()
        subtagged = False
        for choice in grp:
            name = parse_choice(choice, self.__facade)
            choices.append((json.dumps(choice), name))
            if ('subtag' in choice.keys()) and (not subtagged):
                if (choice.get('subtag') == 'SK_ANY') or (choice.get('subtag') == 'TL_ANY'):
                    subtagged = True
        fld_name = 'choice-' + str(i)
        label = str(prefix) + ' choice ' + str(j)
        self.fields[fld_name] = forms.ChoiceField(label=label)
        self.fields[fld_name].choices = choices
        if subtagged:
            stg_name = str(STG_PREFIX) + fld_name
            stg_label = 'Specialization:'
            self.fields[stg_name] = forms.CharField(label=stg_label, required=False)
        i += 1
        return i

    def clean(self):
        cd = self.cleaned_data
        for field_name, value in cd.items():
            if field_name[:len(STG_PREFIX)] == STG_PREFIX:
                stripped_name = field_name[len(STG_PREFIX):]
                if stripped_name in cd.keys():
                    tag = json.loads(cd.get(stripped_name)).get('tag')
                    if (value is not None) and (value != ''):
                        if tag[:2] == 'SK':
                            if not self.__facade.skill_descriptions().get(tag).is_specialist():
                                raise ValidationError('Specialization for non-specialist skill'
                                                      + self.__facade.skill_descriptions().get(tag).get_name('en'))
                        if tag[:2] == 'TL':
                            if not self.__facade.talent_descriptions().get(tag).is_specialist():
                                raise ValidationError('Specialization for non-specialist talent'
                                                      + self.__facade.talent_descriptions().get(tag).get_name('en'))
                else:
                    err = 'Wrong-spawned text field: ' + field_name + ' has no '\
                          + stripped_name + ' match in form fields'
                    raise ValidationError(err)
        return cd


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
