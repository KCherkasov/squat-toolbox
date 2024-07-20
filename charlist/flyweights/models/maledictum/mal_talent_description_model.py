# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel
from charlist.flyweights.maledictum.mal_prerequisite import MalPrerequisite
from charlist.constants.maledictum.tags import *


class MalTalentDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 hints: List[HintModel],
                 prerequisites: List[MalPrerequisite],
                 specializations: List[str],
                 is_stackable: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.prerequisites = prerequisites
        self.specializations = specializations
        self.is_stackable = is_stackable

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data[HINTS_TAG]:
            hints.append(HintModel.from_json(model))
        data[HINTS_TAG] = hints
        prerequisites = list()
        for model in data[PREREQ_TAG]:
            prerequisites.append(MalPrerequisite.from_json(model))
        data[PREREQ_TAG] = prerequisites
        return cls(**data)
