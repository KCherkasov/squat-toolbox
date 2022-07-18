# -*- coding: utf-8 -*-

from charlist.constants.tags import *


STAT_POINTS_PER_UPG = 5
STAT_UPGRADES_CAP = 5


class Stat(object):
    def __init__(self, tag: str, base: int, advances: int = 0):
        self.__tag = tag
        self.__base = base
        self.__advances = advances

    def is_upgradeable(self):
        return (self.__tag == ST_INFLUENCE) or (self.__advances >= STAT_UPGRADES_CAP)

    def get_base(self):
        return self.__base

    def get_upgrades(self):
        return self.__advances

    def value(self):
        return self.__base + STAT_POINTS_PER_UPG * self.__advances

    def bonus(self):
        return self.value() // 10

    def residue(self):
        return self.value() % 10

    def upgrade(self):
        self.__advances += 1

    def damage(self, amount: int = 1):
        self.__base -= amount

    def improve(self, amount: int = 1):
        self.__base += amount

    def is_fatigued(self, fatigue: int):
        return self.bonus() < fatigue

    @classmethod
    def from_json(cls, data):
        return cls(**data)
