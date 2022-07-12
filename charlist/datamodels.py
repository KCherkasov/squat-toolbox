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


class TalentPrerequisite(object):
    def __init__(self, tag: str, value: int, subtag: List[str], alt: Dict = None):
        self.tag = tag
        self.subtag = subtag
        self.value = value
        self.alt = alt

    def has_subtag(self):
        return not (self.subtag is None)

    def has_alt(self):
        return not (self.alt is None)

    def get_alt_tag(self):
        return self.alt['tag']

    def alt_has_subtag(self):
        return 'subtag' in self.alt.keys()

    def get_alt_subtag(self):
        return self.alt['subtag']

    def get_alt_value(self):
        return self.alt['value']

    @classmethod
    def from_json(cls, data):
        return cls(**data)


class TalentDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 hints: List[HintModel], tier: int,
                 aptitudes: List[str],
                 prerequisites: List[TalentPrerequisite],
                 is_specialist: bool,
                 is_stackable: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.tier = tier
        self.aptitudes = aptitudes
        self.prerequisites = prerequisites
        self.is_specialist = is_specialist
        self.is_stackable = is_stackable

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)
