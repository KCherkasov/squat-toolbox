# -*- coding: utf-8 -*-

from charlist.character.character import CharacterModel
from charlist.character.rt_character import RTCharacterModel
from charlist.character.maledictum.mal_character import MalCharacterModel


class CharacterDecoder(object):
    @staticmethod
    def decode(obj: str, is_rt: bool, is_mal: bool):
        if not is_rt:
            if not is_mal:
                return CharacterModel.from_json(obj)
            else:
                return MalCharacterModel.from_json(obj)
        else:
            return RTCharacterModel.from_json(obj)
