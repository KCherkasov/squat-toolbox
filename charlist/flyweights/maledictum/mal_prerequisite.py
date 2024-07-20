# -*- coding: utf-8 -*-

import json

from typing import List

from charlist.constants.maledictum.constants import *
from charlist.constants.maledictum.tags import *
from charlist.flyweights.maledictum.mal_condition import MalCondition


class MalPrerequisite(object):
    def __init__(self, conditions: List[MalCondition]):
        self.conditions = conditions

    def has_alts(self):
        return len(self.conditions) > IM_ONE

    def matched(self, character):
        for condition in self.conditions:
            if condition.matched(character):
                return True
        return False

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        conditions = list()
        for condition in data[CONDITIONS_TAG]:
            conditions.append(MalCondition.from_json(condition))
        data[CONDITIONS_TAG] = conditions
        return cls(**data)
