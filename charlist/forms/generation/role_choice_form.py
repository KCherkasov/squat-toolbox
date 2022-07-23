# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form

from charlist.constants.tags import *

ROLES = ([ROLE_ASSASSIN, 'Assassin'],     [ROLE_CHIRURGEON, 'Chirurgeon'], [ROLE_DESPERADO, 'Desperado'],
         [ROLE_HIEROPHANT, 'Hierophant'], [ROLE_MYSTIC, 'Mystic'],         [ROLE_SAGE, 'Sage'],
         [ROLE_SEEKER, 'Seeker'],         [ROLE_WARRIOR, 'Warrior'],       [ROLE_CRUSADER, 'Crusader'],
         [ROLE_ACE, 'Ace'],               [ROLE_FANATIC, 'Fanatic'],       [ROLE_PENITENT, 'Penitent'])

ROLES_LIST = [ROLE_ASSASSIN, ROLE_CHIRURGEON, ROLE_DESPERADO, ROLE_HIEROPHANT, ROLE_MYSTIC,  ROLE_SAGE,
              ROLE_SEEKER,   ROLE_WARRIOR,    ROLE_CRUSADER,  ROLE_ACE,        ROLE_FANATIC, ROLE_PENITENT]


class RoleChoiceForm(Form):
    roles = forms.ChoiceField(label=u'Роль')
