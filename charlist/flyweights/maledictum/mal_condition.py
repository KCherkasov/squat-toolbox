# -*- coding: utf-8 -*-

from charlist.constants.maledictum.constants import *


class MalCondition(object):
    def __init__(self, tag: str, value: int):
        self.tag = tag
        self.value = value

    def abs_value(self):
        return abs(self.value)

    def is_stat(self):
        return self.tag[PREFIX_LENGTH:] == PREREQ_STAT_PREFIX

    def match_as_stat(self, character):
        if self.value < IM_ZERO:
            return character.stats().get(self.tag) <= self.abs_value()
        else:
            return character.stats().get(self.tag) >= self.value

    def is_skill(self):
        return self.tag[PREFIX_LENGTH:] == PREREQ_SKILL_PREFIX

    def match_as_skill(self, character):
        return character.skills().get(self.tag).advances() >= self.value

    def is_specialization(self):
        return self.tag[PREFIX_LENGTH:] == PREREQ_SPEC_PREFIX

    def match_as_spec(self, character):
        for tag, skill in character.skills().items():
            if skill.has_specialization(self.tag):
                return skill.specialization(self.tag).advances() >= self.value
        return False

    def is_talent(self):
        return self.tag[PREFIX_LENGTH:] == PREREQ_TALENT_PREFIX

    def match_as_talent(self, character):
        if self.value > IM_ZERO:
            return character.has_talent(self.tag)
        else:
            return not character.has_talent(self.tag)

    def is_faction(self):
        return self.tag[PREFIX_LENGTH:] == PREREQ_FACTION_PREFIX

    def match_as_faction(self, character):
        return self.tag == character.faction()

    def matched(self, character):
        if self.is_stat():
            return self.match_as_stat(character)
        if self.is_skill():
            return self.match_as_skill(character)
        if self.is_specialization():
            return self.match_as_spec(character)
        if self.is_talent():
            return self.match_as_talent(character)
        if self.is_faction():
            return self.match_as_faction(character)
        return False

    @classmethod
    def from_json(cls, data):
        return cls(**data)
