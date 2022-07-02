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


class HintModel(object):
    def __init__(self, tag: str, description: Dict[str, str], targets: List[str], bonus):
        self.tag = tag
        self.description = description
        self.targets = targets
        self.bonus = bonus

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class TalentPrerequisite(object):
    def __init__(self, tag: str, value: int):
        self.tag = tag
        self.value = value

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class TalentDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 hints: List[HintModel], tier: int,
                 aptitudes: List[str],
                 prerequisites: List[TalentPrerequisite]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.tier = tier
        self.aptitudes = aptitudes
        self.prerequisites = prerequisites

    @classmethod
    def from_json(cls, data):
        # hints = list()
        # for model in data['hints']:
        #     hints.append(HintModel.from_json(model))
        # data['hints'] = hints
        return cls(**data)
