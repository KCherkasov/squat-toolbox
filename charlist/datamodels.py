# -*- coding: utf-8 -*-

from typing import List
import json


class AptitudeModel(object):
    def __init__(self, tag: str, name: str, description: str):
        self.tag = tag
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(data['tag'], data['name'], data['description'])


class StatDescriptionModel(object):
    def __init__(self, tag: str, name: str, description: str, upgradeable: bool, aptitudes: List[str]):
        self.tag = tag
        self.name = name
        self.description = description
        self.upgradeable = upgradeable
        self.aptitudes = aptitudes

    @classmethod
    def from_json(cls, data):
        return cls(**data)
