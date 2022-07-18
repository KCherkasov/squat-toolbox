# -*- coding: utf-8 -*-


from typing import Dict

from charlist.flyweights.core.object_description import ObjectDescription
from charlist.flyweights.models.aptitude_model import AptitudeModel


class Aptitude(ObjectDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        super().__init__(tag, name, description)

    @classmethod
    def from_model(cls, model: AptitudeModel):
        return cls(model.tag, model.name, model.description)

    @classmethod
    def from_file(cls, fdata):
        aptitudes = list()
        for apt in fdata['aptitudes']:
            aptitudes.append(AptitudeModel.from_json(apt))
        apts = list()
        if len(aptitudes) > 0:
            for apt in aptitudes:
                apts.append(cls.from_model(apt))
        else:
            apts = None
        return apts
