from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class GainEliteAdvanceCommand(BaseCommand):
    def __init__(self, facade):
        super(GainEliteAdvanceCommand, self).__init__(GET_EA, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            ea_ids_count = len(character.ea_id())
            character.gain_ea_id(data.get('tag'))
            if ea_ids_count != len(character.ea_id()):
                ea = self.get_facade().elite_advances().get(data.get('tag'))
                if ea is not None:
                    for cmd in ea.commands():
                        character.pending().append(cmd)
        return character
