from abc import ABC, abstractmethod

from charlist.character.character import CharacterModel


class BaseCommand(ABC):
    def __init__(self, tag: str, facade):
        super(BaseCommand, self).__init__()
        self.__tag = tag
        self.__facade = facade

    def get_tag(self):
        return self.__tag

    def get_facade(self):
        return self.__facade

    def has_alt(self, data):
        if 'alt' in data.keys():
            return True
        return False

    def is_conditional(self, data):
        if 'condition' in data.keys():
            return True
        return False

    def is_skill_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'SK':
                return True
        return False

    def is_talent_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'TL':
                return True
        return False

    def is_trait_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'TR':
                return True
        return False

    def is_background_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'BG':
                return True
        return False

    def condition_met(self, character, data):
        result = None
        if self.is_conditional(data):
            if self.is_background_condition(data):
                result = character.bg_id() == data.get('condition').get('tag')
            if self.is_talent_condition(data):
                if self.get_facade().talent_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        result = character.has_talent_subtag(data.get('condition').get('tag'),
                                                             data.get('condition').get('subtag'))
                    else:
                        return False
                else:
                    result = character.has_talent(data.get('condition').get('tag'))
            if self.is_skill_condition(data):
                if self.get_facade().skill_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        if data.get('condition').get('subtag') == 'SK_ANY':
                            result = data.get('condition').get('tag') in character.skills().keys()
                        else:
                            result = character.has_subskill(data.get('condition').get('tag'),
                                                            data.get('condition').get('subtag'),
                                                            adv=data.get('condition').get('value'))
                    else:
                        return False
                else:
                    result = character.has_skill(data.get('condition').get('tag'),
                                                 adv=data.get('condition').get('value'))
                return result
            if self.is_trait_condition(data):
                if self.get_facade().trait_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        return character.has_trait_subtag(data.get('condition').get('tag'),
                                                          data.get('condition').get('subtag'))
                    else:
                        return False
                else:
                    result = character.has_trait(data.get('condition').get('tag'))
            if data.get('condition').get('value') > 0:
                return result
            return not result
        return False

    def execute(self, character: CharacterModel, data=None):
        return self.do_logic(character, data)

    @abstractmethod
    def do_logic(self, character: CharacterModel, data=None):
        pass

    @abstractmethod
    def is_automatic(self):
        return False
