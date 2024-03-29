from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class IncreaseStatFixCommand(BaseCommand):
    def __init__(self, facade):
        super(IncreaseStatFixCommand, self).__init__(INC_STAT_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            if data.get('tag') in character.stats():
                character.improve_stat(data.get('tag'), data.get('amount'))
        return character
