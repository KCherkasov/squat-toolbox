# -*- coding: utf-8 -*-

from django import template
from charlist import flyweights

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
