# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.bonus_description_model import BonusDescriptionModel


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
