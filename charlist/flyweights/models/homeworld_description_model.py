# -*- coding: utf-8

from typing import List, Dict

from charlist.flyweights.models.hint_model import HintModel
from charlist.flyweights.models.bonus_description_model import BonusDescriptionModel


class HomeworldModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], stat_mods: Dict[str, int],
                 fate: int, blessing: int, bonus: BonusDescriptionModel,
                 aptitude: str, wounds: int):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.stat_mods = stat_mods
        self.fate = fate
        self.blessing = blessing
        self.bonus = bonus
        self.aptitude = aptitude
        self.wounds = wounds

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        bonus = BonusDescriptionModel.from_json(data['bonus'])
        data['bonus'] = bonus
        return cls(**data)
