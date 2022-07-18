# -*- coding: utf-8 -*-

from typing import List, Dict

from charlist.flyweights.models.hint_model import HintModel


class TraitModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], is_specialist: bool, is_stackable: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.is_specialist = is_specialist
        self.is_stackable = is_stackable

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)
