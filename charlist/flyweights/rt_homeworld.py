# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.bonus_description import BonusDescription
from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.models.rt_homeworld_model import RTHomeworldModel


class RTHomeWorldDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint],
                 stat_mods: Dict[str, int], fate: int, blessing: int,
                 bonus: BonusDescription, aptitude: str, wounds: int,
                 skills: List[Dict], skill_choices: List[List[Dict]],
                 talents: List[Dict], talent_choices: List[List[Dict]]):
        super().__init__(tag, name, description, hints)
        self.__stat_mods = stat_mods
        self.__fate = fate
        self.__blessing = blessing
        self.__bonus = bonus
        self.__aptitude = aptitude
        self.__wounds = wounds
        self.__skills = skills
        self.__skill_choices = skill_choices
        self.__talents = talents
        self.__talent_choices = talent_choices

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

    def get_skills(self):
        return self.__skills

    def get_skill_choices(self):
        return self.__skill_choices

    def get_talents(self):
        return self.__talents

    def get_talent_choices(self):
        return self.__talent_choices

    @classmethod
    def from_model(cls, model: RTHomeworldModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        bonus = BonusDescription.from_model(model.bonus)
        return cls(model.tag, model.name, model.description, hints,
                   model.stat_mods, model.fate, model.blessing,
                   bonus, model.aptitude, model.wounds, model.skills,
                   model.skill_choices, model.talents, model.talent_choices)

    @classmethod
    def from_file(cls, fdata):
        hwds = list()
        for hw in fdata['homeworlds']:
            hwds.append(RTHomeworldModel.from_json(hw))
        if len(hwds) > 0:
            homeworlds = list()
            for homeworld in hwds:
                homeworlds.append(RTHomeWorldDescription.from_model(homeworld))
            return homeworlds
        else:
            return None
