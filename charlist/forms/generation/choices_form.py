# -*- coding: utf-8 -*-

from django.forms import Form
from django import forms

from charlist.constants.tags import *
from charlist.flyweights.flyweights import Facade, Aptitude


class ChoicesForm(Form):
    background_apts = forms.ChoiceField(verbose_name=u'Склонность предыстории')
    role_apts = forms.ChoiceField(verbose_name=u'Склонность роли')
    background_skills = forms.ChoiceField(verbose_name=u'Навык предыстории')
    background_skills2 = forms.ChoiceField(verbose_name=u'Второй навык предыстории')
    background_talents = forms.ChoiceField(verbose_name=u'Талант предыстории')
    role_talent = forms.ChoiceField(verbose_name=u'Талант роли')
    background_traits = forms.ChoiceField(verbose_name=u'Черта предыстории')

