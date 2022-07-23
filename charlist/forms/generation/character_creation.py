# -*- coding: utf-8 -*-

from django.forms import Form
from charlist.character.character import CharacterModel, Skill, Stat, Talent, Trait
from charlist.flyweights.flyweights import Facade, RoleDescription, TraitDescription,\
    TalentDescription, BackgroundDescription, HomeWorldDescription,\
    StatDescription, SkillDescription, Aptitude
from charlist.constants.tags import *

# class CharacterGenerationForm(Form):0
