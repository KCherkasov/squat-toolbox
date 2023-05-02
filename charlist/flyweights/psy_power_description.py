from typing import Dict, List

from charlist.flyweights.models.prerequisite import Prerequisite
from charlist.flyweights.models.psy_powerr_description_model import PsyPowerDescriptionModel


class PsyPowerDescription(object):
    def __init__(self, tag: str, name: Dict[str, str], description: [str, List[str]],
                 school: str, types: List[str], effect: Dict, cost: int,
                 prerequisites: List[Prerequisite], sustainable: bool,
                 focus_check: str, focus_mod: int, focus_opposed: bool,
                 ranges: int, action: str, keywords: List[str], sustain=None):
        self.__tag = tag
        self.__name = name
        self.__description = description
        self.__school = school
        self.__type = types
        self.__effect = effect
        self.__cost = cost
        self.__prerequisites = prerequisites
        self.__sustainable = sustainable
        self.__sustain = sustain
        self.__focus_check = focus_check
        self.__focus_mod = focus_mod
        self.__focus_opposed = focus_opposed
        self.__range = ranges
        self.__action = action
        self.__keywords = keywords

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag()

    def name(self):
        return self.__name

    def name_ru(self):
        return self.__name.get('ru')

    def name_en(self):
        return self.__name.get('en')

    def description(self):
        return self.__description

    def school(self):
        return self.__school

    def type(self):
        return self.__type

    def effect(self):
        return self.__effect

    def cost(self):
        return self.__cost

    def prerequisites(self):
        return self.__prerequisites

    def sustainable(self):
        return self.__sustainable

    def sustain(self):
        return self.__sustain

    def focus_check(self):
        return self.__focus_check

    def focus_mod(self):
        return self.__focus_mod

    def focus_opposed(self):
        return self.__focus_opposed

    def base_range(self):
        return self.__range

    def range(self, pr: int):
        return self.__range * pr

    def action(self):
        return self.__action

    def keywords(self):
        return self.__keywords

    def is_attack(self):
        return ('PT_BOLT' in self.type()) or ('PT_BAR' in self.type())\
            or ('PT_STORM' in self.type()) or ('PT_BLAST' in self.type())

    def parse_attack_effect(self):
        if self.is_attack():
            effect = str(self.effect().get('count')).join('d').join(str(self.effect().get('dice')))
            if 'bonus' in self.effect().keys():
                if self.effect().get('bonus') == 'WPB' or self.effect().get('bonus') > 0:
                    effect.join('+').join(str(self.effect().get('bonus')))
            if 'pr_bonus' in self.effect().keys():
                if self.effect().get('pr_bonus') > 0:
                    if self.effect().get('pr_bonus') > 1:
                        effect.join('+').join(str(self.effect().get('pr_bonus'))).join('xPR')
                    else:
                        effect.join('+PR')
            if 'cp_bonus' in self.effect().keys():
                if self.effect().get('cp_bonus') > 0:
                    if self.effect().get('cp_bonus') > 1:
                        effect.join('+').join(str(self.effect().get('cp_bonus'))).join('xCPB')
                    else:
                        effect.join('+CPB')
        else:
            effect = None
        return effect

    @classmethod
    def from_model(cls, model: PsyPowerDescriptionModel):
        return cls(model.tag, model.name, model.description, model.school,
                   model.type, model.effect, model.cost, model.prerequisites,
                   model.sustainable, model.focus_check, model.focus_mod, model.focus_opposed,
                   model.range, model.action, model.keywords, model.sustain)

    @classmethod
    def from_file(cls, fdata):
        psy_models = list()
        for model in fdata['powers']:
            psy_models.append(PsyPowerDescriptionModel.from_json(model))
        if len(psy_models) > 0:
            psy_powers = list()
            for pm in psy_models:
                psy_powers.append(cls.from_model(pm))
        else:
            psy_powers = None
        return psy_powers
