# -*- coding: utf-8 -*-

from typing import Dict

from charlist.constants.constants import *
from charlist.flyweights.core.nameless_description import NamelessDescription


class ObjectDescription(NamelessDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        super().__init__(tag, description)
        self.__name = name

    def get_name(self, lang=RU):
        return self.__name.get(lang)

    def get_name_ru(self):
        return self.get_name(RU)

    def get_name_en(self):
        return self.get_name(EN)
