# -*- coding: utf-8 -*-

from typing import Dict, List



class Prerequisite(object):
    def __init__(self, tag: str, value: int, subtag: List[str] = None, alt: Dict = None):
        self.tag = tag
        self.subtag = subtag
        self.value = value
        self.alt = alt

    def has_subtag(self):
        return not (self.subtag is None)

    def has_alt(self):
        return not (self.alt is None)

    def is_alt_list(self):
        return isinstance(self.alt, list)

    def get_alt_tag(self):
        return self.alt.get('tag')

    def alt_has_subtag(self):
        return 'subtag' in self.alt.keys()

    def get_alt_subtag(self):
        return self.alt.get('subtag')

    def get_alt_value(self):
        return self.alt.get('value')

    def get_alt(self):
        return self.alt

    def is_stat_prereq(self):
        return self.tag[:2] == 'ST'

    def is_skill_prereq(self):
        return self.tag[:2] == 'SK'

    def is_role_prereq(self):
        return (self.tag[:2] == "RL") or (self.tag[:2] == 'CR')

    def is_background_prereq(self):
        return self.tag[:2] == 'BG'

    def is_ea_prereq(self):
        return self.tag[:2] == "EA"

    def is_talent_prereq(self):
        return self.tag[:2] == 'TL'

    def is_trait_prereq(self):
        return self.tag[:2] == 'TR'

    def is_homeworld_prereq(self):
        return self.tag[:2] == 'HW'

    def is_pr_prereq(self):
        return self.tag == 'PR'

    def is_psy_power_prereq(self):
        return self.tag[:2] == 'PP'

    def match_alts(self, character):
        flg = False  # True when prerequisite is NOT matched
        if self.is_alt_list():
            for alt in self.alt:
                flg = False
                alt_tag = alt.get('tag')
                alt_value = alt.get('value')
                if alt_tag[:2] == 'HW':
                    flg = character.hw_id() != alt_tag
                if alt_tag[:2] == 'BG':
                    flg = character.bg_id() != alt_tag
                if (alt_tag[:2] == 'RL') or (alt_tag[:2] == 'CR'):
                    flg = character.role_id() != alt_tag
                if alt_tag[:2] == 'ST':
                    flg = character.stats().get(alt_tag).value() < alt_value
                if alt_tag[:2] == 'SK':
                    if alt_tag in character.skills().keys():
                        skill = character.skills().get(alt_tag)
                        if skill.is_specialist():
                            if 'subtag' in alt.keys():
                                if alt.get('subtag') in skill.advances().keys():
                                    flg = skill.get_adv_bonus_subtag(alt.get('subtag')) < alt_value
                                else:
                                    flg = True
                        else:
                            flg = skill.get_adv_bonus() < alt_value
                    else:
                        flg = True
                if alt_tag[:2] == 'TL':
                    if alt_tag in character.talents().keys():
                        talent = character.talents().get(alt_tag)
                        if talent.is_specialist():
                            if 'subtag' in alt.keys():
                                if alt.get('subtag') in talent.taken().keys():
                                    flg = talent.taken_subtag(alt.get('subtag')) < alt_value
                                else:
                                    flg = True
                        else:
                            flg = talent.taken() < alt_value
                    else:
                        flg = True
                if alt_tag[:2] == 'TR':
                    if alt_tag in character.traits().keys():
                        trait = character.traits().get(alt_tag)
                        if trait.is_specialist():
                            if 'subtag' in alt.keys():
                                if alt.get('subtag') in trait.taken().keys():
                                    flg = trait.taken_subtag(alt.get('subtag')) < alt_value
                                else:
                                    flg = True
                        else:
                            flg = trait.taken() < alt_value
                    else:
                        flg = True
                if alt_tag == 'PR':
                    flg = character.pr() < alt_value
                if alt_tag[:2] == 'PP':
                    flg = alt_tag not in character.psy_powers()
                if alt_tag[:2] == 'EA':
                    flg = alt_tag not in character.ea_id()
                if not flg:
                    return True
            return False
        else:
            alt_tag = self.alt.get('tag')
            alt_value = self.alt.get('value')
            if alt_tag[:2] == 'HW':
                flg = character.hw_id() != alt_tag
            if alt_tag[:2] == 'BG':
                flg = character.bg_id() != alt_tag
            if (alt_tag[:2] == 'RL') or (alt_tag[:2] == 'CR'):
                flg = character.role_id() != alt_tag
            if alt_tag[:2] == 'ST':
                flg = character.stats().get(alt_tag).value() < alt_value
            if alt_tag[:2] == 'SK':
                if alt_tag in character.skills().keys():
                    skill = character.skills().get(alt_tag)
                    if skill.is_specialist():
                        if 'subtag' in self.alt.keys():
                            if self.alt.get('subtag') in skill.advances().keys():
                                flg = skill.get_adv_bonus_subtag(self.alt.get('subtag')) < alt_value
                            else:
                                flg = True
                    else:
                        flg = skill.get_adv_bonus() < alt_value
                else:
                    flg = True
            if alt_tag[:2] == 'TL':
                if alt_tag in character.talents().keys():
                    talent = character.talents().get(alt_tag)
                    if talent.is_specialist():
                        if 'subtag' in self.alt.keys():
                            if self.alt.get('subtag') in talent.taken().keys():
                                flg = talent.taken_subtag(self.alt.get('subtag')) < alt_value
                            else:
                                flg = True
                    else:
                        flg = talent.taken() < alt_value
                else:
                    flg = True
            if alt_tag[:2] == 'TR':
                if alt_tag in character.traits().keys():
                    trait = character.traits().get(alt_tag)
                    if trait.is_specialist():
                        if 'subtag' in self.alt.keys():
                            if self.alt.get('subtag') in trait.taken().keys():
                                flg = trait.taken_subtag(self.alt.get('subtag')) < alt_value
                            else:
                                flg = True
                    else:
                        flg = trait.taken() < alt_value
                else:
                    flg = True
            if alt_tag == 'PR':
                flg = character.pr() < alt_value
            if alt_tag[:2] == 'PP':
                flg = alt_tag not in character.psy_powers()
            if alt_tag[:2] == 'EA':
                flg = alt_tag not in character.ea_id()
            if flg:
                return False
            else:
                return True

    def matched(self, character):
        flg = False  # True when prerequisite is NOT matched
        if self.is_homeworld_prereq():
            flg = character.hw_id() != self.tag
        if self.is_background_prereq():
            flg = character.bg_id() != self.tag
        if self.is_role_prereq():
            flg = character.role_id() != self.tag
        if self.is_stat_prereq():
            flg = character.stats().get(self.tag).value() < self.value
        if self.is_skill_prereq():
            if self.tag in character.skills().keys():
                skill = character.skills().get(self.tag)
                if skill.is_specialist():
                    if self.has_subtag:
                        if isinstance(self.subtag, list):
                            for subtag in self.subtag:
                                if subtag in skill.advances().keys():
                                    flg = skill.get_adv_bonus_subtag(subtag) < self.value
                                    if not flg:
                                        break
                                else:
                                    flg = True
                        else:
                            if self.subtag in skill.advances().keys():
                                flg = skill.get_adv_bonus_subtag(self.subtag) < self.value
                            else:
                                flg = True
                else:
                    flg = skill.get_adv_bonus() < self.value
            else:
                flg = True
        if self.is_talent_prereq():
            if self.tag in character.talents().keys():
                talent = character.talents().get(self.tag)
                if talent.is_specialist():
                    if self.has_subtag():
                        if self.subtag in talent.taken().keys():
                            flg = talent.taken_subtag(self.subtag) < self.value
                        else:
                            flg = True
                else:
                    flg = talent.taken() < self.value
            else:
                flg = True
        if self.is_trait_prereq():
            if self.tag in character.traits().keys():
                trait = character.traits().get(self.tag)
                if trait.is_specialist():
                    if self.has_subtag():
                        if self.subtag in trait.taken().keys():
                            flg = trait.taken_subtag(self.subtag) < self.value
                        else:
                            flg = True
                else:
                    flg = trait.taken() < self.value
            else:
                flg = True
        if self.is_pr_prereq():
            flg = character.pr() < self.value
        if self.is_psy_power_prereq():
            flg = self.tag not in character.psy_powers()
        if self.is_ea_prereq():
            flg = self.tag not in character.ea_id()
            if self.value == 0:
                flg = not flg
        if flg:
            return False
        else:
            if self.has_alt():
                return self.match_alts(character)
            return True

    @classmethod
    def from_json(cls, data):
        return cls(**data)
