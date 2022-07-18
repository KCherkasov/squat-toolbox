# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.bonus_description import BonusDescription
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.models.background_description_model import BackgroundModel


class BackgroundDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str],
                 aptitudes: List[str], apt_choices: List[str],
                 skills: List[Dict[str, str]], skill_choices: List[List[Dict[str, str]]],
                 talents: List[Dict[str, str]], talent_choices: List[List[Dict]],
                 traits: List[Dict], trait_choices: List[Dict], equipment: List[str], bonus: BonusDescription):
        super().__init__(tag, name, description, list())
        self.__aptitudes = aptitudes
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

    @classmethod
    def from_model(cls, model: BackgroundModel):
        bonus = BonusDescription.from_model(model.bonus)
        return cls(model.tag, model.name, model.description, model.aptitudes, model.apt_choices,
                   model.skills, model.skill_choices, model.talents, model.talent_choices,
                   model.traits, model.traits_choices, model.equipment, bonus)

    @classmethod
    def from_file(cls, fdata):
        bgds = list()
        for bg in fdata['backgrounds']:
            bgds.append(BackgroundModel.from_json(bg))
        if len(bgds) > 0:
            backgrounds = list()
            for bg in bgds:
                backgrounds.append(BackgroundDescription.from_model(bg))
            return backgrounds
        else:
            return None
