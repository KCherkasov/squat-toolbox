# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form


class DivinationForm(Form):
    def __init__(self, flyweights, cd, background, *args, **kwargs):
        super(DivinationForm, self).__init__(*args, **kwargs)
        if cd.bg_skill_1 is not None:
            if cd.bg_skill_1_subtag == 'SK_ANY':
                skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_1])
                field_name = 'subtag_' + skill.get_tag()
                self.fields[field_name] = forms.CharField(label=skill.get_name_en(), max_length=30)
                self.fields[field_name].required = True
            if (cd.bg_skill_2 is not None) and (cd.bg_skill_2_subtag == 'SK_ANY'):
                skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_2])
                field_name = 'subtag_' + skill.get_tag()
                self.fields[field_name] = forms.CharField(label=skill.get_name_en(), max_length=30)
                self.fields[field_name].required = True

    divination_roll = forms.IntegerField(label=u'Прорицание (от 1 до 100)', min_value=1, max_value=100)
    wound_roll = forms.IntegerField(label=u'Раны (от 1 до 5)', min_value=1, max_value=5)
    fate_roll = forms.IntegerField(label=u'Благословение Императора (от 1 до 10)', min_value=1, max_value=10)
