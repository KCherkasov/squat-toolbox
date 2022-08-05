# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

STAT_BASE_CHOICES = (['CS_20', 20], ['CS_25', 25])

GENDERS = (['G_MALE', u'Мужской'], ['G_FEMALE', u'Женский'])


class CreationSettingsForm(Form):
    name = forms.CharField(label=u'Имя персонажа', max_length=60)
    gender = forms.ChoiceField(label=u'Пол персонажа', choices=GENDERS)
    height = forms.IntegerField(label=u'Рост, см', min_value=110, max_value=250)
    weight = forms.IntegerField(label=u'Вес, кг')
    age = forms.IntegerField(label=u'Возраст, лет', min_value=16)
    starting_xp = forms.IntegerField(label=u'Стартовые Очки опыта', min_value=0)
    characteristics_base = forms.ChoiceField(label=u'Базовое значение характеристик',
                                             choices=STAT_BASE_CHOICES)
