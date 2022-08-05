# -*- coding: utf-8 -*-

import json

from charlist.character.stat import Stat


class StatDecoder(object):
    @staticmethod
    def decode(obj):
        return Stat.from_json(obj)
