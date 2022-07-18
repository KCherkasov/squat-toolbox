# -*- coding: utf-8 -*-

from typing import Dict

from charlist.constants.constants import *
from charlist.flyweights.core.tagged_object import TaggedObject


class NamelessDescription(TaggedObject):
    def __init__(self, tag: str, description: Dict[str, str]):
        super().__init__(tag)
        self.__description = description

    def get_description(self,  lang=RU):
        return self.__description.get(lang)

    def get_description_ru(self):
        return self.get_description(RU)

    def get_description_en(self):
        return self.get_description(EN)
