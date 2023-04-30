from typing import Dict, List

from charlist.flyweights.models.hint_model import HintModel


class CareerModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], hints: List[HintModel],
                 aptitudes: List[str], skills: List[Dict], traits: List[Dict], talents: List[Dict],
                 choices: List[List[Dict]], commands: List[Dict]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.aptitudes = aptitudes
        self.skills = skills
        self.traits = traits
        self.talents = talents
        self.choices = choices
        self.commands = commands

    @classmethod
    def from_json(cls, data):
        hints = list()
        for hint in data['hints']:
            hints.append(HintModel.from_json(hint))
        data['hints'] = hints
        return cls(**data)
