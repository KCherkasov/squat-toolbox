import charlist.constants.tags
from charlist.character.character import CharacterModel
from charlist.forms.player_todos.base_command import BaseCommand
from charlist.flyweights.flyweights import Facade
from charlist.forms.player_todos.command_tags import *


class GainTraitCommand(BaseCommand):
    def __init__(self, facade: Facade):
        super(GainTraitCommand, self).__init__(GET_TRAIT_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character: CharacterModel, data=None):
        if data is not None:
            tr = self.get_facade().trait_descriptions().get(data.get('tag'))
            taken = None
            if self.has_alt(data) and character.has_trait(data.get('tag')):
                character.pending().append(data.get('alt'))
                return character
            if ('taken' in data.keys()) and (tr.is_stackable()):
                taken = str(data.get('taken'))
                if not taken.isnumeric():
                    if taken == 'CPB':
                        taken = character.corruption_bonus()
                    if taken == 'WPB':
                        taken = character.stats().get(charlist.constants.tags.ST_WILLPOWER).bonus()
                    if 'modifier' in data.keys():
                        taken = round(taken * data.get('modifier'))
                else:
                    taken = int(taken)
            if tr.is_specialist():
                subtag = data.get('subtag')
                if tr.is_stackable() and (taken is not None):
                    for i in range(taken):
                        character.gain_trait_subtag(data.get('tag'), subtag, self.get_facade())
                else:
                    character.gain_trait_subtag(data.get('tag'), subtag, self.get_facade())
            else:
                if tr.is_stackable() and (taken is not None):
                    for i in range(taken):
                        character.gain_trait(data.get('tag'), self.get_facade())
                else:
                    character.gain_trait(data.get('tag'), self.get_facade())
            for hint in tr.get_hints():
                if hint.has_command():
                    character.pending().append(hint.get_command())
        return character
