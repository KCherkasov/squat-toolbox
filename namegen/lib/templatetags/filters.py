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


@register.filter
def get_aptitude(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.aptitudes(), key)

@register.filter
def get_apt_name(apt: flyweights.Aptitude, lang='ru'):
    return apt.get_name(lang)


@register.filter
def get_apt_description(apt: flyweights.Aptitude, lang='ru'):
    return apt.get_description(lang)


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
def get_skill_description(facade: flyweights.Facade, key: str):
    return get_by_dict_key(facade.skill_descriptions(), key)
