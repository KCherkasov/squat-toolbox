# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

STAT_BASE_CHOICES = ([20, 20], [25, 25])

GENDERS = (['G_MALE', u'Мужской'], ['G_FEMALE', u'Женский'])


class CreationSettingsForm(Form):
    name = forms.CharField(label=u'Имя персонажа', max_length=60)
    starting_xp = forms.IntegerField(label=u'Стартовые Очки опыта', min_value=0)
    characteristics_base = forms.ChoiceField(label=u'Базовое значение характеристик',
                                             choices=STAT_BASE_CHOICES)
