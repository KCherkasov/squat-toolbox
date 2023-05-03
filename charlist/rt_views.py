# -*- coding: utf-8 -*-
import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import reverse
from django.template.response import TemplateResponse

import charlist.models as models
from charlist.character.rt_character import RTCharacterModel
from charlist.character.rt_creation_data import RTCreationDataModel
from charlist.character.skill import Skill
from charlist.character.stat import Stat
from charlist.constants.constants import *
from charlist.flyweights.rt_flyweights import *
from charlist.forms.generation.rt.choices_form import RTChoicesForm, STG_PREFIX
from charlist.forms.generation.rt.creation_settings_form import CreationSettingsForm
from charlist.forms.generation.rt.divination_form import DivinationForm
from charlist.forms.generation.rt.double_apts_form import DoubleAptsForm
from charlist.forms.generation.rt.origin_and_career_form import OriginAndCareerForm
from charlist.forms.generation.rt.stat_distribution_form import RTStatDistributionForm
from charlist.forms.generation.rt_stages import *
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
from charlist.forms.player_todos.manual.gain_stat_aptitude_form import GainStatAptitudeForm
from charlist.forms.player_todos.manual.gain_talent_alt_form import GainTalentAltForm
from charlist.forms.player_todos.manual.get_trauma_ip_form import GetTraumaIPForm
from charlist.forms.player_todos.manual.increase_stat_alt_form import IncreaseStatAltForm
from charlist.forms.player_todos.manual.increase_stat_roll_form import IncreaseStatRollForm
from charlist.forms.upgrading.skill_subtag_upgrade_form import SkillSubtagUpgradeForm
from charlist.forms.upgrading.skill_upgrade_form import SkillUpgradeForm
from charlist.forms.upgrading.stat_upgrade_form import StatUpgradeForm
from charlist.forms.upgrading.talent_subtag_upgrade_form import TalentUpgradeSubtagForm
from charlist.forms.upgrading.talent_upgrade_form import TalentUpgradeForm
from charlist.forms.player_todos.manual.origin_xp_extra_choice import GainExtraOriginCommand
from charlist.forms.player_todos.manual.gain_spec_skill_subtag import GainSpecSkillForm
from charlist.forms.player_todos.manual.gain_spec_talent_subtag import GainSpecTalentForm
from charlist.forms.upgrading.psy_power_upgrade_form import PsyPowerUpgradeForm
from charlist.forms.upgrading.elite_advance_upgrade_form import EliteAdvanceUpgradeForm
from charlist.forms.upgrading.pr_upgrade_form import PRUpgrageForm

resources = ['aptitudes.json', 'rt_stat_descriptions.json', 'rt_skill_descriptions.json', 'rt_talent_descriptions.json',
             'traits.json', 'homeworlds.json', 'backgrounds.json', 'roles.json', 'rt_elite_advances.json',
             'divinations.json', 'malignancies.json', 'mutations.json', 'psy.json', 'combat_actions.json',
             'rt_homeworlds.json', 'rt_birthrights.json', 'rt_lures.json', 'rt_trials.json', 'rt_motivations.json',
             'rt_careers.json']
rt_flyweights = RTFacade(resources)
rt_commands_parser = CommandParser(rt_flyweights)


def create_character_rt_start(request):
    creation_data = models.RTCreationData()
    creation_data.owner = models.CharsheetUser.objects.get(pk=request.user.pk)
    creation_data.save()
    return HttpResponseRedirect(reverse('rt-create-character-init', kwargs={'creation_id': creation_data.pk}))


def rt_create_character_init(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        form = CreationSettingsForm(request.POST)
        if 'char-origin-prev' in request.POST:
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[0], 'form': form})
        else:
            if ('char-cr-next' in request.POST) and form.is_valid():
                cleaned_data = form.cleaned_data
                cd.name = cleaned_data['name']
                cd.curr_stage = 'origin-and-career'
                cdm = RTCreationDataModel.new_cd(cleaned_data['name'], int(cleaned_data['starting_xp']),
                                                 int(cleaned_data['characteristics_base']))
                cd.character_data = cdm.to_json()
                cd.last_mod_date = datetime.datetime.now()
                cd.save()
        return HttpResponseRedirect(reverse('rt-create-character-oac', kwargs={'creation_id': cd.pk}))
    else:
        form = CreationSettingsForm()
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'stage': RT_CREATION_STAGES[0], 'form': form})


def rt_create_character_oac_choice(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    if request.method == 'POST':
        if 'char-cr-next' in request.POST:
            form = OriginAndCareerForm(rt_flyweights)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[1], 'form': form})
        form = OriginAndCareerForm(rt_flyweights, request.POST)
        if 'char-origin-next' in request.POST:
            if form.is_valid():
                cdm = cd.data_to_model()
                cdm.hw_id = form.cleaned_data['hw_id']
                cdm.birthright_id = form.cleaned_data['br_id']
                cdm.lure_id = form.cleaned_data['lure_id']
                cdm.trial_id = form.cleaned_data['trial_id']
                cdm.motivation_id = form.cleaned_data['motivation_id']
                cdm.career_id = form.cleaned_data['career_id']
                cdm.full_reset(rt_flyweights)
                cdm.xp[0] += rt_flyweights.birthrights().get(cdm.birthright_id).cost()
                cdm.xp[0] += rt_flyweights.lures().get(cdm.lure_id).cost()
                cdm.xp[0] += rt_flyweights.trials().get(cdm.trial_id).cost()
                cdm.xp[0] += rt_flyweights.motivations().get(cdm.motivation_id).cost()
                cd.last_mod_date = datetime.datetime.now()
                cd.curr_stage = 'stat-distr'
                cd.character_data = cdm.to_json()
                cd.save()
                return HttpResponseRedirect(reverse('rt-create-character-stats', kwargs={'creation_id': cd.pk}))
        if 'char-origin-prev' in request.POST:
            return HttpResponseRedirect(reverse('rt-create-character-init', kwargs={'creation_id': cd.pk}))
    else:
        form = OriginAndCareerForm(rt_flyweights)
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'stage': RT_CREATION_STAGES[1], 'form': form})


def rt_create_character_stat_distribution(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    cdm = cd.data_to_model()
    if request.method == 'POST':
        if 'char-origin-next' in request.POST:
            form = RTStatDistributionForm(rt_flyweights)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[2], 'form': form})
        if 'char-st-prev' in request.POST:
            return HttpResponseRedirect(reverse('rt-create-character-oac', kwargs={'creation_id': cd.pk}))
        form = RTStatDistributionForm(rt_flyweights, request.POST)
        if 'char-st-next' in request.POST:
            if form.is_valid():
                stats = dict()
                for stat in RT_STAT_TAGS:
                    stats[stat] = cdm.stats.get(stat) + form.cleaned_data[stat]
                cdm.stats = stats
            cd.character_data = cdm.to_json()
            cd.last_mod_date = datetime.datetime.now()
            cd.curr_stage = 'choices'
            return HttpResponseRedirect(reverse('rt-create-character-choices', kwargs={'creation_id': cd.pk}))
    else:
        form = RTStatDistributionForm(rt_flyweights)
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'cd': cdm, 'stage': RT_CREATION_STAGES[2],
                                                                   'form': form})


def rt_create_character_choices(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    cdm = cd.data_to_model()
    if request.method == 'POST':
        if 'char-choices-prev' in request.POST:
            return HttpResponseRedirect(reverse('create-character-role', kwargs={'creation_id': cd.pk}))
        if 'char-st-next' in request.POST:
            form = RTChoicesForm(rt_flyweights)
            form.parse(cdm)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[3], 'form': form})
        form = RTChoicesForm(rt_flyweights, request.POST)
        if 'char-apts-prev' in request.POST:
            cdm.full_reset()
            form.parse(cdm)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[3], 'form': form})
        if 'char-choices-next' in request.POST:
            if form.is_valid():
                cleaned_data = form.cleaned_data
                cdm.choices = list()
                for key, choice in cleaned_data.iteritems():
                    cdm.choices.append(choice)
                    if choice.get('tag')[:2] == 'A_':
                        cdm.aptitudes.append(choice.get('tag'))
                    elif choice.get('tag')[:2] == 'SK':
                        if 'subtag' in choice.keys():
                            if choice.get('subtag') == 'SK_ANY':
                                subtag_fld_name = str(STG_PREFIX) + key
                                res_choice = {'tag': choice.get('tag'),
                                              'subtag': cleaned_data.get(subtag_fld_name)}
                                cdm.skills.append(res_choice)
                        else:
                            cdm.skills.append(choice)
                    elif choice.get('tag')[:2] == 'TL':
                        if 'subtag' in choice.keys():
                            if choice.get('subtag') == 'SK_ANY':
                                subtag_fld_name = str(STG_PREFIX) + key
                                res_choice = {'tag': choice.get('tag'),
                                              'subtag': cleaned_data.get(subtag_fld_name)}
                                cdm.talents.append(res_choice)
                        else:
                            cdm.talents.append(choice)
                    else:
                        cmd = dict()
                        cmd['command'] = choice.get('tag')
                        if 'stat' in choice.keys():
                            cmd['tag'] = choice.get('stat')
                            cmd['amount'] = choice.get('amount')
                        cdm.commands.append(cmd)
                cd.curr_stage = 'double-apts'
                cd.last_mod_date = datetime.datetime.now()
                cd.character_data = cdm.to_json()
                cd.save()
                return HttpResponseRedirect(reverse('rt-create-character-double-apts', kwargs={'creation_id': cd.pk}))
            else:
                return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                           'stage': RT_CREATION_STAGES[3], 'cd': cdm,
                                                                           'form': form})
    else:
        form = RTChoicesForm(rt_flyweights)
        form.parse(cdm)
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'cd': cdm, 'stage': RT_CREATION_STAGES[3],
                                                                   'form': form})


def create_character_double_apts(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    cdm = cd.data_to_model()

    if cdm.count_doubles() == 0:
        cdm.aptitudes = cdm.simplify_apts()
        cd.character_data = cdm.to_json()
        cd.curr_stage = 'divination'
        cd.save()
        return HttpResponseRedirect(reverse('rt-create-character-divination', kwargs={'creation_id': cd.pk}))

    if request.method == 'POST':
        if 'char-apts-prev' in request.POST:
            return HttpResponseRedirect(reverse('rt-create-character-choices', kwargs={'creation_id': cd.pk}))
        if 'char-choices-next' in request.POST:
            form = DoubleAptsForm(cdm, rt_flyweights)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[4], 'form': form})
        form = DoubleAptsForm(cdm, rt_flyweights, request.POST)
        if form.is_valid():
            simple_apts = cdm.simplify_apts()
            for key, apt in form.cleaned_data:
                simple_apts.append(apt)
            cd.aptitudes = simple_apts
            cd.character_data = cdm.to_json()
            cd.last_mod_date = datetime.datetime.now()
            cd.curr_stage = 'divination'
            cd.save()
            return HttpResponseRedirect(reverse('rt-create-character-divination', kwargs={'creation_id': cd.pk}))
        else:
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[4], 'form': form})
    else:
        form = DoubleAptsForm(cdm, rt_flyweights)
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'stage': RT_CREATION_STAGES[4], 'form': form})


def prep_stats(cd: RTCreationDataModel):
    stats = dict()
    for stat in STAT_TAGS:
        stats[stat] = Stat(stat, cd.stats.get(stat))
    return stats


def create_character_divination(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    cdm = cd.data_to_model()

    homeworld = rt_flyweights.rt_homeworlds().get(cdm.hw_id)

    if request.method == 'POST':
        if 'char-div-prev' in request.POST:
            return HttpResponseRedirect(reverse('rt-create-character-double-apts', kwargs={'creation_id': cd.pk}))
        if 'char-div-next' in request.POST:
            form = DivinationForm(rt_flyweights, cdm, request.POST)
            div_tag = None
            if form.is_valid():
                divination_roll = form.cleaned_data['divination_roll']
                for div_key in rt_flyweights.divinations().keys():
                    divination = rt_flyweights.divinations().get(div_key)
                    if (divination_roll >= divination.get_roll_range()[0]) \
                            and (divination_roll <= divination.get_roll_range()[1]):
                        div_tag = div_key
                        break
                wound_roll = form.cleaned_data['wound_roll']
                fate_roll = form.cleaned_data['fate_roll']

                xp_given = cdm.xp[1]
                xp_spent = cdm.xp[0]
                fate = homeworld.get_fate()
                if fate_roll >= homeworld.get_blessing():
                    fate += 1
                stats = prep_stats(cdm)
                fatigue = stats.get(ST_TOUGHNESS).bonus() + stats.get(ST_WILLPOWER).bonus()
                wounds = wound_roll + homeworld.get_wounds()
                apts = cdm.aptitudes

                skills = dict()
                skdescrs = rt_flyweights.skill_descriptions()
                for key in skdescrs.keys():
                    if not skdescrs.get(key).is_specialist():
                        skills[key] = Skill(key, 0)
                cdm.to_commands()

                divination = rt_flyweights.divinations().get(div_tag)
                malignancies = list()
                mutations = list()
                disorders = list()
                character = models.Character.objects.create(owner=request.user, character_data='')
                character.is_rt = True
                character.save()
                character_model = RTCharacterModel(character.id, -1, cdm.name, cdm.hw_id, cdm.birthright_id,
                                                   cdm.lure_id, cdm.trial_id, cdm.motivation_id, cdm.career_id,
                                                   div_tag, [], [wounds, wounds], [0, fatigue],
                                                   [xp_given - xp_spent, xp_spent], [fate, fate], 0, 0, 0,
                                                   apts, stats, skills, dict(), dict(), [], [], disorders,
                                                   malignancies, mutations, [], [], [], 0, 0, 0)
                for cmd in divination.get_commands():
                    character_model.pending().append(cmd)
                for cmd in cdm.commands:
                    character_model.pending().append(cmd)
                character_model = rt_commands_parser.process_character(character_model)
                character.character_data = character_model.toJSON()
                character.creation_date = cd.last_mod_date
                character.save()
                cd.delete()
                return HttpResponseRedirect(reverse('characters-list'))
            else:
                return TemplateResponse(request, 'rt-creation-form.html',
                                        {'version': VERSION, 'facade': rt_flyweights,
                                         'stage': RT_CREATION_STAGES[5], 'form': form})
        if 'char-apts-next' in request.POST:
            form = DivinationForm(rt_flyweights, cdm)
            return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                       'stage': RT_CREATION_STAGES[5], 'form': form})
    else:
        form = DivinationForm(rt_flyweights, cdm)
        return TemplateResponse(request, 'rt-creation-form.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                   'stage': RT_CREATION_STAGES[5], 'form': form})


def clean_completed(character_model: RTCharacterModel, request):
    if int(request.POST.get('cmd_id')) >= 0:
        for cmd in character_model.pending():
            if cmd.get('cmd_id') == int(request.POST.get('cmd_id')):
                character_model.pending().remove(cmd)
                break
    return character_model


def find_cmd(request, character_model: RTCharacterModel):
    cmd = dict()
    for pcmd in character_model.pending():
        if pcmd.get('cmd_id') == int(request.POST.get('cmd_id')):
            cmd = pcmd
            break
    return cmd


def gain_insanity(request, character: RTCharacterModel, character_record: models.Character):
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


def gain_corruption(request, character: RTCharacterModel, character_record: models.Character):
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


def decrease_stat_alt(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = DecreaseStatAltForm(cmd, rt_flyweights, request.POST)
    if form.is_valid():
        character_model.damage_stat(form.cleaned_data['choices'], form.amount())
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def increase_stat_alt(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = IncreaseStatAltForm(cmd, rt_flyweights, request.POST)
    if form.is_valid():
        character_model.improve_stat(form.cleaned_data['choices'], form.amount())
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_talent_alt(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainTalentAltForm(cmd, rt_flyweights, request.POST)
    if form.is_valid():
        character_model.gain_talent(form.cleaned_data['choices'], rt_flyweights)
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def decrease_stat_roll(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = DecreaseStatRollForm(cmd, rt_flyweights, request.POST)
    if form.is_valid():
        character_model.damage_stat(cmd.get('tag'), form.cleaned_data['roll_value'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def increase_stat_roll(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = IncreaseStatRollForm(cmd, rt_flyweights, request.POST)
    if form.is_valid():
        character_model.improve_stat(cmd.get('tag'), form.cleaned_data['roll_value'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def abort_gain(request, character_model: RTCharacterModel, character: models.Character):
    character_model = clean_completed(character_model, request)
    character.character_data = character_model.toJSON()
    character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def abort_gain_ip_conseq(request, character_model: RTCharacterModel, character: models.Character):
    character_model.inc_ip_tests()
    abort_gain(request, character_model, character)


def abort_gain_cp_conseq(request, character_model: RTCharacterModel, character: models.Character):
    character_model.inc_cp_tests()
    abort_gain(request, character_model, character)


def gain_disorder(request, character_model: RTCharacterModel, character: models.Character):
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


def gain_trauma(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GetTraumaIPForm(cmd, request.POST)
    if form.is_valid():
        character_model = clean_completed(character_model, request)
        character_model.inc_ip_tests()
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_malignancy(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainMalignancyRollForm(cmd, request.POST)
    if form.is_valid():
        roll_result = form.cleaned_data['roll_result']
        for mal_key, mal in rt_flyweights.malignancies().items():
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


def gain_mutation(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainMutationRollForm(cmd, request.POST)
    if form.is_valid():
        roll_result = form.cleaned_data['roll_result']
        for mut_key, mut in rt_flyweights.mutations().items():
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


def gain_malignance_choice(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainMalignancyChoiceForm(rt_flyweights, cmd, request.POST)
    if form.is_valid():
        choice = form.cleaned_data['choices']
        if choice not in character_model.malignances():
            character_model.malignances().append(choice)
            for cmd in rt_flyweights.malignancies().get(choice).get_commands():
                character_model.pending().append(cmd)
            character_model = clean_completed(character_model, request)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_mutation_choice(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainMutationChoiceForm(rt_flyweights, cmd, request.POST)
    if form.is_valid():
        choice = form.cleaned_data['choices']
        if choice not in character_model.mutations():
            character_model.mutations().append(choice)
            character_model = clean_completed(character_model, request)
            for cmd in rt_flyweights.mutations().get(choice):
                character_model.pending().append(cmd)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_stat_aptitude(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainStatAptitudeForm(character_model, rt_flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.aptitudes().append(form.cleaned_data['choices'])
        character_model = clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_spec_skill(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainSpecSkillForm(rt_flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.improve_skill_subtag(form.sk_tag, form.cleaned_data['subtag'], rt_flyweights)
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def origin_extra_confirm(request, character_model: RTCharacterModel, character: models.Character):
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


def origin_extra_abort(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainExtraOriginCommand(cmd)
    if form.is_valid():
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def gain_spec_talent(request, character_model: RTCharacterModel, character: models.Character):
    cmd = find_cmd(request, character_model)
    form = GainSpecTalentForm(rt_flyweights, cmd, request.POST)
    if form.is_valid():
        character_model.gain_talent_subtag(form.sk_tag, form.cleaned_data['subtag'], rt_flyweights)
        clean_completed(character_model, request)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-details', kwargs={'char_id': character.pk, }))


def parse_manual_cmds(request, character: models.Character, character_model: RTCharacterModel):
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


def upg_data_to_forms(character: RTCharacterModel):
    upg_costs = character.make_upg_costs(rt_flyweights)
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
    for stat_tag in rt_flyweights.stat_tags():
        if stat_tag in upg_costs.get('stats').keys():
            forms.get('stats').append(
                StatUpgradeForm(stat_tag, character.stats().get(stat_tag).value(),
                                upg_costs.get('stats').get(stat_tag).get('cost'),
                                upg_costs.get('stats').get(stat_tag).get('colour')))
    for skill_tag in upg_costs.get('skills').keys():
        if not rt_flyweights.skill_descriptions().get(skill_tag).is_specialist():
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
                        form_map.get('forms').append(TalentUpgradeSubtagForm(
                            tl_tag, key, talent.get('cost'), True, taken))
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
                                tl_tag, key, talent.get('cost'), False, taken))
                    forms.get('talents').get('unavailable')[tier].get('spec').append(form_map)
    for ea_key, cost in upg_costs.get('ea').get('available').items():
        forms.get('ea').get('available').append(EliteAdvanceUpgradeForm(ea_key, cost, True))
    for ea_key, cost in upg_costs.get('ea').get('unavailable').items():
        forms.get('ea').get('unavailable').append(EliteAdvanceUpgradeForm(ea_key, cost, False))
    if 'pr' in upg_costs.keys():
        forms['pr'] = PRUpgrageForm(character.pr(), upg_costs.get('pr'))
    if 'psy' in upg_costs.keys():
        forms['psy'] = {'available': dict(), 'unavailable': dict()}
        for school, powers in upg_costs.get('psy').get('available').items():
            forms.get('psy').get('available')[school] = list()
            for power, cost in powers.items():
                forms.get('psy').get('available').get(school).append(PsyPowerUpgradeForm(power, cost, True))
        for school, powers in upg_costs.get('psy').get('unavailable').items():
            forms.get('psy').get('unavailable')[school] = list()
            for power, cost in powers.items():
                forms.get('psy').get('unavailable').get(school).append(PsyPowerUpgradeForm(power, cost, False))
    return forms


def character_view(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    character_model = character.data_to_model()
    insanity_form = None
    corruption_form = None
    reminders = None
    if (request.user is not None) and (request.user == character.owner):
        if request.method == 'POST':
            parse_manual_cmds(request, character, character_model)
        insanity_form = GainInsanityRollForm()
        corruption_form = GainCorruptionRollForm()
        character_model = rt_commands_parser.process_character(character_model)
        reminders = list()
        # TODO: controls (stats/skills/talents upgrading, XP gaining, etc.
        if len(character_model.pending()) > 0:
            for cmd in character_model.pending():
                reminder = rt_commands_parser.make_reminder(cmd, character_model)
                if reminder is not None:
                    reminders.append(reminder)
                else:
                    character_model.pending().remove(cmd)
        character.character_data = character_model.toJSON()
        character.save()
    return TemplateResponse(request, "charsheet.html", {'version': VERSION, 'facade': rt_flyweights,
                                                        'command_parser': rt_commands_parser,
                                                        'character': character_model,
                                                        'hookups': character_model.make_hookups(rt_flyweights),
                                                        'insanity_form': insanity_form,
                                                        'corruption_form': corruption_form,
                                                        'reminders': reminders,
                                                        'upg_view': character.get_upgrade_url(), })


def upg_midlayer(request, char_id):
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': char_id, }))


def upgrade_stat(request, character: models.Character, character_model: RTCharacterModel):
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


def upgrade_skill(request, character: models.Character, character_model: RTCharacterModel):
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


def upgrade_subskill(request, character: models.Character, character_model: RTCharacterModel):
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
        character_model.improve_skill_subtag(skill_tag, sk_subtag, rt_flyweights)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_talent(request, character: models.Character, character_model: RTCharacterModel):
    tl_tag = request.POST.get('tl_tag')
    cost = int(request.POST.get('cost'))
    form = TalentUpgradeForm(tl_tag, cost, 'success', True, 0, request.POST)
    if form.is_valid():
        if character_model.xp_current() >= cost:
            character_model.spend_xp(cost)
            character_model.gain_talent(tl_tag, rt_flyweights)
            character.character_data = character_model.toJSON()
            character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_talent_subtag(request, character: models.Character, character_model: RTCharacterModel):
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
        character_model.gain_talent_subtag(tl_tag, tl_subtag, rt_flyweights)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_ea(request, character: models.Character, character_model: RTCharacterModel):
    ea_tag = request.POST.get('ea_tag')
    cost = int(request.POST.get('cost'))
    form = EliteAdvanceUpgradeForm(ea_tag, cost, True, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.gain_ea_id(ea_tag)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_pr(request, character: models.Character, character_model: RTCharacterModel):
    cost = int(request.POST.get('cost'))
    form = PRUpgrageForm(character_model.pr(), cost, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.gain_pr()
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def upgrade_psy_power(request, character: models.Character, character_model: RTCharacterModel):
    pp_tag = request.POST.get('pp_tag')
    cost = int(request.POST.get('cost'))
    form = PsyPowerUpgradeForm(pp_tag, cost, True, request.POST)
    if form.is_valid():
        character_model.spend_xp(cost)
        character_model.psy_powers().append(pp_tag)
        character.character_data = character_model.toJSON()
        character.save()
    return HttpResponseRedirect(reverse('character-upgrade', kwargs={'char_id': character.pk, }))


def parse_upgrades(request, character: models.Character, character_model: RTCharacterModel):
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


def character_upgrade(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    character_model = character.data_to_model()
    if request.method == 'POST':
        parse_upgrades(request, character, character_model)
    forms = upg_data_to_forms(character_model)
    return TemplateResponse(request, 'charsheet-upgrade.html', {'version': VERSION, 'facade': rt_flyweights,
                                                                'character': character_model, 'forms': forms,
                                                                'return': True,
                                                                'char_view': character.get_view_url(), })


def character_delete(request, char_id):
    character = models.Character.objects.get(pk=char_id)
    if (character is not None) and (character.owner == request.user):
        character.delete()
    return HttpResponseRedirect(reverse('characters-list'))


def creation_data_delete(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        cd.delete()
    return HttpResponseRedirect(reverse('characters-list'))


def resume_creation_edit(request, creation_id):
    cd = models.RTCreationData.objects.get(pk=creation_id)
    if (cd is not None) and (cd.owner == request.user):
        if cd.curr_stage == 'init':
            return HttpResponseRedirect(reverse('rt-create-character-init', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'origin-and-career':
            return HttpResponseRedirect(reverse('rt-create-character-oac', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'stat-distr':
            return HttpResponseRedirect(reverse('rt-create-character-stats', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'choices':
            return HttpResponseRedirect(reverse('rt-create-character-choices', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'double-apts':
            return HttpResponseRedirect(reverse('rt-create-character-double-apts', kwargs={'creation_id': cd.pk}))
        if cd.curr_stage == 'divination':
            return HttpResponseRedirect(reverse('rt-create-character-divination', kwargs={'creation_id': cd.pk}))
    else:
        return reverse('characters-list')
