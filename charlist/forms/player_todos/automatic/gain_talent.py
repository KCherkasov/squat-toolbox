from charlist.character.character import CharacterModel
from charlist.forms.player_todos.base_command import BaseCommand
from charlist.forms.player_todos.command_tags import *
from charlist.flyweights.flyweights import Facade
from charlist.forms.player_todos.automatic.increase_stat_fix import IncreaseStatFixCommand


class GainTalentCommand(BaseCommand):
    def __init__(self, facade: Facade):
        super(GainTalentCommand, self).__init__(GET_TALENT_FIX, facade)

    def is_automatic(self):
        return True

    def do_logic(self, character: CharacterModel, data=None):
        if data is not None:
            if 'tag' in data.keys():
                talent = self.get_facade().talent_descriptions().get(data.get('tag'))
                flg = False
                if talent.is_specialist():
                    if data.get('tag') in character.talents().keys():
                        if character.talents().get(data.get('tag')).taken_subtag(self.get_facade(), data.get_subtag()):
                            flg = True
                        else:
                            character.gain_talent_subtag(data.get('tag'), data.get('subtag'), self.get_facade())
                elif data.get('tag') not in character.talents().keys():
                    character.gain_talent(data.get('tag'), self.get_facade())
                else:
                    flg = True
                if flg:
                    alt_data = data.get('alt')
                    character.pending().append(alt_data)  # TODO: test this approach, if not working - instantiate
                    # TODO: required command and execute it manually from here
        return character
