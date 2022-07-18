# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.constants.constants import *
from charlist.flyweights.core.hint import Hint
from charlist.flyweights.core.object_description import ObjectDescription


class HintedDescription(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], hints: List[Hint]):
        super().__init__(tag, name, description)
        self.__hints = hints

    def get_hints(self):
        return self.__hints

    def get_hints_str(self, lang=RU):
        res = u''
        for hint in self.__hints:
            res += hint.get_description(lang) + '\n'
        return res

    def get_description(self, lang=RU):
        res = super().get_description(lang)
        for hint in self.__hints:
            res += '\n\n'
            res += hint.get_description(lang)
        return res

    def get_short_description(self, lang=RU):
        return super().get_description(lang)

    def get_full_description_ru(self):
        return self.get_description(RU)

    def get_full_description_en(self):
        return self.get_description(EN)

    def get_short_description_ru(self):
        return self.get_short_description(RU)

    def get_short_description_en(self):
        return self.get_short_description(EN)