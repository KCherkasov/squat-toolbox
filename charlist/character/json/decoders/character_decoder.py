# -*- coding: utf-8 -*-

from charlist.character.character import CharacterModel
from charlist.character.rt_character import RTCharacterModel


class CharacterDecoder(object):
    @staticmethod
    def decode(obj: str, is_rt: bool):
        if not is_rt:
            return CharacterModel.from_json(obj)
        else:
            return RTCharacterModel.from_json(obj)
