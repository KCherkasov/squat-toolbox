from charlist.character.character import *
from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class GainFateCommand(BaseCommand):
    def __init__(self, facade: Facade):
        super(GainFateCommand, self).__init__(GET_FATE, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character: CharacterModel, data=None):
        if data is not None:
            character.gain_fate(data.get('amount'))
        return character
