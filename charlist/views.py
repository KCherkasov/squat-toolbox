# -*- coding: utf-8 -*-
import datetime
import logging
from operator import itemgetter
from urllib.parse import unquote

from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

import charlist.models as models
from charlist import rt_views
from charlist import mal_views
from charlist.character.character import CharacterModel
from charlist.character.skill import Skill
from charlist.character.stat import Stat
from charlist.character.talent import Talent
from charlist.character.trait import Trait
from charlist.constants.constants import *
from charlist.flyweights.flyweights import *
from charlist.forms.authorization.signin import SignInForm
from charlist.forms.authorization.signup import UserCreationForm
from charlist.forms.authorization.edit import UserEditForm
from charlist.forms.generation.background_choice_form import BackgroundChoiceForm
from charlist.forms.generation.choices_form import ChoicesForm
from charlist.forms.generation.creation_settings_form import CreationSettingsForm
from charlist.forms.generation.divination_form import DivinationForm
from charlist.forms.generation.double_apts_choices import DoubleAptsChoiceForm
from charlist.forms.generation.homeworld_choice_form import HomeworldsChoiceForm
from charlist.forms.generation.role_choice_form import RoleChoiceForm
from charlist.forms.generation.stages import *
from charlist.forms.generation.stat_distribution_form import StatDistributionForm
from charlist.forms.master.create_game_session import CreateSessionForm
from charlist.forms.master.create_group_form import CreateGroupForm
from charlist.forms.master.create_season_form import CreateSeasonForm
from charlist.forms.master.end_session_form import EndSessionForm
from charlist.forms.master.group_xp_giver_form import GroupXPGiverForm
from charlist.forms.master.influence_controls_form import InfluenceControlsForm
from charlist.forms.master.initiative_line_maker import InitiativeLineMaker
from charlist.forms.player.add_doc_form import AddDocLinkForm
from charlist.forms.player.fate_controls_form import FateControlsForm
from charlist.forms.player.fatigue_controls_form import FatigueControlsForm
from charlist.forms.player.wound_controls_form import WoundControlsForm
from charlist.forms.player_todos.command_parser import CommandParser
from charlist.forms.player_todos.manual.decrease_stat_alt_form import DecreaseStatAltForm
from charlist.forms.player_todos.manual.decrease_stat_roll_form import DecreaseStatRollForm
from charlist.forms.player_todos.manual.gain_corruption_roll import GainCorruptionRollForm
from charlist.forms.player_todos.manual.gain_disorder_ip_form import GainDisorderIPForm
from charlist.forms.player_todos.manual.gain_insanity_roll_form import GainInsanityRollForm
from charlist.forms.player_todos.manual.gain_malignancy_choice_form import GainMalignancyChoiceForm
from charlist.forms.player_todos.manual.gain_malignancy_roll_form import GainMalignancyRollForm
from charlist.forms.player_todos.manual.gain_mutation_choice_form import GainMutationChoiceForm
from charlist.forms.player_todos.manual.gain_mutation_roll_form import GainMutationRollForm
from charlist.forms.player_todos.manual.gain_spec_skill_subtag import GainSpecSkillForm
from charlist.forms.player_todos.manual.gain_spec_talent_subtag import GainSpecTalentForm
from charlist.forms.player_todos.manual.gain_stat_aptitude_form import GainStatAptitudeForm
from charlist.forms.player_todos.manual.gain_talent_alt_form import GainTalentAltForm
from charlist.forms.player_todos.manual.get_trauma_ip_form import GetTraumaIPForm
from charlist.forms.player_todos.manual.increase_stat_alt_form import IncreaseStatAltForm
from charlist.forms.player_todos.manual.increase_stat_roll_form import IncreaseStatRollForm
from charlist.forms.player_todos.manual.origin_xp_extra_choice import GainExtraOriginCommand
from charlist.forms.upgrading.elite_advance_upgrade_form import EliteAdvanceUpgradeForm
from charlist.forms.upgrading.pr_upgrade_form import PRUpgrageForm
from charlist.forms.upgrading.psy_power_upgrade_form import PsyPowerUpgradeForm
from charlist.forms.upgrading.skill_subtag_upgrade_form import SkillSubtagUpgradeForm
from charlist.forms.upgrading.skill_upgrade_form import SkillUpgradeForm
from charlist.forms.upgrading.stat_upgrade_form import StatUpgradeForm
from charlist.forms.upgrading.talent_subtag_upgrade_form import TalentUpgradeSubtagForm
from charlist.forms.upgrading.talent_upgrade_form import TalentUpgradeForm
from charlist.rt_views import rt_flyweights, rt_commands_parser


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return force_str(user.pk) + force_str(timestamp) + force_str(user.is_active)


fact_words = {
    'SK_CML': u'Они думают, что что-то знают (коммонки):',
    'SK_SCL': u'А этих даже чему-то учили (схоластика)',
    'SK_FBL': u'Тааак... тут кое-кто накопал всякого. Вызнать бы еще, где... (форбидки)',
    'SK_LNG': u'Они думают, что знают готик и не только:',
    'SK_NVG': u'А эти считают, что не заблудятся (и где-то прячут третий глаз): ',
    'SK_OPR': u'У них и водятлы есть!',
    'SK_TRD': u'О, кружок народных умельцев!',
    'SK_PSY': u'Откуда это больше пяти чувств? (пси-сенс)',
    'TR_PSY': u'Псякры!',
    'TL_JD': u'Этих можно пугать только варп-хтонью:',
    'TL_PR': u'Вы посмотрите, они даже знают, как себя вести, хотя бы в отдельно взятой компании:',
    'TL_WS': u'Варп-нюхающие:',
    'TL_LTSL': u'Кто-то плохо спит. Интересно почему?',
    'TL_MDTN': u'Подобия монахов - говорят, медитировать умеют:',
    'TL_FRLS': u'Номинация "Слабоумие или отвага?":',
    'TL_UNRM': u'Мыши серые обыкновенные:',
    'TL_ENM': u'Кто-то нажил себе врагов:',
    'TL_KI': u'Да тут интуиты:',
    'TL_QD': u'Мастера быстрого отхва...выхватывания:',
    'TL_TKD': u'Ловцы человеков (и не только):',
    'TL_RST': u'Обмазались резистами и думают, что это поможет:',
    'TL_MGTR': u'Это кто разрешил не бояться лестниц? В смысле "они еще и летают"?!',
    'TL_CMST': u'Это ж надо, так дрыном махать, и не окружить гадов:',
    'TL_CNVG': u'Эт что, они ничему не удивляются? А сюрпризы зачем готовить тогда? Скучно...',
    'TL_CNNT': u'Кто-то отрастил связей. Ну-ну, больше связей - больше компромата...',
    'TL_CVUP': u'Смотри-ка кое-кто даже знает, как этими связями пользоваться:',
    'TL_STMN': u'Надо ж было так накачать мозг, что у него мышцы появились, теперь туда лезть стремно...',
    'TL_ADFT': u'Ярые веруны, настолько ярые, что ничего не боятся (наверняка врут):',
    'TL_FOIN': u'Хорошая работа, эти настолько отчаялись, что готовы тратить фейты на прямые вопросы мастеру!',
    'TL_INKN': u'Всезнаек развелось, плюнуть некуда!',
    'TL_BG': u'Look out, sir! или ma\'m... Телохранители, в общем:',
    'TL_DMH': u'Эти не только знают про демонов, но и любят их охотить:',
    'TL_WTFN': u'Э, никто не предупреждал, что тут ведьмоловы! Нечестно!',
    'TL_AMIM': u'Цельные послы. Кто и куда их послал почему-то не говорят...',
    'TL_ARCH': u'Пылищу развели, тьфу, дышать нечем! Кто книжных червей из загона... то есть либрариума, выпустил?! ',
    'TL_LXG': u'Человеки-переводчики, фу такими быть...',
    'TL_XNS': u'Все понимаю, у всех разные пристрастия но в сортах гов...ксеносов копаться зачем?!',
    'TL_INCN': u'Мало того, что сами сопротивляются безумию, так и другим обмазаться мешают!',
    'TL_AGOC': u'Гляньте-ка, какие снобы, ничто-то их не берет...',
    'TL_AROA': u'Смотри-ка, пыжатся, щеки надувают, пытаются авторитетом давить. Ну-ну...',
    'TL_ARCN': u'Это кто разрешил сопротивляться корапту?! В смысле "никто не запрещал"?!',
    'TL_CHGD': u'Самые ленивые, спокойные, жирные... стоп, мы не про фафта сейчас? Вашу ж мать...',
    'TL_CLSL': u'Не-не-не-не, к этим отморозкам я близко не подойду!',
    'TL_CLRD': u'Шарлатаны, мошенники, аферисты:',
    'TL_CMFR': u'Так, где тут сборник анекдотов про ходящих строем - вон еще "формация" топает, с форматором во главе:',
    'TL_DSVC': u'Какой чарующий голос (спойлер - нет):',
    'TL_ETVG': u'Не просто параноики, эти еще шмальнуть могут без предупреждения, чего доброго. Ну их в зог...',
    'TL_FRST': u'Аналитики, скучно с ними...',
    'TL_IRDS': u'Дисциплина, дисциплина и дисциплина, задолбали...',
    'TL_MSCM': u'Отцы-командиры... Спорим, на деле просто самые горластые в компании?',
    'TL_MTMZ': u'Не, вот этим я в голову не полезу, не проси, там такое... до сих пор икается, брр...',
    'TL_MMC': u'Птица-говорун, в смысле поют на разные голоса:',
    'TL_OPCN': u'Настоящий оперативник может допросить допрашивающего... Ну вот эти так думают. Может, проверим?',
    'TL_PRN': u'Параноики! Их так весело провоцировать!',
    'TL_PLG': u'Полиглоты. А если подсунуть им тарабарщину, как быстро они поймут, что это не новый язык?',
    'TL_RPRC': u'В смысле они отказываются стоять на месте, попав в засаду?!',
    'TL_RNWR': u'Гляньте на этот патент! Блестит, пробы негде ставить, аж тошно! Пойду принесу коричневой краски...',
    'TL_STCN': u'Скучные люди, сопротивляются безумию, зачем?',
    'TL_WOEX': u'Осторожно, читеры!!! Потратят фейту и скажут, что у них запрещенное число на броске!'
               u' Вот и что с ними делать?',
    'TOT_HOW': u'Тут у кой-кого контры завелись, лютые зело. Как бы с ними свести...',
    'TOT_PRGN': u'Вот это богатая биография - приводы, скандалы, интриги, расследования!'
                u'Почему-то не любят посягательств на свою свободу, с чего бы это?',
    'TOT_HGVD': u'Какой темперамент, прям плюнь - закипят! Или косо посмотри...'
                u'Да с этими еще интереснее, чем с параноиками!'
}


player_fact_words = {
    'SK_CML': u'Общедоступные, но оттого не менее важные знания (коммонки):',
    'SK_SCL': u'Среди вас есть образованные люди! (схоластика)',
    'SK_FBL': u'Особо ценные знания, но о способах получения лучше помалкивать, мало ли что... (форбидки)',
    'SK_LNG': u'Среди вас есть настоящие лингвисты, которым ведомы многие языки:',
    'SK_NVG': u'Их способности ориентироваться и находить дорогу можно только завидовать:',
    'SK_OPR': u'Некоторые из вас с легкостью управляют разными видами транспорта:',
    'SK_TRD': u'Среди вас есть мастера, освоившие различные профессии и ремесла:',
    'SK_PSY': u'Немногие способны подметить проявления нематериального (пси-сенс):',
    'TR_PSY': u'Среди вас есть пси-одаренные!',
    'TL_JD': u'Некоторых из вас может напугать лишь пришествие из-за завесы:',
    'TL_PR': u'Какие манеры, какое воспитание!',
    'TL_WS': u'Умение столь тонко чувствовать течения варпа - настоящая редкость!',
    'TL_LTSL': u'Сложно пробраться незамеченным мимо тех, у кого столь чуткий сон:',
    'TL_MDTN': u'Люди великой силы воли - они освоили искусство медитации:',
    'TL_FRLS': u'Эти храбрецы ничего не боятся и никогда не отступают:',
    'TL_UNRM': u'Умение быть неприметным - особый талант:',
    'TL_ENM': u'Подумаешь, враги, у кого их нет?',
    'TL_KI': u'Столь чуткая интуиция - настоящий дар Императора!',
    'TL_QD': u'Безоружными их не застать:',
    'TL_TKD': u'Убить врага нетрудно. Взять живьем - вот искусство:',
    'TL_RST': u'Их стойкость поистине поразительна:',
    'TL_MGTR': u'Омниссия в щедрости своей научил их летать:',
    'TL_CMST': u'Эти бойцы стоят целого отряда:',
    'TL_CNVG': u'Постоянная бдительность - их девиз:',
    'TL_CNNT': u'Эти персонажи широко известны в определенных кругах:',
    'TL_CVUP': u'Умение воспользоваться знакомствами - особое искусство:',
    'TL_STMN': u'Крепкий разум - надежная преграда перед вражескими колдунами:',
    'TL_ADFT': u'О крепости их веры можно слагать легенды:',
    'TL_FOIN': u'С этими людьми порой говорит сам Император:',
    'TL_INKN': u'Обладатели воистину энциклопедических познаний обо всем:',
    'TL_BG': u'Нужно обладать большой храбростью, чтобы принять не предназначенный тебе удар:',
    'TL_DMH': u'Для этих храбрецов демоны - всего лишь дичь:',
    'TL_WTFN': u'Благородное призвание охотника за колдунами нередко недооценивают, совершенно напрасно:',
    'TL_AMIM': u'Они с достоинством несут тяжелую миссию переговоров с ксеномразями и другими недоразумениями:',
    'TL_ARCH': u'Либрариумы - их второй дом, массивы данных - любимые инструменты:',
    'TL_LXG': u'Для них нет непознаваемых языков',
    'TL_XNS': u'Кто-то же должен разбираться в ксеносах. Эти люди взвалили столь неблагодарную работу на себя:',
    'TL_INCN': u'Сохранить собственный рассудок непросто,'
               u'помешать впасть в безумие другим - многократно сложнее, но им - посильно:',
    'TL_AGOC': u'Сохранить свою и чужие души в частоте при их-то роде деятельности - настоящий подвиг:',
    'TL_AROA': u'Властность и авторитет этих людей воистину непререкаемы:',
    'TL_ARCN': u'Только воистину крепкие в своей вере могут остаться нетронутыми порчей:',
    'TL_CHGD': u'Спокойствию и стойкости этих людей нет равных:',
    'TL_CLSL': u'Жестокость бывает необходима, даже такая, что присуща этим людям:',
    'TL_CLRD': u'Умение верно истолковать намерения контрагента и обернуть их к своей выгоде - ценнейший дар:',
    'TL_CMFR': u'Столь грамотно организовать соратников в бою - дар, достойный высочайшего превознесения:',
    'TL_DSVC': u'Отнюдь не каждому дано поставить собеседника на место парой слов,'
               u'еще меньше тех, у кого хватит для этого стали в голосе:',
    'TL_ETVG': u'Первый выстрел точно будет за ними:',
    'TL_FRST': u'Обладатели быстрого и живого ума, надежного подспорья в решении любых задач:',
    'TL_IRDS': u'Дисциплина подчиненных этим людям бойцов делает командирам честь:',
    'TL_MSCM': u'Взрастить в подчиненных не только исполнительность, но и настоящую преданность - великий труд:',
    'TL_MTMZ': u'Их разум - не просто преграда перед псайкером, но опасный капкан:',
    'TL_MMC': u'Поистине удивительное владение голосом!',
    'TL_OPCN': u'Мало кто может извлечь выгоду из пребывания в кресле допрашиваемого - этим людям такое по силам:',
    'TL_PRN': u'Не бывает чрезмерной бдительности, эти люди - тому подтверждение:',
    'TL_PLG': u'Подлинная склонность к освоению различных языков встречается нечасто, здесь есть, чем гордиться',
    'TL_RPRC': u'Они всегда готовы дать бой любому врагу',
    'TL_RNWR': u'Столь заслуженная и почетная история стоит далеко не за каждым патентом...',
    'TL_STCN': u'Крепость убеждений - основа здравости ума, эти люди - живое тому подтверждение:',
    'TL_WOEX': u'Император поистине любит и ведет их, даруя успех в начинаниях:',
    'TOT_HOW': u'Какая-то богопротивная шваль посмела нанести оскорбление сим почтеннейшим исследователям:',
    'TOT_PRGN': u'Как смеют всякие безродные шавки пытаться ограничить свободу ТАКИМ людям?!',
    'TOT_HGVD': u'Кодекс чести и достойные подражания манеры '
                u'не позволяют этим благочестивым гражданам Империума оставлять урон чести без ответа:'
}


account_activation_token = TokenGenerator()

resources = ['aptitudes.json', 'stat_descriptions.json', 'skill_descriptions.json', 'talent_descriptions.json',
             'traits.json', 'homeworlds.json', 'backgrounds.json', 'roles.json', 'elite_advances.json',
             'divinations.json', 'malignancies.json', 'mutations.json', 'psy.json', 'combat_actions.json']
flyweights = Facade(resources)
commands_parser = CommandParser(flyweights)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return TemplateResponse(request, 'charlist_test.html', {'version': VERSION, 'facade': flyweights, })


def charsheet_mockup(request):
    return TemplateResponse(request, 'charsheet-mockup.html', {'version': VERSION, })


def interactive_charsheet_mockup(request):
    character = CharacterModel(1, 1, u'Бергрим Коллвирсон', GENDER_MALE, 157, 114, 69,
                               'HW_FDWL', 'BG_ADMN', 'RL_CRS', 'D_TNSZ',
                               [], [11, 11], [0, 9], [64, 16950], [3, 3], 13, 14, 0,
                               [A_GENERAL, A_KNOWLEDGE, A_OFFENCE, A_STRENGTH, A_TOUGHNESS,
                                A_WILLPOWER, A_SOCIAL, A_WEAPON_SKILL], {ST_WEAPON_SKILL: Stat(ST_WEAPON_SKILL, 39, 2),
                                                                         ST_INTELLIGENCE: Stat(ST_INTELLIGENCE, 24, 1),
                                                                         ST_BALLISTIC_SKILL: Stat(ST_BALLISTIC_SKILL,
                                                                                                  26),
                                                                         ST_PERCEPTION: Stat(ST_PERCEPTION, 32, 1),
                                                                         ST_STRENGTH: Stat(ST_STRENGTH, 33, 4),
                                                                         ST_WILLPOWER: Stat(ST_WILLPOWER, 29, 5),
                                                                         ST_TOUGHNESS: Stat(ST_TOUGHNESS, 33, 2),
                                                                         ST_FELLOWSHIP: Stat(ST_FELLOWSHIP, 26),
                                                                         ST_AGILITY: Stat(ST_AGILITY, 30),
                                                                         ST_INFLUENCE: Stat(ST_INFLUENCE, 40)},
                               {SK_ACROBATICS: Skill(SK_ACROBATICS, 0), SK_ATHLETICS: Skill(SK_ATHLETICS, 2),
                                SK_AWARENESS: Skill(SK_AWARENESS, 1), SK_CHARM: Skill(SK_CHARM, 1),
                                SK_COMMAND: Skill(SK_COMMAND, 1), SK_COMMERCE: Skill(SK_COMMERCE, 1),
                                SK_DECEIVE: Skill(SK_DECEIVE, 0), SK_DODGE: Skill(SK_DODGE, 0),
                                SK_INQUIRY: Skill(SK_INQUIRY, 1), SK_INTERROGATION: Skill(SK_INTERROGATION, 1),
                                SK_INTIMIDATE: Skill(SK_INTIMIDATE, 1),
                                SK_LOGIC: Skill(SK_LOGIC, 0), SK_MEDICAE: Skill(SK_MEDICAE, 0),
                                SK_PARRY: Skill(SK_PARRY, 1), SK_PSYNISCIENCE: Skill(SK_PSYNISCIENCE, 0),
                                SK_SCRUTINY: Skill(SK_SCRUTINY, 1), SK_SECURITY: Skill(SK_SECURITY, 0),
                                SK_SLEIGHT_OF_HANDS: Skill(SK_SLEIGHT_OF_HANDS, 0), SK_STEALTH: Skill(SK_STEALTH, 0),
                                SK_SURVIVAL: Skill(SK_SURVIVAL, 1), SK_TECH_USE: Skill(SK_TECH_USE, 0),
                                SK_COMMON_LORE: Skill(SK_COMMON_LORE, {"Adeptus Ministorum": 1}),
                                SK_FORBIDDEN_LORE: Skill(SK_FORBIDDEN_LORE, {"Daemonology": 1, "Inquisition": 1}),
                                SK_LINGUISTICS: Skill(SK_LINGUISTICS, {"High gothic": 1}),
                                SK_TRADE: Skill(SK_TRADE, {"Armourer": 1})},
                               {"TL_BG": Talent("TL_BG", 1), "TL_TRGT": Talent("TL_TRGT", 1),
                                "TL_DTW": Talent("TL_DTW", 1), "TL_WTR": Talent("TL_WTR", {"Low-tech": 1,
                                                                                           "Solid projectile": 1,
                                                                                           "Power": 1}),
                                "TL_CFTC": Talent("TL_CFTC", 1), "TL_FRZ": Talent("TL_FRZ", 1),
                                "TL_BTRG": Talent("TL_BTRG", 1), "TL_FLGT": Talent("TL_FLGT", 1),
                                "TL_ADFT": Talent("TL_ADFT", 1), "TL_INAT": Talent("TL_INAT", {"Melee": 1}),
                                "TL_CRBL": Talent("TL_CRBL", 1), "TL_SWAT": Talent("TL_SWAT", 1),
                                "TL_CNAT": Talent("TL_CNAT", 1), "TL_SHWL": Talent("TL_SHWL", 1),
                                "TL_JD": Talent("TL_JD", 1), "TL_STMN": Talent("TL_STMN", 1),
                                "TL_IR": Talent("TL_IR", 1), "TL_DT": Talent("TL_DT", 1), "TL_AMB": Talent("TL_AMB", 1),
                                "TL_CMST": Talent("TL_CMST", 1), "TL_RST": Talent("TL_RST", {"Fear": 1,
                                                                                             "Psychic powers": 1}),
                                "TL_DMH": Talent("TL_DMH", 1), "TL_HTRD": Talent("TL_HTRD", {"Daemons": 1}),
                                "TL_POH": Talent("TL_POH", {"Daemons": 1}), "TL_ROB": Talent("TL_ROB", 1),
                                "TL_IOHW": Talent("TL_IOHW", 1)}, {}, [], [], [], [], [], [], [], [], 0, 0)
    char_dump = character.toJSON()
    unpacked_char = CharacterModel.from_json(char_dump)
    return TemplateResponse(request, "charsheet-mockup-interactive.html", {'version': VERSION, 'facade': flyweights,
                                                                           'character': unpacked_char,
                                                                           'hookups': character.make_hookups(
                                                                               flyweights)})


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = True
            if user.pk == 'irveron':
                user.is_superuser = True
                user.is_admin = True
            else:
                user.is_superuser = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = u'Подтвердите Ваш почтовый адрес на squat-toolbox.ru'
            message = render_to_string('signup_activation_mail.html', {
                'user': user, 'domain': current_site, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            to_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, from_email='signup@squattoolbox.ru', to=[to_mail])
            email.send()
            return HttpResponseRedirect(reverse('main'))
        else:
            return TemplateResponse(request, 'signup.html', {'version': VERSION, 'form': form, })
    else:
        form = UserCreationForm()
        return TemplateResponse(request, 'signup.html', {'version': VERSION, 'form': form, })


def signup_activate(request):
    return TemplateResponse(request, 'activate.html', {'version': VERSION, })


@csrf_exempt
def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(reverse('main'))
        else:
            return HttpResponseRedirect(reverse('signin'))
    else:
        form = SignInForm()
    return TemplateResponse(request, 'signin.html', {'version': VERSION, 'form': form, })


@csrf_exempt
def profile_edit(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            if len(form.cleaned_data.get('password_set')) > 0:
                request.user.set_password(form.cleaned_data.get('password_set'))
            request.user.preferable_language = form.cleaned_data.get('preferable_language')
            request.user.save()
            return HttpResponseRedirect(reverse('main'))
        else:
            return TemplateResponse(request, 'profile_edit.html', {'version': VERSION, 'form': form,
                                                                   'uname': request.user.id, })
    else:
        user_dict = model_to_dict(request.user)
        form = UserEditForm(user_dict)
        return TemplateResponse(request, 'profile_edit.html', {'version': VERSION, 'form': form,
                                                               'uname': request.user.id, })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('main'))


def activate(request, uidb64, token):
    user_model = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('main'))
    else:
        return HttpResponse('Activation link is invalid!')


def characters_list(request):
    user = request.user
    characters = models.Character.objects.by_uid(user.pk)
    char_data = dict()
    for character in characters:
        char_data[character.pk] = character.data_to_model()
        if char_data.get(character.pk).is_rt():
            if 'ST_IFL' in char_data.get(character.pk).stats().keys():
                char_data.get(character.pk).stats().pop('ST_IFL', None)
                character.character_data = char_data.get(character.pk).toJSON()
                character.save()
    in_progress = models.CreationData.objects.by_uid(user.pk)
    in_progress_rt = models.RTCreationData.objects.by_uid(user.pk)
    return TemplateResponse(request, 'characters_list.html',
                            {'version': VERSION, 'facade': rt_flyweights, 'characters': characters,
                             'in_progress': in_progress, 'in_progress_rt': in_progress_rt,
                             'char_data': char_data, })


def create_character_start(request):
    creation_data = models.CreationData()
    creation_data.owner = models.CharsheetUser.objects.get(pk=request.user.pk)
    creation_data.save()
    return HttpResponseRedirect(reverse('create-character-init', kwargs={'creation_id': creation_data.pk}))


@csrf_exempt
def create_character_init(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        form = CreationSettingsForm(request.POST)
        if 'char-hw-prev' in request.POST:
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[0],
                                                                              'form': form})
        else:
            if ('char-cr-next' in request.POST) and form.is_valid():
                cleaned_data = form.cleaned_data
                cd.name = cleaned_data['name']
                cd.gender = cleaned_data['gender']
                cd.height = cleaned_data['height']
                cd.weight = cleaned_data['weight']
                cd.age = cleaned_data['age']
                cd.starting_xp = cleaned_data['starting_xp']
                cd.characteristic_base = cleaned_data['characteristics_base']
                cd.last_mod_date = datetime.datetime.now()
                cd.curr_stage = 'hw_choice'
                cd.save()
        return HttpResponseRedirect(reverse('create-character-hw', kwargs={'creation_id': cd.pk}))
    else:
        form = CreationSettingsForm()
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[0], 'form': form})


@csrf_exempt
def create_character_hw_choice(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-cr-next' in request.POST:
            form = HomeworldsChoiceForm()
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[1],
                                                                              'form': form})
        form = HomeworldsChoiceForm(request.POST)
        if 'char-hw-next' in request.POST:
            if form.is_valid():
                cd.homeworld = form.cleaned_data['homeworld']
                cd.last_mod_date = datetime.datetime.now()
                cd.curr_stage = 'stat_distr'
                cd.save()
                return HttpResponseRedirect(reverse('create-character-stats', kwargs={'creation_id': cd.pk}))
        if 'char-hw-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-init', kwargs={'creation_id': cd.pk}))
    else:
        form = HomeworldsChoiceForm()
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[1], 'form': form})


def create_character_stat_distribution(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-hw-next' in request.POST:
            form = StatDistributionForm()
            return TemplateResponse(request, 'character_creation_form', {'version': VERSION, 'facade': flyweights,
                                                                         'stage': CREATION_STAGES[2], 'form': form})
        if 'char-st-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-hw', kwargs={'creation_id': cd.pk}))
        form = StatDistributionForm(request.POST)
        if 'char-st-next' in request.POST:
            if form.is_valid():
                stats = dict()
                homeworld = flyweights.homeworlds().get(cd.homeworld)
                cleaned_data = form.cleaned_data
                base = 20
                if cd.characteristic_base == 'CS_25':
                    base += 5
                for stat in STAT_TAGS:
                    stats[stat] = Stat(stat, base)
                    if stat in homeworld.get_stat_mods().keys():
                        stats.get(stat).improve(homeworld.get_stat_mods().get(stat))
                stats.get(ST_WEAPON_SKILL).improve(cleaned_data['ws_value'])
                stats.get(ST_BALLISTIC_SKILL).improve(cleaned_data['bs_value'])
                stats.get(ST_STRENGTH).improve(cleaned_data['str_value'])
                stats.get(ST_TOUGHNESS).improve(cleaned_data['t_value'])
                stats.get(ST_AGILITY).improve(cleaned_data['ag_value'])
                stats.get(ST_INTELLIGENCE).improve(cleaned_data['int_value'])
                stats.get(ST_PERCEPTION).improve(cleaned_data['per_value'])
                stats.get(ST_WILLPOWER).improve(cleaned_data['wp_value'])
                stats.get(ST_FELLOWSHIP).improve(cleaned_data['fel_value'])
                stats.get(ST_INFLUENCE).improve(cleaned_data['ifl_value'])

                cd.weapon_skill = stats.get(ST_WEAPON_SKILL).value()
                cd.ballistic_skill = stats.get(ST_BALLISTIC_SKILL).value()
                cd.strength = stats.get(ST_STRENGTH).value()
                cd.toughness = stats.get(ST_TOUGHNESS).value()
                cd.agility = stats.get(ST_AGILITY).value()
                cd.intelligence = stats.get(ST_INTELLIGENCE).value()
                cd.perception = stats.get(ST_PERCEPTION).value()
                cd.willpower = stats.get(ST_WILLPOWER).value()
                cd.fellowship = stats.get(ST_FELLOWSHIP).value()
                cd.influence = stats.get(ST_INFLUENCE).value()
                cd.curr_stage = 'bg_choice'
                cd.last_mod_date = datetime.datetime.now()
                cd.save()
                return HttpResponseRedirect(reverse('create-character-bg', kwargs={'creation_id': cd.pk}))
    else:
        form = StatDistributionForm()
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[2], 'form': form})


@csrf_exempt
def create_character_bg_choice(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        form = BackgroundChoiceForm(request.POST)
        if 'char-bg-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-stats', kwargs={'creation_id': cd.pk}))
        if 'char-bg-next' in request.POST:
            if form.is_valid():
                cd.background = form.cleaned_data['backgrounds']
                cd.curr_stage = 'role_choice'
                cd.last_mod_date = datetime.datetime.now()
                cd.save()
                return HttpResponseRedirect(reverse('create-character-role', kwargs={'creation_id': cd.pk}))
    else:
        form = BackgroundChoiceForm()
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[3], 'form': form})


@csrf_exempt
def create_character_role_choice(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-st-next' in request.POST:
            form = RoleChoiceForm()
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[4],
                                                                              'form': form})
        if 'char-role-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-bg', kwargs={'creation_id': cd.pk}))
        form = RoleChoiceForm(request.POST)
        if 'char-role-next' in request.POST:
            if form.is_valid():
                cd.role = form.cleaned_data['roles']
                cd.last_mod_date = datetime.datetime.now()
                cd.curr_stage = 'choices'
                cd.save()
                return HttpResponseRedirect(reverse('create-character-choice', kwargs={'creation_id': cd.pk}))

    else:
        form = RoleChoiceForm()
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[4], 'form': form})


@csrf_exempt
def create_character_choices(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-choices-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-role', kwargs={'creation_id': cd.pk}))
        if 'char-role-next' in request.POST:
            form = ChoicesForm(flyweights, cd)
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[5],
                                                                              'form': form})
        form = ChoicesForm(flyweights, cd, request.POST)
        if 'char-apts-prev' in request.POST:
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[5],
                                                                              'form': form})
        if 'char-choices-next' in request.POST:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                cd.background_apt = cleaned_data['background_apts']
                if len(flyweights.backgrounds().get(cd.background).get_skill_choices()) > 0:
                    cd.bg_skill_1 = cleaned_data['background_skills']
                    if 'background-skills-subtag' in cleaned_data:
                        cd.bg_skill_1_subtag = cleaned_data['background-skills-subtag']
                    if len(flyweights.backgrounds().get(cd.background).get_skill_choices()) > 1:
                        cd.bg_skill_2 = cleaned_data['background_skills2']
                        if 'background-skills-subtag2' in cleaned_data:
                            cd.bg_skill_2_subtag = cleaned_data['background-skills-subtag2']
                if form.fields['background_talents'].required:
                    cd.bg_talent = cleaned_data['background_talents']
                if form.fields['background_traits'].required:
                    cd.bg_trait = cleaned_data['background_traits']
                if form.fields['role_apts'].required:
                    cd.role_apt = cleaned_data['role_apts']
                cd.role_talent = cleaned_data['role_talent']
                if 'hw-bonus-talent' in form.fields.keys():
                    cd.hw_bonus_talent = cleaned_data['hw-bonus-talent']
                cd.curr_stage = 'double_apts'
                cd.last_mod_date = datetime.datetime.now()
                cd.save()
                return HttpResponseRedirect(reverse('create-character-double-apts', kwargs={'creation_id': cd.pk}))
            else:
                return TemplateResponse(request, 'character_creation_form.html',
                                        {'version': VERSION, 'facade': flyweights,
                                         'stage': CREATION_STAGES[5], 'form': form})
    else:
        form = ChoicesForm(flyweights, cd)
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[5], 'form': form})


def count_doubles(cd, hw, role):
    doubles = 0
    hw_apt = hw.get_aptitude()
    bg_apt = cd.background_apt
    role_apts = role.get_aptitudes()
    if bg_apt == hw_apt:
        doubles += 1
    if cd.role_apt is not None:
        if (cd.role_apt == bg_apt) or (cd.role_apt == hw_apt):
            doubles += 1
    for apt in role_apts:
        if (apt == bg_apt) or (apt == hw_apt):
            doubles += 1
        if cd.role_apt is not None:
            if cd.role_apt == apt:
                doubles += 1
    return doubles


def make_apts(cd, hw, role):
    hw_apt = hw.get_aptitude()
    bg_apt = cd.background_apt
    role_apts = role.get_aptitudes()
    role_apt = None
    if cd.role_apt is not None:
        role_apt = cd.role_apt

    apts = list()
    apts.append(A_GENERAL)

    apts.append(hw_apt)
    if bg_apt not in apts:
        apts.append(bg_apt)
    for apt in role_apts:
        if apt not in apts:
            apts.append(apt)
    if role_apt is not None:
        if role_apt not in apts:
            apts.append(role_apt)
    return apts


def create_character_double_apts(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    role = flyweights.roles().get(cd.role)
    homeworld = flyweights.homeworlds().get(cd.homeworld)
    doubled = count_doubles(cd, homeworld, role)
    apts = make_apts(cd, homeworld, role)

    if doubled == 0:
        cd.curr_stage = 'divination'
        cd.save()
        return HttpResponseRedirect(reverse('create-character-divination', kwargs={'creation_id': cd.pk}))

    if request.method == 'POST':
        if 'char-apts-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-choice', kwargs={'creation_id': cd.pk}))
        if 'char-choices-next' in request.POST:
            form = DoubleAptsChoiceForm(doubled, apts, flyweights)
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[6],
                                                                              'form': form})
        form = DoubleAptsChoiceForm(doubled, apts, flyweights, request.POST)
        if form.is_valid():
            cd.apt_1 = form.cleaned_data['apt_choice']
            if doubled > 1:
                cd.apt_2 = form.cleaned_data['apt_choice2']
            else:
                cd.apt_2 = None
            cd.last_mod_date = datetime.datetime.now()
            cd.curr_stage = 'divination'
            cd.save()
            return HttpResponseRedirect(reverse('create-character-divination', kwargs={'creation_id': cd.pk}))
        else:
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[6],
                                                                              'form': form})
    else:
        form = DoubleAptsChoiceForm(doubled, apts, flyweights)
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[6], 'form': form})


def prep_stats(cd: models.CreationData):
    stats = dict()
    stats[ST_WEAPON_SKILL] = Stat(ST_WEAPON_SKILL, cd.weapon_skill)
    stats[ST_BALLISTIC_SKILL] = Stat(ST_BALLISTIC_SKILL, cd.ballistic_skill)
    stats[ST_STRENGTH] = Stat(ST_STRENGTH, cd.strength)
    stats[ST_TOUGHNESS] = Stat(ST_TOUGHNESS, cd.toughness)
    stats[ST_AGILITY] = Stat(ST_AGILITY, cd.agility)
    stats[ST_INTELLIGENCE] = Stat(ST_INTELLIGENCE, cd.intelligence)
    stats[ST_PERCEPTION] = Stat(ST_PERCEPTION, cd.perception)
    stats[ST_WILLPOWER] = Stat(ST_WILLPOWER, cd.willpower)
    stats[ST_FELLOWSHIP] = Stat(ST_FELLOWSHIP, cd.fellowship)
    stats[ST_INFLUENCE] = Stat(ST_INFLUENCE, cd.influence)
    return stats


def create_character_divination(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)

    background = flyweights.backgrounds().get(cd.background)
    homeworld = flyweights.homeworlds().get(cd.homeworld)
    role = flyweights.roles().get(cd.role)

    if request.method == 'POST':
        if 'char-div-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-double-apts', kwargs={'creation_id': cd.pk}))
        if 'char-div-next' in request.POST:
            form = DivinationForm(flyweights, cd, background, request.POST)
            div_tag = None
            if form.is_valid():
                divination_roll = form.cleaned_data['divination_roll']
                for div_key in flyweights.divinations().keys():
                    divination = flyweights.divinations().get(div_key)
                    if (divination_roll >= divination.get_roll_range()[0]) \
                            and (divination_roll <= divination.get_roll_range()[1]):
                        div_tag = div_key
                        break
                cd.wound_roll = form.cleaned_data['wound_roll']
                cd.fate_roll = form.cleaned_data['fate_roll']
                cd.last_mod_date = datetime.datetime.now()

                for field in form.cleaned_data:
                    if 'subtag_' in field:
                        if len(cd.spec_skill_subtag_1) == 0:
                            cd.spec_skill_subtag_1 = form.cleaned_data[field]
                        else:
                            cd.spec_skill_subtag_2 = form.cleaned_data[field]
                cd.last_mod_date = datetime.datetime.now()
                cd.save()

                xp_given = cd.starting_xp
                fate = homeworld.get_fate()
                if cd.fate_roll >= homeworld.get_blessing():
                    fate += 1

                stats = prep_stats(cd)

                fatigue = stats.get(ST_TOUGHNESS).bonus() + stats.get(ST_WILLPOWER).bonus()
                if cd.background == BACKGROUND_OUTCAST:
                    fatigue += 2
                wounds = cd.wound_roll + homeworld.get_wounds()

                apts = make_apts(cd, homeworld, role)
                if (cd.apt_1 is not None) and (len(cd.apt_1) > 0):
                    apts.append(cd.apt_1)
                    if (cd.apt_2 is not None) and (len(cd.apt_2) > 0):
                        apts.append(cd.apt_2)

                skills = dict()
                skdescrs = flyweights.skill_descriptions()
                any_count = 0
                for key in skdescrs.keys():
                    if not skdescrs.get(key).is_specialist():
                        skills[key] = Skill(key, 0)
                for skill in background.get_skills():
                    if skill.get('tag') in skills.keys():
                        if skdescrs.get(skill.get('tag')).is_specialist():
                            if skill.get('subtag') != 'SK_ANY':
                                subtag = skill.get('subtag')
                            else:
                                if any_count == 0:
                                    subtag = cd.spec_skill_subtag_1
                                    any_count += 1
                                else:
                                    subtag = cd.spec_skill_subtag_2
                            skills.get(skill.get('tag')).upgrade_subtag(subtag)
                        else:
                            skills.get(skill.get('tag')).upgrade()

                    else:
                        if flyweights.skill_descriptions().get(skill.get('tag')).is_specialist():
                            if skill.get('subtag') == 'SK_ANY':
                                if any_count == 0:
                                    subtag = cd.spec_skill_subtag_1
                                    any_count += 1
                                else:
                                    subtag = cd.spec_skill_subtag_2
                            else:
                                subtag = skill.get('subtag')
                            skills[skill.get('tag')] = Skill(skill.get('tag'), {subtag: 1})

                if cd.bg_skill_1 is not None:
                    choice = background.get_skill_choices()[0][cd.bg_skill_1]
                    if choice.get('tag') in flyweights.skill_descriptions().keys():
                        if choice.get('tag') in skills.keys():
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') != 'SK_ANY':
                                    cs = choice.get('subtag')
                                else:
                                    cs = cd.bg_skill_1_subtag
                                skills.get(choice.get('tag')).upgrade_subtag(cs)
                            else:
                                skills.get(choice.get('tag')).upgrade()
                        else:
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') == 'SK_ANY':
                                    subtag = cd.bg_skill_1_subtag
                                else:
                                    subtag = choice.get('subtag')
                                skills[choice.get('tag')] = Skill(choice.get('tag'), {subtag: 1})
                if cd.bg_skill_2 is not None:
                    choice = background.get_skill_choices()[0][cd.bg_skill_2]
                    if choice.get('tag') in flyweights.skill_descriptions().keys():
                        if choice.get('tag') in skills.keys():
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                    if choice.get('subtag') != 'SK_ANY':
                                        cs = choice.get('subtag')
                                    else:
                                        cs = cd.bg_skill_2_subtag
                                    skills.get(choice.get('tag')).upgrade_subtag(cs)
                                else:
                                    skills.get(choice.get('tag')).upgrade()
                            else:
                                skills.get(choice.get('tag')).upgrade()
                        else:
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') == 'SK_ANY':
                                    subtag = cd.bg_skill_2_subtag
                                else:
                                    subtag = choice.get('subtag')
                                skills[choice.get('tag')] = Skill(choice.get('tag'), {subtag: 1})

                talents = dict()
                hw_bonus = homeworld.get_bonus()
                bg_bonus = background.get_bonus()

                for talent in background.get_talents():
                    if talent.get('tag') in talents.keys():
                        if flyweights.talent_descriptions().get(talent.get('tag')).is_specialist():
                            for key in talent.keys():
                                if (key in ['subtag', 'subtag1', 'subtag2']) \
                                        and (key not in talents.get(talent.get('tag')).taken().keys()):
                                    talents.get(talent.get('tag')).take_subtag(flyweights, talent.get(key))
                    else:
                        if flyweights.talent_descriptions().get(talent.get('tag')).is_specialist():
                            taken = dict()
                            for key in talent.keys():
                                if key in ['subtag', 'subtag1', 'subtag2']:
                                    taken[talent.get(key)] = 1
                        else:
                            taken = 1
                        bg_talent = Talent(talent.get('tag'), taken)
                        talents[bg_talent.tag()] = bg_talent

                if cd.bg_talent is not None:
                    bg_talent_choice = background.get_talent_choices()[cd.bg_talent]
                    if bg_talent_choice.get('tag') in talents.keys():
                        if flyweights.talent_descriptions().get(bg_talent_choice.get('tag')).is_specialist():
                            for key in bg_talent_choice.keys():
                                if (key in ['subtag', 'subtag1', 'subtag2']) \
                                        and (key not in talents.get(bg_talent_choice.get('tag')).taken().keys()):
                                    talents.get(bg_talent_choice.get('tag')).take_subtag(flyweights,
                                                                                         bg_talent_choice.get(key))
                    else:
                        if flyweights.talent_descriptions().get(bg_talent_choice.get('tag')).is_specialist():
                            taken = dict()
                            for key in bg_talent_choice.keys():
                                if key in ['subtag', 'subtag1', 'subtag2']:
                                    taken[bg_talent_choice.get(key)] = 1
                        else:
                            taken = 1
                        talent = Talent(bg_talent_choice.get('tag'), taken)
                        talents[talent.tag()] = talent

                if role.get_talent_choices()[0].get('tag') == cd.role_talent:
                    role_talent_choice = role.get_talent_choices()[0]
                else:
                    role_talent_choice = role.get_talent_choices()[1]
                if role_talent_choice.get('tag') not in talents.keys():
                    if flyweights.talent_descriptions().get(role_talent_choice.get('tag')).is_specialist():
                        taken = dict()
                        for key in role_talent_choice.keys():
                            if key in ['subtag', 'subtag1', 'subtag2']:
                                taken[role_talent_choice.get(key)] = 1
                    else:
                        taken = 1
                    talents[role_talent_choice.get('tag')] = Talent(role_talent_choice.get('tag'), taken)
                elif flyweights.talent_descriptions().get(role_talent_choice.get('tag')).is_specialist():
                    for key in role_talent_choice.keys():
                        if (key in ['subtag', 'subtag1', 'subtag2']) \
                                and (role_talent_choice.get(key) not in
                                     talents.get(role_talent_choice.get('tag')).taken().keys()):
                            talents.get(role_talent_choice.get('tag')).take_subtag(flyweights,
                                                                                   role_talent_choice.get(key))

                traits = dict()
                for trait in background.get_traits():
                    if flyweights.trait_descriptions().get(trait.get('tag')).is_specialist():
                        taken = dict()
                        for key in trait.keys():
                            if key in ['subtag', 'subtag1', 'subtag2']:
                                if flyweights.trait_descriptions().get(trait.get('tag')).is_stackable():
                                    taken[trait.get(key)] = trait.get('taken')
                                else:
                                    taken[trait.get(key)] = 1
                    else:
                        if flyweights.trait_descriptions().get(trait.get('tag')).is_stackable():
                            taken = trait.get('taken')
                        else:
                            taken = 1
                    traits[trait.get('tag')] = Trait(trait.get('tag'), taken)

                divination = flyweights.divinations().get(div_tag)
                malignancies = list()
                mutations = list()
                disorders = list()
                character = models.Character.objects.create(owner=request.user, character_data='')
                character.save()
                character_model = CharacterModel(character.id, -1, cd.name, cd.gender, cd.height,
                                                 cd.weight, cd.age, cd.homeworld,
                                                 cd.background, cd.role, div_tag, [],
                                                 [wounds, wounds], [0, fatigue], [xp_given, 0], [fate, fate], 0, 0,
                                                 0, apts, stats, skills, talents, traits, [],
                                                 [], disorders, malignancies, mutations, list(), list(), list(),
                                                 0, 0)
                for cmd in divination.get_commands():
                    character_model.pending().append(cmd)
                for cmd in bg_bonus.get_commands():
                    character_model.pending().append(cmd)
                for cmd in hw_bonus.get_commands():
                    character_model.pending().append(cmd)
                for cmd in role.get_bonus().get_commands():
                    character_model.pending().append(cmd)
                character_model = commands_parser.process_character(character_model)
                character.character_data = character_model.toJSON()
                character.creation_date = cd.last_mod_date
                character.save()
                cd.delete()
                return HttpResponseRedirect(reverse('characters-list'))
            else:
                return TemplateResponse(request, 'character_creation_form.html',
                                        {'version': VERSION, 'facade': flyweights,
                                         'stage': CREATION_STAGES[7], 'form': form})
        if 'char-apts-next' in request.POST:
            form = DivinationForm(flyweights, cd, background)
            return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                              'stage': CREATION_STAGES[7],
                                                                              'form': form})
    else:
        form = DivinationForm(flyweights, cd, background)
        return TemplateResponse(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                          'stage': CREATION_STAGES[7], 'form': form})


def clean_completed(character_model, request):
    if character_model.is_rt():
        return rt_views.clean_completed(character_model, request)
    if int(request.POST.get('cmd_id')) >= 0:
        for cmd in character_model.pending():
            if cmd.get('cmd_id') == int(request.POST.get('cmd_id')):
                character_model.pending().remove(cmd)
                break
    return character_model


def find_cmd(request, character_model):
    if character_model.is_rt():
        return rt_views.find_cmd(request, character_model)
    cmd = dict()
    for pcmd in character_model.pending():
        if pcmd.get('cmd_id') == int(request.POST.get('cmd_id')):
            cmd = pcmd
            break
    return cmd


def gain_insanity(request, character, character_record: models.Character):
    if character.is_rt():
        return rt_views.gain_insanity(rt_views, character, character_record)
    if int(request.POST.get('cmd_id')) >= 0:
        cmd = find_cmd(request, character)
    else:
        cmd = None
    insanity_form = GainInsanityRollForm(cmd, request.POST)
    if insanity_form.is_valid():
        character.gain_insanity(insanity_form.cleaned_data['roll_value'])
        character = clean_completed(character, request)
        character_record.character_data = character.toJSON()
        character_record.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character_record.pk, }))


def gain_corruption(request, character, character_record: models.Character):
    if character.is_rt():
        return rt_views.gain_corruption(request, character, character_record)
    if int(request.POST.get('cmd_id')) >= 0:
        cmd = find_cmd(request, character)
    else:
        cmd = None
    corruption_form = GainCorruptionRollForm(cmd, request.POST)
    if corruption_form.is_valid():
        character.gain_corruption(corruption_form.cleaned_data['roll_value'])
        character = clean_completed(character, request)
        character_record.character_data = character.toJSON()
        character_record.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character_record.pk, }))


def decrease_stat_alt(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.decrease_stat_alt(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = DecreaseStatAltForm(cmd, flyweights, request.POST)
    if form.is_valid():
        character_model.damage_stat(form.cleaned_data['choices'], form.amount())
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def increase_stat_alt(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.increase_stat_alt(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = IncreaseStatAltForm(cmd, flyweights, request.POST)
    if form.is_valid():
        character_model.improve_stat(form.cleaned_data['choices'], form.amount())
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_talent_alt(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_talent_alt(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainTalentAltForm(cmd, flyweights, request.POST)
    if form.is_valid():
        character_model.gain_talent(form.cleaned_data['choices'], flyweights)
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def decrease_stat_roll(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.decrease_stat_roll(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = DecreaseStatRollForm(cmd, flyweights, request.POST)
    if form.is_valid():
        character_model.damage_stat(cmd.get('tag'), form.cleaned_data['roll_value'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def increase_stat_roll(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.increase_stat_roll(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = IncreaseStatRollForm(cmd, flyweights, request.POST)
    if form.is_valid():
        character_model.improve_stat(cmd.get('tag'), form.cleaned_data['roll_value'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def abort_gain(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.abort_gain(request, character_model, character)
    character_model = clean_completed(character_model, request)
    character.character_data = character_model.toJSON()
    character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def abort_gain_ip_conseq(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.abort_gain_ip_conseq(request, character_model, character)
    character_model.inc_ip_tests()
    abort_gain(request, character_model, character)


def abort_gain_cp_conseq(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.abort_gain_cp_conseq(request, character_model, character)
    character_model.inc_cp_tests()
    abort_gain(request, character_model, character)


def gain_disorder(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_disorder(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainDisorderIPForm(cmd, request.POST)
    if form.is_valid():
        disorder = {'name': form.cleaned_data['disorder_name'],
                    'description': form.cleaned_data['disorder_description']}
        character_model.disorders().append(disorder)
        character_model.inc_ip_tests()
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_trauma(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_trauma(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GetTraumaIPForm(cmd, request.POST)
    if form.is_valid():
        character_model = clean_completed(character_model, request)
        character_model.inc_ip_tests()
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_malignancy(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_malignancy(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainMalignancyRollForm(cmd, request.POST)
    if form.is_valid():
        roll_result = form.cleaned_data['roll_result']
        for mal_key, mal in flyweights.malignancies().items():
            if (roll_result >= mal.get_rolls_range()[0]) and (roll_result <= mal.get_rolls_range()[1]):
                if mal_key not in character_model.malignances():
                    character_model.malignances().append(mal_key)
                    for cmd in mal.get_commands():
                        character_model.pending().append(cmd)
                    character_model.inc_cp_tests()
                    character_model = clean_completed(character_model, request)
                    character.character_data = character_model.toJSON()
                    character.save()
                break
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_mutation(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_mutation(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainMutationRollForm(cmd, request.POST)
    if form.is_valid():
        roll_result = form.cleaned_data['roll_result']
        for mut_key, mut in flyweights.mutations().items():
            if (roll_result >= mut.get_rolls_range()[0]) and (roll_result <= mut.get_rolls_range()[1]):
                if mut_key not in character_model.mutations():
                    character_model.mutations().append(mut_key)
                    for cmd in mut.get_commands():
                        character_model.pending().append(cmd)
                    character_model.inc_cp_tests()
                    character_model = clean_completed(character_model, request)
                    character.character_data = character_model.toJSON()
                    character.save()
                break
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_malignance_choice(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_malignance_choice(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainMalignancyChoiceForm(flyweights, cmd, request.POST)
    if form.is_valid():
        choice = form.cleaned_data['choices']
        if choice not in character_model.malignances():
            character_model.malignances().append(choice)
            for cmd in flyweights.malignancies().get(choice).get_commands():
                character_model.pending().append(cmd)
            character_model = clean_completed(character_model, request)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_mutation_choice(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_mutation_choice(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainMutationChoiceForm(flyweights, cmd, request.POST)
    if form.is_valid():
        choice = form.cleaned_data['choices']
        if choice not in character_model.mutations():
            character_model.mutations().append(choice)
            character_model = clean_completed(character_model, request)
            for cmd in flyweights.mutations().get(choice).get_commands():
                character_model.pending().append(cmd)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_stat_aptitude(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_stat_aptitude(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainStatAptitudeForm(character_model, flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.aptitudes().append(form.cleaned_data['choices'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_spec_skill(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_spec_skill(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainSpecSkillForm(flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.improve_skill_subtag(form.sk_tag, form.cleaned_data['subtag'], flyweights)
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def origin_extra_confirm(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.origin_extra_confirm(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainExtraOriginCommand(cmd, request.POST)
    if form.is_valid():
        character_model.spend_xp(cmd.get('cost'))
        for command in cmd.get('commands'):
            character_model.pending().append(command)
        character.character_data = character_model.toJSON()
        clean_completed(character_model, request)
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_spec_talent(request, character_model, character: models.Character):
    if character_model.is_rt():
        return rt_views.gain_spec_talent(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainSpecTalentForm(rt_flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.gain_talent_subtag(form.sk_tag, form.cleaned_data['subtag'], rt_flyweights)
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def origin_extra_abort(request, character_model, character: models.Character):
    if character_model.is_rt():
        return origin_extra_abort(request, character_model, character)
    cmd = find_cmd(request, character_model)
    form = GainExtraOriginCommand(cmd)
    if form.is_valid():
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def parse_manual_cmds(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.parse_manual_cmds(request, character, character_model)
    if 'gain-insanity-confirm' in request.POST:
        gain_insanity(request, character_model, character)
    if 'gain-corruption-confirm' in request.POST:
        gain_corruption(request, character_model, character)
    if 'statdec-alt-confirm' in request.POST:
        decrease_stat_alt(request, character_model, character)
    if 'statinc-alt-confirm' in request.POST:
        increase_stat_alt(request, character_model, character)
    if 'talent-alt-confirm' in request.POST:
        gain_talent_alt(request, character_model, character)
    if 'dec-stat-confirm' in request.POST:
        decrease_stat_roll(request, character_model, character)
    if 'inc-stat-confirm' in request.POST:
        increase_stat_roll(request, character_model, character)
    if 'gain-mut-confirm' in request.POST:
        gain_mutation(request, character_model, character)
    if 'gain-mal-confirm' in request.POST:
        gain_malignancy(request, character_model, character)
    if ('gain-mut-abort' in request.POST) or ('gain-mal-abort' in request.POST):
        abort_gain_cp_conseq(request, character_model, character)
    if 'gain-disorder-confirm' in request.POST:
        gain_disorder(request, character_model, character)
    if 'gain-trauma-confirm' in request.POST:
        gain_trauma(request, character_model, character)
    if ('gain-disorder-abort' in request.POST) or ('gain-trauma-abort' in request.POST):
        abort_gain_ip_conseq(request, character_model, character)
    if 'mal-choice-confirm' in request.POST:
        gain_malignance_choice(request, character_model, character)
    if 'mut-choice-confirm' in request.POST:
        gain_mutation_choice(request, character_model, character)
    if 'gain-stat-apt-confirm' in request.POST:
        gain_stat_aptitude(request, character_model, character)
    if 'skill-spec-confirm' in request.POST:
        gain_spec_skill(request, character_model, character)
    if 'talent-spec-confirm' in request.POST:
        gain_spec_talent(request, character_model, character)
    if 'origin-extra-confirm' in request.POST:
        origin_extra_confirm(request, character_model, character)
    if 'origin-extra-abort' in request.POST:
        origin_extra_abort(request, character_model, character)


def upg_data_to_forms(character):
    if character.is_rt():
        return rt_views.upg_data_to_forms(character)
    upg_costs = character.make_upg_costs(flyweights)
    forms = {'stats': list(),
             'skills': {'common': list(), 'spec': list()},
             'talents': {'available': dict(), 'unavailable': dict()},
             'ea': {'available': list(), 'unavailable': list()}
             }

    forms.get('talents').get('available')[1] = {'common': list(), 'spec': list()}
    forms.get('talents').get('available')[2] = {'common': list(), 'spec': list()}
    forms.get('talents').get('available')[3] = {'common': list(), 'spec': list()}

    forms.get('talents').get('unavailable')[1] = {'common': list(), 'spec': list()}
    forms.get('talents').get('unavailable')[2] = {'common': list(), 'spec': list()}
    forms.get('talents').get('unavailable')[3] = {'common': list(), 'spec': list()}
    for stat_tag in flyweights.stat_tags():
        if stat_tag in upg_costs.get('stats').keys():
            forms.get('stats').append(
                StatUpgradeForm(stat_tag, character.stats().get(stat_tag).value(),
                                upg_costs.get('stats').get(stat_tag).get('cost'),
                                upg_costs.get('stats').get(stat_tag).get('colour')))
    for skill_tag in upg_costs.get('skills').keys():
        if not flyweights.skill_descriptions().get(skill_tag).is_specialist():
            forms.get('skills').get('common').append(
                SkillUpgradeForm(skill_tag, upg_costs.get('skills').get(skill_tag).get('cost'),
                                 character.skills().get(skill_tag).get_adv_bonus(),
                                 upg_costs.get('skills').get(skill_tag).get('colour')))
        else:
            form_map = dict()
            form_map['skill_tag'] = skill_tag
            form_map['forms'] = list()
            for key, value in upg_costs.get('skills').get(skill_tag).items():
                if key == 'colour':
                    form_map[key] = value
                else:
                    if skill_tag in character.skills().keys():
                        adv_bonus = character.skills().get(skill_tag).get_adv_bonus_subtag(key)
                    else:
                        adv_bonus = -20
                    form_map.get('forms').append(SkillSubtagUpgradeForm(
                        skill_tag, key, value, adv_bonus))
            forms.get('skills').get('spec').append(form_map)
    for tier in upg_costs.get('talents').get('available').keys():
        for tl_tag, talent in upg_costs.get('talents').get('available').get(tier).items():
            if not flyweights.talent_descriptions().get(tl_tag).is_specialist():
                if not character.has_talent(tl_tag):
                    if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                        taken = 0
                    else:
                        taken = -1
                else:
                    if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                        taken = character.talents().get(tl_tag).taken()
                    else:
                        taken = -1
                forms.get('talents').get('available')[tier].get('common').append(
                    TalentUpgradeForm(tl_tag, talent.get('cost'), talent.get('colour'), True, taken))
            else:
                form_map = dict()
                form_map['tl_tag'] = tl_tag
                form_map['forms'] = list()
                for key, value in talent.items():
                    if key == 'colour':
                        form_map[key] = value
                    else:
                        if key == 'TL_ANY':
                            if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                                taken = 0
                            else:
                                taken = -1
                        else:
                            if character.has_talent_subtag(tl_tag, key):
                                taken = character.talents().get(tl_tag).taken_subtag(key)
                            else:
                                taken = 0
                        form_map.get('forms').append(TalentUpgradeSubtagForm(tl_tag, key, value, True, taken))
                forms.get('talents').get('available')[tier].get('spec').append(form_map)
    if 'unavailable' in upg_costs.get('talents').keys():
        for tier in upg_costs.get('talents').get('unavailable').keys():
            for tl_tag, talent in upg_costs.get('talents').get('unavailable').get(tier).items():
                if not rt_flyweights.talent_descriptions().get(tl_tag).is_specialist():
                    if not character.has_talent(tl_tag):
                        if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                            taken = 0
                        else:
                            taken = -1
                    else:
                        if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                            taken = character.talents().get(tl_tag).taken()
                        else:
                            taken = -1
                    forms.get('talents').get('unavailable')[tier].get('common').append(
                        TalentUpgradeForm(tl_tag, talent.get('cost'), talent.get('colour'), False, taken))
                else:
                    form_map = dict()
                    form_map['tl_tag'] = tl_tag
                    form_map['forms'] = list()
                    for key, value in talent.items():
                        if key == 'colour':
                            form_map[key] = value
                        else:
                            if key == 'TL_ANY':
                                if rt_flyweights.talent_descriptions().get(tl_tag).is_stackable():
                                    taken = 0
                                else:
                                    taken = -1
                            else:
                                if character.has_talent_subtag(tl_tag, key):
                                    taken = character.talents().get(tl_tag).taken_subtag(key)
                                else:
                                    taken = 0
                            form_map.get('forms').append(TalentUpgradeSubtagForm(
                                tl_tag, key, value, False, taken))
                    forms.get('talents').get('unavailable')[tier].get('spec').append(form_map)
    for ea_key, cost in upg_costs.get('ea').get('available').items():
        forms.get('ea').get('available').append(EliteAdvanceUpgradeForm(ea_key, cost, True))
    for ea_key, cost in upg_costs.get('ea').get('unavailable').items():
        forms.get('ea').get('unavailable').append(EliteAdvanceUpgradeForm(ea_key, cost, False))
    if 'pr' in upg_costs.keys():
        forms['pr'] = PRUpgrageForm(character.pr(), upg_costs.get('pr'))
    if 'psy' in upg_costs.keys():
        forms['psy'] = {'available': dict(), 'unavailable': dict()}
        for school in upg_costs.get('psy').get('available').keys():
            forms.get('psy').get('available')[school] = list()
            for power, cost in upg_costs.get('psy').get('available').get(school).items():
                forms.get('psy').get('available').get(school).append(PsyPowerUpgradeForm(power, cost, True))
        for school in upg_costs.get('psy').get('unavailable').keys():
            forms.get('psy').get('unavailable')[school] = list()
            for power, cost in upg_costs.get('psy').get('unavailable').get(school).items():
                forms.get('psy').get('unavailable').get(school).append(PsyPowerUpgradeForm(power, cost, False))
    return forms


@csrf_exempt
def process_wounds(request, character, character_model):
    form = WoundControlsForm(request.POST)
    if 'wound' in request.POST:
        if form.is_valid():
            character_model.damage(form.cleaned_data.get('amount'))
            character.character_data = character_model.toJSON()
            character.save()
    if 'heal' in request.POST:
        if form.is_valid():
            character_model.heal(form.cleaned_data.get('amount'))
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


@csrf_exempt
def process_fatigue(request, character, character_model):
    form = FatigueControlsForm(request.POST)
    if 'gainFatigue' in request.POST:
        if form.is_valid():
            character_model.add_fatigue(form.cleaned_data.get('amount'))
            character.character_data = character_model.toJSON()
            character.save()
    if 'restoreFatigue' in request.POST:
        if form.is_valid():
            character_model.remove_fatigue(form.cleaned_data.get('amount'))
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


@csrf_exempt
def process_fate(request, character, character_model):
    if 'spend-fate' in request.POST:
        character_model.spend_fate()
        character.character_data = character_model.toJSON()
        character.save()
    if 'burn-fate' in request.POST:
        character_model.burn_fate()
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


@csrf_exempt
def character_view(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    character_model = character.data_to_model()
    insanity_form = None
    corruption_form = None
    wounds_form = None
    fate_form = None
    fatigue_form = None
    link_form = None
    reminders = None
    notes_link = None
    if character_model.is_rt():
        facade = rt_flyweights
        parser = rt_commands_parser
    else:
        facade = flyweights
        parser = commands_parser
    if (request.user is not None) and (request.user == character.owner):
        if request.method == 'POST':
            parse_manual_cmds(request, character, character_model)
            if 'char-link-change' in request.POST:
                link_form = AddDocLinkForm(request.POST)
                if link_form.is_valid():
                    character.notes = link_form.cleaned_data['link']
                    character.save()
                return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))
            if ('wound' in request.POST) or ('heal' in request.POST):
                return process_wounds(request, character, character_model)
            if ('gainFatigue' in request.POST) or ('restoreFatigue' in request.POST):
                return process_fatigue(request, character, character_model)
            if ('spend-fate' in request.POST) or ('burn-fate' in request.POST):
                return process_fate(request, character, character_model)
        wounds_form = WoundControlsForm()
        fate_form = FateControlsForm()
        fatigue_form = FatigueControlsForm()
        link_form = AddDocLinkForm({'link': character.notes_url()})
        insanity_form = GainInsanityRollForm()
        corruption_form = GainCorruptionRollForm()
        character_model = parser.process_character(character_model)
        reminders = list()
        if character.notes_url() and (character.notes_url()[:8] == 'https://'):
            notes_link = character.notes_url()
        else:
            notes_link = None
        # TODO: controls (stats/skills/talents upgrading, XP gaining, etc.
        if len(character_model.pending()) > 0:
            for cmd in character_model.pending():
                reminder = parser.make_reminder(cmd, character_model)
                if reminder is not None:
                    reminders.append(reminder)
                else:
                    character_model.pending().remove(cmd)
        character_model.check_fatigue_match()
        character.character_data = character_model.toJSON()
        character.save()
    is_owner = request.user == character.owner
    groups = character.groups.all()
    return TemplateResponse(request, "charsheet.html", {'version': VERSION, 'facade': facade,
                                                        'command_parser': parser, 'is_rt': character.is_rt,
                                                        'character': character_model,
                                                        'hookups': character_model.make_hookups(facade),
                                                        'insanity_form': insanity_form,
                                                        'corruption_form': corruption_form,
                                                        'notes': link_form, 'wounds_form': wounds_form,
                                                        'notes_link': notes_link, 'fate_form': fate_form,
                                                        'reminders': reminders, 'fatigue_form': fatigue_form,
                                                        'upg_view': character.get_upgrade_url(),
                                                        'is_owner': is_owner, 'groups': groups, })


def upgrade_stat(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_stat(request, character, character_model)
    stat_tag = request.POST.get('stat_tag')
    cost = int(request.POST.get('cost'))
    form = StatUpgradeForm(stat_tag, 0, cost, 'success', request.POST)
    if form.is_valid():
        if character_model.xp_current() >= cost:
            character_model.spend_xp(cost)
            character_model.upgrade_stat(stat_tag)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_skill(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_skill(request, character, character_model)
    skill_tag = request.POST.get('skill_tag')
    cost = int(request.POST.get('cost'))
    form = SkillUpgradeForm(skill_tag, cost, 0, 'success', request.POST)
    if form.is_valid():
        if character_model.xp_current() >= cost:
            character_model.spend_xp(cost)
            character_model.improve_skill(skill_tag)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_subskill(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_subskill(request, character, character_model)
    skill_tag = request.POST.get('skill_tag')
    subtag = request.POST.get('subtag_skill')
    cost = int(request.POST.get('cost'))
    form = SkillSubtagUpgradeForm(skill_tag, subtag, cost, 0, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        if subtag != 'SK_ANY':
            sk_subtag = subtag
        else:
            sk_subtag = form.cleaned_data.get('subtag')
        character_model.improve_skill_subtag(skill_tag, sk_subtag, flyweights)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_talent(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_talent(request, character, character_model)
    tl_tag = request.POST.get('tl_tag')
    cost = int(request.POST.get('cost'))
    form = TalentUpgradeForm(tl_tag, cost, 'success', True, 0, request.POST)
    if form.is_valid():
        if character_model.xp_current() >= cost:
            character_model.spend_xp(cost)
            character_model.gain_talent(tl_tag, flyweights)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_talent_subtag(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_talent_subtag(request, character, character_model)
    tl_tag = request.POST.get('tl_tag')
    subtag = request.POST.get('subtag_tl')
    cost = int(request.POST.get('cost'))
    form = TalentUpgradeSubtagForm(tl_tag, subtag, cost, True, 0, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        if subtag != 'TL_ANY':
            tl_subtag = subtag
        else:
            tl_subtag = form.cleaned_data.get('subtag')
        character_model.gain_talent_subtag(tl_tag, tl_subtag, flyweights)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_ea(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_ea(request, character, character_model)
    ea_tag = request.POST.get('ea_tag')
    cost = int(request.POST.get('cost'))
    form = EliteAdvanceUpgradeForm(ea_tag, cost, True, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.gain_ea_id(ea_tag)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_pr(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_pr(request, character, character_model)
    cost = int(request.POST.get('cost'))
    form = PRUpgrageForm(character_model.pr(), cost, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.gain_pr()
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_psy_power(request, character: models.Character, character_model):
    if character_model.is_rt():
        return rt_views.upgrade_psy_power(request, character, character_model)
    pp_tag = request.POST.get('pp_tag')
    cost = int(request.POST.get('cost'))
    form = PsyPowerUpgradeForm(pp_tag, cost, True, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.psy_powers().append(pp_tag)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def parse_upgrades(request, character: models.Character, character_model):
    if 'upg-stat-confirm' in request.POST:
        upgrade_stat(request, character, character_model)
    if 'upg-skill-confirm' in request.POST:
        upgrade_skill(request, character, character_model)
    if 'upg-skill-subtag-confirm' in request.POST:
        upgrade_subskill(request, character, character_model)
    if 'upg-talent-confirm' in request.POST:
        upgrade_talent(request, character, character_model)
    if 'upg-tl-subtag-confirm' in request.POST:
        upgrade_talent_subtag(request, character, character_model)
    if 'upg-ea-confirm' in request.POST:
        upgrade_ea(request, character, character_model)
    if 'upg-pr-confirm' in request.POST:
        upgrade_pr(request, character, character_model)
    if 'upg-pp-confirm' in request.POST:
        upgrade_psy_power(request, character, character_model)

@csrf_exempt
def character_upgrade(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    if request.user != character.owner:
        return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': char_id, }))
    if character.is_rt:
        return rt_views.character_upgrade(request, char_id)
    character_model = character.data_to_model()
    if request.method == 'POST':
        parse_upgrades(request, character, character_model)
    if character_model.is_rt():
        facade = rt_flyweights
    else:
        facade = flyweights
    forms = upg_data_to_forms(character_model)
    is_owner = character.owner == request.user
    groups = character.groups.all()
    return TemplateResponse(request, 'charsheet-upgrade.html', {'version': VERSION, 'facade': facade,
                                                                'character': character_model, 'forms': forms,
                                                                'return': True, 'is_owner': is_owner,
                                                                'char_view': character.get_view_url(),
                                                                'groups': groups, })


@csrf_exempt
def character_delete(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    if (character is not None) and (character.owner == request.user):
        character.delete()
    return HttpResponseRedirect(reverse('characters-list'))


def creation_data_delete(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        cd.delete()
    return HttpResponseRedirect(reverse('characters-list'))


def resume_creation_edit(request, creation_id):
    cd = models.CreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        if cd.curr_stage == 'init':
            return HttpResponseRedirect(reverse('create-character-init', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'hw_choice':
            return HttpResponseRedirect(reverse('create-character-hw', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'stat_distr':
            return HttpResponseRedirect(reverse('create-character-stats', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'bg_choice':
            return HttpResponseRedirect(reverse('create-character-bg', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'role_choice':
            return HttpResponseRedirect(reverse('create-character-role', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'choices':
            return HttpResponseRedirect(reverse('create-character-choice', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'double_apts':
            return HttpResponseRedirect(reverse('create-character-double-apts', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'divination':
            return HttpResponseRedirect(reverse('create-character-divination', kwargs={'creation_id': cd.pk}))
    else:
        return reverse('characters-list')


def seasons_list(request):
    seasons = models.Season.objects.by_uid(request.user.pk)
    groups = dict()
    for season in seasons:
        groups[season.pk] = list()
        for group in models.CharacterGroup.objects.get_by_season(season.pk):
            groups.get(season.pk).append(group)
    return TemplateResponse(request, 'seasons_list.html', {'version': VERSION, 'seasons': seasons, 'groups': groups})


@csrf_exempt
def create_season(request):
    if request.method == 'POST':
        if request.user.is_master:
            form = CreateSeasonForm(request.POST)
            if form.is_valid():
                season = models.Season.objects.create(creator=request.user,
                                                      name=form.cleaned_data.get('name'),
                                                      description=form.cleaned_data.get('description'))
                season.name_id = season.make_name_id()
                season.save()
                return HttpResponseRedirect(reverse('seasons-list'))
            else:
                return TemplateResponse(request, 'create_season_form.html', {'version': VERSION, 'form': form})
        else:
            return HttpResponseRedirect(reverse('main'))
    else:
        form = CreateSeasonForm()
        return TemplateResponse(request, 'create_season_form.html', {'version': VERSION, 'form': form})


@csrf_exempt
def season_edit(request, season_id):
    season_name = unquote(season_id, encoding='utf-8', errors='replace')
    return HttpResponseRedirect(reverse('main'))


@csrf_exempt
def season_delete(request, season_id):
    season_name = unquote(season_id, encoding='utf-8', errors='replace')
    season = models.Season.objects.by_name_id(season_name)
    if season is not None:
        if request.user.is_master and (request.user == season.creator):
            season.delete()
    return HttpResponseRedirect(reverse('seasons-list'))


def season_view(request, season_id):
    season_name = unquote(season_id, encoding='utf-8', errors='replace')
    season = models.Season.objects.by_name_id(season_name)
    groups = models.CharacterGroup.objects.get_by_season(season.pk)
    return TemplateResponse(request, 'season.html', {'version': VERSION, 'season': season, 'groups': groups, })


@csrf_exempt
def create_group(request, season_id):
    if not request.user.is_master:
        return HttpResponseRedirect(reverse('main'))
    season_name = unquote(season_id, encoding='utf-8', errors='replace')
    season = models.Season.objects.by_name_id(season_name)
    characters = models.Character.objects.all().order_by('groups')
    if request.method == 'POST':
        form = CreateGroupForm(characters, request.POST)
        if form.is_valid():
            group = models.CharacterGroup.objects.create(creator=request.user, season=season,
                                                         name=form.cleaned_data.get('name'),
                                                         description=form.cleaned_data.get('description'),
                                                         is_rt=form.cleaned_data.get('is_rt'))
            group.name_id = group.make_name_id()
            group.purse = season.purse
            group.save()
            for key, value in form.cleaned_data.items():
                if key not in ['creator', 'name', 'description', 'is_rt']:
                    if value:
                        cid = int(key[1:])
                        character = models.Character.objects.get(pk=cid)
                        if character:
                            character.groups.add(group)
                            model = character.data_to_model()
                            model.restore_fate()
                            character.character_data = model.toJSON()
                            character.save()
            return HttpResponseRedirect(reverse('season', kwargs={'season_id': season_id, }))
        else:
            return TemplateResponse(request, 'create_group_form.html', {'version': VERSION, 'form': form,
                                                                        'season': season, })
    else:
        form = CreateGroupForm(characters)
        return TemplateResponse(request, 'create_group_form.html', {'version': VERSION, 'form': form,
                                                                    'season': season, })


@csrf_exempt
def group_edit(request, group_id):
    group_name = unquote(group_id, encoding='utf-8', errors='replace')
    return HttpResponseRedirect(reverse('main'))


@csrf_exempt
def group_delete(request, group_id):
    group_name = unquote(group_id, encoding='utf-8', errors='replace')
    group = models.CharacterGroup.objects.get_by_name_id(group_name)
    if group is not None:
        if request.user.is_master and (request.user == group.creator):
            group.delete()
    return HttpResponseRedirect(reverse('seasons-list'))


@csrf_exempt
def group_gain_influence(request, group: models.CharacterGroup):
    form = InfluenceControlsForm(request.POST)
    if form.is_valid():
        amount = int(form.cleaned_data.get('amount'))
        if group.purse:
            group.purse.cash += amount
            group.purse.save()
        else:
            group.group_ifl += amount
        group.save()
    return HttpResponseRedirect(reverse('group', kwargs={'group_id': group.name_id}))


@csrf_exempt
def group_loose_influence(request, group: models.CharacterGroup):
    form = InfluenceControlsForm(request.POST)
    if form.is_valid():
        amount = int(form.cleaned_data.get('amount'))
        if group.purse:
            group.purse.cash -= amount
            group.purse.save()
        else:
            group.group_ifl -= amount
        group.save()
    return HttpResponseRedirect(reverse('group', kwargs={'group_id': group.name_id}))


@csrf_exempt
def group_gain_xp(request, group: models.CharacterGroup):
    form = GroupXPGiverForm(group, request.POST)
    if form.is_valid() and (request.user == group.creator):
        amount = int(form.cleaned_data.get('amount'))
        characters = models.Character.objects.by_group(group)
        for key, value in form.cleaned_data.items():
            if (key == 'all') and value:
                for character in characters:
                    model = character.data_to_model()
                    if value:
                        model.get_xp(amount)
                        model.restore_fate()
                        character.character_data = model.toJSON()
                        character.save()
            else:
                if key not in ['amount', 'all']:
                    if value:
                        cid = int(key[1:])
                        character = models.Character.objects.get(pk=cid)
                        if character:
                            model = character.data_to_model()
                            if value:
                                model.get_xp(amount)
                                model.restore_fate()
                                character.character_data = model.toJSON()
                                character.save()
    return HttpResponseRedirect(reverse('group', kwargs={'group_id': group.name_id}))


def collect_facts(characters, facade):
    facts = {'spec_skills': dict(), 'psy': dict(), 'talents': dict()}
    for pk, character in characters.items():
        for skill_tag, skill in character.skills().items():
            if skill.is_specialist():
                if skill.tag() not in facts.get('spec_skills').keys():
                    facts.get('spec_skills')[skill.tag()] = dict()
                for subtag in skill.advances().keys():
                    if subtag not in facts.get('spec_skills').get(skill.tag()).keys():
                        facts.get('spec_skills').get(skill.tag())[subtag] = list()
                    facts.get('spec_skills').get(skill.tag()).get(subtag).append(
                        character.name() + ' +' + str(skill.get_adv_bonus_subtag(subtag)))
            if skill.tag() == 'SK_PSY':
                if skill.tag() not in facts.get('psy').keys():
                    facts.get('psy')[skill.tag()] = list()
                if skill.get_adv_bonus() >= 0:
                    facts.get('psy').get(skill.tag()).append(character.name() + ' +' + str(skill.get_adv_bonus()))
        for talent_tag, talent in character.talents().items():
            if (talent.tag() in INTERESTING_TALENTS) and (talent.tag() in facade.talent_descriptions().keys()):
                if talent.tag() not in facts.get('talents').keys():
                    facts.get('talents')[talent.tag()] = list()
                name = character.name()
                if talent.is_specialist():
                    name += ' ('
                    for subtag in talent.taken().keys():
                        name += ' ' + subtag + ','
                    name = name[:len(name) - 1] + ')'
                facts.get('talents').get(talent.tag()).append(name)
        for trait_tag, trait in character.traits().items():
            if trait.tag() == 'TR_PSY':
                if trait.tag() not in facts.get('psy').keys():
                    facts.get('psy')[trait.tag()] = list()
                name = character.name()
                if 'TR_SNC' in character.traits():
                    name += u' (санкционат)'
                else:
                    name += u' (несанкционат)'
                facts.get('psy').get(trait.tag()).append(name)
        if character.is_rt():
            facts['trials'] = dict()
            if character.trial_id() in INTERESTING_TRIALS:
                if character.trial_id() not in facts.get('trials'):
                    facts.get('trials')[character.trial_id()] = list()
                facts.get('trials').get(character.trial_id()).append(character.name())
    return facts


@csrf_exempt
def group_view(request, group_id):
    group_name = unquote(group_id, encoding='utf-8', errors='replace')
    group = models.CharacterGroup.objects.get_by_name_id(group_name)
    if request.method == 'POST':
        if 'ifl-get-confirm' in request.POST:
            return group_gain_influence(request, group)
        if 'ifl-loose-confirm' in request.POST:
            return group_loose_influence(request, group)
        if 'group-give-xp' in request.POST:
            return group_gain_xp(request, group)
        if 'gr-link-change' in request.POST:
            link_form = AddDocLinkForm(request.POST)
            if link_form.is_valid():
                group.group_notes_url = link_form.cleaned_data['link']
                group.save()
            return HttpResponseRedirect(reverse('group', kwargs={'group_id': group.name_id}))
        if 'ms-link-change' in request.POST:
            link_form = AddDocLinkForm(request.POST)
            if link_form.is_valid():
                group.master_notes_url = link_form.cleaned_data['link']
                group.save()
            return HttpResponseRedirect(reverse('group', kwargs={'group_id': group.name_id}))
    characters = models.Character.objects.by_group(group)
    character_models = dict()
    if group.is_rt:
        facade = rt_flyweights
    else:
        facade = flyweights

    is_captain = False
    is_player = False
    for character in characters:
        character_models[character.pk] = character.data_to_model()
        if not is_player:
            is_player = character.owner == request.user
        if (not is_captain) and group.is_rt:
            is_captain = (request.user == character.owner)\
                         and (character_models.get(character.pk).career_id() == 'CR_RT')
    is_master = request.user == group.creator
    active_sessions = models.GameSession.objects.get_by_group(group).get_active()
    finished_sessions = models.GameSession.objects.get_by_group(group).get_finished()
    ifl_form = None
    xp_form = None
    group_notes_form = None
    master_notes_form = None
    if is_master:
        ifl_form = InfluenceControlsForm()
        xp_form = GroupXPGiverForm(group)
        master_notes_form = AddDocLinkForm({'link': group.master_notes()})
    if is_captain:
        ifl_form = InfluenceControlsForm()
        group_notes_form = AddDocLinkForm({'link': group.group_notes()})
    facts = collect_facts(character_models, facade)
    if is_master:
        view_words = fact_words
    else:
        view_words = player_fact_words
    return TemplateResponse(request, 'group.html', {'version': VERSION, 'group': group, 'facade': facade,
                                                    'characters': characters, 'char_data': character_models,
                                                    'is_master': is_master, 'is_captain': is_captain,
                                                    'active': active_sessions, 'finished': finished_sessions,
                                                    'ifl_form': ifl_form, 'xp_form': xp_form, 'facts': facts,
                                                    'group_notes': group_notes_form, 'fact_words': view_words,
                                                    'master_notes': master_notes_form, 'group_member': is_player,
                                                    'gr_notes_url': group.group_notes(),
                                                    'ms_notes_url': group.master_notes()})


def make_session_name(name: str, group: models.CharacterGroup):
    const_part = u'Сессия №' + str(group.sessions_count + 1) + u' группы ' + group.name\
                 + u' в кампании ' + group.season.name
    if name and (len(name) > 0):
        session_name = name + u' (' + const_part + u')'
    else:
        session_name = const_part
    return session_name


@csrf_exempt
def create_session(request, group_id):
    group_name = unquote(group_id, encoding='utf-8', errors='replace')
    group = models.CharacterGroup.objects.get_by_name_id(group_name)
    if request.user.is_master and (request.user == group.creator):
        characters = models.Character.objects.by_group(group)
        if request.method == 'POST':
            form = CreateSessionForm(group, characters, False, request.POST)
            if form.is_valid():
                session = models.GameSession(creator=request.user, base_group=group,
                                             name=make_session_name(form.cleaned_data['name'], group))
                session.save()
                for character in characters:
                    character.sessions.add(session)
                    character.save()
                return HttpResponseRedirect(reverse('session', kwargs={'game_session_id': session.pk, }))
            return TemplateResponse(request, 'create_session_form.html', {'version': VERSION, 'crossover': False,
                                                                          'group': group, 'form': form })
        else:
            form = CreateSessionForm(group, characters, False)
            return TemplateResponse(request, 'create_session_form.html', {'version': VERSION, 'crossover': False,
                                                                          'group': group, 'form': form })
    else:
        HttpResponseRedirect(reverse('main'))


@csrf_exempt
def create_crossover_session(request, group_id):
    group_name = unquote(group_id, encoding='utf-8', errors='replace')
    group = models.CharacterGroup.objects.get_by_name_id(group_name)
    if request.user.is_master and (request.user == group.creator):
        characters = models.Character.objects.by_group(group)
        if request.method == 'POST':
            form = CreateSessionForm(group, characters, True, request.POST)
            if form.is_valid():
                session = models.GameSession(creator=request.user, base_group=group,
                                             name=make_session_name(form.cleaned_data['name'], group))
                session.save()
                for character in characters:
                    character.sessions.add(session)
                    character.save()
                return HttpResponseRedirect(reverse('session', kwargs={'game_session_id': session.pk, }))
            return TemplateResponse(request, 'create_session_form.html', {'version': VERSION, 'crossover': True,
                                                                          'group': group, 'form': form })
        else:
            form = CreateSessionForm(group, characters, False)
            return TemplateResponse(request, 'create_session_form.html', {'version': VERSION, 'crossover': True,
                                                                          'group': group, 'form': form })
    else:
        HttpResponseRedirect(reverse('main'))


@csrf_exempt
def session_gain_influence(request, session: models.GameSession):
    form = InfluenceControlsForm(request.POST)
    if form.is_valid():
        session.base_group.group_ifl += int(form.cleaned_data.get('amount'))
        session.base_group.save()
    return HttpResponseRedirect(reverse('session', kwargs={'game_session_id': session.pk}))


@csrf_exempt
def session_loose_influence(request, session: models.GameSession):
    form = InfluenceControlsForm(request.POST)
    if form.is_valid():
        session.base_group.group_ifl -= int(form.cleaned_data.get('amount'))
        session.base_group.save()
    return HttpResponseRedirect(reverse('session', kwargs={'game_session_id': session.pk}))


@csrf_exempt
def finish_session(request, session: models.GameSession):
    form = EndSessionForm(request.POST)
    if form.is_valid():
        session.finished = True
        session.base_group.sessions_count += 1
        session.save()
        session.base_group.save()
        xp_gain = int(form.cleaned_data['xp_amount'])
        participants = models.Character.objects.by_session(session)
        for participant in participants:
            model = participant.data_to_model()
            model.gain_xp(xp_gain)
            participant.character_data = model.toJSON()
            participant.save()
    return HttpResponseRedirect(reverse('group', kwargs={'group_id': session.base_group.name_id}))


def parse_prompt(prompt: str):
    raw_participants = prompt.split(';')
    participants = list()
    for i in range(len(raw_participants)):
        if i > 0:
            participants.append(raw_participants[i][1:len(raw_participants[i])])
        else:
            participants.append(raw_participants[i][:len(raw_participants[i])])
    parsed = list()
    for participant in participants:
        splitted = participant.split('-', maxsplit=3)
        parsed.append({'name': splitted[0], 'roll': int(splitted[1]), 'stat': int(splitted[2])})
    return parsed


@csrf_exempt
def make_initiative_line(request, participants, facade, session):
    characters = list()
    for cid, model in participants.items():
        characters.append(model)
    form = InitiativeLineMaker(characters, facade, request.POST)
    if form.is_valid():
        parsed = parse_prompt(form.cleaned_data.get('prompt'))
        for cid, character in participants.items():
            roll_field = 'roll-c-' + str(cid)
            stat_field = 'stat-c-' + str(cid)
            parsed.append({'name': character.name(), 'roll': int(form.cleaned_data.get(roll_field)),
                           'stat': character.stats().get(form.cleaned_data.get(stat_field)).value()})
        parsed.sort(key=itemgetter('roll', 'stat', 'name'), reverse=True)
        ifl_form = InfluenceControlsForm()
        finish_form = EndSessionForm()
        facts = collect_facts(participants, facade)
        return TemplateResponse(request, 'session_view.html', {'version': VERSION, 'session': session,
                                                               'char_data': participants, 'ifl_form': ifl_form,
                                                               'finish_form': finish_form, 'facts': facts,
                                                               'initiative_line': form, 'parsed': parsed,
                                                               'is_master': True, 'is_captain': False,
                                                               'group_notes': None, 'fact_words': fact_words,
                                                               'gr_notes_url': '',
                                                               'ms_notes_url': session.base_group.master_notes()
                                                               })


@csrf_exempt
def session_view(request, game_session_id):
    session = models.GameSession.objects.get(pk=game_session_id)
    group_chars = list()
    crossover_chars = list()
    char_urls = dict()
    participants = list()
    character_models = dict()
    if session.base_group.is_rt:
        facade = rt_flyweights
    else:
        facade = flyweights
    for character in models.Character.objects.all():
        if session in character.sessions.all():
            if session.base_group in character.groups.all():
                group_chars.append(character)
            else:
                crossover_chars.append(character)
            model = character.data_to_model()
            character_models[character.pk] = model
            char_urls[character.pk] = character.get_view_url()
            participants.append(model)
    if request.method == 'POST':
        if 'ifl-get-confirm' in request.POST:
            return session_gain_influence(request, session)
        if 'ifl-loose-confirm' in request.POST:
            return session_loose_influence(request, session)
        if 'end-session-confirm' in request.POST:
            return finish_session(request, session)
        if 'mk-init-line' in request.POST:
            return make_initiative_line(request, character_models, facade, session)
        finish_form = None
        initiative_line = None
        ifl_form = None
        is_captain = False
        for character in group_chars:
            if request.user == character.owner:
                initiative_line = InitiativeLineMaker(participants, facade)
                if character.is_rt and (character.data_to_model().career_id() == 'CR_RT'):
                    ifl_form = InfluenceControlsForm()
                    is_captain = True
                break
        for character in crossover_chars:
            if request.user == character.owner:
                initiative_line = InitiativeLineMaker(participants, facade)
                break
        facts = collect_facts(character_models, facade)
        is_master = request.user == session.creator

        return TemplateResponse(request, 'session_view.html', {'version': VERSION, 'session': session,
                                                               'char_data': character_models, 'ifl_form': ifl_form,
                                                               'finish_form': finish_form, 'facts': facts,
                                                               'initiative_line': None, 'fact_words': fact_words,
                                                               'is_master': is_master, 'is_captain': is_captain,
                                                               'group_notes': None, 'char_urls': char_urls,
                                                               'gr_notes_url': session.base_group.group_notes(),
                                                               'ms_notes_url': session.base_group.master_notes()
                                                               })
    else:
        if request.user.is_master and (request.user == session.creator):
            ifl_form = InfluenceControlsForm()
            finish_form = EndSessionForm()
            initiative_line = InitiativeLineMaker(participants, facade)
        else:
            finish_form = None
            initiative_line = None
            ifl_form = None
            for character in group_chars:
                if request.user == character.owner:
                    initiative_line = InitiativeLineMaker(participants, facade)
                    if character.is_rt and (character.data_to_model().career_id() == 'CR_RT'):
                        ifl_form = InfluenceControlsForm()
                    break
            for character in crossover_chars:
                if request.user == character.owner:
                    initiative_line = InitiativeLineMaker(participants, facade)
                    break
        facts = collect_facts(character_models, facade)
        return TemplateResponse(request, 'session_view.html', {'version': VERSION, 'session': session,
                                                               'char_data': character_models, 'ifl_form': ifl_form,
                                                               'finish_form': finish_form, 'facts': facts,
                                                               'initiative_line': initiative_line, })


def sessions_list_master(request):
    if not request.user.is_master:
        return HttpResponseRedirect(reverse('main'))
    active_sessions = models.GameSession.objects.get_by_creator(request.user).get_active()
    finished_sessions = models.GameSession.objects.get_by_creator(request.user).get_finished()
    return TemplateResponse(request, 'sessions_list.html',
                            {'version': VERSION, 'active': active_sessions,
                             'finished': finished_sessions, })


def character_sessions_list(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    active_sessions = character.sessions.objects.get_active()
    finished_sessions = character.sessions.objects.get_finished()
    return TemplateResponse(request, 'sessions_list_char.html',
                            {'version': VERSION, 'character': character.data_to_model(),
                             'char_url': character.get_view_url(),
                             'active': active_sessions, 'finished': finished_sessions, })


def character_groups_list(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    return TemplateResponse(request, 'groups_list_character.html',
                            {'version': VERSION, 'character': character.data_to_model(),
                             'char_url': character.get_view_url(),
                             'groups': character.groups.all(), })
