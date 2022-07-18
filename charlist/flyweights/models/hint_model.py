# -*- coding: utf-8 -*-

from typing import Dict, List


class HintModel(object):
    def __init__(self, tag: str, description: Dict[str, str], targets: List[str],
                 bonus: int = None, condition: str = None, base: float = None, command: Dict = None):
        self.tag = tag
        self.description = description
        self.targets = targets
        self.bonus = bonus
        self.condition = condition
        self.base = base
        self.command = command

    @classmethod
    def from_json(cls, data):
        return cls(**data)
