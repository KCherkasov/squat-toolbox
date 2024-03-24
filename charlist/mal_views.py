# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.template.response import TemplateResponse

import charlist.models as models

from charlist.character.maledictum.mal_character import MalCharacterModel
from charlist.character.maledictum.mal_stat import MalStat
from charlist.character.maledictum.mal_skill import MalSkill
from charlist.character.maledictum.mal_specialization import MalSpecialization
from charlist.constants.constants import *
from charlist.constants.maledictum.constants import *
from charlist.constants.maledictum.tags import *
from charlist.flyweights.mal_flyweights import MalFacade

from random import Random


mal_flyweights = MalFacade()


def mal_character_mock_view(request):
    stats = dict()
    rnd = Random(datetime.datetime.now())
    for stat_id in STAT_TAGS_GEN:
        stats[stat_id] = MalStat(stat_id, IM_BASE_STAT + rnd.random() % IM_D10 + IM_ONE
                                 + rnd.random() % IM_D10 + IM_ONE, IM_ZERO)
    skills = dict()
    character_model = MalCharacterModel(IM_ZERO, "Test Maledictum Character", [100, 0], [3, 3],
                                        [10, 10], stats, skills)
    return TemplateResponse(request, "charsheet.html", {'version': VERSION, 'facade': mal_flyweights,
                                                        'character': character_model,
                                                        })