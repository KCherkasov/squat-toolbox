# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.models.prerequisite import Prerequisite
from charlist.flyweights.models.talent_description_model import TalentDescriptionModel


class TalentDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 tier: int, aptitudes: List[str], prerequisites: List[Prerequisite],
                 is_specialist: bool, is_stackable: bool):
        super().__init__(tag, name, description, hints)
        self.__tier = tier
        self.__aptitudes = aptitudes
        self.__prerequisites = prerequisites
        self.__is_specialist = is_specialist
        self.__is_stackable = is_stackable

    def get_tier(self):
        return self.__tier

    def get_aptitudes(self):
        return self.__aptitudes

    def has_prerequisites(self):
        return len(self.__prerequisites) > 0

    def get_prerequisites(self):
        return self.__prerequisites

    def is_specialist(self):
        return self.__is_specialist

    def is_stackable(self):
        return self.__is_stackable

    @classmethod
    def from_model(cls, model: TalentDescriptionModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description,
                   hints, model.tier, model.aptitudes, model.prerequisites,
                   model.is_specialist, model.is_stackable)

    @classmethod
    def from_file(cls, fdata):
        talent_descriptions = list()
        for description in fdata['talents']:
            talent_descriptions.append(TalentDescriptionModel.from_json(description))
        if len(talent_descriptions) > 0:
            talents = list()
            for talent in talent_descriptions:
                talents.append(TalentDescription.from_model(talent))
        else:
            talents = None
        return talents
