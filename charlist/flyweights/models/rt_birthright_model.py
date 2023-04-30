from typing import Dict, List


class BirthrightModel(object):
    def __init__(self, tag: str, name: Dict[str, str], choices: List[List[Dict]],
                 commands: List[Dict], aptitude_choices: List[str], cost: int):
        self.tag = tag
        self.name = name
        self.choices = choices
        self.commands = commands
        self.aptitude_choices = aptitude_choices
        self.cost = cost

    @classmethod
    def from_json(cls, data):
        return cls(**data)
