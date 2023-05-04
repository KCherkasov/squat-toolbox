from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class GainSkillCommand(BaseCommand):
    def __init__(self, facade):
        super(GainSkillCommand, self).__init__(GET_SKILL_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            sk = self.get_facade().skill_descriptions().get(data.get('tag'))
            if sk is not None:
                if sk.is_specialist():
                    character.improve_skill_subtag(data.get('tag'), data.get('subtag'), self.get_facade())
                else:
                    character.improve_skill(data.get('tag'))
        return character
