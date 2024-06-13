# -*- coding: utf-8 -*-

from typing import Dict, List

# TODO: add starting item!


class MalOriginModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 roll_range: List[int], stat_bonus: str, stat_choice: List[str]):
        self.tag = tag
        self.name = name
        self.description = description
        self.roll_range = roll_range
        self.stat_bonus = stat_bonus
        self.stat_choice = stat_choice

    @classmethod
    def from_json(cls, data):
        return cls(**data)
