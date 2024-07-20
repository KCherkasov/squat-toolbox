# -*- coding: utf-8 -*-

from typing import Dict

from charlist.constants.maledictum.tags import *
from charlist.constants.maledictum.constants import *

from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.maledictum.mal_specialization_description_model import MalSpecializationDescriptionModel


class MalSpecializationDescription(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 parent: str, restricted: bool, forbidden: bool):
        super().__init__(tag, name, description)
        self.__parent = parent
        self.__restricted = restricted
        self.__forbidden = forbidden

    def parent(self):
        return self.__parent

    def restricted(self):
        return self.__restricted

    def forbidden(self):
        return self.__forbidden

    @classmethod
    def from_model(cls, model: MalSpecializationDescriptionModel):
        return cls(model.tag, model.name, model.description, model.parent, model.restricted, model.forbidden)

    @classmethod
    def from_file(cls, fdata):
        spec_descriptions = list()
        for spec in fdata[DESCR_TAG]:
            spec_descriptions.append(MalSpecializationDescriptionModel.from_json(spec))
        result_descriptions = list()
        for spec_model in spec_descriptions:
            result_descriptions.append(cls.from_model(spec_model))
        if len(result_descriptions) > IM_ZERO:
            return result_descriptions
        else:
            return None
