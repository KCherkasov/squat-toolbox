from typing import Dict, List

from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.models.rt_tot_model import TrialAndTravailModel


class TrialAndTravail(object):
    def __init__(self, tag: str, name: Dict[str, str], hints: List[Hint],
                 choices: List[List[Dict]], commands: List[Dict], cost: int):
        self.__tag = tag
        self.__name = name
        self.__hints = hints
        self.__choices = choices
        self.__commmands = commands
        self.__cost = cost

    def tag(self):
        return self.__tag

    def name(self):
        return self.__name

    def hints(self):
        return self.__hints

    def choices(self):
        return self.__choices

    def commands(self):
        return self.__commmands

    def cost(self):
        return self.__cost

    @classmethod
    def from_model(cls, model: TrialAndTravailModel):
        hints = list()
        for hm in model.hints:
            hints.append(Hint.from_model(hm))
        return cls(model.tag, model.name, hints, model.choices, model.commands, model.cost)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['trials']:
            models.append(TrialAndTravailModel.from_json(model))
        if len(models) > 0:
            trials = list()
            for model in models:
                trials.append(TrialAndTravail.from_model(model))
        else:
            trials = None
        return trials
