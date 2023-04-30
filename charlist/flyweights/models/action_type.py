from typing import Dict


class CombatActionType(object):
    def __init__(self, tag: str, name: Dict[str, str]):
        self.__tag = tag
        self.__name = name

    def get_tag(self):
        return self.__tag

    def get_names(self):
        return self.__name

    def get_name(self, lang='ru'):
        return self.__name.get(lang)

    def get_name_ru(self):
        return self.get_name('ru')

    def get_name_en(self):
        return self.get_name('en')

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @classmethod
    def from_file(cls, fdata):
        action_types = list()
        for model in fdata['types']:
            action_types.append(cls.from_json(model))
        return action_types
