# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.bonus_description import BonusDescription
from charlist.flyweights.models.role_description_model import RoleModel


class RoleDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 aptitudes: List[str], apt_choices: List[str],
                 talent_choices: List[Dict], bonus: BonusDescription):
        super().__init__(tag, name, description, hints)
        self.__aptitudes = aptitudes
        self.__apt_choices = apt_choices
        self.__talent_choices = talent_choices
        self.__bonus = bonus

    def get_aptitudes(self):
        return self.__aptitudes

    def get_apt_choices(self):
        return self.__apt_choices

    def get_talent_choices(self):
        return self.__talent_choices

    def get_bonus(self):
        return self.__bonus

    @classmethod
    def from_model(cls, model: RoleModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        bonus = BonusDescription.from_model(model.bonus)
        return cls(model.tag, model.name, model.description, hints,
                   model.aptitudes, model.apt_choices, model.talent_choices,
                   bonus)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for role in fdata['roles']:
            models.append(RoleModel.from_json(role))
        if len(models) > 0:
            roles = list()
            for role in models:
                roles.append(RoleDescription.from_model(role))
            return roles
        else:
            return None
