# -*- coding: utf-8 -*-

from charlist.character.skill import Skill


class SkillDecoder(object):
    @staticmethod
    def decode(obj):
        return Skill.from_json(obj)
