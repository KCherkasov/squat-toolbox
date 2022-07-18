# -*- coding: utf-8 -*-

from typing import List, Dict

from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.models.prerequisite import Prerequisite
from charlist.flyweights.models.elite_advance_model import EliteAdvanceModel


class EliteAdvance(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], hints: List[Hint],
                 cost: int, prerequisites: List[Prerequisite], commands: List[Dict]):
        super().__init__(tag, name, description, hints)
        self.__cost = cost
        self.__prerequisites = prerequisites
        self.__commands = commands

    def cost(self):
        return self.__cost

    def prerequisites(self):
        return self.__prerequisites

    def commands(self):
        return self.__commands

    @classmethod
    def from_model(cls, model: EliteAdvanceModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description, hints,
                   model.cost, model.prerequisites, model.commands)

    @classmethod
    def from_file(cls, fdata):
        eads = list()
        for ead in fdata['elite_advances']:
            eads.append(EliteAdvanceModel.from_json(ead))
        if len(eads) > 0:
            elite_advances = list()
            for ead in eads:
                elite_advances.append(EliteAdvance.from_model(ead))
            return elite_advances
        else:
            return None
