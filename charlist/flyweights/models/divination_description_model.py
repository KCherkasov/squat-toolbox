# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel


class DivinationModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], commands: List[Dict], roll_range: List[int]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.commands = commands
        self.roll_range = roll_range

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)
