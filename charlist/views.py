# -*- coding: utf-8 -*-
import logging

import datetime
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
from charlist.character.character import CharacterModel
from charlist.character.skill import Skill
from charlist.character.stat import Stat
from charlist.character.talent import Talent
from charlist.character.trait import Trait
from charlist.constants.constants import *
from charlist.flyweights.flyweights import *
from charlist.forms.authorization.signin import SignInForm
from charlist.forms.authorization.signup import UserCreationForm


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
    user = request.user
    characters = charlist.models.Character.objects.by_uid(user.pk)
    char_data = dict()
    for character in characters:
        char_data[character.pk] = character.data_to_model()
    in_progress = charlist.models.CreationData.objects.by_uid(user.pk)
    return render(request, 'characters_list.html', {'version': VERSION, 'facade': flyweights, 'characters': characters,
                                                    'in_progress': in_progress, 'char_data': char_data, })


def create_character_start(request):
    creation_data = charlist.models.CreationData()
    creation_data.owner = charlist.models.CharsheetUser.objects.get(pk=request.user.pk)
    creation_data.save()
    return HttpResponseRedirect(reverse('create-character-init', kwargs={'creation_id': creation_data.pk}))


def create_character_init(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        form = CreationSettingsForm(request.POST)
        if 'char-hw-prev' in request.POST:
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[0], 'form': form})
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
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[0], 'form': form})


def create_character_hw_choice(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-cr-next' in request.POST:
            form = HomeworldsChoiceForm()
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[1], 'form': form})
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
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[1], 'form': form})


def create_character_stat_distribution(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-hw-next' in request.POST:
            form = StatDistributionForm()
            return render(request, 'character_creation_form', {'version': VERSION, 'facade': flyweights,
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
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                           'stage': CREATION_STAGES[2], 'form': form})


def create_character_bg_choice(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
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
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[3], 'form': form})


def create_character_role_choice(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-st-next' in request.POST:
            form = RoleChoiceForm()
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[4], 'form': form})
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
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[4], 'form': form})


def prepare_choices_form(form, cd):
    homeworld = flyweights.homeworlds().get(cd.homeworld)
    hw_bonus = homeworld.get_bonus()
    for command in hw_bonus.get_commands():
        if command.get('tag') == 'GainTalentAlt':
            choices = []
            i = 0
            for tag in command.get('tags'):
                sk_name = flyweights.talent_descriptions().get(tag).get_name_en()
                choices.append((i, sk_name))
                i += 1
            form.fields['hw-bonus-talent'] = django.forms.ChoiceField(
                label="Талант (бонус родного мира)", choices=choices)

    background = flyweights.backgrounds().get(cd.background)

    bg_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en())
               for apt in background.get_apt_choices()]
    form.fields['background_apts'].choices = bg_apts

    role = flyweights.roles().get(cd.role)

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

    for sk in background.get_skills():
        skill = flyweights.skill_descriptions().get(sk.get('tag'))
        if skill is not None:
            if (skill.is_specialist()) and (sk.get('subtag') == 'SK_ANY'):
                field_name = 'subtag_' + sk.get('tag')
                form.fields[field_name] = CharField(label=skill.get_name_en(), max_length=30)
                form.fields[field_name].required = True

    bg_talents = background.get_talent_choices()
    bg_tals = []
    for tal in bg_talents:
        talent = flyweights.talent_descriptions().get(tal.get('tag'))
        name = talent.get_name_en()
        if talent.is_specialist():
            name += ' ('
            name += tal.get('subtag')
            if tal.get('subtag1') is not None:
                name += ', ' + tal.get('subtag1')
                if tal.get('subtag2') is not None:
                    name += ', ' + tal.get('subtag2')
            name += ')'
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
    return form


def create_character_choices(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-choices-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-role', kwargs={'creation_id': cd.pk}))
        if 'char-role-next' in request.POST:
            form = ChoicesForm()
            form = prepare_choices_form(form, cd)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[5], 'form': form})
        form = ChoicesForm(request.POST)
        if 'char-apts-prev' in request.POST:
            form = prepare_choices_form(form, cd)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[5], 'form': form})
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
        form = ChoicesForm()
        form = prepare_choices_form(form, cd)
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[5], 'form': form})


def count_doubles(cd, hw, role):
    doubles = 0
    hw_apt = hw.get_aptitude()
    bg_apt = cd.background_apt
    role_apts = role.get_aptitudes()
    if cd.role_apt is not None:
        if (cd.role_apt == bg_apt) or (cd.role_apt == hw_apt):
            doubles += 1
    if bg_apt == hw_apt:
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


def prepare_apts_form(form, doubled, apts):
    choices = []
    for st_apt in STAT_APTS:
        if st_apt not in apts:
            choices.append((st_apt, flyweights.aptitudes().get(st_apt).get_name_en()))
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
    return form


def create_character_double_apts(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    role = flyweights.roles().get(cd.role)
    homeworld = flyweights.homeworlds().get(cd.homeworld)
    doubled = count_doubles(cd, homeworld, role)
    apts = make_apts(cd, homeworld, role)
    if doubled == 0:
        return create_character_divination(request, creation_id)

    if request.method == 'POST':
        if 'char-apts-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-choice', kwargs={'creation_id': cd.pk}))
        if 'char-choices-next' in request.POST:
            form = DoubleAptsChoiceForm()
            form = prepare_apts_form(form, doubled, apts)
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[6], 'form': form})
        form = DoubleAptsChoiceForm(request.POST)
        if 'char-apts-next' in request.POST:
            if form.is_valid():
                if doubled > 0:
                    cd.apt_1 = form.cleaned_data['apt_choice']
                    if doubled > 1:
                        cd.apt_2 = form.cleaned_data['apt_choice2']
                cd.last_mod_date = datetime.datetime.now()
                cd.curr_stage = 'divination'
                cd.save()
                return HttpResponseRedirect(reverse('create-character-divination', kwargs={'creation_id': cd.pk}))

    else:
        form = DoubleAptsChoiceForm()
        form = prepare_apts_form(form, doubled, apts)
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[6], 'form': form})


def prep_stats(cd: charlist.models.CreationData):
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
    cd = charlist.models.CreationData.objects.get(pk=creation_id)

    background = flyweights.backgrounds().get(cd.background)
    homeworld = flyweights.homeworlds().get(cd.homeworld)
    role = flyweights.roles().get(cd.role)

    if request.method == 'POST':
        if 'char-div-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-double-apts', kwargs={'creation_id': cd.pk}))
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
                if len(cd.apt_1) > 0:
                    apts.append(cd.apt_1)
                    if len(cd.apt_2) > 0:
                        apts.append(cd.apt_2)

                skills = dict()
                skdescrs = flyweights.skill_descriptions()
                any_count = 0
                for key in skdescrs.keys():
                    if not skdescrs.get(key).is_specialist():
                        skills[key] = Skill(key, 0)
                for skill in background.get_skills():
                    if skill.get('tag') in skills.keys():
                        if skill.is_specialist():
                            skills.get(skill.get('tag')).upgrade_subtag(skill.get('subtag'))
                        else:
                            skills.get(skill.get('tag')).upgrade()

                    else:
                        if flyweights.skill_descriptions().get(skill.get('tag')).is_specialist():
                            if skill.get_tag('subtag') == 'SK_ANY':
                                if any_count == 0:
                                    subtag = cd.spec_skill_subtag_1
                                    any_count += 1
                                else:
                                    subtag = cd.spec_skill_subtag_2
                            else:
                                subtag = skill.get_tag('subtag')
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

                bg_talent_choice = background.get_talent_choices()[cd.bg_talent]
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

                role_talent_choice = role.get_talent_choices()[cd.role_talent]
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
                character_model = CharacterModel(character.id, -1, cd.name, cd.gender, cd.height,
                                                 cd.weight, cd.age, cd.homeworld,
                                                 cd.background, cd.role, div_tag, [],
                                                 [wounds, wounds], [0, fatigue], [xp_given, 0], [fate, fate], 0, 0,
                                                 0, apts, stats, skills, talents, traits, [], [], [], [], [])
                character.character_data = character_model.toJSON()
                character.creation_date = cd.last_mod_date
                character.save()
                cd.delete()
                return HttpResponseRedirect(reverse('characters-list'))
            else:
                return render(request, 'character_creation_form.html',
                              {'version': VERSION, 'facade': flyweights,
                               'stage': CREATION_STAGES[7], 'form': form})
        if 'char-apts-next' in request.POST:
            form = DivinationForm()
            if cd.bg_skill_1 is not None:
                if cd.bg_skill_1_subtag == 'SK_ANY':
                    skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_1])
                    field_name = 'subtag_' + skill.get_tag()
                    form.fields[field_name] = CharField(label=skill.get_name_en(), max_length=30)
                    form.fields[field_name].required = True
                if (cd.bg_skill_2 is not None) and (cd.bg_skill_2_subtag == 'SK_ANY'):
                    skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_2])
                    field_name = 'subtag_' + skill.get_tag()
                    form.fields[field_name] = CharField(label=skill.get_name_en(), max_length=30)
                    form.fields[field_name].required = True
            return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                    'stage': CREATION_STAGES[7], 'form': form})
    else:
        form = DivinationForm()
        if cd.bg_skill_1 is not None:
            if cd.bg_skill_1_subtag == 'SK_ANY':
                skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_1])
                field_name = 'subtag_' + skill.get_tag()
                form.fields[field_name] = CharField(label=skill.get_name_en(), max_length=30)
                form.fields[field_name].required = True
            if (cd.bg_skill_2 is not None) and (cd.bg_skill_2_subtag == 'SK_ANY'):
                skill = flyweights.skill_descriptions().get(background.get_skill_choices[0][cd.bg_skill_2])
                field_name = 'subtag_' + skill.get_tag()
                form.fields[field_name] = CharField(label=skill.get_name_en(), max_length=30)
                form.fields[field_name].required = True
        return render(request, 'character_creation_form.html', {'version': VERSION, 'facade': flyweights,
                                                                'stage': CREATION_STAGES[7], 'form': form})


def character_view(request, char_id):
    character = charlist.models.Character.objects.get(pk=char_id)
    character_model = CharacterModel.from_json(character.character)
    return render(request, "charsheet-mockup-interactive.html", {'version': VERSION, 'facade': flyweights,
                                                                 'character': character_model,
                                                                 'hookups': character_model.make_hookups(flyweights)})


def character_delete(request, char_id):
    character = charlist.models.Character.objects.get(pk=char_id)
    if (character is not None) and (character.owner == request.user):
        character.delete()
    return reverse('characters-list')


def creation_data_delete(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        cd.delete()
    return reverse('characters-list')


def resume_creation_edit(request, creation_id):
    cd = charlist.models.CreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        if cd.curr_stage == 'init':
            return create_character_init(request, creation_id)
        if cd.curr_stage == 'hw_choice':
            return create_character_hw_choice(request, creation_id)
        if cd.curr_stage == 'stat_distr':
            return create_character_stat_distribution(request, creation_id)
        if cd.curr_stage == 'bg_choice':
            return create_character_bg_choice(request, creation_id)
        if cd.curr_stage == 'role_choice':
            return create_character_role_choice(request, creation_id)
        if cd.curr_stage == 'choices':
            return create_character_choices(request, creation_id)
        if cd.curr_stage == 'double_apts':
            return create_character_double_apts(request, creation_id)
        if cd.curr_stage == 'divination':
            return create_character_divination(request, creation_id)
    else:
        return reverse('characters-list')
