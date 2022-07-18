# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.skill_description_model import SkillDescriptionModel


class SkillDescription(ObjectDescription):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 aptitudes: List[str], stats: List[str], is_specialist: bool):
        super().__init__(tag, name, description)
        self.__aptitudes = aptitudes
        self.__stats = stats
        self.__is_specialist = is_specialist

    def get_aptitudes(self):
        return self.__aptitudes

    def get_stats(self):
        return self.__stats

    def get_primary_stat(self):
        return self.__stats[0]

    def get_alt_stats(self):
        if len(self.__stats) > 1:
            return self.__stats[1:]
        else:
            return None

    def is_specialist(self):
        return self.__is_specialist

    @classmethod
    def from_model(cls, model: SkillDescriptionModel):
        return cls(model.tag, model.name, model.description,
                   model.aptitudes, model.stats, model.is_specialist)

    @classmethod
    def from_file(cls, fdata):
        skill_descriptions = list()
        for skill_description in fdata['skills']:
            skill_descriptions.append(SkillDescriptionModel.from_json(skill_description))
        result_descriptions = list()
        if len(skill_descriptions) > 0:
            for description in skill_descriptions:
                result_descriptions.append(cls.from_model(description))
        else:
            result_descriptions = None
        return result_descriptions
