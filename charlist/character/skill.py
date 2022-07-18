# -*- coding: utf-8 -*-

from charlist.constants.tags import *

SKILL_POINTS_PER_UPG = 10

UNTRAINED_SKILL = -20

SKILL_UPGRADES_CAP = 4


class Skill(object):
    def __init__(self, tag: str, advances):
        self.__tag = tag
        self.__advances = advances

    def tag(self):
        return self.__tag

    def is_specialist(self):
        return self.__tag in SUBTAGGED_SKILLS

    def advances(self):
        return self.__advances

    def get_subskill_advance(self, subtag: str):
        if self.is_specialist() and (subtag in self.__advances.keys()):
            return self.__advances.get(subtag)
        else:
            return None

    def get_adv_bonus(self):
        if self.is_specialist():
            return None
        if self.__advances > 0:
            return self.__advances * SKILL_POINTS_PER_UPG - 10
        else:
            return UNTRAINED_SKILL

    def get_adv_bonus_subtag(self, subtag: str):
        adv = self.get_subskill_advance(subtag)
        if adv is None:
            return None
        else:
            if adv > 0:
                return adv * SKILL_POINTS_PER_UPG - 10
            else:
                return UNTRAINED_SKILL

    def upgradeable(self):
        return (self.__advances < SKILL_UPGRADES_CAP) and (self.__tag != ST_INFLUENCE)

    def upgradeable_subtag(self, subtag: str):
        if subtag not in self.__advances.keys():
            return True
        else:
            return self.__advances.get(subtag) < SKILL_UPGRADES_CAP

    def upgrade(self):
        if not self.is_specialist() and self.upgradeable():
            self.__advances += 1

    def upgrade_subtag(self, subtag: str):
        if self.is_specialist() and self.upgradeable_subtag(subtag):
            if subtag in self.__advances.keys():
                self.__advances[subtag] += 1
            else:
                self.__advances[subtag] = 1

    @classmethod
    def from_json(cls, data):
        return cls(**data)
