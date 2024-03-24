# -*- coding: utf-8 -*-

from typing import Dict

from charlist.constants.constants import *
from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.maledictum.mal_skill_description_model import MalSkillDescriptionModel


class MalSkillDescription(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 stat: str):
        super().__init__(tag, name, description)
        self.__stat = stat

    def stat(self):
        return self.__stat

    @classmethod
    def from_model(cls, model: MalSkillDescriptionModel):
        return cls(model.tag, model.name, model.description, model.stat)

    @classmethod
    def from_file(cls, fdata):
        skill_descriptions = list()
        for skill_description in fdata['descriptions']:
            skill_descriptions.append(MalSkillDescriptionModel.from_json(skill_description))
        result_descriptions = list()
        if len(skill_descriptions) > 0:
            for skill_description in skill_descriptions:
                result_descriptions.append(cls.from_model(skill_description))
        else:
            result_descriptions = None
        return result_descriptions
