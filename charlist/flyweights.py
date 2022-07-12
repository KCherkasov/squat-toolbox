# -*- coding: utf-8 -*-
import json
from typing import List, Dict

from .constants import *
from .datamodels import *
from .tags import *


class TaggedObject(object):
    def __init__(self, tag=''):
        self.__tag = tag

    def get_tag(self):
        return self.__tag


class NamelessDescription(TaggedObject):
    def __init__(self, tag: str, description: Dict[str, str]):
        super().__init__(tag)
        self.__description = description

    def get_description(self,  lang=RU):
        return self.__description.get(lang)

    def get_description_ru(self):
        return self.get_description(RU)

    def get_description_en(self):
        return self.get_description(EN)


class ObjectDescription(NamelessDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        super().__init__(tag, description)
        self.__name = name

    def get_name(self, lang=RU):
        return self.__name.get(lang)

    def get_name_ru(self):
        return self.get_name(RU)

    def get_name_en(self):
        return self.get_name(EN)


class Aptitude(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        super().__init__(tag, name, description)

    @classmethod
    def from_model(cls, model: AptitudeModel):
        return cls(model.tag, model.name, model.description)

    @classmethod
    def from_file(cls, fdata):
        aptitudes = list()
        for apt in fdata['aptitudes']:
            aptitudes.append(AptitudeModel.from_json(apt))
        apts = list()
        if len(aptitudes) > 0:
            for apt in aptitudes:
                apts.append(cls.from_model(apt))
        else:
            apts = None
        return apts


class StatDescription(ObjectDescription):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 upgradeable: bool, aptitudes: List[str]):
        super().__init__(tag, name, description)
        self.__upgradeable = upgradeable
        self.__aptitudes = aptitudes

    def is_upgradeable(self):
        return self.__upgradeable

    def get_aptitudes(self):
        return self.__aptitudes

    @classmethod
    def from_model(cls, model: StatDescriptionModel):
        return cls(model.tag, model.name, model.description, model.upgradeable, model.aptitudes)

    @classmethod
    def from_file(cls, fdata):
        stat_descriptions = list()
        for stat_description in fdata['descriptions']:
            stat_descriptions.append(StatDescriptionModel.from_json(stat_description))
        result_descriptions = list()
        if len(stat_descriptions) > 0:
            for stat_description in stat_descriptions:
                result_descriptions.append(cls.from_model(stat_description))
        else:
            result_descriptions = None
        return result_descriptions


class SkillDescription(ObjectDescription):
    def __init__(self, tag: str,
                 name: Dict[str, str], description: Dict[str, str],
                 aptitudes: List[str], stats: List[str], is_specialist: bool):
        super().__init__(tag, name, description)
        self.__aptitudes = aptitudes
        self.__stats = stats
        self.__is_specialist = is_specialist

    def get_aptitudes(self):
        return self.__aptitudes

    def get_stats(self):
        return self.__stats

    def get_primary_stat(self):
        return self.__stats[0]

    def get_alt_stats(self):
        if len(self.__stats) > 1:
            return self.__stats[1:]
        else:
            return None

    def is_specialist(self):
        return self.__is_specialist

    @classmethod
    def from_model(cls, model: SkillDescriptionModel):
        return cls(model.tag, model.name, model.description,
                   model.aptitudes, model.stats, model.is_specialist)

    @classmethod
    def from_file(cls, fdata):
        skill_descriptions = list()
        for skill_description in fdata['skills']:
            skill_descriptions.append(SkillDescriptionModel.from_json(skill_description))
        result_descriptions = list()
        if len(skill_descriptions) > 0:
            for description in skill_descriptions:
                result_descriptions.append(cls.from_model(description))
        else:
            result_descriptions = None
        return result_descriptions


class Hint(NamelessDescription):
    def __init__(self, tag: str, description: Dict[str, str], target: List[str]):
        super().__init__(tag, description)
        self.__target = target

    def get_target(self):
        return self.__target

    @classmethod
    def from_model(cls, model: HintModel):
        return cls(model.tag, model.description, model.targets)


class HintedDescription(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint]):
        super().__init__(tag, name, description)
        self.__hints = hints

    def get_hints(self):
        return self.__hints

    def get_hints_str(self, lang=RU):
        res = u''
        for hint in self.__hints:
            res += hint.get_description(lang) + '\n'
        return res

    def get_description(self, lang=RU):
        return super().get_description(lang).join('\n\n').join(self.get_hints_str(lang))

    def get_short_description(self, lang=RU):
        return super().get_description(lang)

    def get_full_description_ru(self):
        return self.get_description(RU)

    def get_full_description_en(self):
        return self.get_description(EN)

    def get_short_description_ru(self):
        return self.get_short_description(RU)

    def get_short_description_en(self):
        return self.get_short_description(EN)


class TalentDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 tier: int, aptitudes: List[str], prerequisites: List[TalentPrerequisite],
                 is_specialist: bool, is_stackable: bool):
        super().__init__(tag, name, description, hints)
        self.__tier = tier
        self.__aptitudes = aptitudes
        self.__prerequisites = prerequisites
        self.__is_specialist = is_specialist
        self.__is_stackable = is_stackable

    def get_tier(self):
        return self.__tier

    def get_aptitudes(self):
        return self.__aptitudes

    def has_prerequisites(self):
        return len(self.__prerequisites) > 0

    def get_prerequisites(self):
        return self.__prerequisites

    def is_specialist(self):
        return self.__is_specialist

    def is_stackable(self):
        return self.__is_stackable

    @classmethod
    def from_model(cls, model: TalentDescriptionModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description,
                   hints, model.tier, model.aptitudes, model.prerequisites,
                   model.is_specialist, model.is_stackable)

    @classmethod
    def from_file(cls, fdata):
        talent_descriptions = list()
        for description in fdata['talents']:
            talent_descriptions.append(TalentDescriptionModel.from_json(description))
        if len(talent_descriptions) > 0:
            talents = list()
            for talent in talent_descriptions:
                talents.append(TalentDescription.from_model(talent))
        else:
            talents = None
        return talents


class BonusDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 commands):
        super().__init__(tag, name, description, hints)
        self.__commands = commands

    def get_commands(self):
        return self.__commands


class HomeWorldDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 stat_mods: Dict[str, int], fate: int, blessing: int,
                 bonus: BonusDescription, aptitude: str, wounds: int):
        super().__init__(tag, name, description, hints)
        self.__stat_mods = stat_mods
        self.__fate = fate
        self.__blessing = blessing
        self.__bonus = bonus
        self.__aptitude = aptitude
        self.__wounds = wounds

    def get_stat_mods(self):
        return self.__stat_mods

    def get_fate(self):
        return self.__fate

    def get_blessing(self):
        return self.__blessing

    def get_bonus(self):
        return self.__bonus

    def get_aptitude(self):
        return self.__aptitude

    def get_wounds(self):
        return self.__wounds


class RoleDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 aptitudes: List[str], apt_choices: List[str],
                 talent_choices: List[str], bonus: BonusDescription):
        super().__init__(tag, name, description, hints)
        self.__aptitudes = aptitudes
        self.__apt_choices = apt_choices
        self.__talent_choices = talent_choices
        self.__bonus = bonus

    def get_aptitudes(self):
        return self.__aptitudes

    def get_apt_choices(self):
        return self.__apt_choices

    def get_talent_choices(self):
        return self.__talent_choices

    def get_bonus(self):
        return self.__bonus


class BackgroundDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 aptitudes: List[str], apt_choices: List[str],
                 skills: List[Dict[str, str]], skill_choices: List[List[Dict[str, str]]],
                 talents: List[Dict[str, str]], talent_choices: List[Dict[str, str]],
                 traits: List[str], trait_choices: List[Dict[str, str]], equipment: List[str], bonus: BonusDescription):
        super().__init__(tag, name, description, hints)
        self.__aptitudes  = aptitudes
        self.__apt_choices = apt_choices
        self.__skills = skills
        self.__skill_choices = skill_choices
        self.__talents = talents
        self.__talent_choices = talent_choices
        self.__traits = traits
        self.__traits_choices = trait_choices
        self.__equipment = equipment
        self.__bonus = bonus

    def get_aptitudes(self):
        return self.__aptitudes

    def get_apt_choices(self):
        return self.__apt_choices

    def get_skills(self):
        return self.__skills

    def get_skill_choices(self):
        return self.__skill_choices

    def get_talents(self):
        return self.__talents

    def get_talent_choices(self):
        return self.__talent_choices

    def get_traits(self):
        return self.__traits

    def get_traits_choices(self):
        return self.__traits_choices

    def get_equipment(self):
        return self.__equipment

    def get_bonus(self):
        return self.__bonus


def to_map(lst):
    res_map = dict()
    for item in lst:
        res_map[item.get_tag()] = item
    return res_map


# resource paths order
# 0 - aptitude models
# 1 - stat description models
# 2 - skill description models
# 3 - talent description models
class Facade:
    def __init__(self, resources_paths):
        prefix = 'static/json/'
        aptitudes = Aptitude.from_file(
            json.load(open(prefix + resources_paths[0], 'r', encoding='utf-8')))
        self.__aptitudes = to_map(aptitudes)
        stat_descriptions = StatDescription.from_file(
            json.load(open(prefix + resources_paths[1], 'r', encoding='utf-8')))
        self.__stat_descriptions = to_map(stat_descriptions)
        skill_descriptions = SkillDescription.from_file(
            json.load(open(prefix + resources_paths[2], 'r', encoding='utf-8')))
        self.__skill_descriptions = to_map(skill_descriptions)
        talent_descriptions = TalentDescription.from_file(
            json.load(open(prefix + resources_paths[3], 'r', encoding='utf-8')))
        self.__talent_descriptions = to_map(talent_descriptions)
        self.__spec_skills_subtags = SUBTAG_SKILLS_MAP

    def aptitudes(self):
        return self.__aptitudes

    def stat_descriptions(self):
        return self.__stat_descriptions

    def skill_descriptions(self):
        return self.__skill_descriptions

    def talent_descriptions(self):
        return self.__talent_descriptions

    def spec_skills_subtags(self):
        return self.__spec_skills_subtags
