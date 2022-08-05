# -*- coding: utf-8 -*-

import json

from charlist.character.talent import Talent


class TalentDecoder(object):
    @staticmethod
    def decode(obj):
        return Talent.from_json(obj)
