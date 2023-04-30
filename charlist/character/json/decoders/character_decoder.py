# -*- coding: utf-8 -*-

from charlist.character.character import CharacterModel
from charlist.character.rt_character import RTCharacterModel


class CharacterDecoder(object):
    @staticmethod
    def decode(obj: str):
        if isinstance(obj, CharacterModel):
            return CharacterModel.from_json(obj)
        if isinstance(obj, RTCharacterModel):
            return RTCharacterModel.from_json(obj)
