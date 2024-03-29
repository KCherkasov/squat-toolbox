# -*- coding: utf-8 -*-
import json

from typing import Dict

from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *

from charlist.character.maledictum.mal_specialization import MalSpecialization

SKILL_POINTS_PER_UPG = 5

UNTRAINED_SKILL = -20

SKILL_UPGRADES_CAP = 4


class MalSkill(object):
    def __init__(self, tag: str, advances: int, specializations: Dict[str, MalSpecialization]):
        self.__tag = tag
        self.__advances = advances
        self.__specializations = specializations

    def rowspan(self):
        return len(self.__specializations.keys()) + IM_TWO

    def tag(self):
        return self.__tag

    def advances(self):
        return self.__advances

    def adv_bonus(self):
        return self.__advances * IM_SKILL_ADVANCE

    def is_upgradeable(self):
        return self.__advances < IM_SKILL_ADV_CAP

    def upgrade(self):
        self.__advances += IM_ONE

    def specializations(self):
        return self.__specializations

    def specialization(self, tag: str):
        return self.__specializations.get(tag)

    def has_specialization(self, tag: str):
        return tag in self.__specializations.keys()

    def specialization_adv_bonus(self, tag: str):
        if self.has_specialization(tag):
            return self.adv_bonus() + self.specialization(tag).adv_bonus()
        else:
            return self.adv_bonus()

    def gain_specialization(self, spec: MalSpecialization):
        if spec.tag() not in self.__specializations.keys():
            self.__specializations[spec.tag()] = spec

    def upgrade_specialization(self, tag: str):
        if self.has_specialization(tag):
            if self.__specializations.get(tag).is_upgradeable():
                self.__specializations.get(tag).upgrade()

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        specializations = dict()
        for spec_tag, spec in data[SKILL_SPEC_TAG]:
            specializations[spec_tag] = MalSpecialization.from_json(spec)
        data[SKILL_SPEC_TAG] = specializations
        return cls(**data)

    def toJSON(self):
        fields = dict()
        for key, val in self.__dict__.items():
            field_key = key[11:]
            if field_key != SKILL_SPEC_TAG:
                fields[field_key] = val
            else:
                specs = dict()
                for skey, sval in self.specializations().items():
                    specs[skey] = sval.toJSON()
                fields[SKILL_SPEC_TAG] = specs
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=JSON_INDENT)
