from typing import List, Dict

from charlist.flyweights.core.hinted_description import Hint
from charlist.flyweights.models.rt_career_model import CareerModel


class Career(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], hints: List[Hint],
                 aptitudes: List[str], skills: List[Dict], traits: List[Dict], talents: List[Dict],
                 choices: List[List[Dict]], commands: List[Dict]):
        self.__tag = tag
        self.__name = name
        self.__description = description
        self.__hints = hints
        self.__aptitudes = aptitudes
        self.__skills = skills
        self.__traits = traits
        self.__talents = talents
        self.__choices = choices
        self.__commands = commands

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag()

    def name(self):
        return self.__name

    def description(self):
        return self.__description

    def hints(self):
        return self.__hints

    def aptitudes(self):
        return self.__aptitudes

    def skills(self):
        return self.__skills

    def traits(self):
        return self.__traits

    def talents(self):
        return self.__talents

    def choices(self):
        return self.__choices

    def commands(self):
        return self.__commands

    @classmethod
    def from_model(cls, model: CareerModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description, hints, model.aptitudes, model.skills,
                   model.traits, model.talents, model.choices, model.commands)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['careers']:
            models.append(CareerModel.from_json(model))
        if len(models) > 1:
            careers = list()
            for model in models:
                careers.append(Career.from_model(model))
        else:
            careers = None
        return careers
