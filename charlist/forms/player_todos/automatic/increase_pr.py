from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class IncreasePRCommand(BaseCommand):
    def __init__(self, facade):
        super(IncreasePRCommand, self).__init__(INC_PR, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            for i in range(data.get('value')):
                character.gain_pr()
        return character
