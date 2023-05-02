from typing import Dict, List

from charlist.flyweights.models.rt_birthright_model import BirthrightModel


class Birthright(object):
    def __init__(self, tag: str, name: Dict[str, str], choices: List[List[Dict]],
                 commands: List[Dict], aptitude_choices: List[str], cost: int):
        self.__tag = tag
        self.__name = name
        self.__choices = choices
        self.__commands = commands
        self.__aptitude_choices = aptitude_choices
        self.__cost = cost

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.__tag

    def name(self):
        return self.__name

    def choices(self):
        return self.__choices

    def commands(self):
        return self.__commands

    def aptitude_choices(self):
        return self.__aptitude_choices

    def cost(self):
        return self.__cost

    @classmethod
    def from_model(cls, model: BirthrightModel):
        return cls(model.tag, model.name, model.choices, model.commands, model.aptitude_choices, model.cost)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['birthrights']:
            models.append(BirthrightModel.from_json(model))
        if len(models) > 0:
            birthrights = list()
            for model in models:
                birthrights.append(Birthright.from_model(model))
        else:
            birthrights = None
        return birthrights
