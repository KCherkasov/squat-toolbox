# -*- coding: utf-8 -*-

from charlist.character.character import CharacterModel


class CharacterDecoder(object):
    @staticmethod
    def decode(obj: str):
        return CharacterModel.from_json(obj)
