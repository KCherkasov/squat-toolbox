from charlist.forms.player_todos.automatic.decrease_stat_fix import DecreaseStatFixCommand
from charlist.forms.player_todos.automatic.gain_aptitude import GainAptitudeCommand
from charlist.forms.player_todos.automatic.gain_elite_advance import GainEliteAdvanceCommand
from charlist.forms.player_todos.automatic.gain_fate import GainFateCommand
from charlist.forms.player_todos.automatic.gain_fix_disorder import GainFixDisorderCommand
from charlist.forms.player_todos.automatic.gain_pr import GainPRCommand
from charlist.forms.player_todos.automatic.gain_talent import GainTalentCommand
from charlist.forms.player_todos.automatic.gain_trait import GainTraitCommand
from charlist.forms.player_todos.automatic.increase_pr import IncreasePRCommand
from charlist.forms.player_todos.automatic.increase_stat_fix import IncreaseStatFixCommand
from charlist.forms.player_todos.automatic.lose_fate import LoseFateCommand
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
from charlist.forms.player_todos.manual.origin_xp_extra_choice import GainExtraOriginCommand
from charlist.forms.player_todos.manual.gain_spec_skill_subtag import GainSpecSkillForm
from charlist.forms.player_todos.automatic.gain_skill import GainSkillCommand
from charlist.forms.player_todos.manual.gain_spec_talent_subtag import GainSpecTalentForm


# TODO: check conditional commands and alter where needed!


class Reminder(object):
    def __init__(self, tag: str, form, tmp_name: str, colour: str, cmd_id: int):
        self.tag = tag
        self.form = form
        self.tmp_name = tmp_name
        self.colour = colour
        self.cmd_id = cmd_id


class CommandParser(object):
    def __init__(self, facade):
        super(CommandParser, self).__init__()
        self.__facade = facade
        self.__commands = CommandParser.make_commands(facade)
        self.__links = CommandParser.link_templates()
        self.__titles = CommandParser.make_titles()

    def links(self):
        return self.__links

    def titles(self):
        return self.__titles

    def is_conditional(self, data):
        return 'condition' in data.keys()

    def is_skill_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'SK':
                return True
        return False

    def is_talent_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'TL':
                return True
        return False

    def is_trait_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'TR':
                return True
        return False

    def is_background_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == 'BG':
                return True
        return False

    def is_career_condition(self, data):
        if self.is_conditional(data):
            if data.get('condition').get('tag')[:2] == "CR":
                return True
        return False

    def condition_met(self, character, data):
        result = None
        if self.is_conditional(data):
            if character.is_rt():
                if self.is_career_condition(data):
                    result = character.career_id() == data.get('condition').get('tag')
            else:
                if self.is_background_condition(data):
                    result = character.bg_id() == data.get('condition').get('tag')
            if self.is_talent_condition(data):
                if self.__facade.talent_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        result = character.has_talent_subtag(data.get('condition').get('tag'),
                                                             data.get('condition').get('subtag'))
                    else:
                        return False
                else:
                    result = character.has_talent(data.get('condition').get('tag'))
            if self.is_skill_condition(data):
                if self.__facade.skill_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        if data.get('condition').get('subtag') == 'SK_ANY':
                            result = data.get('condition').get('tag') in character.skills().keys()
                        else:
                            result = character.has_subskill(data.get('condition').get('tag'),
                                                            data.get('condition').get('subtag'),
                                                            adv=data.get('condition').get('value'))
                    else:
                        return False
                else:
                    result = character.has_skill(data.get('condition').get('tag'),
                                                 adv=data.get('condition').get('value'))
                return result
            if self.is_trait_condition(data):
                if self.__facade.trait_descriptions().get(data.get('condition').get('tag')).is_specialist():
                    if 'subtag' in data.get('condition').keys():
                        return character.has_trait_subtag(data.get('condition').get('tag'),
                                                          data.get('condition').get('subtag'))
                    else:
                        return False
                else:
                    result = character.has_trait(data.get('condition').get('tag'))
            if data.get('condition').get('value') > 0:
                return result
            return not result
        return False

    def make_reminder(self, cmd, character):
        reminder = None
        form = None
        colour = 'info'
        if 'cmd_id' not in cmd.keys():
            cmd['cmd_id'] = character.cmd_count() + 1
            character.inc_cmd_count()
        if self.is_conditional(cmd):
            if not self.condition_met(character, cmd):
                return reminder
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
        if cmd.get('command') == ORIGIN_EXTRA:
            form = GainExtraOriginCommand(cmd)
            colour = 'success'
        if cmd.get('command') == GET_SUBTAG_SKILL:
            form = GainSpecSkillForm(self.__facade, cmd)
            colour = 'success'
        if cmd.get('command') == GET_SUBTAG_TALENT:
            form = GainSpecTalentForm(self.__facade, cmd)
        reminder = Reminder(cmd.get('command'), form, self.__links[cmd.get('command')], colour, cmd.get('cmd_id'))
        return reminder

    def process_character(self, character):
        completed = list()
        for command in character.pending():
            if command.get('command') in self.__commands.keys():
                if self.__commands[command.get('command')].is_automatic():
                    character = self.__commands[command.get('command')].execute(character, data=command)
                    completed.append(command)
        for command in completed:
            character.completed().append(command)
            for cmd in character.pending():
                if cmd.get('command') == command.get('command'):
                    character.pending().remove(cmd)
                    break
        return character

    @classmethod
    def make_commands(cls, facade):
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
        commands[LOSE_FATE] = LoseFateCommand(facade)
        commands[GET_SKILL_FIX] = GainSkillCommand(facade)

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
        templates[ORIGIN_EXTRA] = 'origin_extra_choice_form.html'
        templates[GET_SUBTAG_SKILL] = 'gain_spec_skill_form.html'
        templates[GET_SUBTAG_TALENT] = 'gain_spec_talent_form.html'

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
        titles[ORIGIN_EXTRA] = 'Дополнительная опция от происхождения'
        titles[GET_SUBTAG_SKILL] = 'Получите специализацию в навыке'
        titles[GET_SUBTAG_TALENT] = 'Получите специализацию в таланте'

        return titles

