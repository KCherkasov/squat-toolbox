from typing import Dict


class PsyPowerType(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        self.tag = tag
        self.name = name
        self.description = description

    def get_tag(self):
        return self.tag

    def get_name(self, lang = 'ru'):
        return self.name.get(lang)

    def name_ru(self):
        return self.get_name('ru')

    def name_en(self):
        return self.get_name('en')

    def get_description(self, lang = 'ru'):
        return self.description.get(lang)

    def description_ru(self):
        return self.get_description('ru')

    def description_en(self):
        return self.get_description('en')

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    @classmethod
    def from_file(cls, fdata):
        types = list()
        for model in fdata['types']:
            types.append(PsyPowerType.from_json(model))
        return types
