# -*- coding: utf-8 -*-
import logging

from django.shortcuts import render, reverse

from .character import CharacterModel, Stat, Skill, Talent
from .flyweights import *
from .constants import *


resources = ['aptitudes.json', 'stat_descriptions.json', 'skill_descriptions.json', 'talent_descriptions.json',
             'traits.json', 'homeworlds.json', 'backgrounds.json', 'roles.json', 'elite_advances.json',
             'divinations.json', 'psy.json']
flyweights = Facade(resources)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return render(request, 'charlist_test.html', {'version': VERSION, 'facade': flyweights, })


def charsheet_mockup(request):
    return render(request, 'charsheet-mockup.html', {'version': VERSION, })


def interactive_charsheet_mockup(request):
    character = CharacterModel(1, 1, u'Бергрим Коллвирсон', 'HW_FDWL', 'BG_ADMN', 'RL_CRSD', 'D_TNSZ',
                               [], [11, 11], [0, 9], [64, 16950], [3, 3], 13, 14, 0,
                               [A_GENERAL, A_KNOWLEDGE, A_OFFENCE, A_STRENGTH, A_TOUGHNESS,
                                A_WILLPOWER, A_SOCIAL, A_WEAPON_SKILL], {ST_WEAPON_SKILL: Stat(ST_WEAPON_SKILL, 39, 2),
                                                                         ST_INTELLIGENCE: Stat(ST_INTELLIGENCE, 24, 1),
                                                                         ST_BALLISTIC_SKILL: Stat(ST_BALLISTIC_SKILL,
                                                                                                  26),
                                                                         ST_PERCEPTION: Stat(ST_PERCEPTION, 32, 1),
                                                                         ST_STRENGTH: Stat(ST_STRENGTH, 33, 4),
                                                                         ST_WILLPOWER: Stat(ST_WILLPOWER, 29, 5),
                                                                         ST_TOUGHNESS: Stat(ST_TOUGHNESS, 33, 2),
                                                                         ST_FELLOWSHIP: Stat(ST_FELLOWSHIP, 26),
                                                                         ST_AGILITY: Stat(ST_AGILITY, 30),
                                                                         ST_INFLUENCE: Stat(ST_INFLUENCE, 40)},
                               {SK_ACROBATICS: Skill(SK_ACROBATICS, 0), SK_ATHLETICS: Skill(SK_ATHLETICS, 2),
                                SK_AWARENESS: Skill(SK_AWARENESS, 1), SK_CHARM: Skill(SK_CHARM, 1),
                                SK_COMMAND: Skill(SK_COMMAND, 1), SK_COMMERCE: Skill(SK_COMMERCE, 1),
                                SK_COMMON_LORE: Skill(SK_COMMON_LORE, {"Adeptus Ministorum": 1}),
                                SK_DECEIVE: Skill(SK_DECEIVE, 0), SK_DODGE: Skill(SK_DODGE, 0),
                                SK_FORBIDDEN_LORE: Skill(SK_FORBIDDEN_LORE, {"Daemonology": 1, "Inquisition": 1}),
                                SK_INQUIRY: Skill(SK_INQUIRY, 1), SK_INTERROGATION: Skill(SK_INTERROGATION, 1),
                                SK_INTIMIDATE: Skill(SK_INTIMIDATE, 1),
                                SK_LINGUISTICS: Skill(SK_LINGUISTICS, {"High gothic": 1}),
                                SK_LOGIC: Skill(SK_LOGIC, 0), SK_MEDICAE: Skill(SK_MEDICAE, 0),
                                SK_PARRY: Skill(SK_PARRY, 1), SK_PSYNISCIENCE: Skill(SK_PSYNISCIENCE, 0),
                                SK_SCRUTINY: Skill(SK_SCRUTINY, 1), SK_SECURITY: Skill(SK_SECURITY, 0),
                                SK_SLEIGHT_OF_HANDS: Skill(SK_SLEIGHT_OF_HANDS, 0), SK_STEALTH: Skill(SK_STEALTH, 0),
                                SK_SURVIVAL: Skill(SK_SURVIVAL, 1), SK_TECH_USE: Skill(SK_TECH_USE, 0),
                                SK_TRADE: Skill(SK_TRADE, {"Armourer": 1})},
                               {"TL_BG": Talent("TL_BG", 1), "TL_TRGT": Talent("TL_TRGT", 1),
                                "TL_DTW": Talent("TL_DTW", 1), "TL_WPT": Talent("TL_WPT", {"Low-tech": 1,
                                                                                           "Solid projectile": 1,
                                                                                           "Power": 1}),
                                "TL_CFTC": Talent("TL_CFTC", 1), "TL_FRZ": Talent("TL_FRZ", 1),
                                "TL_BTRG": Talent("TL_BTRG", 1), "TL_FLGT": Talent("TL_FLGT", 1),
                                "TL_ADFT": Talent("TL_ADFT", 1), "TL_INAT": Talent("TL_INAT", {"Melee": 1}),
                                "TL_CRBL": Talent("TL_CRBL", 1), "TL_SWAT": Talent("TL_SWAT", 1),
                                "TL_CNAT": Talent("TL_CNAT", 1), "TL_SHWL": Talent("TL_SHWL", 1),
                                "TL_JD": Talent("TL_JD", 1), "TL_STMN": Talent("TL_STMN", 1),
                                "TL_IR": Talent("TL_IR", 1), "TL_DT": Talent("TL_DT", 1), "TL_AMB": Talent("TL_AMB", 1),
                                "TL_CMST": Talent("TL_CMST", 1), "TL_RST": Talent("TL_RST", {"Fear": 1,
                                                                                             "Psychic powers": 1}),
                                "TL_DMH": Talent("TL_DMH", 1), "TL_HTRD": Talent("TL_HTRD", {"Daemons": 1}),
                                "TL_POH": Talent("TL_POH", {"Daemons": 1}), "TL_ROB": Talent("TL_ROB", 1),
                                "TL_IOHW": Talent("TL_IOHW", 1)}, {}, [], [], [], [], [])
    return render(request, "charsheet-mockup-interactive.html", {'version': VERSION, 'facade': flyweights,
                                                                 'character': character,
                                                                 'hookups': character.make_hookups(flyweights)})
