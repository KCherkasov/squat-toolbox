# -*- coding: utf-8 -*-

from django.forms import Form
from django import forms


STAT_BASE_CHOICES = (['CS_20', 20], ['CS_25', 25])


class CreationSettingsForm(Form):
    starting_xp = forms.IntegerField(verbose_name=u'Стартовые Очки опыта', min_value=0)
    characteristics_base = forms.ChoiceField(verbose_name=u'Базовое значение характеристик',
                                             choices=STAT_BASE_CHOICES)
