# -*- coding: utf-8 -*-

from charlist.character.trait import Trait


class TraitDecoder(object):
    @staticmethod
    def decode(obj):
        return Trait.from_json(obj)
