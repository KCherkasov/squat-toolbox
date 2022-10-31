# -*- coding: utf-8 -*-
import logging

import django.forms
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms.fields import CharField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import charlist.models
from charlist.forms.generation.background_choice_form import BackgroundChoiceForm
from charlist.forms.generation.choices_form import ChoicesForm
from charlist.forms.generation.creation_settings_form import CreationSettingsForm
from charlist.forms.generation.divination_form import DivinationForm
from charlist.forms.generation.double_apts_choices import DoubleAptsChoiceForm
from charlist.forms.generation.homeworld_choice_form import HomeworldsChoiceForm
from charlist.forms.generation.role_choice_form import RoleChoiceForm
from charlist.forms.generation.stages import *
from charlist.forms.generation.stat_distribution_form import StatDistributionForm
from .character.character import CharacterModel
from .character.skill import Skill
from .character.stat import Stat
from .character.talent import Talent
from .character.trait import Trait
from .constants.constants import *
from .flyweights.flyweights import *
from .forms.authorization.signin import SignInForm
from .forms.authorization.signup import UserCreationForm


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return force_str(user.pk) + force_str(timestamp) + force_str(user.is_active)


account_activation_token = TokenGenerator()

resources = ['aptitudes.json', 'stat_descriptions.json', 'skill_descriptions.json', 'talent_descriptions.json',
             'traits.json', 'homeworlds.json', 'backgrounds.json', 'roles.json', 'elite_advances.json',
             'divinations.json', 'psy.json']
flyweights = Facade(resources)


def aptitudes_test(request):
    logger = logging.getLogger('charlist_logger')
    logger.info('test')
    return render(request, 'charlist_test.html', {'version': VERSION, 'facade': flyweights, })


def charsheet_mockup(request):
    return render(request, 'charsheet-mockup.html', {'version': VERSION, })


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
                                "TL_IOHW": Talent("TL_IOHW", 1)}, {}, [], [], [], [], [])
    char_dump = character.toJSON()
    unpacked_char = CharacterModel.from_json(char_dump)
    return render(request, "charsheet-mockup-interactive.html", {'version': VERSION, 'facade': flyweights,
                                                                 'character': unpacked_char,
                                                                 'hookups': character.make_hookups(flyweights)})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = u'Подтвердите Ваш почтовый адрес на squat-toolbox.ru'
            message = render_to_string('signup_activation_mail.html', {
                'user': user, 'domain': current_site, 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user), })
            to_mail = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, from_email='signup@squattoolbox.ru', to=[to_mail])
            email.send()
            return HttpResponseRedirect(reverse('signup-activate'))
        else:
            return render(request, 'signup.html', {'version': VERSION, 'form': form, })
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'version': VERSION, 'form': form, })


def signup_activate(request):
    return render(request, 'activate.html', {'version': VERSION, })


def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            login(request, form.cleaned_data['user'])
            return HttpResponseRedirect(reverse('characters-list'))
        else:
            return HttpResponseRedirect(reverse('signin'))
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'version': VERSION, 'form': form, })


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Activation link is invalid!')


def characters_list(request):
    return render(request, 'characters_list.html', {'version': VERSION, 'facade': flyweights})


def create_character_init(request, data=None):
    if request.method == 'POST':
        if 'char-hw-prev' in request.POST:
            form = CreationSettingsForm(data)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[0], 'form': form})
        if data is None:
            data = dict()
        form = CreationSettingsForm(request.POST)
        if ('char-cr-next' in request.POST) and form.is_valid():
            cleaned_data = form.cleaned_data
            data['name'] = cleaned_data['name']
            data['gender'] = cleaned_data['gender']
            data['height'] = cleaned_data['height']
            data['weight'] = cleaned_data['weight']
            data['age'] = cleaned_data['age']
            data['starting_xp'] = cleaned_data['starting_xp']
            data['characteristics_base'] = cleaned_data['characteristics_base']
            return create_character_hw_choice(request, data)
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[0], 'form': form})
    else:
        form = CreationSettingsForm()
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[0], 'form': form})


def create_character_hw_choice(request, data):
    if 'char-hw-next' in request.POST:
        form = HomeworldsChoiceForm(request.POST)
        if form.is_valid():
            data['homeworld'] = form.cleaned_data['homeworld']
            return create_character_stat_distribution(request, data)
    if request.method == 'POST':
        if 'char-hw-prev' in request.POST:
            return create_character_init(request, data)
        if 'char-st-prev' in request.POST:
            form = HomeworldsChoiceForm(data)
        else:
            form = HomeworldsChoiceForm()
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[1], 'form': form})
    else:
        return HttpResponseRedirect(reverse('index'))


def create_character_stat_distribution(request, data):
    if request.method == 'POST':
        if 'char-st-prev' in request.POST:
            return create_character_hw_choice(request, data)
        if 'char-st-next' in request.POST:
            form = StatDistributionForm(request.POST)
            if form.is_valid():
                stats = dict()
                homeworld = flyweights.homeworlds().get(data['homeworld'])
                cleaned_data = form.cleaned_data
                base = 20
                if data['characteristics_base'] == 'CS_25':
                    base += 5
                for stat in STAT_TAGS:
                    stats[stat] = Stat(stat, base)
                    if stat in homeworld.get_stat_mods().keys():
                        val = homeworld.get_stat_mods().get(stat)
                        if val > 0:
                            stats.get(stat).improve(val)
                        else:
                            stats.get(stat).damage(val)
                stats.get(ST_WEAPON_SKILL).improve(cleaned_data['ws_value'])
                stats.get(ST_BALLISTIC_SKILL).improve(cleaned_data['bs_value'])
                stats.get(ST_STRENGTH).improve(cleaned_data['str_value'])
                stats.get(ST_TOUGHNESS).improve(cleaned_data['t_value'])
                stats.get(ST_AGILITY).improve(cleaned_data['ag_value'])
                stats.get(ST_INTELLIGENCE).improve(cleaned_data['int_value'])
                stats.get(ST_PERCEPTION).improve(cleaned_data['per_value'])
                stats.get(ST_WILLPOWER).improve(cleaned_data['wp_value'])
                stats.get(ST_INFLUENCE).improve(cleaned_data['ifl_value'])
                data['stats'] = stats
                return create_character_bg_choice(request, data)
        if 'char-bg-prev' in request.POST:
            form = StatDistributionForm(data)
        else:
            form = StatDistributionForm()
        return render(request, 'character_creation_form', {'version': VERSION, 'facade': flyweights,
                                                           'stage': CREATION_STAGES[2], 'form': form})
    else:
        return HttpResponseRedirect(reverse('index'))


def create_character_bg_choice(request, data):
    if request.method == 'POST':
        if 'char-bg-prev' in request.POST:
            return create_character_stat_distribution(request, data)
        if 'char-bg-next' in request.POST:
            form = BackgroundChoiceForm(request.POST)
            if form.is_valid():
                data['background'] = form.cleaned_data['background']
                return create_character_role_choice(request, data)
        else:
            if 'char-role-prev' in request.POST:
                form = BackgroundChoiceForm(data)
            else:
                form = BackgroundChoiceForm()
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[3], 'form': form})
    else:
        return HttpResponseRedirect('create-character-init')


def create_character_role_choice(request, data):
    if request.method == 'POST':
        if 'char-role-prev' in request.POST:
            return create_character_bg_choice(request, data)
        if 'char-role-next' in request.POST:
            form = RoleChoiceForm(request.POST)
            if form.is_valid():
                data['role'] = form.cleaned_data['role']
                return create_character_choices(request, data)
        else:
            if 'char-choices-prev' in request.POST:
                form = RoleChoiceForm(data)
            else:
                form = RoleChoiceForm()
                return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                        'stage': CREATION_STAGES[4], 'form': form})
    else:
        return HttpResponseRedirect(reverse('create-character-init'))


def create_character_choices(request, data):
    if request.method == 'POST':
        if 'char-choices-prev' in request.POST:
            return create_character_role_choice(request, data)
        if 'char-choices-next' in request.POST:
            form = ChoicesForm(request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                data['background_apts'] = cleaned_data['background_apts']
                if len(flyweights.backgrounds().get(data['background']).get_skill_choices()) > 0:
                    data['background_skills'] = cleaned_data['background_skills']
                    if 'background-skills-subtag' in cleaned_data:
                        data['background-skills-subtag'] = cleaned_data['background-skills-subtag']
                    if len(flyweights.backgrounds().get(data['background']).get_skill_choices()) > 1:
                        data['background_skills2'] = cleaned_data['background_skills2']
                        if 'background-skills-subtag2' in cleaned_data:
                            data['background-skills-subtag2'] = cleaned_data['background-skills-subtag2']
                if form.fields['background_talents'].required:
                    data['background_talents'] = cleaned_data['background_talents']
                if form.fields['background_traits'].required:
                    data['background_traits'] = cleaned_data['background_traits']
                if form.fields['role_apts'].required:
                    data['role_apts'] = cleaned_data['role_apts']
                data['role_talent'] = cleaned_data['role_talent']
                if 'hw-bonus-talent' in form.fields.keys():
                    data['hw-bonus-talent'] = cleaned_data['hw-bonus-talent']
                cpy = request.POST.copy()
                cpy.update({'data': data})
                request.POST = cpy
                return create_character_double_apts(request, data)
        else:
            if 'char-apts-prev' in request.POST:
                form = ChoicesForm(data)

                homeworld = flyweights.homeworlds().get(data['homeworld'])
                hw_bonus = homeworld.get_bonus()
                for command in hw_bonus.get_commands():
                    if command.get('tag') == 'GainTalentAlt':
                        choices = []
                        i = 0
                        for tag in command.get('tags'):
                            sk_name = flyweights.skill_descriptions().get(tag).get_name_en()
                            choices.append((i, sk_name))
                            i += 1
                        form.fields['hw-bonus-talent'] = django.forms.ChoiceField(
                            label="Талант (бонус родного мира)", choices=choices)

                background = flyweights.backgrounds().get(data['background'])

                bg_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en())
                           for apt in background.get_apt_choices()]
                form.fields['background_apts'].choices = bg_apts

                role = flyweights.roles().get(data['role'])

                role_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en()) for
                                apt in role.get_apt_choices()]
                form.fields['role_apts'].choices = role_apts
                if len(role_apts) == 0:
                    form.fields['role_apts'].required = False
                    form.fields['role_apts'].widget = django.forms.Select(
                        {'class': 'form-control disabled', }, role_apts)

                bg_skill_choices = background.get_skill_choices()
                if len(bg_skill_choices) > 0:
                    skill_choice = bg_skill_choices[0]
                    i = 0
                    sk_choices = []
                    for skill in skill_choice:
                        tag = skill.get('tag')
                        sk = flyweights.skill_descriptions().get(tag)
                        subtag = None
                        sk_name = sk.get_name_en()
                        if sk.is_specialist():
                            subtag = skill.get('subtag')
                        if subtag:
                            if subtag == 'SK_ANY':
                                sk_name += '(any)'
                                if 'background-skills-subtag' not in form.fields:
                                    form.fields['background-skills-subtag'] = \
                                        CharField(label=u'Специализация', max_length=30)
                            else:
                                sk_name += ' ('
                                for tag in subtag:
                                    sk_name += tag + ', '
                                sk_name = sk_name[:-2] + ')'
                        sk_choices.append((i, sk_name))
                        i += 1
                    form.fields['background_skills'].choices = sk_choices
                    if len(bg_skill_choices) > 1:
                        skill_choice2 = bg_skill_choices[1]
                        i = 0
                        sk_choices2 = []
                        for skill in skill_choice2:
                            tag = skill.get('tag')
                            subtag = None
                            sk = flyweights.skill_descriptions().get(tag)
                            sk_name = sk.get_name_en()
                            if flyweights.skill_descriptions().get('tag').is_specialist():
                                subtag = skill.get('subtag')
                            if subtag:
                                if subtag == 'SK_ANY' and 'background-skills-subtag2' not in form.fields:
                                    form.fields['background-skills-subtag2'] = \
                                        CharField(label=u'Специализация', max_length=30)
                                    sk_name += '(any)'
                                else:
                                    if subtag == 'SK_ANY':
                                        sk_name += '(any)'
                                    else:
                                        sk_name += ' ('
                                        for st in subtag:
                                            sk_name += st + ', '
                                        sk_name = sk_name[:-2] + ')'
                            sk_choices2.append((i, sk_name))
                            i += 1
                        form.fields['background_skills2'].choices = sk_choices2
                    else:
                        form.fields['background_skills2'].required = False
                        form.fields['background_skills2'].widget = django.forms.Select(
                            {'class': 'form-control disabled'}, [])

                bg_talents = background.get_talent_choices()
                bg_tals = []
                for tal in bg_talents:
                    talent = flyweights.talent_descriptions().get(tal.get('tag'))
                    name = talent.get_name_en()
                    if talent.is_specialist():
                        name += ' ('
                        for tag in tal.get('subtag'):
                            name += tag + ', '
                        name = name[:-2] + ')'
                    bg_tals.append((tal, name))
                form.fields['background_talents'].choices = bg_tals
                if len(bg_tals) == 0:
                    form.fields['background_talents'].required = False
                    form.fields['background_talents'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, bg_tals)

                role_talents = role.get_talent_choices()
                role_tals = []
                i = 0
                for tal in role_talents:
                    talent = flyweights.talent_descriptions().get(tal.get('tag'))
                    name = talent.get_name_en()
                    if talent.is_specialist():
                        name += ' ('
                        for tag in tal.get('subtag'):
                            name += tag + ', '
                        name = name[:-2] + ')'
                    role_tals.append((i, name))
                    i += 1
                form.fields['role_talent'].choices = role_tals
                if len(role_tals) == 0:
                    form.fields['role_talent'].required = False
                    form.fields['role_talent'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, role_tals)

                background_traits = background.get_traits_choices
                bg_traits = []
                if len(background_traits) > 0:
                    i = 0
                    for trait in background_traits:
                        trdesc = flyweights.trait_descriptions().get(trait.get('tag'))
                        name = trdesc.get_name_en()
                        if trdesc.is_specialist():
                            name += '('
                            if trait.get('tag') == 'TR_UNCH':
                                subname = flyweights.stat_descriptions().get(trait.get('subtag')).get_name_en()
                                name += subname + ')'
                            else:
                                name += trait.get('subtag') + ')'
                        if trdesc.is_stackable():
                            name += '(' + trait.get('taken') + ')'
                        bg_traits.append((i, name))
                        i += 1
                form.fields['background_traits'].choices = bg_traits
                if len(form.fields['background_traits'].choices) == 0:
                    form.fields['background_traits'].required = False
                    form.fields['background_traits'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, bg_traits)
            else:
                form = ChoicesForm()

                homeworld = flyweights.homeworlds().get(data['homeworld'])
                hw_bonus = homeworld.get_bonus()
                for command in hw_bonus.get_commands():
                    if command.get('tag') == 'GainTalentAlt':
                        choices = []
                        i = 1
                        for tag in command.get('tags'):
                            sk_name = flyweights.skill_descriptions().get(tag).get_name_en()
                            choices.append((i, sk_name))
                            i += 1
                        form.fields['hw-bonus-talent'] = django.forms.ChoiceField(
                            label="Талант (бонус родного мира)", choices=choices)

                background = flyweights.backgrounds().get(data['background'])

                bg_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en())
                            for apt in background.get_apt_choices()]
                form.fields['background_apts'].choices = bg_apts

                role = flyweights.roles().get(data['role'])

                role_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en()) for
                             apt in role.get_apt_choices()]
                form.fields['role_apts'].choices = role_apts
                if len(role_apts) == 0:
                    form.fields['role_apts'].required = False
                    form.fields['role_apts'].widget = django.forms.Select(
                        {'class': 'form-control disabled', }, role_apts)

                bg_skill_choices = background.get_skill_choices()
                if len(bg_skill_choices) > 0:
                    skill_choice = bg_skill_choices[0]
                    i = 0
                    sk_choices = []
                    for skill in skill_choice:
                        tag = skill.get('tag')
                        sk = flyweights.skill_descriptions().get(tag)
                        subtag = None
                        sk_name = sk.get_name_en()
                        if sk.is_specialist():
                            subtag = skill.get('subtag')
                        if subtag:
                            if subtag == 'SK_ANY':
                                sk_name += '(any)'
                                if 'background-skills-subtag' not in form.fields:
                                    form.fields['background-skills-subtag'] = \
                                        CharField(label=u'Специализация', max_length=30)
                            else:
                                sk_name += ' ('
                                for tag in subtag:
                                    sk_name += tag + ', '
                                sk_name = sk_name[:-2] + ')'
                        sk_choices.append((i, sk_name))
                        i += 1
                    form.fields['background_skills'].choices = sk_choices
                    if len(bg_skill_choices) > 1:
                        skill_choice2 = bg_skill_choices[1]
                        i = 0
                        sk_choices2 = []
                        for skill in skill_choice2:
                            tag = skill.get('tag')
                            subtag = None
                            sk = flyweights.skill_descriptions().get(tag)
                            sk_name = sk.get_name_en()
                            if flyweights.skill_descriptions().get('tag').is_specialist():
                                subtag = skill.get('subtag')
                            if subtag:
                                if subtag == 'SK_ANY' and 'background-skills-subtag2' not in form.fields:
                                    form.fields['background-skills-subtag2'] = \
                                        CharField(label=u'Специализация', max_length=30)
                                    sk_name += '(any)'
                                else:
                                    if subtag == 'SK_ANY':
                                        sk_name += '(any)'
                                    else:
                                        sk_name += ' ('
                                        for st in subtag:
                                            sk_name += st + ', '
                                        sk_name = sk_name[:-2] + ')'
                            sk_choices2.append((i, sk_name))
                            i += 1
                        form.fields['background_skills2'].choices = sk_choices2
                    else:
                        form.fields['background_skills2'].required = False
                        form.fields['background_skills2'].widget = django.forms.Select(
                            {'class': 'form-control disabled'}, [])

                bg_talents = background.get_talent_choices()
                bg_tals = []
                for tal in bg_talents:
                    talent = flyweights.talent_descriptions().get(tal.get('tag'))
                    name = talent.get_name_en()
                    if talent.is_specialist():
                        name += ' ('
                        for tag in tal.get('subtag'):
                            name += tag + ', '
                        name = name[:-2] + ')'
                    bg_tals.append((tal, name))
                form.fields['background_talents'].choices = bg_tals
                if len(bg_tals) == 0:
                    form.fields['background_talents'].required = False
                    form.fields['background_talents'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, bg_tals)

                role_talents = role.get_talent_choices()
                role_tals = []
                i = 0
                for tal in role_talents:
                    talent = flyweights.talent_descriptions().get(tal.get('tag'))
                    name = talent.get_name_en()
                    if talent.is_specialist():
                        name += ' ('
                        for tag in tal.get('subtag'):
                            name += tag + ', '
                        name = name[:-2] + ')'
                        role_tals.append((i, name))
                        i += 1
                    form.fields['role_talent'].choices = role_tals
                    if len(role_tals) == 0:
                        form.fields['role_talent'].required = False
                        form.fields['role_talent'].widget = django.forms.Select(
                            {'class': 'form-control disabled'}, role_tals)

                background_traits = background.get_traits_choices
                bg_traits = []
                if len(background_traits) > 0:
                    i = 0
                    for trait in background_traits:
                        trdesc = flyweights.trait_descriptions().get(trait.get('tag'))
                        name = trdesc.get_name_en()
                        if trdesc.is_specialist():
                            name += '('
                            if trait.get('tag') == 'TR_UNCH':
                                subname = flyweights.stat_descriptions().get(trait.get('subtag')).get_name_en()
                                name += subname + ')'
                            else:
                                name += trait.get('subtag') + ')'
                        if trdesc.is_stackable():
                            name += '(' + trait.get('taken') + ')'
                        bg_traits.append((i, name))
                        i += 1
                form.fields['background_traits'].choices = bg_traits
                if len(form.fields['background_traits'].choices) == 0:
                    form.fields['background_traits'].required = False
                    form.fields['background_traits'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, bg_traits)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[5], 'form': form})
    else:
        return HttpResponseRedirect('create-character-init')


def create_character_double_apts(request, data):
    if request.method == 'POST':
        if 'char-apts-prev' in request.POST:
            return create_character_choices(request, data)

        role = flyweights.roles().get(data['role'])
        homeworld = flyweights.homeworlds().get(data['homeworld'])

        hw_apt = homeworld.get_aptitude()
        bg_apt = data['background_apts']
        role_apts = role.get_aptitudes()
        role_apt = None
        if data['role_apts']:
            role_apt = data['role_apts']

        apts = list()
        apts.append(A_GENERAL)
        doubled = 0

        apts.append(hw_apt)
        if bg_apt in apts:
            doubled += 1
        else:
            apts.append(bg_apt)
        for apt in role_apts:
            if apt in apts:
                doubled += 1
            else:
                apts.append(apt)
        if role_apt:
            if role_apt in apts:
                doubled += 1
            else:
                apts.append(role_apt)

        if 'char-apts-next' in request.POST:
            form = DoubleAptsChoiceForm(request.POST)
            if form.is_valid():
                if doubled > 0:
                    data['apt_choice'] = form.cleaned_data['apt_choice']
                    if doubled > 1:
                        data['apt_choice2'] = form.cleaned_data['apt_choice2']
                data['apts'] = apts
                return create_character_divination(request, data)
        else:
            choices = []
            for st_apt in STAT_APTS:
                if st_apt not in apts:
                    choices.append((st_apt, flyweights.aptitudes().get(st_apt).get_name_en()))

            if 'char-div-prev' in request.POST:
                form = DoubleAptsChoiceForm(data)
                if doubled > 0:
                    form.fields['apt_choice'].choices = choices
                    if doubled > 1:
                        form.fields['apt_choice2'].choice = choices
                    else:
                        form.fields['apt_choice2'].required = False
                        form.fields['apt_choice2'].widget = django.forms.Select(
                            {'class': 'form-control disabled'}, choices)
                else:
                    form.fields['apt_choice'].required = False
                    form.fields['apt_choice'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, choices)
                    form.fields['apt_choice2'].required = False
                    form.fields['apt_choice2'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, choices)
            else:
                form = DoubleAptsChoiceForm()
                if doubled > 0:
                    form.fields['apt_choice'].choices = choices
                    if doubled > 1:
                        form.fields['apt_choice2'].choice = choices
                    else:
                        form.fields['apt_choice2'].required = False
                        form.fields['apt_choice2'].widget = django.forms.Select(
                            {'class': 'form-control disabled'}, choices)
                else:
                    form.fields['apt_choice'].required = False
                    form.fields['apt_choice'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, choices)
                    form.fields['apt_choice2'].required = False
                    form.fields['apt_choice2'].widget = django.forms.Select(
                        {'class': 'form-control disabled'}, choices)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[6], 'form': form})
    else:
        return HttpResponseRedirect(reverse('create-character-init'))


def create_character_divination(request, data):
    if request.method == 'POST':
        if 'char-div-prev' in request.POST:
            return create_character_double_apts(request, data)
        if 'char-div-next' in request.POST:
            form = DivinationForm(request.POST)
            div_tag = None
            if form.is_valid():
                divination_roll = form.cleaned_data['divination_roll']
                for div_key in flyweights.divinations().keys():
                    divination = flyweights.divinations().get(div_key)
                    if (divination_roll >= divination.get_roll_range()[0]) \
                            and (divination_roll <= divination.get_roll_range()[1]):
                        div_tag = div_key
                        break
                data['divination'] = div_tag
                data['wounds'] = form.cleaned_data['wound_roll']
                data['fate_roll'] = form.cleaned_data['fate_roll']

                background = flyweights.backgrounds().get(data['background'])
                homeworld = flyweights.homeworlds().get(data['homeworld'])
                role = flyweights.roles().get(data['role'])

                xp_given = data['starting_xp']
                fate = homeworld.get_fate()
                if data['fate_roll'] >= homeworld.get_blessing():
                    fate += 1

                fatigue = data['stats'].get(ST_TOUGHNESS).bonus() + data['stats'].get(ST_WILLPOWER).bonus()
                if data['background'] == BACKGROUND_OUTCAST:
                    fatigue += 2
                wounds = data['wounds'] + homeworld.get_wounds()

                apts = data['apts']
                if 'apt_choice' in data:
                    apts.append(data['apt_choice'])
                    if 'apt_choice2' in data:
                        apts.append(data['apt_choice2'])

                stats = dict()
                for key, stat in data['stats'].items():
                    stats[key] = stat

                skills = dict()
                skdescrs = flyweights.skill_descriptions()
                for key in skdescrs.keys():
                    if not skdescrs.get(key).is_specialist():
                        skills[key] = Skill(key, 0)
                for skill in background.get_skills():
                    if skill.get('tag') in skills.keys():
                        skills.get(skill.get('tag')).upgrade()
                    else:
                        if flyweights.skill_descriptions().get(skill.get('tag')).is_specialist():
                            skills[skill.get('tag')] = Skill(skill.get('tag'), {skill.get('subtag'): 1})

                if 'background_skills' in data:
                    choice = background.get_skill_choices()[0][data['background_skills']]
                    if choice.get('tag') in flyweights.skill_descriptions().keys():
                        if choice.get('tag') in skills.keys():
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') != 'SK_ANY':
                                    if skills.get(choice.get('tag')).get_subskill_advance(
                                            choice.get('subtag')) == 0:
                                        skills.get(choice.get('tag')).upgrade_subtag(choice.get('subtag'))
                                else:
                                    subtag = data['background-skills-subtag']
                                    if skills.get(choice.get('tag')).get_subskill_advance(subtag) == 0:
                                        skills.get(choice.get('tag')).upgrade_subtag(subtag)
                            else:
                                if skills.get(choice.get('tag')).advances() == 0:
                                    skills.get(choice.get('tag')).upgrade()
                        else:
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                subtag = ''
                                if choice.get('subtag') == 'SK_ANY':
                                    subtag = data['background-skills-subtag']
                                else:
                                    subtag = choice.get('subtag')
                                skills[choice.get('tag')] = Skill(choice.get('tag'), {subtag: 1})
                if 'background_skills2' in data:
                    choice = background.get_skill_choices()[0][data['background_skills2']]
                    if choice.get('tag') in flyweights.skill_descriptions().keys():
                        if choice.get('tag') in skills.keys():
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') != 'SK_ANY':
                                    if skills.get(choice.get('tag')).get_subskill_advance(
                                            choice.get('subtag')) == 0:
                                        skills.get(choice.get('tag')).upgrade_subtag(choice.get('subtag'))
                                else:
                                    subtag = data['background-skills-subtag2']
                                    if skills.get(choice.get('tag')).get_subskill_advance(subtag) == 0:
                                        skills.get(choice.get('tag')).upgrade_subtag(subtag)
                            else:
                                if skills.get(choice.get('tag')).advances() == 0:
                                    skills.get(choice.get('tag')).upgrade()
                        else:
                            if flyweights.skill_descriptions().get(choice.get('tag')).is_specialist():
                                if choice.get('subtag') == 'SK_ANY':
                                    subtag = data['background-skills-subtag2']
                                else:
                                    subtag = choice.get('subtag')
                                skills[choice.get('tag')] = Skill(choice.get('tag'), {subtag: 1})

                talents = dict()
                hw_bonus = homeworld.get_bonus()
                bg_bonus = background.get_bonus()

                for cmd in hw_bonus.get_commands():
                    if cmd.get('command') == 'GainTalent':
                        if cmd.get('tag') not in talents.keys():
                            if flyweights.talent_descriptions().get(cmd.get('tag')).is_specialist():
                                taken = dict()
                                for key in cmd.keys():
                                    if key in ['subtag', 'subtag1', 'subtag2']:
                                        taken[cmd.get(key)] = 1
                            else:
                                if flyweights.talent_descriptions().get(cmd.get('tag')).is_stackable():
                                    taken = cmd.get('taken')
                                else:
                                    taken = 1
                            talent = Talent(cmd.get('tag'), taken)
                            talents[cmd.get('tag')] = talent

                for cmd in bg_bonus.get_bonus():
                    if cmd.get('command') == 'GainTalent':
                        if cmd.get('tag') not in talents.keys():
                            if flyweights.talent_descriptions().get(cmd.get('tag')).is_specialist():
                                taken = dict()
                                for key in cmd.keys():
                                    if key in ['subtag', 'subtag1', 'subtag2']:
                                        taken[cmd.get(key)] = 1
                            else:
                                if flyweights.talent_descriptions().get(cmd.get('tag')).is_stackable():
                                    taken = cmd.get('taken')
                                else:
                                    taken = 1
                            talent = Talent(cmd.get('tag'), taken)
                            talents[cmd.get('tag')] = talent
                        elif flyweights.talent_descriptions().get(cmd.get('tag')).is_specialist():
                            for key in cmd.keys():
                                if (key in ['subtag', 'subtag1', 'subtag2']) \
                                        and (key not in talents.get(cmd.get('tag')).taken().keys()):
                                    talents.get(cmd.get('tag')).take_subtag(flyweights, cmd.get(key))

                bg_talent_choice = background.get_talent_choices()[data['bg_talents']]
                if bg_talent_choice.get['tag'] in talents.keys():
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

                role_talent_choice = role.get_talent_choices()[data['role_talent']]
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
                for cmd in hw_bonus.get_commands():
                    if cmd.get('tag') == 'GainTrait':
                        if flyweights.trait_descriptions().get(cmd.get('tag')).is_specialist() \
                                or (cmd.get('tag') not in traits.keys()):
                            if flyweights.trait_descriptions().get(cmd.get('tag')).is_specialist() \
                                    or flyweights.trait_descriptions().get(cmd.get('tag')).is_stackable():
                                taken = cmd.get('taken')
                            else:
                                taken = 1
                            if cmd.get('tag') in traits.keys():
                                for tag in cmd.get('taken'):
                                    traits.get(cmd.get('key')).take_subtag(flyweights, tag)
                            else:
                                traits[cmd.get('key')] = Trait(cmd.get('tag'), taken)

                character = charlist.models.Character.objects.create(owner=request.user, character_data='')
                character.save()
                character_model = CharacterModel(character.id, -1, data['name'], data['gender'], data['height'],
                                                 data['weight'], data['age'], data['homeworld'],
                                                 data['background'], data['role'], data['divination'], [],
                                                 [wounds, wounds], [0, fatigue], [xp_given, 0], [fate, fate], 0, 0,
                                                 0, apts, stats, skills, talents, traits, [], [], [], [], [])
                character.character = character_model.toJSON()
                character.save()
                return HttpResponseRedirect(reverse('characters-list'))
            else:
                return render(request, 'character_creation_form.html',
                              {'version': VERSION, 'facade': flyweights,
                               'stage': CREATION_STAGES[7], 'form': form})
        else:
            form = DivinationForm()
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[7], 'form': form})
    else:
        return HttpResponseRedirect(reverse('create-character-init'))


def character_view(request, char_id):
    character = charlist.models.Character.objects.filter(id=char_id)
    character_model = CharacterModel.from_json(character.character)
    return render(request, "charsheet-mockup-interactive.html", {'version': VERSION, 'facade': flyweights,
                                                                 'character': character_model,
                                                                 'hookups': character_model.make_hookups(flyweights)})
