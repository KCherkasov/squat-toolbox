from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel


class MotivationModel(object):
    def __init__(self, tag: str, name: Dict[str, str], hints: List[HintModel],
                 choices: List[List[Dict]], commands: List[Dict], aptitudes: List[str], cost: int):
        self.tag = tag
        self.name = name
        self.hints = hints
        self.choices = choices
        self.commands = commands
        self.aptitudes = aptitudes
        self.cost = cost

    @classmethod
    def from_json(cls, data):
        hints = list()
        for hint in data['hints']:
            hints.append(HintModel.from_json(hint))
        data['hints'] = hints
        return cls(**data)
