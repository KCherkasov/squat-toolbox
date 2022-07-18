# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.models.divination_description_model import DivinationModel


class DivinationDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[Hint], commands: List[Dict], roll_range: List[int]):
        super().__init__(tag, name, description, hints)
        self.__commands = commands
        self.__roll_range = roll_range

    def get_commands(self):
        return self.__commands

    def get_roll_range(self):
        return self.__roll_range

    @classmethod
    def from_model(cls, model: DivinationModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description,
                   hints, model.commands, model.roll_range)

    @classmethod
    def from_file(cls, fdata):
        dvs = list()
        for dv in fdata['divinations']:
            dvs.append(DivinationModel.from_json(dv))
        if len(dvs) > 0:
            divinations = list()
            for dv in dvs:
                divinations.append(DivinationDescription.from_model(dv))
            return divinations
        else:
            return None
