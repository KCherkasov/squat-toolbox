# -*- coding: utf-8 -*-

from typing import Dict


class MalSkillDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], stat: str):
        self.tag = tag
        self.name = name
        self.description = description
        self.stat = stat

    @classmethod
    def from_json(cls, data):
        return cls(**data)
