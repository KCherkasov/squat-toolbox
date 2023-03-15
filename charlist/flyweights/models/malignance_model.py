from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel


class MalignanceModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], hints: List[HintModel],
                 commands: List[Dict], rolls_range: List[int]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.commands = commands
        self.rolls_range = rolls_range

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)
