# -*- coding: utf-8 -*-


from django.forms import Form
from django import forms

from charlist.constants.tags import *


class StatDistributionForm(Form):
    ws_value = forms.IntegerField(verbose_name=u'Weapon Skill', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    bs_value = forms.IntegerField(verbose_name=u'Ballistic Skill', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    str_value = forms.IntegerField(verbose_name=u'Strength', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    t_value = forms.IntegerField(verbose_name=u'Toughness', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    ag_value = forms.IntegerField(verbose_name=u'Agility', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    per_value = forms.IntegerField(verbose_name=u'Perception', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    int_value = forms.IntegerField(verbose_name=u'Intelligence', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    wp_value = forms.IntegerField(verbose_name=u'Willpower', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    fel_value = forms.IntegerField(verbose_name=u'Fellowship', min_value=2, max_value=20, placeholder=u'от 2 до 20')
    ifl_value = forms.IntegerField(verbose_name=u'Influence', min_value=2, max_value=20, placeholder=u'от 2 до 20')

    def get_field(self, stat: str):
        field = None
        if stat in STAT_TAGS:
            if stat == ST_WEAPON_SKILL:
                field = self.ws_value
            if stat == ST_BALLISTIC_SKILL:
                field = self.bs_value
            if stat == ST_STRENGTH:
                field = self.str_value
            if stat == ST_TOUGHNESS:
                field = self.t_value
            if stat == ST_AGILITY:
                field = self.ag_value
            if stat == ST_PERCEPTION:
                field = self.per_value
            if stat == ST_INTELLIGENCE:
                field = self.int_value
            if stat == ST_WILLPOWER:
                field = self.wp_value
            if stat == ST_FELLOWSHIP:
                field = self.fel_value
            if stat == ST_INFLUENCE:
                field = self.ifl_value
        return field
