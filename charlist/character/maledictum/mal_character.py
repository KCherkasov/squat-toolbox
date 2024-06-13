# -*- coding: utf-8 -*-

import json

from charlist.character.helpers import *

from charlist.constants.maledictum.constants import *
from charlist.constants.maledictum.tags import *
from charlist.character.maledictum.mal_stat import MalStat
from charlist.character.maledictum.mal_skill import MalSkill
from charlist.character.maledictum.mal_specialization import MalSpecialization


class MalCharacterModel(object):
    def __init__(self, cid: int, name: str, xp: List[int],
                 origin: str,
                 fate: List[int], wounds: int,
                 stats: Dict[str, MalStat],
                 skills: Dict[str, MalSkill]):
        self.__cid = cid
        self.__name = name
        self.__xp = xp
        self.__origin = origin
        self.__fate = fate
        self.__wounds = wounds
        self.__stats = stats
        self.__skills = skills

    def is_rt(self):
        return False

    def is_im(self):
        return True

    def id(self):
        return self.__cid

    def name(self):
        return self.__name

    def xp(self):
        return self.__xp

    def xp_current(self):
        return self.xp()[IM_CUR_ID]

    def xp_spent(self):
        return self.xp()[IM_SPENT_ID]

    def xp_total(self):
        return self.xp_current() + self.xp_spent()

    def get_xp(self, amount: int):
        if amount > IM_ZERO:
            self.__xp[IM_CUR_ID] += amount
            return True
        else:
            return False

    def spend_xp(self, amount: int):
        if amount > self.xp_current():
            return False
        else:
            self.__xp[IM_CUR_ID] -= amount
            self.__xp[IM_SPENT_ID] += amount
            return True

    def origin(self):
        return self.__origin

    def fate(self):
        return self.__fate

    def fate_current(self):
        return self.fate()[IM_CUR_ID]

    def fate_cap(self):
        return self.fate()[IM_CAP_ID]

    def spend_fate(self):
        if self.fate_current() > IM_ZERO:
            self.__fate[IM_CUR_ID] -= IM_ONE
            return True
        else:
            return False

    def burn_fate(self):
        if self.__fate[IM_CAP_ID] > 0:
            self.__fate[IM_CAP_ID] -= 1
            if self.__fate[IM_CAP_ID] > self.__fate[IM_CUR_ID]:
                self.__fate[IM_CUR_ID] = self.__fate[IM_CAP_ID]
            return True
        else:
            return False

    def restore_fate(self):
        self.__fate[IM_CUR_ID] = self.__fate[IM_CAP_ID]

    def gain_fate(self, amount: int):
        if amount > IM_ZERO:
            self.__fate[IM_CAP_ID] += amount

    def initiative(self):
        return self.__stats.get(ST_AGILITY).bonus() + self.__stats.get(ST_PERCEPTION).bonus()

    def wounds(self):
        return self.__wounds

    def wounds_cap(self):
        wnd = self.__stats.get(ST_STRENGTH).bonus() + self.__stats.get(ST_TOUGHNESS).bonus()\
               + self.__stats.get(ST_TOUGHNESS).bonus() + self.__stats.get(ST_WILLPOWER).bonus()
        return wnd

    def wounds_current(self):
        return self.__wounds

    def damage(self, dmg: int):
        if dmg > IM_ZERO:
            self.__wounds -= dmg
            return True
        else:
            return False

    def heal(self, hld: int):
        if hld > IM_ZERO:
            self.__wounds += hld
            if self.__wounds > self.wounds_cap():
                self.__wounds = self.wounds_cap()
            return True
        else:
            return False

    def stats(self):
        return self.__stats

    def advance_stat(self, stat: str):
        if stat in self.stats().keys():
            if self.stats().get(stat).is_upgradeable():
                self.__stats.get(stat).upgrade()

    def advance_stat_5(self, stat: str):
        if stat in self.stats().keys():
            if self.stats().get(stat).is_upgradeable():
                self.__stats.get(stat).upgrade_5()

    def advance_stat_10(self, stat: str):
        if stat in self.stats().keys():
            if self.stats().get(stat).is_upgradeable():
                self.__stats.get(stat).upgrade_10()

    def improve_stat(self, stat: str, amount: int):
        if (stat in self.stats().keys()) and (amount > IM_ZERO):
            self.__stats.get(stat).improve(amount)

    def damage_stat(self, stat: str, amount: int):
        if (stat in self.stats().keys()) and (amount > IM_ZERO):
            self.__stats.get(stat).damage(amount)

    def skills(self):
        return self.__skills

    def skill(self, tag: str):
        return self.skills().get(tag)

    def get_skill_diff(self, tag: str, stat: str):
        if (tag not in self.skills().keys()) or (stat not in self.stats().keys()):
            return None
        diff = self.stats().get(stat).value() + self.skills().get(tag).adv_bonus()
        return diff

    def get_subskill_diff(self, tag: str, subskill: str, stat: str):
        if (tag not in self.skills().keys()) \
                or (not self.skills().get(tag).has_specialization(subskill)) \
                or (stat not in self.stats().keys()):
            return None
        diff = self.stats().get(stat).value() + self.skills().get(tag).specialization_adv_bonus(subskill)
        return diff

    @classmethod
    def from_json(cls, sdata: str):
        data = json.loads(sdata)
        stats = dict()
        for stat_key, stat in data[CHAR_STAT_TAG]:
            stats[stat_key] = MalStat.from_json(stat)
        data[CHAR_STAT_TAG] = stats
        skills = dict()
        for skill_key, skill in data[CHAR_SKILL_TAG]:
            skills[skill_key] = MalSkill.from_json(skill)
        data[CHAR_SKILL_TAG] = skills
        return cls(**data)

    def toJSON(self):
        fields = dict()
        data = self.__dict__
        for key, val in data.items():
            field_key = key[20:]
            if field_key in SPECIAL_CHARACTER_TAGS:
                if field_key == CHAR_STAT_TAG:
                    stats = dict()
                    for skey, sval in self.stats().items():
                        stats[skey] = sval.toJSON()
                    fields[CHAR_STAT_TAG] = stats
                if field_key == CHAR_SKILL_TAG:
                    skills = dict()
                    for skey, sval in self.skills().items():
                        skills[skey] = sval.toJSON()
                    fields[CHAR_SKILL_TAG] = skills
            else:
                fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=JSON_INDENT)

