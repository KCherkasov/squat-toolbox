from typing import Dict, List
from charlist.flyweights.models.psy_school_description_model import PsySchoolDescriptionModel


class PsySchoolDescription(object):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str]):
        self.__tag = tag
        self.__name = name
        self.__description = description

    def tag(self):
        return self.__tag

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

    def description(self, lang='ru'):
        return self.__description.get(lang)

    def description_ru(self):
        return self.description('ru')

    def description_en(self):
        return self.description('en')

    @classmethod
    def from_model(cls, data: PsySchoolDescriptionModel):
        return cls(data.tag, data.name, data.description)

    @classmethod
    def from_file(cls, fdata):
        school_models = list()
        for model in fdata['schools']:
            school_models.append(PsySchoolDescriptionModel.from_json(model))
        if len(school_models) > 0:
            psy_schools = list()
            for model in school_models:
                psy_schools.append(PsySchoolDescription.from_model(model))
        else:
            psy_schools = None
        return psy_schools
