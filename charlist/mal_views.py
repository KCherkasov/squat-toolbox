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
    origin_roll = int(rnd.randrange(IM_ONE, IM_D100))
    origin = mal_flyweights.origin_by_roll(origin_roll)
    chosen_stat = int(rnd.randrange(IM_ZERO, len(origin.stat_choice()) - IM_ONE))
    for stat_id in STAT_TAGS_GEN:
        base = IM_BASE_STAT
        if (stat_id == origin.bonus_stat()) or (stat_id == origin.stat_choice()[chosen_stat]):
            base += IM_ORIGIN_STAT_BONUS
        stats[stat_id] = MalStat(stat_id, base + int(rnd.randrange(IM_ONE, IM_D10))
                                 + int(rnd.randrange(IM_ONE, IM_D10)), int(rnd.randrange(IM_ZERO, IM_D10)))
    skills = dict()
    for skill_tag in SKILL_TAGS:
        specs = dict()
        skills[skill_tag] = MalSkill(skill_tag, int(rnd.randrange(IM_ZERO, IM_SKILL_ADV_CAP)), specs)
    for spec_tag, descr in mal_flyweights.specialization_descriptions().items():
        spec = MalSpecialization(spec_tag, int(rnd.randrange(IM_ONE, IM_SKILL_ADV_CAP)))
        if spec.advances() > IM_ZERO:
            skills.get(descr.parent()).gain_specialization(spec)
    wounds = (stats.get(ST_STRENGTH).bonus() + stats.get(ST_TOUGHNESS).bonus()
              + stats.get(ST_TOUGHNESS).bonus() + stats.get(ST_WILLPOWER).bonus())
    character_model = MalCharacterModel(IM_ZERO, "Test Maledictum Character", [100, 0], origin.get_tag(),
                                        [3, 3], wounds, stats, skills)
    return TemplateResponse(request, "charsheet.html", {'version': VERSION, 'facade': mal_flyweights,
                                                        'character': character_model, 'is_test': True,
                                                        })
