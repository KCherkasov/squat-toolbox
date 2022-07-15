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
    def __init__(self, tag: str, value: int, subtag: List[str] = None, alt: Dict = None):
        self.tag = tag
        self.subtag = subtag
        self.value = value
        self.alt = alt

    def has_subtag(self):
        return not (self.subtag is None)

    def has_alt(self):
        return not (self.alt is None)

    def is_alt_list(self):
        return isinstance(self.alt, list)

    def get_alt_tag(self):
        return self.alt.get('tag')

    def alt_has_subtag(self):
        return 'subtag' in self.alt.keys()

    def get_alt_subtag(self):
        return self.alt.get('subtag')

    def get_alt_value(self):
        return self.alt.get('value')

    def get_alt(self):
        return self.alt

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
        prerequisites = list()
        for model in data['prerequisites']:
            prerequisites.append(TalentPrerequisite.from_json(model))
        data['prerequisites'] = prerequisites
        return cls(**data)


class TraitModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], is_specialist: bool, is_stackable: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.is_specialist = is_specialist
        self.is_stackable = is_stackable

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)


class BonusDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], commands: List[Dict]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.commands = commands

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)


class HomeworldModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], stat_mods: Dict[str, int],
                 fate: int, blessing: int, bonus: BonusDescriptionModel,
                 aptitude: str, wounds: int):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.stat_mods = stat_mods
        self.fate = fate
        self.blessing = blessing
        self.bonus = bonus
        self.aptitude = aptitude
        self.wounds = wounds

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        bonus = BonusDescriptionModel.from_json(data['bonus'])
        data['bonus'] = bonus
        return cls(**data)


class BackgroundModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 skills: List[Dict[str, str]], skill_choices: List[List[Dict]],
                 talents: List[Dict], talent_choices: List[List[Dict]],
                 aptitudes: List[str], apt_choices: List[str], traits: List[Dict],
                 traits_choices: List[Dict], equipment: List, bonus: BonusDescriptionModel):
        self.tag = tag
        self.name = name
        self.description = description
        self.skills = skills
        self.skill_choices = skill_choices
        self.talents = talents
        self.talent_choices = talent_choices
        self.aptitudes = aptitudes
        self.apt_choices = apt_choices
        self.traits = traits
        self.traits_choices = traits_choices
        self.equipment = equipment
        self.bonus = bonus

    @classmethod
    def from_json(cls, data):
        bonus = BonusDescriptionModel.from_json(data['bonus'])
        data['bonus'] = bonus
        return cls(**data)


class RoleModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], aptitudes: List[str], apt_choices: List[str],
                 talent_choices: List[Dict], bonus: BonusDescriptionModel):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.aptitudes = aptitudes
        self.apt_choices = apt_choices
        self.talent_choices = talent_choices
        self.bonus = bonus

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        bonus = BonusDescriptionModel.from_json(data['bonus'])
        data['bonus'] = bonus
        return cls(**data)


class EliteAdvanceModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], cost: int, prerequisites: List[TalentPrerequisite],
                 commands: List[Dict]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.cost = cost
        self.prerequisites = prerequisites
        self.commands = commands

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        prerequisites = list()
        for model in data['prerequisites']:
            prerequisites.append(TalentPrerequisite.from_json(model))
        data['prerequisites'] = prerequisites
        return cls(**data)


class DivinationModel(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[HintModel], commands: List[Dict], roll_range: List[int]):
        self.tag = tag
        self.name = name
        self.description = description
        self.hints = hints
        self.commands = commands
        self.roll_range = roll_range

    @classmethod
    def from_json(cls, data):
        hints = list()
        for model in data['hints']:
            hints.append(HintModel.from_json(model))
        data['hints'] = hints
        return cls(**data)
