from charlist.character.character import CharacterModel
from charlist.flyweights.flyweights import Facade
from charlist.forms.player_todos.automatic.decrease_stat_fix import DecreaseStatFixCommand
from charlist.forms.player_todos.automatic.gain_fix_disorder import GainFixDisorderCommand
from charlist.forms.player_todos.automatic.gain_talent import GainTalentCommand
from charlist.forms.player_todos.automatic.increase_stat_fix import IncreaseStatFixCommand
from charlist.forms.player_todos.automatic.gain_elite_advance import GainEliteAdvanceCommand
from charlist.forms.player_todos.automatic.gain_pr import GainPRCommand
from charlist.forms.player_todos.automatic.gain_fate import GainFateCommand
from charlist.forms.player_todos.automatic.gain_aptitude import GainAptitudeCommand
from charlist.forms.player_todos.automatic.increase_pr import IncreasePRCommand
from charlist.forms.player_todos.automatic.gain_trait import GainTraitCommand
from charlist.forms.player_todos.command_tags import *
from charlist.forms.player_todos.manual.decrease_stat_alt_form import DecreaseStatAltForm
from charlist.forms.player_todos.manual.decrease_stat_roll_form import DecreaseStatRollForm
from charlist.forms.player_todos.manual.gain_corruption_roll import GainCorruptionRollForm
from charlist.forms.player_todos.manual.gain_disorder_ip_form import GainDisorderIPForm
from charlist.forms.player_todos.manual.gain_insanity_roll_form import GainInsanityRollForm
from charlist.forms.player_todos.manual.gain_malignancy_choice_form import GainMalignancyChoiceForm
from charlist.forms.player_todos.manual.gain_malignancy_roll_form import GainMalignancyRollForm
from charlist.forms.player_todos.manual.gain_mutation_choice_form import GainMutationChoiceForm
from charlist.forms.player_todos.manual.gain_mutation_roll_form import GainMutationRollForm
from charlist.forms.player_todos.manual.gain_stat_aptitude_form import GainStatAptitudeForm
from charlist.forms.player_todos.manual.gain_talent_alt_form import GainTalentAltForm
from charlist.forms.player_todos.manual.get_trauma_ip_form import GetTraumaIPForm
from charlist.forms.player_todos.manual.increase_stat_alt_form import IncreaseStatAltForm
from charlist.forms.player_todos.manual.increase_stat_roll_form import IncreaseStatRollForm

# TODO: check conditional commands and alter where needed!


class Reminder(object):
    def __init__(self, tag: str, form, tmp_name: str, colour: str, cmd_id: int):
        self.tag = tag
        self.form = form
        self.tmp_name = tmp_name
        self.colour = colour
        self.cmd_id = cmd_id


class CommandParser(object):
    def __init__(self, facade: Facade):
        super(CommandParser, self).__init__()
        self.__facade = facade
        self.__commands = CommandParser.make_commands(facade)
        self.__links = CommandParser.link_templates()
        self.__titles = CommandParser.make_titles()

    def links(self):
        return self.__links

    def titles(self):
        return self.__titles

    def make_reminder(self, cmd, character: CharacterModel):
        reminder = None
        form = None
        colour = 'info'
        if 'cmd_id' not in cmd.keys():
            cmd['cmd_id'] = character.cmd_count() + 1
            character.inc_cmd_count()
        if cmd.get('command') == GET_DISORDER_IP:
            form = GainDisorderIPForm(cmd)
            colour = 'danger'
        if cmd.get('command') == GET_TRAUMA_IP:
            form = GetTraumaIPForm(cmd)
            colour = 'danger'
        if cmd.get('command') == GET_TALENT_ALT:
            form = GainTalentAltForm(cmd, self.__facade)
        if cmd.get('command') == INC_STAT_ALT:
            form = IncreaseStatAltForm(cmd, self.__facade)
        if cmd.get('command') == DEC_STAT_ALT:
            form = DecreaseStatAltForm(cmd, self.__facade)
            colour = 'danger'
        if cmd.get('command') == GET_APT_DOUBLE:
            form = GainStatAptitudeForm(character, self.__facade, cmd)
        if cmd.get('command') == INC_STAT_ROLL:
            form = IncreaseStatRollForm(cmd, self.__facade)
        if cmd.get('command') == DEC_STAT_ROLL:
            form = DecreaseStatRollForm(cmd, self.__facade)
            colour = 'danger'
        if cmd.get('command') == GET_CORRUPTION_ROLL:
            form = GainCorruptionRollForm(cmd)
        if cmd.get('command') == GET_INSANITY_ROLL:
            form = GainInsanityRollForm(cmd)
        if cmd.get('command') == GET_MAL_ROLL:
            form = GainMalignancyRollForm(cmd)
            colour = 'danger'
        if cmd.get('command') == GET_MAL_CP_RT:
            form = GainMalignancyRollForm(cmd)
            colour = 'danger'
        if cmd.get('command') == GET_MAL_CHOICE:
            form = GainMalignancyChoiceForm(self.__facade, cmd)
            colour = 'danger'
        if cmd.get('command') == GET_MUT_CP_RT:
            form = GainMutationRollForm(cmd)
            colour = 'danger'
        if cmd.get('command') == GET_MUT_CHOICE:
            form = GainMutationChoiceForm(self.__facade, cmd)
            colour = 'danger'
        reminder = Reminder(cmd.get('command'), form, self.__links[cmd.get('command')], colour, cmd.get('cmd_id'))
        return reminder

    def process_character(self, character: CharacterModel):
        for command in character.pending():
            if command.get('command') in self.__commands.keys():
                if self.__commands[command.get('command')].is_automatic():
                    self.__commands[command.get('command')].do_logic(character, data=command)
                    character.completed().append(command.get('command'))
        for command in character.completed():
            for cmd in character.pending():
                if cmd.get('command') == command:
                    character.pending().remove(cmd)
                    break
        return character

    @classmethod
    def make_commands(cls, facade: Facade):
        commands = dict()

        commands[INC_STAT_FIX] = IncreaseStatFixCommand(facade)
        commands[DEC_STAT_FIX] = DecreaseStatFixCommand(facade)
        commands[GET_TALENT_FIX] = GainTalentCommand(facade)
        commands[GET_FIX_DISORDER] = GainFixDisorderCommand(facade)
        commands[GET_EA] = GainEliteAdvanceCommand(facade)
        commands[GET_PR] = GainPRCommand(facade)
        commands[GET_FATE] = GainFateCommand(facade)
        commands[GET_APT_FIX] = GainAptitudeCommand(facade)
        commands[INC_PR] = IncreasePRCommand(facade)
        commands[GET_TRAIT_FIX] = GainTraitCommand(facade)

        return commands

    @classmethod
    def link_templates(cls):
        templates = dict()

        templates[GET_DISORDER_IP] = 'gain_disorder_form.html'
        templates[GET_TRAUMA_IP] = 'gain_trauma_form.html'
        templates[GET_TALENT_ALT] = 'get_talent_alt_form.html'
        templates[INC_STAT_ALT] = 'increase_stat_alt_form.html'
        templates[DEC_STAT_ALT] = 'decrease_stat_alt_form.html'
        templates[GET_APT_DOUBLE] = 'gain_stat_aptitude_form.html'
        templates[INC_STAT_ROLL] = 'increase_stat_roll_form.html'
        templates[DEC_STAT_ROLL] = 'decrease_stat_roll_form.html'
        templates[GET_CORRUPTION_ROLL] = 'gain_corruption_form.html'
        templates[GET_INSANITY_ROLL] = 'gain_insanity_form.html'
        templates[GET_MAL_CHOICE] = 'gain_malignance_choice_form.html'
        templates[GET_MAL_CP_RT] = 'gain_malignance_form.html'
        templates[GET_MUT_CP_RT] = 'gain_mutation_form.html'
        templates[GET_MUT_CHOICE] = 'gain_mutation_choice_form.html'

        return templates

    @classmethod
    def make_titles(cls):
        titles = dict()

        titles[GET_DISORDER_IP] = 'Получите психическое расстройство'
        titles[GET_TRAUMA_IP] = 'Получите психическую травму'
        titles[GET_TALENT_ALT] = 'Выберите талант'
        titles[INC_STAT_ALT] = 'Улучшите одну характеристику на выбор'
        titles[DEC_STAT_ALT] = 'Ухудшите одну характеристику на выбор'
        titles[GET_APT_DOUBLE] = 'Получите склонность-характеристику'
        titles[INC_STAT_ROLL] = 'Улучшите характеристику'
        titles[DEC_STAT_ROLL] = 'Ухудшите характеристику'
        titles[GET_CORRUPTION_ROLL] = 'Получите Очки Порчи'
        titles[GET_INSANITY_ROLL] = 'Получите Очки Безумия'
        titles[GET_MAL_CHOICE] = 'Получите Малигнацию на выбор'
        titles[GET_MAL_CP_RT] = 'Получите случайную Малигнацию'
        titles[GET_MUT_CP_RT] = 'Получите случайную Мутацию'
        titles[GET_MUT_CHOICE] = 'Получите Мутацию на выбор'

        return titles

