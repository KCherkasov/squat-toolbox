from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *


class GainAptitudeCommand(BaseCommand):
    def __init__(self, facade):
        super(GainAptitudeCommand, self).__init__(GET_APT_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character, data=None):
        if data is not None:
            if data.get('tag') not in character.aptitudes():
                character.aptitudes().append(data.get('tag'))
            else:
                character.pending().append({"command": "GainStatAptitude"})
        return character
