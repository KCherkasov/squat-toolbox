# -*- coding: utf-8 -*-

from django import template

from charlist import flyweights
from charlist.character import *

register = template.Library()


@register.filter
def get_by_dict_key(dictionary, key):
    return dictionary.get(key)


@register.filter
def member(obj, key: str):
    return getattr(obj, key, None)


# charsheet filters


# aptitudes
@register.filter
def get_aptitude(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.aptitudes(), key)


@register.filter
def get_apt_name(apt: flyweights.Aptitude, lang='ru'):
    return apt.get_name(lang)


@register.filter
def get_apt_description(apt: flyweights.Aptitude, lang='ru'):
    return apt.get_description(lang)


# stat descriptions
@register.filter
def get_stat_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.stat_descriptions(), key)


@register.filter
def get_stdescr_name(stdescr: flyweights.StatDescription, lang='ru'):
    return stdescr.get_name(lang)


@register.filter
def get_stdescr_description(stdescr: flyweights.StatDescription, lang='ru'):
    return stdescr.get_description(lang)


@register.filter
def get_stdescr_upgradeable(stdescr: flyweights.StatDescription):
    return stdescr.is_upgradeable()


# skill descriptions
@register.filter
def get_skill_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.skill_descriptions(), key)


@register.filter
def get_skdescr_name(skdescr: flyweights.SkillDescription, lang='ru'):
    return skdescr.get_name(lang)


@register.filter
def get_skdescr_description(skdescr: flyweights.SkillDescription, lang='ru'):
    return skdescr.get_description(lang)


@register.filter
def get_skdescr_stats(skdescr: flyweights.SkillDescription):
    return skdescr.get_stats()


@register.filter
def get_skdescr_is_specialist(skdescr: flyweights.SkillDescription):
    return skdescr.is_specialist()


# hints
@register.filter
def get_hint_description(hint: flyweights.Hint, lang='ru'):
    return hint.get_description(lang)


# talent descriptions
@register.filter
def get_talent_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.talent_descriptions(), key)


@register.filter
def get_tldescr_tag(tldescr: flyweights.TalentDescription):
    return tldescr.get_tag()


@register.filter
def get_tldescr_name(tldescr: flyweights.TalentDescription, lang='ru'):
    return tldescr.get_name(lang)


@register.filter
def get_tldescr_description(tldescr: flyweights.TalentDescription, lang='ru'):
    return tldescr.get_short_description(lang)


@register.filter
def get_tldescr_hints(tldescr: flyweights.TalentDescription):
    return tldescr.get_hints()


@register.filter
def get_tldescr_tier(tldescr: flyweights.TalentDescription):
    return tldescr.get_tier()


@register.filter
def get_tldescr_prerequisites(tldescr: flyweights.TalentDescription):
    return tldescr.get_prerequisites()


@register.filter
def get_tldescr_is_specialist(tldescr: flyweights.TalentDescription):
    return tldescr.is_specialist()


@register.filter
def get_tldescr_is_stackable(tldescr: flyweights.TalentDescription):
    return tldescr.is_stackable()


# trait descriptions
@register.filter
def get_trait_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.trait_descriptions(), key)


@register.filter
def get_trdescr_name(trdescr: flyweights.TraitDescription, lang='ru'):
    return trdescr.get_name(lang)


@register.filter
def get_trdescr_description(trdescr: flyweights.TraitDescription, lang='ru'):
    return trdescr.get_description(lang)


@register.filter
def get_trdescr_hints(trdescr: flyweights.TraitDescription):
    return trdescr.get_hints()


# homeworlds
@register.filter
def get_homeworld_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.homeworlds(), key)


@register.filter
def get_hw_name(hw: flyweights.HomeWorldDescription, lang='ru'):
    return hw.get_name(lang)


@register.filter
def get_hw_description(hw: flyweights.HomeWorldDescription, langs='ru'):
    return hw.get_description(langs)


@register.filter
def get_hw_hints(hw: flyweights.HomeWorldDescription):
    return hw.get_hints()


@register.filter
def get_hw_stat_mods(hw: flyweights.HomeWorldDescription):
    return hw.get_stat_mods()


@register.filter
def get_hw_fate(hw: flyweights.HomeWorldDescription):
    return hw.get_fate()


@register.filter
def get_hw_blessing(hw: flyweights.HomeWorldDescription):
    return hw.get_blessing()


@register.filter
def get_hw_bonus(hw: flyweights.HomeWorldDescription):
    return hw.get_bonus()


@register.filter
def get_hw_aptitude(hw: flyweights.HomeWorldDescription):
    return hw.get_aptitude()


@register.filter
def get_hw_wounds(hw: flyweights.HomeWorldDescription):
    return hw.get_wounds()


# bonus description
@register.filter
def get_bonus_name(bonus: flyweights.BonusDescription, lang='ru'):
    return bonus.get_name(lang)


@register.filter
def get_bonus_description(bonus: flyweights.BonusDescription, lang='ru'):
    return bonus.get_description(lang)


@register.filter
def get_bonus_hints(bonus: flyweights.BonusDescription):
    return bonus.get_hints()


@register.filter
def get_bonus_commands(bonus: flyweights.BonusDescription):
    return bonus.get_commands()


# backgrounds
@register.filter
def get_background_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.backgrounds(), key)


@register.filter
def get_bg_name(bg: flyweights.BackgroundDescription, lang='ru'):
    return bg.get_name(lang)


@register.filter
def get_bg_description(bg: flyweights.BackgroundDescription, lang='ru'):
    return bg.get_description(lang)


@register.filter
def get_bg_hints(bg: flyweights.BackgroundDescription):
    return bg.get_hints()


@register.filter
def get_bg_aptitudes(bg: flyweights.BackgroundDescription):
    return bg.get_aptitudes()


@register.filter
def get_bg_apt_choices(bg: flyweights.BackgroundDescription):
    return bg.get_apt_choices()


@register.filter
def get_bg_skills(bg: flyweights.BackgroundDescription):
    return bg.get_skills()


@register.filter
def get_bg_skill_choices(bg: flyweights.BackgroundDescription):
    return bg.get_skill_choices()


@register.filter
def get_bg_talents(bg: flyweights.BackgroundDescription):
    return bg.get_talents()


@register.filter
def get_bg_talent_choices(bg: flyweights.BackgroundDescription):
    return bg.get_talent_choices()


@register.filter
def get_bg_traits(bg: flyweights.BackgroundDescription):
    return bg.get_traits()


@register.filter
def get_bg_trait_choices(bg: flyweights.BackgroundDescription):
    return bg.get_traits_choices()


@register.filter
def get_bg_equipment(bg: flyweights.BackgroundDescription):
    return bg.get_equipment()


@register.filter
def get_bg_bonus(bg: flyweights.BackgroundDescription):
    return bg.get_bonus()


# roles
@register.filter
def get_role_description_big(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.roles(), key)


@register.filter
def get_role_name(role: flyweights.RoleDescription, lang='ru'):
    return role.get_name(lang)


@register.filter
def get_role_description(role: flyweights.RoleDescription, lang='ru'):
    return role.get_description(lang)


@register.filter
def get_role_hints(role: flyweights.RoleDescription):
    return role.get_hints()


@register.filter
def get_role_aptitudes(role: flyweights.RoleDescription):
    return role.get_aptitudes()


@register.filter
def get_role_apt_choices(role: flyweights.RoleDescription):
    return role.get_apt_choices()


@register.filter
def get_role_talent_choices(role: flyweights.RoleDescription):
    return role.get_talent_choices()


@register.filter
def get_role_bonus(role: flyweights.RoleDescription):
    return role.get_bonus()


# elite advances
@register.filter
def get_elite_advance(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.elite_advances(), key)


@register.filter
def get_ea_name(ea: flyweights.EliteAdvance, lang='ru'):
    return ea.get_name(lang)


@register.filter
def get_ea_description(ea: flyweights.EliteAdvance, lang='ru'):
    return ea.get_description(lang)


@register.filter
def get_ea_hints(ea: flyweights.EliteAdvance):
    return ea.get_hints()


@register.filter
def get_ea_cost(ea: flyweights.EliteAdvance):
    return ea.cost()


@register.filter
def get_ea_prerequisites(ea: flyweights.EliteAdvance):
    return ea.prerequisites()


@register.filter
def get_ea_commands(ea: flyweights.EliteAdvance):
    return ea.commands()


@register.filter
def get_divination_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.divinations(), key)


@register.filter
def get_div_name(div: flyweights.DivinationDescription, lang: str = 'ru'):
    return div.get_name(lang)


@register.filter
def get_div_description(div: flyweights.DivinationDescription, lang: str = 'ru'):
    return div.get_description(lang)


@register.filter
def get_div_hints(div: flyweights.DivinationDescription):
    return div.get_hints()


@register.filter
def get_div_commands(div: flyweights.DivinationDescription):
    return div.get_commands()


@register.filter
def get_div_roll_range(div: flyweights.DivinationDescription):
    return div.get_roll_range()


@register.filter
def get_stat_short(facade: flyweights.Facade, key: str):
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
    return character.skills().get(sk_tag).get_subskill_advance(subskill)


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
def get_short_stat(facade: flyweights.Facade, stat: str):
    return facade.stat_shorts().get(stat)


@register.filter
def get_short_stat_name(short: Dict[str, str], lang: str = 'ru'):
    return short.get(lang)
