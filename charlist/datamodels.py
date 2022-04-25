# -*- coding: utf-8 -*-

from typing import List, Dict


class AptitudeModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        self.tag = tag
        self.name = dict()
        for k in name.keys():
            self.name[k] = name.get(k)
        self.description = dict()
        for k in description.keys():
            self.description[k] = description.get(k)

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class StatDescriptionModel(object):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 upgradeable: bool, aptitudes: List[str]):
        self.tag = tag
        self.name = dict()
        for k in name.keys():
            self.name[k] = name.get(k)
        self.description = dict()
        for k in description.keys():
            self.description[k] = description.get(k)
        self.upgradeable = upgradeable
        self.aptitudes = aptitudes

    @classmethod
    def from_json(cls, data):
        return cls(**data)
