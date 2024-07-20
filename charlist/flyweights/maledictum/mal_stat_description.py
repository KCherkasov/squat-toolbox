# -*- coding: utf-8 -*-

from typing import Dict

from charlist.constants.constants import *
from charlist.constants.maledictum.tags import *
from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.maledictum.mal_stat_description_model import MalStatDescriptionModel


class MalStatDescription(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 short_name: Dict[str, str],
                 description: Dict[str, str]):
        super().__init__(tag, name, description)
        self.__short_name = short_name

    def short_name(self):
        return self.__short_name

    def get_short_name(self, lang=RU):
        return self.__short_name.get(lang)

    def get_short_name_ru(self):
        return self.get_short_name(RU)

    def get_short_name_en(self):
        return self.get_short_name(EN)

    @classmethod
    def from_model(cls, model: MalStatDescriptionModel):
        return cls(model.tag, model.name, model.short_name, model.description)

    @classmethod
    def from_file(cls, fdata):
        stat_descriptions = list()
        for stat_description in fdata[DESCR_TAG]:
            stat_descriptions.append(MalStatDescriptionModel.from_json(stat_description))
        result_descriptions = list()
        if len(stat_descriptions) > 0:
            for stat_description in stat_descriptions:
                result_descriptions.append(cls.from_model(stat_description))
        else:
            result_descriptions = None
        return result_descriptions
