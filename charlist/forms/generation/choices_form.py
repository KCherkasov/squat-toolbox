# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form


class ChoicesForm(Form):
    def __init__(self, flyweights, creation_data, *args, **kwargs):
        super(ChoicesForm, self).__init__(*args, **kwargs)
        homeworld = flyweights.homeworlds().get(creation_data.homeworld)
        hw_bonus = homeworld.get_bonus()
        for command in hw_bonus.get_commands():
            if command.get('tag') == 'GainTalentAlt':
                choices = []
                i = 0
                for tag in command.get('tags'):
                    sk_name = flyweights.talent_descriptions().get(tag).get_name_en()
                    choices.append((i, sk_name))
                    i += 1
                self.fields['hw-bonus-talent'] = forms.ChoiceField(
                    label="Талант (бонус родного мира)", choices=choices)

        background = flyweights.backgrounds().get(creation_data.background)

        bg_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en())
                   for apt in background.get_apt_choices()]
        self.fields['background_apts'].choices = bg_apts

        role = flyweights.roles().get(creation_data.role)

        role_apts = [(apt, flyweights.aptitudes().get(apt).get_name_en()) for
                     apt in role.get_apt_choices()]
        self.fields['role_apts'].choices = role_apts
        if len(role_apts) == 0:
            self.fields['role_apts'].required = False
            self.fields['role_apts'].widget = forms.Select(
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
                        if 'background-skills-subtag' not in self.fields:
                            self.fields['background-skills-subtag'] = \
                                forms.CharField(label=u'Специализация', max_length=30)
                    else:
                        sk_name += ' ('
                        for tag in subtag:
                            sk_name += tag + ', '
                        sk_name = sk_name[:-2] + ')'
                sk_choices.append((i, sk_name))
                i += 1
            self.fields['background_skills'].choices = sk_choices
            if len(bg_skill_choices) > 1:
                skill_choice2 = bg_skill_choices[1]
                i = 0
                sk_choices2 = []
                for skill in skill_choice2:
                    tag = skill.get('tag')
                    subtag = None
                    sk = flyweights.skill_descriptions().get(tag)
                    sk_name = sk.get_name_en()
                    if flyweights.skill_descriptions().get(tag).is_specialist():
                        subtag = skill.get('subtag')
                    if subtag:
                        if subtag == 'SK_ANY' and 'background-skills-subtag2' not in self.fields:
                            self.fields['background-skills-subtag2'] = \
                                forms.CharField(label=u'Специализация', max_length=30)
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
                self.fields['background_skills2'].choices = sk_choices2
            else:
                self.fields['background_skills2'].required = False
                self.fields['background_skills2'].widget = forms.Select(
                    {'class': 'form-control disabled'}, [])

        for sk in background.get_skills():
            skill = flyweights.skill_descriptions().get(sk.get('tag'))
            if skill is not None:
                if (skill.is_specialist()) and (sk.get('subtag') == 'SK_ANY'):
                    field_name = 'subtag_' + sk.get('tag')
                    self.fields[field_name] = forms.CharField(label=skill.get_name_en(), max_length=30)
                    self.fields[field_name].required = True

        bg_talents = background.get_talent_choices()
        bg_tals = []
        i = 0
        for tal in bg_talents:
            talent = flyweights.talent_descriptions().get(tal.get('tag'))
            name = talent.get_name_en()
            if talent.is_specialist():
                name += ' ('
                if 'subtag' in tal.keys():
                    name += tal.get('subtag')
                if 'subtag1' in tal.keys():
                    name += tal.get('subtag1')
                    if 'subtag2' in tal.keys():
                        name += ', ' + tal.get('subtag2')
                name += ')'
            bg_tals.append((i, name))
            i += 1
        self.fields['background_talents'].choices = bg_tals
        if len(bg_tals) == 0:
            self.fields['background_talents'].required = False
            self.fields['background_talents'].widget = forms.Select(
                {'class': 'form-control disabled'}, bg_tals)

        role_talents = role.get_talent_choices()
        role_tals = []
        i = 0
        for tal in role_talents:
            talent = flyweights.talent_descriptions().get(tal.get('tag'))
            name = talent.get_name_en()
            if talent.is_specialist():
                name += ' ('
                if 'subtag' in tal.keys():
                    name += tal.get('subtag')
                if 'subtag1' in tal.keys():
                    name += tal.get('subtag1')
                    if 'subtag2' in tal.keys():
                        name += ', ' + tal.get('subtag2')
                name += ')'
            role_tals.append((i, name))
            i += 1
        self.fields['role_talent'].choices = role_tals
        if len(role_tals) == 0:
            self.fields['role_talent'].required = False
            self.fields['role_talent'].widget = forms.Select(
                {'class': 'form-control disabled'}, role_tals)

        background_traits = background.get_traits_choices()
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
                    name += '(' + str(trait.get('taken')) + ')'
                bg_traits.append((i, name))
                i += 1
        self.fields['background_traits'].choices = bg_traits
        if len(self.fields['background_traits'].choices) == 0:
            self.fields['background_traits'].required = False
            self.fields['background_traits'].widget = forms.Select(
                {'class': 'form-control disabled'}, bg_traits)

    background_apts = forms.ChoiceField(label=u'Склонность предыстории')
    role_apts = forms.ChoiceField(label=u'Склонность роли', required=False)
    background_skills = forms.ChoiceField(label=u'Навык предыстории')
    background_skills2 = forms.ChoiceField(label=u'Второй навык предыстории', required=False)
    background_talents = forms.ChoiceField(label=u'Талант предыстории')
    role_talent = forms.ChoiceField(label=u'Талант роли')
    background_traits = forms.ChoiceField(label=u'Черта предыстории', required=False)
