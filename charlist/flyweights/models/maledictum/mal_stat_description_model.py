# -*- coding: utf-8 -*-

from typing import Dict


class MalStatDescriptionModel(object):
    def __init__(self, tag: str,
                 name: Dict[str, str], short_name: Dict[str, str],
                 description: Dict[str, str]):
        self.tag = tag
        self.name = name
        self.short_name = short_name
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(**data)
