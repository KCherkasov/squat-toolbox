from typing import Dict, List

from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.models.rt_motivation_model import MotivationModel


class Motivation(object):
    def __init__(self, tag: str, name: Dict[str, str], hints: List[Hint], choices: List[List[Dict]],
                 commands: List[Dict], aptitudes: List[str], cost: int):
        self.__tag = tag
        self.__name = name
        self.__hints = hints
        self.__choices = choices
        self.__commands = commands
        self.__aptitudes = aptitudes
        self.__cost = cost

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag()

    def name(self):
        return self.__name

    def hints(self):
        return self.__hints

    def choices(self):
        return self.__choices

    def commands(self):
        return self.__commands

    def aptitudes(self):
        return self.__aptitudes

    def cost(self):
        return self.__cost

    @classmethod
    def from_model(cls, model: MotivationModel):
        hints = list()
        for hm in model.hints:
            hints.append(Hint.from_model(hm))
        return cls(model.tag, model.name, hints, model.choices, model.commands, model.aptitudes, model.cost)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['motivations']:
            models.append(MotivationModel.from_json(model))
        if len(models) > 0:
            motivations = list()
            for model in models:
                motivations.append(Motivation.from_model(model))
        else:
            motivations = None
        return motivations
