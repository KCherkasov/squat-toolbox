# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.hinted_description import Hint, HintedDescription
from charlist.flyweights.maledictum.mal_prerequisite import MalPrerequisite
from charlist.flyweights.models.maledictum.mal_talent_description_model import MalTalentDescriptionModel
from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *


class MalTalentDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 prerequisites: List[MalPrerequisite],
                 specializations: List[str], is_stackable: bool):
        super().__init__(tag, name, description, hints)
        self.__prerequisites = prerequisites
        self.__specializations = specializations
        self.__is_stackable = is_stackable

    def prerequisites(self):
        return self.__prerequisites

    def specializations(self):
        return self.__specializations

    def is_stackable(self):
        return self.__is_stackable

    @classmethod
    def from_model(cls, model: MalTalentDescriptionModel):
        hints = list()
        for model in model.hints:
            hints.append(Hint.from_model(model))
        return cls(model.tag, model.name, model.description, hints,
                   model.prerequisites, model.specializations,
                   model.is_stackable)

    @classmethod
    def from_file(cls, fdata):
        talent_models = list()
        for model in fdata[TALENTS_TAG]:
            talent_models.append(MalTalentDescriptionModel.from_json(model))
        if len(talent_models) > IM_ZERO:
            talent_descriptions = list()
            for model in talent_models:
                talent_descriptions.append(MalTalentDescription.from_model(model))
        else:
            talent_descriptions = None
        return talent_descriptions
