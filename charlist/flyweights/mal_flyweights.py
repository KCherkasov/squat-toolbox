# -*- coding: utf-8 -*-
import json

from typing import List, Dict

from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *

from charlist.flyweights.maledictum.mal_stat_description import MalStatDescription
from charlist.flyweights.maledictum.mal_skill_description import MalSkillDescription
from charlist.flyweights.maledictum.mal_specialzation_description import MalSpecializationDescription


def to_map(lst):
    res_map = dict()
    for item in lst:
        res_map[item.get_tag()] = item
    return res_map


def fname_to_path(fname: str):
    return RESOURCES_PATH + fname


class MalFacade:
    def __init__(self, resources_paths: List[str] = MAL_RESOURCES):
        stats = MalStatDescription.from_file(
            json.load(open(fname_to_path(resources_paths[STATS_DESCR_ID]), 'r', encoding='utf-8')))
        self.__stat_descriptions = to_map(stats)
        skills = MalSkillDescription.from_file(
            json.load(open(fname_to_path(resources_paths[SKILL_DESCR_ID]), 'r', encoding='utf-8')))
        self.__skill_descriptions = to_map(skills)
        specializations = MalSpecializationDescription.from_file(
            json.load(open(fname_to_path(resources_paths[SPEC_DESCR_ID]), 'r', encoding='utf-8')))
        self.__specialization_descriptions = to_map(specializations)
        self.__langs = MAL_LANGS
        self.__stat_tags = STAT_TAGS_GEN
        self.__skill_tags = SKILL_TAGS

    def stat_descriptions(self):
        return self.__stat_descriptions

    def skill_descriptions(self):
        return self.__skill_descriptions

    def specialization_descriptions(self):
        return self.__specialization_descriptions

    def langs(self):
        return self.__langs

    def stat_tags(self):
        return self.__stat_tags

    def skill_tags(self):
        return self.__skill_tags
