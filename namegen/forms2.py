# -*- coding: utf-8 -*-

from django import forms


class Constants:
    SCAND = 'AU'
    LATIN = 'HG'
    SPAIN = 'IB'
    ITALY = 'AP'
    POLAND = 'PO'
    JAPAN = 'NI'
    ROMANIA = 'SY'
    HUNGARY = 'MA'
    TECH = 'TC'
    CHINA = 'CE'
    GERMANY = 'TE'
    FRANCE = 'BR'

    MALE = 'M'
    FEMALE = 'F'

    NOBLE = 'N'
    SIMPLE = 'S'

    RANDOM = 'R'


class NamegenForm(forms.Form):
    LANGS = ([Constants.SCAND, u'Готик Аурорика'], [Constants.LATIN, u'Высокий готик'],
             [Constants.SPAIN, u'Готик Иберика'], [Constants.ITALY, u'Готик Аппенин'],
             [Constants.POLAND, u'Готик Полоника'], [Constants.JAPAN, u'Готик Ниппон'],
             [Constants.ROMANIA, u'Готик Сильваника'], [Constants.HUNGARY, u'Готик Магьярика'],
             [Constants.CHINA, u'Готик Церес'], [Constants.GERMANY, u'Готик Тевтоника'],
             [Constants.TECH, u'Лингва бинарика'], [Constants.FRANCE, u'Готик Бретоника'],
             [Constants.RANDOM, u'Nomen mixta'],)

    GENDERS = ([Constants.MALE, u'Мужской'], [Constants.FEMALE, u'Женский'], [Constants.RANDOM, u'Случайно'],)

    NOBILITY = ([Constants.NOBLE, u'Благородный'], [Constants.SIMPLE, u'Простолюдин'], [Constants.RANDOM, u'Случайно'],)

    lang = forms.ChoiceField(label=u'Языковая группа', required=True, choices=LANGS, initial=Constants.RANDOM)
    gender = forms.ChoiceField(label=u'Пол', required=True, choices=GENDERS, initial=Constants.RANDOM)
    nobility = forms.ChoiceField(label=u'Благородный', required=True, choices=NOBILITY, initial=Constants.RANDOM)
    count = forms.IntegerField(localize=False, min_value=1, max_value=100000, required=True, initial=1,
                               widget=forms.NumberInput(attrs={'class': 'form-control',
                                                               'placeholder': u'Количество имен', }),
                               label=u'Количество генерируемых имен')
