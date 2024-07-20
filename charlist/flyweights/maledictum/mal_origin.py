# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *

from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.maledictum.mal_origin_model import MalOriginModel


class MalOrigin(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 roll_range: List[int], stat_bonus: str, stat_choice: List[str]):
        super().__init__(tag, name, description)
        self.__roll_range = roll_range
        self.__stat_bonus = stat_bonus
        self.__stat_choice = stat_choice

    def roll_range(self):
        return self.__roll_range

    def stat_bonus(self):
        return self.__stat_bonus

    def stat_choice(self):
        return self.__stat_choice

    @classmethod
    def from_model(cls, model: MalOriginModel):
        return cls(model.tag, model.name, model.description,
                   model.roll_range, model.stat_bonus, model.stat_choice)

    @classmethod
    def from_file(cls, fdata):
        origins = list()
        for origin in fdata[ORIGINS_TAG]:
            origins.append(MalOriginModel.from_json(origin))
        result_origins = list()
        if len(origins) > IM_ZERO:
            for model in origins:
                result_origins.append(cls.from_model(model))
        else:
            result_origins = None
        return result_origins
