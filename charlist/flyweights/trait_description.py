# -*- coding: utf-8 -*-

from typing import Dict, List

from charlist.flyweights.models.trait_description_model import TraitModel
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.core.hinted_description import Hint


class TraitDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str],
                 hints: List[Hint], is_specialist: bool, is_stackable: bool):
        super().__init__(tag, name, description, hints)
        self.__is_specialist = is_specialist
        self.__is_stackable = is_stackable

    def is_specialist(self):
        return self.__is_specialist

    def is_stackable(self):
        return self.__is_stackable

    @classmethod
    def from_model(cls, model: TraitModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description,
                   hints, model.is_specialist, model.is_stackable)

    @classmethod
    def from_file(cls, fdata):
        trait_descriptions = list()
        for description in fdata['traits']:
            trait_descriptions.append(TraitModel.from_json(description))
        if len(trait_descriptions) > 0:
            traits = list()
            for trait in trait_descriptions:
                traits.append(TraitDescription.from_model(trait))
        else:
            traits = None
        return traits
