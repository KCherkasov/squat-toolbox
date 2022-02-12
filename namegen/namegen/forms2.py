# -*- coding: utf-8 -*-

from django import forms


class NamegenForm(forms.Form):
    SCAND = 'SC'

    MALE = 'M'
    FEMALE = 'F'
    RANDOM = 'R'

    LANGS = (['SC', u'Скандинавия'],)

    GENDERS = (['M', u'Мужской'], ['F', u'Женский'], ['R', u'Случайно'],)

    lang = forms.ChoiceField(label=u'Языковая группа', required=True, choices=LANGS, initial=SCAND)
    gender = forms.ChoiceField(label=u'Пол', required=True, choices=GENDERS, initial=RANDOM)
    count = forms.IntegerField(localize=False, min_value=1, max_value=100000, required=True, initial=1,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': u'Количество имен', }),
                               label=u'Количество генерируемых имен')
