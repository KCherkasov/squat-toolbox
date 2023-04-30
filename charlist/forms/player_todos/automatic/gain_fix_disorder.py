from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class GainFixDisorderCommand(BaseCommand):
    def __init__(self, facade):
        super(GainFixDisorderCommand, self).__init__(GET_FIX_DISORDER, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            if 'disorder' in data.keys():
                character.disorders().append(data.get('disorder'))
        return character
