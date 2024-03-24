# -*- coding: utf-8 -*-

import json

from charlist.constants.maledictum.constants import *
from charlist.constants.maledictum.tags import *


class MalStat(object):
    def __init__(self, tag: str, base: int, advances: int = IM_DEFAULT_ADVANCE):
        self.__tag = tag
        self.__base = base
        self.__advances = advances

    def get_base(self):
        return self.__base

    def advances(self):
        return self.__advances

    def value(self):
        return self.__base + self.__advances

    def is_upgradeable(self):
        return self.value() < IM_STAT_CAP_HUMAN

    def upgrade(self, amount: int = IM_ADVANCE_STEP):
        self.__advances += amount

    def upgrade_5(self):
        self.upgrade(IM_STAT_ADV_FIVE)

    def upgrade_10(self):
        self.upgrade(IM_STAT_ADV_TEN)

    def bonus(self):
        return self.value() // 10

    def residue(self):
        return self.value() % 10

    def improve(self, amount: int = IM_ONE):
        self.__base += amount

    def damage(self, amount: int = IM_ONE):
        self.__base -= amount

    def get_upg_cost(self):
        cost = 0
        for key, val in STAT_UPG_COSTS.items():
            if (key <= (self.value() + 1)) and (val > cost):
                cost = val
        return cost

    def get_batch_cost(self, amount: int):
        total = 0
        temp_stat = self.value() + 1
        for i in range(1, amount):
            cost = 0
            for key, val in STAT_UPG_COSTS.items():
                if (key <= temp_stat) and (val > cost):
                    cost = val
            total += cost
            temp_stat += 1
            if temp_stat == IM_STAT_CAP_HUMAN:
                break
        return total

    def get_cost_5(self):
        return self.get_batch_cost(5)

    def get_cost_10(self):
        return self.get_batch_cost(10)

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        return cls(**sdata)

    def toJSON(self):
        fields = dict()
        for key, val in self.__dict__.items():
            field_key = key[10:]
            fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=JSON_INDENT)
