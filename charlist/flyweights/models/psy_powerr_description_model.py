from typing import Dict, List
from charlist.flyweights.models.prerequisite import Prerequisite

class PsyPowerDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, List[str]], school: str,
                 type: List[str], effect: Dict, cost: int, prerequisites: List[Prerequisite],
                 sustainable: bool, focus_check: str, focus_mod: int, focus_opposed: bool,
                 range: int, action: str, keywords: List[str], sustain = None):
        self.tag = tag
        self.name = name
        self.description = description
        self.school = school
        self.type = type
        self.effect = effect
        self.cost = cost
        self.prerequisites = prerequisites
        self.sustainable = sustainable
        self.sustain = sustain
        self.focus_check = focus_check
        self.focus_mod = focus_mod
        self.focus_opposed = focus_opposed
        self.range = range
        self.action = action
        self.keywords = keywords

    @classmethod
    def from_json(cls, data):
        prerequisites = list()
        for model in data['prerequisites']:
            prerequisites.append(Prerequisite.from_json(model))
        data['prerequisites'] = prerequisites
        return cls(**data)
