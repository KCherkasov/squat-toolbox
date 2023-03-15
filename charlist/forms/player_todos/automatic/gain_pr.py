from charlist.character.character import CharacterModel
from charlist.forms.player_todos.command_tags import *
from charlist.forms.player_todos.base_command import BaseCommand
from charlist.flyweights.flyweights import Facade


class GainPRCommand(BaseCommand):
    def __init__(self, facade: Facade):
        super(GainPRCommand, self).__init__(INC_PR, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character: CharacterModel, data=None):
        if data is not None:
            if character.pr() == 0:
                for i in range(data.get('value')):
                    character.gain_pr()
        return character
