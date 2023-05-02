from typing import Dict, List

from charlist.flyweights.models.rt_lov_model import LureOfTheVoidModel
from charlist.flyweights.core.hinted_description import Hint


class LureOfTheVoid(object):
    def __init__(self, tag: str, name: Dict[str, str], hints: List[Hint], choices: List[List[Dict]],
                 commands: List[Dict], cost: int):
        self.__tag = tag
        self.__name = name
        self.__choices = choices
        self.__commands = commands
        self.__cost = cost

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag()

    def name(self):
        return self.__name

    def choices(self):
        return self.__choices

    def commands(self):
        return self.__commands

    def cost(self):
        return self.__cost

    @classmethod
    def from_model(cls, model: LureOfTheVoidModel):
        hints = list()
        for hm in model.hints:
            hints.append(Hint.from_model(hm))
        return cls(model.tag, model.name, hints, model.choices, model.commands, model.cost)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['lures']:
            models.append(LureOfTheVoidModel.from_json(model))
        if len(models) > 0:
            lures = list()
            for lure in models:
                lures.append(LureOfTheVoid.from_model(lure))
        else:
            lures = None
        return lures
