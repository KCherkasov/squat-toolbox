from typing import List, Dict
import json

from charlist.constants.tags import *
from charlist.flyweights.rt_flyweights import RTFacade


class RTCreationDataModel(object):
    def __init__(self, name: str = '', hw_id: str = '', birthright_id: str = '',
                 lure_id: str = '', trial_id: str = '', motivation_id: str = '',
                 career_id: str = '', aptitudes: List[str] = None, stats: Dict[str, int] = None,
                 skills: List[Dict] = None, talents: List[Dict] = None,
                 traits: List[Dict] = None, commands: List[Dict] = None, xp: List[int] = None,
                 choices: List[Dict] = None, stat_base: int = 20):
        self.name = name
        self.hw_id = hw_id
        self.birthright_id = birthright_id
        self.lure_id = lure_id
        self.trial_id = trial_id
        self.motivation_id = motivation_id
        self.career_id = career_id
        self.aptitudes = aptitudes
        self.stats = stats
        self.skills = skills
        self.talents = talents
        self.traits = traits
        self.commands = commands
        self.xp = xp
        if choices is None:
            self.choices = list()
        else:
            self.choices = choices
        self.stat_base = stat_base

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        return cls(**data)

    def reset_stats(self, facade: RTFacade):
        hw = facade.rt_homeworlds().get(self.hw_id)
        for key in self.stats.keys():
            md = 0
            if hw is not None:
                md = hw.get_stat_mods().get(key, 0)
            self.stats[key] = self.stat_base + md

    def reset_skills(self, facade: RTFacade):
        self.skills = list()
        if self.hw_id in facade.rt_homeworlds().keys():
            for skill in facade.rt_homeworlds().get(self.hw_id).get_skills():
                self.skills.append(skill)
        if self.career_id in facade.careers().keys():
            for skill in facade.careers().get(self.career_id).skills():
                self.skills.append(skill)

    def reset_talents(self, facade: RTFacade):
        self.talents = list()
        if self.hw_id in facade.rt_homeworlds().keys():
            for talent in facade.rt_homeworlds().get(self.hw_id).get_talents():
                self.talents.append(talent)
        if self.career_id in facade.careers().keys():
            for talent in facade.careers().get(self.career_id).talents():
                self.talents.append(talent)

    def reset_traits(self, facade: RTFacade):
        self.traits = list()
        if self.career_id in facade.careers().keys():
            for trait in facade.careers().get(self.career_id).traits():
                self.talents.append(trait)

    def reset_apts(self, facade: RTFacade):
        reset = ['A_GEN']
        if self.hw_id in facade.rt_homeworlds().keys():
            reset.append(facade.rt_homeworlds().get(self.hw_id).aptitude())
        if self.career_id in facade.careers().keys():
            for apt in facade.careers().get(self.career_id).aptitudes():
                reset.append(apt)
        if len(self.choices) > 0:
            for choice in self.choices:
                if choice.get('tag')[:2] == 'A_':
                    reset.append(choice.get('tag'))
        self.aptitudes = reset

    def full_reset(self, facade: RTFacade):
        self.reset_skills(facade)
        self.reset_talents(facade)
        self.reset_traits(facade)

    @classmethod
    def new_cd(cls, name: str, xp: int, stat_base: int):
        aptitudes = [A_GENERAL]
        stats = dict()
        for tag in RT_STAT_TAGS:
            stats[tag] = stat_base
        skills = list()
        talents = list()
        traits = list()
        commands = list()
        xp_list = [0, xp]
        return cls(name, aptitudes=aptitudes, stats=stats,
                   skills=skills, talents=talents, traits=traits,
                   commands=commands, xp=xp_list, stat_base=stat_base)

    def count_doubles(self):
        doubled = 0
        for i in range(len(self.aptitudes)):
            for j in range(i, len(self.aptitudes)):
                if self.aptitudes[i] == self.aptitudes[j]:
                    doubled += 1
        return doubled

    def simplify_apts(self):
        simplified_apts = list()
        for apt in self.aptitudes:
            if apt not in simplified_apts:
                simplified_apts.append(apt)
        return simplified_apts

    def to_commands(self):
        for skill in self.skills:
            cmd = {'command': 'GainSkill', 'tag': skill.get('tag')}
            if 'subtag' in skill.keys():
                cmd['subtag'] = skill.get('subtag')
            self.commands.append(cmd)
        for talent in self.talents:
            cmd = {'command': 'GainTalent', 'tag': talent.get('tag')}
            if 'subtag' in talent.keys():
                cmd['subtag'] = talent.get('subtag')
            self.commands.append(cmd)
        for trait in self.traits:
            cmd = {'command': 'GainTrait', 'tag': trait.get('tag')}
            if 'subtag' in trait.keys():
                cmd['subtag'] = trait.get('subtag')
            self.commands.append(cmd)

    def to_json(self):
        fields_preset = self.__dict__
        fields = dict()
        for key, val in fields_preset.items():
            fields[key] = val
        return json.dumps(self, default=lambda o: fields, sort_keys=True, indent=4)
