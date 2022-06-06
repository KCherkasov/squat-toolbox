# -*- coding: utf-8 -*-

from typing import List, Dict


class AptitudeModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        self.tag = tag
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class StatDescriptionModel(object):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 upgradeable: bool, aptitudes: List[str]):
        self.tag = tag
        self.name = name
        self.description = description
        self.upgradeable = upgradeable
        self.aptitudes = aptitudes

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class SkillDescriptionModel(object):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 aptitudes: List[str], stats: List[str],
                 is_specialist: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.aptitudes = aptitudes
        self.stats = stats
        self.is_specialist = is_specialist

    @classmethod
    def from_json(cls, data):
        return cls(**data)
