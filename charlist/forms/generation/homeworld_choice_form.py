# -*- coding: utf-8 -*-

from django.forms import Form
from django import forms

from charlist.constants.tags import *

HOMEWORLDS = ([HOMEWORLD_FERAL, 'Feral world'],   [HOMEWORLD_FORGE, 'Forge world'],   [HOMEWORLD_HIGHBORN, 'Highborn'],
              [HOMEWORLD_HIVE, 'Hive-world'],     [HOMEWORLD_SHRINE, 'Shrine world'], [HOMEWORLD_VOIDBORN, 'Voidborn'],
              [HOMEWORLD_DEATH, 'Death world'],   [HOMEWORLD_GARDEN, 'Garden world'], [HOMEWORLD_STATION,
                                                                                       'Research station'],
              [HOMEWORLD_DAEMON, 'Daemon world'], [HOMEWORLD_PENAL, 'Penal colony'],  [HOMEWORLD_QUARANTINE,
                                                                                       'Quarantine world'],
              [HOMEWORLD_AGRI, 'Agri world'],     [HOMEWORLD_FEUDAL, 'Feudal world'], [HOMEWORLD_FRONTIER,
                                                                                       'Frontier world'])

HOMEWORLDS_LIST = [HOMEWORLD_FERAL, HOMEWORLD_FORGE, HOMEWORLD_HIGHBORN, HOMEWORLD_HIVE,
                   HOMEWORLD_SHRINE, HOMEWORLD_VOIDBORN, HOMEWORLD_DEATH, HOMEWORLD_GARDEN, HOMEWORLD_STATION,
                   HOMEWORLD_DAEMON, HOMEWORLD_PENAL, HOMEWORLD_QUARANTINE, HOMEWORLD_AGRI, HOMEWORLD_FEUDAL,
                   HOMEWORLD_FRONTIER]


class HomeworldsChoiceForm(Form):
    homeworlds = forms.ChoiceField(verbose_name=u'Родной мир', choices=HOMEWORLDS)
