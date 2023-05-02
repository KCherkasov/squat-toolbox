from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class LoseFateCommand(BaseCommand):
    def __init__(self, facade):
        super(LoseFateCommand, self).__init__(LOSE_FATE, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            for i in range(data.get('amount')):
                character.burn_fate()
        return character
