# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.bonus_description_model import BonusDescriptionModel
from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.core.hinted_description import HintedDescription


class BonusDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 commands):
        super().__init__(tag, name, description, hints)
        self.__commands = commands

    def get_commands(self):
        return self.__commands

    @classmethod
    def from_model(cls, model: BonusDescriptionModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description, hints, model.commands)
