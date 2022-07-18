# -** coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.nameless_description import NamelessDescription
from charlist.flyweights.models.hint_model import HintModel


class Hint(NamelessDescription):
    def __init__(self, tag: str, description: Dict[str, str], target: List[str], bonus: int = None,
                 base: float = None, condition: str = None, command: Dict = None):
        super().__init__(tag, description)
        self.__target = target
        self.__bonus = bonus
        self.__base = base
        self.__condition = condition
        self.__command = command

    def get_target(self):
        return self.__target

    def get_bonus(self):
        return self.__bonus

    def get_base(self):
        return self.__base

    def get_condition(self):
        return self.__condition

    def get_command(self):
        return self.__command

    def has_command(self):
        return not (self.__command is None)

    def has_bonus(self):
        return not (self.__bonus is None)

    def has_base(self):
        return not (self.__base is None)

    @classmethod
    def from_model(cls, model: HintModel):
        return cls(model.tag, model.description, model.targets, model.bonus,
                   model.base, model.condition, model.command)
