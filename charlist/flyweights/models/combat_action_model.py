from typing import Dict, List


class CombatActionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, List[str]],
                 types: List[str], keywords: List[str]):
        self.tag = tag
        self.name = name
        self.description = description
        self.types = types
        self.keywords = keywords

    @classmethod
    def from_json(cls, data):
        return cls(**data)
