# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.stat_description_model import StatDescriptionModel


class StatDescription(ObjectDescription):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 upgradeable: bool, aptitudes: List[str]):
        super().__init__(tag, name, description)
        self.__upgradeable = upgradeable
        self.__aptitudes = aptitudes

    def is_upgradeable(self):
        return self.__upgradeable

    def get_aptitudes(self):
        return self.__aptitudes

    @classmethod
    def from_model(cls, model: StatDescriptionModel):
        return cls(model.tag, model.name, model.description, model.upgradeable, model.aptitudes)

    @classmethod
    def from_file(cls, fdata):
        stat_descriptions = list()
        for stat_description in fdata['descriptions']:
            stat_descriptions.append(StatDescriptionModel.from_json(stat_description))
        result_descriptions = list()
        if len(stat_descriptions) > 0:
            for stat_description in stat_descriptions:
                result_descriptions.append(cls.from_model(stat_description))
        else:
            result_descriptions = None
        return result_descriptions
