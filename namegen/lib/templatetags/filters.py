# -*- coding: utf-8 -*-

from typing import Dict

from django import template

from charlist.character.character import CharacterModel
from charlist.flyweights.aptitude import Aptitude
from charlist.flyweights.background_description import BackgroundDescription
from charlist.flyweights.bonus_description import BonusDescription
from charlist.flyweights.core.hint import Hint
from charlist.flyweights.divination_description import DivinationDescription
from charlist.flyweights.elite_advance_description import EliteAdvance
from charlist.flyweights.flyweights import Facade
from charlist.flyweights.homeworld_description import HomeWorldDescription
from charlist.flyweights.role_description import RoleDescription
from charlist.flyweights.skill_description import SkillDescription
from charlist.flyweights.stat_description import StatDescription
from charlist.flyweights.talent_description import TalentDescription
from charlist.flyweights.trait_description import TraitDescription
from charlist.flyweights.malignance_description import MalignanceDescription
from charlist.flyweights.mutation_description import MutationDescription
from charlist.forms.generation.stat_distribution_form import StatDistributionForm

register = template.Library()


@register.filter
def escape_spaces(string: str):
    return string.replace(' ', '-')


@register.filter
def get_by_dict_key(dictionary, key):
    return dictionary.get(key)


@register.filter
def member(obj, key: str):
    return getattr(obj, key, None)


@register.filter
def starts_with(tag: str, start: str):
    return tag[:len(start)] == start


@register.filter
def has_key(tgt: Dict, key: str):
    return key in tgt.keys()


# charsheet filters


# aptitudes
@register.filter
def get_aptitude(facade: Facade, key: str):
    return get_by_dict_key(facade.aptitudes(), key)


@register.filter
def get_apt_name(apt: Aptitude, lang='ru'):
    return apt.get_name(lang)


@register.filter
def get_apt_description(apt: Aptitude, lang='ru'):
    return apt.get_description(lang)


# stat descriptions
@register.filter
def get_stat_description(facade: Facade, key: str):
    return get_by_dict_key(facade.stat_descriptions(), key)


@register.filter
def get_stdescr_name(stdescr: StatDescription, lang='ru'):
    return stdescr.get_name(lang)


@register.filter
def get_stdescr_description(stdescr: StatDescription, lang='ru'):
    return stdescr.get_description(lang)


@register.filter
def get_stdescr_upgradeable(stdescr: StatDescription):
    return stdescr.is_upgradeable()


# skill descriptions
@register.filter
def get_skill_description(facade: Facade, key: str):
    return get_by_dict_key(facade.skill_descriptions(), key)


@register.filter
def get_skdescr_name(skdescr: SkillDescription, lang='ru'):
    return skdescr.get_name(lang)


@register.filter
def get_skdescr_description(skdescr: SkillDescription, lang='ru'):
    return skdescr.get_description(lang)


@register.filter
def get_skdescr_stats(skdescr: SkillDescription):
    return skdescr.get_stats()


@register.filter
def get_skdescr_is_specialist(skdescr: SkillDescription):
    return skdescr.is_specialist()


# hints
@register.filter
def get_hint_description(hint: Hint, lang='ru'):
    return hint.get_description(lang)


# talent descriptions
@register.filter
def get_talent_description(facade: Facade, key: str):
    return get_by_dict_key(facade.talent_descriptions(), key)


@register.filter
def get_tldescr_tag(tldescr: TalentDescription):
    return tldescr.get_tag()


@register.filter
def get_tldescr_name(tldescr: TalentDescription, lang='ru'):
    return tldescr.get_name(lang)


@register.filter
def get_tldescr_description(tldescr: TalentDescription, lang='ru'):
    return tldescr.get_short_description(lang)


@register.filter
def get_tldescr_hints(tldescr: TalentDescription):
    return tldescr.get_hints()


@register.filter
def get_tldescr_tier(tldescr: TalentDescription):
    return tldescr.get_tier()


@register.filter
def get_tldescr_prerequisites(tldescr: TalentDescription):
    return tldescr.get_prerequisites()


@register.filter
def get_tldescr_is_specialist(tldescr: TalentDescription):
    return tldescr.is_specialist()


@register.filter
def get_tldescr_is_stackable(tldescr: TalentDescription):
    return tldescr.is_stackable()


# trait descriptions
@register.filter
def get_trait_description(facade: Facade, key: str):
    return get_by_dict_key(facade.trait_descriptions(), key)


@register.filter
def get_trdescr_name(trdescr: TraitDescription, lang='ru'):
    return trdescr.get_name(lang)


@register.filter
def get_trdescr_description(trdescr: TraitDescription, lang='ru'):
    return trdescr.get_description(lang)


@register.filter
def get_trdescr_hints(trdescr: TraitDescription):
    return trdescr.get_hints()


# homeworlds
@register.filter
def get_homeworld_description(facade: Facade, key: str):
    return get_by_dict_key(facade.homeworlds(), key)


@register.filter
def get_trdescr_is_specialist(trdescr: TraitDescription):
    return trdescr.is_specialist()


@register.filter
def get_trdescr_is_stackable(trdescr: TalentDescription):
    return trdescr.is_stackable()


@register.filter
def get_hw_name(hw: HomeWorldDescription, lang='ru'):
    return hw.get_name(lang)


@register.filter
def get_hw_description(hw: HomeWorldDescription, langs='ru'):
    return hw.get_description(langs)


@register.filter
def get_hw_hints(hw: HomeWorldDescription):
    return hw.get_hints()


@register.filter
def get_hw_stat_mods(hw: HomeWorldDescription):
    return hw.get_stat_mods()


@register.filter
def get_hw_fate(hw: HomeWorldDescription):
    return hw.get_fate()


@register.filter
def get_hw_blessing(hw: HomeWorldDescription):
    return hw.get_blessing()


@register.filter
def get_hw_bonus(hw: HomeWorldDescription):
    return hw.get_bonus()


@register.filter
def get_hw_aptitude(hw: HomeWorldDescription):
    return hw.get_aptitude()


@register.filter
def get_hw_wounds(hw: HomeWorldDescription):
    return hw.get_wounds()


# bonus description
@register.filter
def get_bonus_name(bonus: BonusDescription, lang='ru'):
    return bonus.get_name(lang)


@register.filter
def get_bonus_description(bonus: BonusDescription, lang='ru'):
    return bonus.get_description(lang)


@register.filter
def get_bonus_hints(bonus: BonusDescription):
    return bonus.get_hints()


@register.filter
def get_bonus_commands(bonus: BonusDescription):
    return bonus.get_commands()


# backgrounds
@register.filter
def get_background_description(facade: Facade, key: str):
    return get_by_dict_key(facade.backgrounds(), key)


@register.filter
def get_bg_name(bg: BackgroundDescription, lang='ru'):
    return bg.get_name(lang)


@register.filter
def get_bg_description(bg: BackgroundDescription, lang='ru'):
    return bg.get_description(lang)


@register.filter
def get_bg_hints(bg: BackgroundDescription):
    return bg.get_hints()


@register.filter
def get_bg_aptitudes(bg: BackgroundDescription):
    return bg.get_aptitudes()


@register.filter
def get_bg_apt_choices(bg: BackgroundDescription):
    return bg.get_apt_choices()


@register.filter
def get_bg_skills(bg: BackgroundDescription):
    return bg.get_skills()


@register.filter
def get_bg_skill_choices(bg: BackgroundDescription):
    return bg.get_skill_choices()


@register.filter
def get_bg_talents(bg: BackgroundDescription):
    return bg.get_talents()


@register.filter
def get_bg_talent_choices(bg: BackgroundDescription):
    return bg.get_talent_choices()


@register.filter
def get_bg_traits(bg: BackgroundDescription):
    return bg.get_traits()


@register.filter
def get_bg_trait_choices(bg: BackgroundDescription):
    return bg.get_traits_choices()


@register.filter
def get_bg_equipment(bg: BackgroundDescription):
    return bg.get_equipment()


@register.filter
def get_bg_bonus(bg: BackgroundDescription):
    return bg.get_bonus()


# roles
@register.filter
def get_role_description_big(facade: Facade, key: str):
    return get_by_dict_key(facade.roles(), key)


@register.filter
def get_role_name(role: RoleDescription, lang='ru'):
    return role.get_name(lang)


@register.filter
def get_role_description(role: RoleDescription, lang='ru'):
    return role.get_description(lang)


@register.filter
def get_role_hints(role: RoleDescription):
    return role.get_hints()


@register.filter
def get_role_aptitudes(role: RoleDescription):
    return role.get_aptitudes()


@register.filter
def get_role_apt_choices(role: RoleDescription):
    return role.get_apt_choices()


@register.filter
def get_role_talent_choices(role: RoleDescription):
    return role.get_talent_choices()


@register.filter
def get_role_bonus(role: RoleDescription):
    return role.get_bonus()


# elite advances
@register.filter
def get_elite_advance(facade: Facade, key: str):
    return get_by_dict_key(facade.elite_advances(), key)


@register.filter
def get_ea_name(ea: EliteAdvance, lang='ru'):
    return ea.get_name(lang)


@register.filter
def get_ea_description(ea: EliteAdvance, lang='ru'):
    return ea.get_description(lang)


@register.filter
def get_ea_hints(ea: EliteAdvance):
    return ea.get_hints()


@register.filter
def get_ea_cost(ea: EliteAdvance):
    return ea.cost()


@register.filter
def get_ea_prerequisites(ea: EliteAdvance):
    return ea.prerequisites()


@register.filter
def get_ea_commands(ea: EliteAdvance):
    return ea.commands()


@register.filter
def get_divination_description(facade: Facade, key: str):
    return get_by_dict_key(facade.divinations(), key)


@register.filter
def get_div_name(div: DivinationDescription, lang: str = 'ru'):
    return div.get_name(lang)


@register.filter
def get_div_description(div: DivinationDescription, lang: str = 'ru'):
    return div.get_description(lang)


@register.filter
def get_div_hints(div: DivinationDescription):
    return div.get_hints()


@register.filter
def get_div_commands(div: DivinationDescription):
    return div.get_commands()


@register.filter
def get_div_roll_range(div: DivinationDescription):
    return div.get_roll_range()


@register.filter
def get_malignance(facade: Facade, key: str):
    return facade.malignancies().get(key)


@register.filter
def get_malignance_name(mal: MalignanceDescription, lang: str = 'ru'):
    return mal.get_name(lang)


@register.filter
def get_malignance_description(mal: MalignanceDescription, lang: str = 'ru'):
    return mal.get_description(lang)


@register.filter
def get_mutation(facade: Facade, key: str):
    return facade.mutations().get(key)


@register.filter
def get_mutation_name(mut: MutationDescription, lang: str = 'ru'):
    return mut.get_name(lang)


@register.filter
def get_mutation_description(mut: MutationDescription, lang: str = 'ru'):
    return mut.get_description(lang)


@register.filter
def get_stat_short(facade: Facade, key: str):
    return get_by_dict_key(facade.stat_shorts(), key)


@register.filter
def get_stat_short_name(stat_short: Dict[str, str], lang: str = 'ru'):
    return stat_short.get(lang)


# character
@register.simple_tag
def get_skill_diff(character: CharacterModel, sk_tag: str, stat: str):
    return character.get_skill_diff(sk_tag, stat)


@register.simple_tag
def get_subskill_diff(character: CharacterModel, sk_tag: str, subskill: str, stat: str):
    return character.get_subskill_diff(sk_tag, subskill, stat)


@register.simple_tag
def get_subskill_adv(character: CharacterModel, sk_tag: str, subskill: str):
    return character.skills().get(sk_tag).get_adv_bonus_subtag(subskill)


@register.filter
def get_stat_value(character: CharacterModel, stat: str):
    return character.stats().get(stat).value()


@register.filter
def get_stat_bonus(character: CharacterModel, stat: str):
    return character.stats().get(stat).bonus()


@register.filter
def get_stat_residual(character: CharacterModel, stat: str):
    return character.stats().get(stat).residue()


@register.filter
def get_short_stat(facade: Facade, stat: str):
    return facade.stat_shorts().get(stat)


@register.filter
def get_short_stat_name(short: Dict[str, str], lang: str = 'ru'):
    return short.get(lang)


@register.simple_tag
def mtp(a: float, b: float):
    return a * b


# stat distribution form
@register.filter
def get_field(form: StatDistributionForm, stat: str):
    return form.get_field(stat)
