# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel
from charlist.flyweights.models.prerequisite import Prerequisite


class TalentDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 hints: List[HintModel], tier: int,
                 aptitudes: List[str],
                 prerequisites: List[Prerequisite],
                 is_specialist: bool,
                 is_stackable: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.tier = tier
        self.aptitudes = aptitudes
        self.prerequisites = prerequisites
        self.is_specialist = is_specialist
        self.is_stackable = is_stackable

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        prerequisites = list()
        for model in data['prerequisites']:
            prerequisites.append(Prerequisite.from_json(model))
        data['prerequisites'] = prerequisites
        return cls(**data)
