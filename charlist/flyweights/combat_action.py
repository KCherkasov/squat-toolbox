from typing import Dict, List

from charlist.flyweights.models.combat_action_model import CombatActionModel


class CombatAction(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, List[str]],
                 types: List[str], keywords: List[str]):
        self.__tag = tag
        self.__name = name
        self.__description = description
        self.__types = types
        self.__keywords = keywords

    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag()

    def names(self):
        return self.__name

    def name(self, lang = 'ru'):
        return self.__name.get(lang)

    def name_ru(self):
        return self.name('ru')

    def name_en(self):
        return self.name('en')

    def descriptions(self):
        return self.__description

    def description(self, lang = 'ru'):
        return self.__description.get(lang)

    def description_ru(self):
        return self.description('ru')

    def description_en(self):
        return self.description('en')


    def types(self):
        return self.__types

    def keywords(self):
        return self.__keywords

    @classmethod
    def from_model(cls, model: CombatActionModel):
        return cls(model.tag, model.name, model.description, model.types, model.keywords)

    @classmethod
    def from_file(cls, fdata):
        models = list()
        for model in fdata['actions']:
            models.append(CombatActionModel.from_json(model))
        if len(models) > 0:
            actions = list()
            for action in models:
                actions.append(CombatAction.from_model(action))
        else:
            actions = None
        return actions
