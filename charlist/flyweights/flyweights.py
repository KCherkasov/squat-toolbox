# -*- coding: utf-8 -*-
import json

from typing import List, Dict

import charlist.constants.tags
from charlist.constants.tags import *
from charlist.flyweights.aptitude import Aptitude
from charlist.flyweights.background_description import BackgroundDescription
from charlist.flyweights.divination_description import DivinationDescription
from charlist.flyweights.elite_advance_description import EliteAdvance
from charlist.flyweights.homeworld_description import HomeWorldDescription
from charlist.flyweights.role_description import RoleDescription
from charlist.flyweights.skill_description import SkillDescription
from charlist.flyweights.stat_description import StatDescription
from charlist.flyweights.talent_description import TalentDescription
from charlist.flyweights.trait_description import TraitDescription
from charlist.flyweights.malignance_description import MalignanceDescription
from charlist.flyweights.mutation_description import MutationDescription

STAT_SHORTS = {
    ST_WEAPON_SKILL: {"ru": "НР", "en": "WS"},
    ST_BALLISTIC_SKILL: {"ru": "НС", "en": "BS"},
    ST_STRENGTH: {"ru": "Сил", "en": "Str"},
    ST_TOUGHNESS: {"ru": "Вын", "en": "T"},
    ST_AGILITY: {"ru": "Лов", "en": "Ag"},
    ST_INTELLIGENCE: {"ru": "Инт", "en": "Int"},
    ST_PERCEPTION: {"ru": "Вос", "en": "Per"},
    ST_WILLPOWER: {"ru": "СВ", "en": "WP"},
    ST_FELLOWSHIP: {"ru": "Общ", "en": "Fel"},
    ST_INFLUENCE: {"ru": "Вл", "en": "IFL"}
}

STAT_XP_COSTS = [[500, 750, 1000, 1500, 2500], [250, 500, 750, 1000, 1500], [100, 250, 500, 750, 1250]]

SKILL_XP_COSTS = [100, 200, 300, 400]  # without aptitudes matching, 1 apt x2, 0 apt x3

TALENT_XP_COSTS = [200, 300, 400]  # without aptitudes matching, 1 apt - x1.5, 0 apt - x3


def to_map(lst):
    res_map = dict()
    for item in lst:
        res_map[item.get_tag()] = item
    return res_map


# resource paths order
#  0 - aptitude models
#  1 - stat description models
#  2 - skill description models
#  3 - talent description models
#  4 - trait description models
#  5 - homeworlds
#  6 - backgrounds
#  7 - roles
#  8 - elite advances
#  9 - divinations
# 10 - malignancies
# 11 - mutations
# 12 - psychic powers - TODO
# 13 - combat actions - TODO

class Facade:
    def __init__(self, resources_paths):
        prefix = 'static/json/'
        aptitudes = Aptitude.from_file(
            json.load(open(prefix + resources_paths[0], 'r', encoding='utf-8')))
        self.__aptitudes = to_map(aptitudes)
        stat_descriptions = StatDescription.from_file(
            json.load(open(prefix + resources_paths[1], 'r', encoding='utf-8')))
        self.__stat_descriptions = to_map(stat_descriptions)
        skill_descriptions = SkillDescription.from_file(
            json.load(open(prefix + resources_paths[2], 'r', encoding='utf-8')))
        self.__skill_descriptions = to_map(skill_descriptions)
        talent_descriptions = TalentDescription.from_file(
            json.load(open(prefix + resources_paths[3], 'r', encoding='utf-8')))
        self.__talent_descriptions = to_map(talent_descriptions)
        trait_descriptions = TraitDescription.from_file(
            json.load(open(prefix + resources_paths[4], 'r', encoding='utf-8')))
        self.__trait_descriptions = to_map(trait_descriptions)
        homeworlds = HomeWorldDescription.from_file(
            json.load(open(prefix + resources_paths[5], 'r', encoding='utf-8')))
        self.__homeworlds = to_map(homeworlds)
        backgrounds = BackgroundDescription.from_file(
            json.load(open(prefix + resources_paths[6], 'r', encoding='utf-8')))
        self.__backgrounds = to_map(backgrounds)
        roles = RoleDescription.from_file(
            json.load(open(prefix + resources_paths[7], 'r', encoding='utf-8')))
        self.__roles = to_map(roles)
        elite_advances = EliteAdvance.from_file(
            json.load(open(prefix + resources_paths[8], 'r', encoding='utf-8')))
        self.__elite_advances = to_map(elite_advances)
        divinations = DivinationDescription.from_file(
            json.load(open(prefix + resources_paths[9], 'r', encoding='utf-8')))
        self.__divinations = to_map(divinations)
        malignancies = MalignanceDescription.from_file(
            json.load(open(prefix + resources_paths[10], 'r', encoding='utf-8')))
        self.__malignancies = to_map(malignancies)
        mutations = MutationDescription.from_file(
            json.load(open(prefix + resources_paths[11], 'r', encoding='utf-8')))
        self.__mutations = to_map(mutations)
        self.__spec_skills_subtags = SUBTAG_SKILLS_MAP
        self.__st_adv_range = range(1, 6)
        self.__sk_adv_range = range(1, 5)
        self.__stat_shorts = STAT_SHORTS
        self.__langs = ['ru', 'en']
        self.__stat_costs = STAT_XP_COSTS
        self.__skill_costs = SKILL_XP_COSTS
        self.__talent_costs = TALENT_XP_COSTS

    def aptitudes(self):
        return self.__aptitudes

    def stat_descriptions(self):
        return self.__stat_descriptions

    def skill_descriptions(self):
        return self.__skill_descriptions

    def talent_descriptions(self):
        return self.__talent_descriptions

    def trait_descriptions(self):
        return self.__trait_descriptions

    def homeworlds(self):
        return self.__homeworlds

    def backgrounds(self):
        return self.__backgrounds

    def roles(self):
        return self.__roles

    def elite_advances(self):
        return self.__elite_advances

    def divinations(self):
        return self.__divinations

    def malignancies(self):
        return self.__malignancies

    def mutations(self):
        return self.__mutations

    def spec_skills_subtags(self):
        return self.__spec_skills_subtags

    def stat_shorts(self):
        return self.__stat_shorts

    def langs(self):
        return self.__langs

    def sk_adv_range(self):
        return self.__sk_adv_range

    def st_adv_range(self):
        return self.__st_adv_range

    def skill_costs(self):
        return self.__skill_costs

    def stat_costs(self):
        return self.__stat_costs

    def talent_costs(self):
        return self.__talent_costs

    def stat_upg_cost(self, adv_no: int, matches: int):
        return self.stat_costs()[matches][adv_no - 1]

    def skill_upg_cost(self, adv_no: int, matches: int):
        return self.skill_costs()[adv_no - 1] * (1 + 2 - matches)

    def talent_upg_cost(self, tier: int, matches: int):
        cost = self.talent_costs()[tier - 1]
        if matches == 0:
            return cost * 3
        if matches == 1:
            return round(cost * 1.5)
        return cost

    def count_stat_apt_matches(self, st_tag: str, apts: List[str]):
        res = 0
        for apt in apts:
            for st_apt in self.stat_descriptions().get(st_tag).get_aptitudes():
                if apt == st_apt:
                    res += 1
                    break
        return res

    def count_skill_apt_matches(self, sk_tag: str, apts: List[str]):
        res = 0
        for apt in apts:
            for sk_apt in self.skill_descriptions().get(sk_tag).get_aptitudes():
                if apt == sk_apt:
                    res += 1
                    break
        return res

    def count_talent_apt_matches(self, tal_tag: str, apts: List[str]):
        res = 0
        for apt in apts:
            for tl_apt in self.talent_descriptions().get(tal_tag).get_aptitudes():
                if apt == tl_apt:
                    res += 1
                    break
        return res

    def stat_tags(self):
        return charlist.constants.tags.STAT_TAGS

    def skill_tags(self):
        return charlist.constants.tags.SKILL_TAGS
