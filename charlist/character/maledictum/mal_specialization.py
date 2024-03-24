# -*- coding: utf-8 -*-

import json

from typing import Dict
from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *


class MalSpecialization(object):
    def __init__(self, tag: str, advances: int = IM_DEFAULT_ADVANCE):
        self.__tag = tag
        self.__advances = advances

    def tag(self):
        return self.__tag

    def advances(self):
        return self.__advances * IM_ADVANCE_STEP

    def is_upgradeable(self):
        return self.__advances < IM_SKILL_ADV_CAP

    def upgrade(self):
        self.__advances += IM_ONE

    def is_upgradeable(self):
        return self.__advances < IM_SKILL_ADV_CAP

    def is_custom(self):
        return self.tag() not in SKILL_SPECS

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        return cls(**data)

    def toJSON(self):
        fields_preset = self.__dict__
        fields = dict()
        for key, val in fields_preset.items():
            field_key = key[20:]
            fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=JSON_INDENT)
