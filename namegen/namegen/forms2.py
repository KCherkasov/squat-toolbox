# -*- coding: utf-8 -*-

from django import forms


class Constants:
    SCAND = 'SC'
    LATIN = 'LAT'
    SPAIN = 'SP'
    ITALY = 'IT'
    POLAND = 'PL'

    MALE = 'M'
    FEMALE = 'F'
    RANDOM = 'R'

    NOBLE = 'N'
    SIMPLE = 'S'


class NamegenForm(forms.Form):
    LANGS = (['SC', u'Скандинавия'], ['LAT', u'Латынь'], ['SP', u'Испания'], ['IT', u'Италия'], ['PL', u'Польша'],
             ['R', u'Микс'],)

    GENDERS = (['M', u'Мужской'], ['F', u'Женский'], ['R', u'Случайно'],)

    NOBILITY = (['N', u'Благородный'], ['S', u'Простолюдин'], ['R', u'Случайно'],)

    lang = forms.ChoiceField(label=u'Языковая группа', required=True, choices=LANGS, initial=Constants.RANDOM)
    gender = forms.ChoiceField(label=u'Пол', required=True, choices=GENDERS, initial=Constants.RANDOM)
    nobility = forms.ChoiceField(label=u'Благородный', required=True, choices=NOBILITY, initial=Constants.RANDOM)
    count = forms.IntegerField(localize=False, min_value=1, max_value=100000, required=True, initial=1,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': u'Количество имен', }),
                               label=u'Количество генерируемых имен')
