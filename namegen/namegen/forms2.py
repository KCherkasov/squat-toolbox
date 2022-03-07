# -*- coding: utf-8 -*-

from django import forms


class Constants:
    SCAND = 'SC'
    LATIN = 'LAT'
    SPAIN = 'SP'
    ITALY = 'IT'
    POLAND = 'PL'
    JAPAN = 'JP'
    ROMANIA = 'RM'
    HUNGARY = 'HG'
    TECH = 'TC'
    CHINA = 'CH'

    MALE = 'M'
    FEMALE = 'F'

    NOBLE = 'N'
    SIMPLE = 'S'

    RANDOM = 'R'


class NamegenForm(forms.Form):
    LANGS = ([Constants.SCAND, u'Скандинавия'], [Constants.LATIN, u'Латынь'], [Constants.SPAIN, u'Испания'],
             [Constants.ITALY, u'Италия'], [Constants.POLAND, u'Польша'], [Constants.JAPAN, u'Япония'],
             [Constants.ROMANIA, u'Румыния'], [Constants.HUNGARY, u'Венгрия'], [Constants.CHINA, u'Китай'],
             [Constants.TECH, u'Техно'], [Constants.RANDOM, u'Микс'],)

    GENDERS = ([Constants.MALE, u'Мужской'], [Constants.FEMALE, u'Женский'], [Constants.RANDOM, u'Случайно'],)

    NOBILITY = ([Constants.NOBLE, u'Благородный'], [Constants.SIMPLE, u'Простолюдин'], [Constants.RANDOM, u'Случайно'],)

    lang = forms.ChoiceField(label=u'Языковая группа', required=True, choices=LANGS, initial=Constants.RANDOM)
    gender = forms.ChoiceField(label=u'Пол', required=True, choices=GENDERS, initial=Constants.RANDOM)
    nobility = forms.ChoiceField(label=u'Благородный', required=True, choices=NOBILITY, initial=Constants.RANDOM)
    count = forms.IntegerField(localize=False, min_value=1, max_value=100000, required=True, initial=1,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': u'Количество имен', }),
                               label=u'Количество генерируемых имен')
