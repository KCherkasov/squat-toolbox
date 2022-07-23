# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form


class ChoicesForm(Form):
    background_apts = forms.ChoiceField(label=u'Склонность предыстории')
    role_apts = forms.ChoiceField(label=u'Склонность роли')
    background_skills = forms.ChoiceField(label=u'Навык предыстории')
    background_skills2 = forms.ChoiceField(label=u'Второй навык предыстории')
    background_talents = forms.ChoiceField(label=u'Талант предыстории')
    role_talent = forms.ChoiceField(label=u'Талант роли')
    background_traits = forms.ChoiceField(label=u'Черта предыстории')
