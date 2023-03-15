from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *
from charlist.flyweights.flyweights import Facade
from charlist.character.character import CharacterModel


class GainSkillCommand(BaseCommand):
    def __init__(self, facade: Facade):
        super(GainSkillCommand, self).__init__(GET_SKILL_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character: CharacterModel, data=None):
        if data is not None:
            sk = self.get_facade().skill_descriptions().get(data.get('tag'))
            if sk is not None:
                if sk.is_specialist():
                    if not character.has_subskill(data.get('tag'), data.get('subtag')):
                        character.improve_skill_subtag(data.get('tag'), data.get('subtag'), self.get_facade())
                    else:
                        if 'alt' in data.keys():
                            character.pending().append(data.get('alt'))
                else:
                    if data.get('tag') not in character.skills():
                        character.improve_skill(data.get('tag'))
                    else:
                        if 'alt' in data.keys():
                            character.pending().append(data.get('alt'))
        return character
