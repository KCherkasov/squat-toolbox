# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel
from charlist.flyweights.models.bonus_description_model import BonusDescriptionModel


class RoleModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], aptitudes: List[str], apt_choices: List[str],
                 talent_choices: List[Dict], bonus: BonusDescriptionModel):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.aptitudes = aptitudes
        self.apt_choices = apt_choices
        self.talent_choices = talent_choices
        self.bonus = bonus

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        bonus = BonusDescriptionModel.from_json(data['bonus'])
        data['bonus'] = bonus
        return cls(**data)
