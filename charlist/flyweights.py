# -*- coding: utf-8 -*-

from .constants import *
from .datamodels import *


class TaggedObject(object):
    def __init__(self, tag=''):
        self.__tag = tag

    def get_tag(self):
        return self.__tag


class NamelessDescription(TaggedObject):
    def __init__(self, tag, description):
        super().__init__(tag)
        self.__description = description

    def get_description(self,  lang=RU):
        return self.__description[lang]

    def get_description_ru(self):
        return self.get_description(RU)

    def get_description_en(self):
        return self.get_description(EN)


class ObjectDescription(NamelessDescription):
    def __init__(self, tag, name, description):
        super().__init__(tag, description)
        self.__name = name

    def get_name(self, lang=RU):
        return self.__name[lang]

    def get_name_ru(self):
        return self.get_name(RU)

    def get_name_en(self):
        return self.get_name(EN)


class Aptitude(ObjectDescription):
    def __init__(self, tag, name, description):
        super().__init__(tag, name, description)

    @classmethod
    def from_model(cls, model: AptitudeModel):
        return cls(model.tag, model.name, model.description)


class Aptitudes(object):
    def __init__(self):
        self.apts = list()

    def from_file(self, fdata):
        aptitudes = list()
        for apt in fdata['aptitudes']:
            aptitudes.append(AptitudeModel.from_json(apt))
        for apt in aptitudes:
            self.apts.append(Aptitude.from_model(apt))


class StatDescription(ObjectDescription):
    def __init__(self, tag,
                 name, description,
                 upgradeable, aptitudes):
        super().__init__(tag, name, description)
        self.__upgradeable = upgradeable
        self.__aptitudes = aptitudes

    def is_upgradeable(self):
        return self.__upgradeable

    def get_aptitudes(self):
        return self.__aptitudes


class SkillDescription(ObjectDescription):
    def __init__(self, tag,
                 name, description,
                 aptitudes, stats):
        super().__init__(tag, name, description)
        self.__aptitudes = aptitudes
        self.__stats = stats

    def get_aptitudes(self):
        return self.__aptitudes

    def get_stats(self):
        return self.__stats

    def get_primary_stat(self):
        return self.__stats[0]

    def get_alt_stats(self):
        return self.__stats[1:]


class Hint(NamelessDescription):
    def __init__(self, tag, description, target):
        super().__init__(tag, description)
        self.__target = target

    def get_target(self):
        return self.__target


class HintedDescription(ObjectDescription):
    def __init__(self, tag, name, description, hints):
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


class TalentDescription(HintedDescription):
    def __init__(self, tag, name, description,
                 hints, tier, aptitudes):
        super().__init__(tag, name, description, hints)
        self.__tier = tier
        self.__aptitudes = aptitudes

    def get_tier(self):
        return self.__tier

    def get_aptitudes(self):
        return self.__aptitudes


class BonusDescription(HintedDescription):
    def __init__(self, tag, name, description, hints, commands):
        super().__init__(tag, name, description, hints)
        self.__commands = commands

    def get_commands(self):
        return self.__commands


class HomeWorldDescription(HintedDescription):
    def __init__(self, tag, name, description, hints, stat_mods,
                 fate, blessing, bonus, aptitude, wounds):
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
    def __init__(self, tag, name, description, hints, aptitudes, apt_choices, skills, skill_choices):
        super().__init__(tag, name, description, hints)
