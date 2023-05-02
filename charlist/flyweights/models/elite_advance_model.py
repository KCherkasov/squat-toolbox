# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel
from charlist.flyweights.models.prerequisite import Prerequisite


class EliteAdvanceModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], cost: int, prerequisites: List[Prerequisite],
                 commands: List[Dict]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.cost = cost
        self.prerequisites = prerequisites
        self.commands = commands

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
