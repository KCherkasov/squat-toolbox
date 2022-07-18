# -*- coding: utf-8 -*-


from typing import Dict, List

from charlist.flyweights.flyweights import Facade
from charlist.flyweights.core.hint import Hint

TALENT_PREFIX = 'TL'
TRAIT_PREFIX = 'TR'
HOMEWORLD_PREFIX = 'HW'
BACKGROUND_PREFX = 'BG'
ROLE_PREFIX = 'RL'
ELITE_ADVANCE_PREFIX = 'EA'
DIVINATION_PREFIX = 'D_'

PARSE_TAG = '$'


class HookupHint(object):
    def __init__(self, tag: str, description: Dict[str, str], talent_name: Dict[str, str]):
        self.tag = tag
        self.description = description
        self.talent_name = talent_name


def needs_parsing(hint: Hint):
    for lang in ['ru', 'en']:
        descr = hint.get_description(lang)
        if PARSE_TAG not in descr:
            return False
    return True


def parse_hint(hint: Hint, facade: Facade):
    parsed = dict()
    tag = hint.get_tag()[:-3]
    owner = None
    if tag[:2] == TALENT_PREFIX:
        owner = facade.talent_descriptions().get(tag)
    elif tag[:2] == TRAIT_PREFIX:
        owner = facade.trait_descriptions().get(tag)
    elif tag[:2] == HOMEWORLD_PREFIX:
        owner = facade.homeworlds().get(tag).get_bonus()
    elif tag[:2] == BACKGROUND_PREFX:
        owner = facade.backgrounds().get(tag).get_bonus()
    elif tag[:2] == ELITE_ADVANCE_PREFIX:
        owner = facade.elite_advances().get(tag)
    elif tag[:2] == DIVINATION_PREFIX:
        owner = facade.divinations().get(tag)
    if owner is not None:

        return parsed
    else:
        return None


def map_hints(res: Dict[str, List[HookupHint]], hints: List[Hint], name: Dict[str, str], facade: Facade):
    for hint in hints:
        for tgt in hint.get_target():
            if tgt not in res.keys():
                res[tgt] = list()
            hook_description = dict()
            if needs_parsing(hint):
                hook_description = parse_hint(hint, facade)
            else:
                for lang in ['ru', 'en']:
                    hook_description[lang] = hint.get_description(lang)
            hook_hint = HookupHint(hint.get_tag(), hook_description, name)
            res.get(tgt).append(hook_hint)
