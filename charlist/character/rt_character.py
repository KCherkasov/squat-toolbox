# -*- coding: utf-8 -*-
import json

from charlist.character.helpers import *
from charlist.character.skill import Skill
from charlist.character.stat import Stat
from charlist.character.talent import Talent
from charlist.character.trait import Trait
from charlist.flyweights.rt_flyweights import RTFacade

SKILL_POINTS_PER_UPG = 10

UNTRAINED_SKILL = -20

SKILL_UPGRADES_CAP = 4

CURRENT_ID = 0
CAP_ID = 1
SPENT_ID = 1


class RTCharacterModel(object):
    def __init__(self, cid: int, squad_id: int, name: str,
                 hw_id: str, birthright: str, lure_id: str,
                 trial_id: str, motivation_id: str, career_id: str,
                 div_id: str, ea_id: List[str], wounds: List[int],
                 fatigue: List[int], xp: List[int], fate: List[int],
                 insanity: int, corruption: int, pr: int,
                 apts: List[str], stats: Dict[str, Stat],
                 skills: Dict[str, Skill], talents: Dict[str, Talent],
                 traits: Dict[str, Trait], psy: List[str], equipment: List[str],
                 disorders: List[str], malignancies: List[str],
                 mutations: List[str], pending: List[Dict], completed: List[str],
                 used_stats: List[str], cp_tests: int, ip_tests: int, cmd_count: int = 0):
        self.__cid = cid
        self.__squad_id = squad_id
        self.__name = name
        self.__hw_id = hw_id
        self.__birthright = birthright
        self.__lure_id = lure_id
        self.__trial_id = trial_id
        self.__motivation_id = motivation_id
        self.__career_id = career_id
        self.__div_id = div_id
        self.__ea_id = ea_id
        self.__wounds = wounds
        self.__fatigue = fatigue
        self.__xp = xp
        self.__fate = fate
        self.__insanity = insanity
        self.__corruption = corruption
        self.__pr = pr
        self.__apts = apts
        self.__stats = stats
        self.__skills = skills
        self.__talents = talents
        self.__traits = traits
        self.__psy = psy
        self.__equipment = equipment
        self.__disorders = disorders
        self.__malignancies = malignancies
        self.__mutations = mutations
        self.__pending = pending
        self.__completed = completed
        self.__used_stats = used_stats
        self.__cp_tests = cp_tests
        self.__ip_tests = ip_tests
        self.__cmd_count = cmd_count

    def is_rt(self):
        return True

    def id(self):
        return self.__cid

    def squad_id(self):
        return self.__squad_id

    def name(self):
        return self.__name

    def hw_id(self):
        return self.__hw_id

    def birthright(self):
        return self.__birthright

    def lure_id(self):
        return self.__lure_id

    def trial_id(self):
        return self.__trial_id

    def motivation_id(self):
        return self.__motivation_id

    def career_id(self):
        return self.__career_id

    def div_id(self):
        return self.__div_id

    def ea_id(self):
        return self.__ea_id

    def has_ea_id(self, ea_id: str):
        return ea_id in self.__ea_id

    def gain_ea_id(self, ea_id: str):
        if not self.has_ea_id(ea_id):
            self.__ea_id.append(ea_id)

    def wounds(self):
        return self.__wounds

    def wounds_cap(self):
        return self.__wounds[CAP_ID]

    def wounds_current(self):
        return self.__wounds[CURRENT_ID]

    def damage(self, dmg: int):
        if dmg > 0:
            self.__wounds[CURRENT_ID] -= dmg
            return True
        else:
            return False

    def heal(self, hld: int):
        if hld > 0:
            self.__wounds[CURRENT_ID] += hld
            if self.__wounds[CURRENT_ID] > self.__wounds[CAP_ID]:
                self.__wounds[CURRENT_ID] = self.__wounds[CAP_ID]
            return True
        else:
            return False

    def fatigue(self):
        return self.__fatigue

    def fatigue_cap(self):
        return self.__fatigue[CAP_ID]

    def fatigue_current(self):
        return self.__fatigue[CURRENT_ID]

    def add_fatigue(self, amount: int):
        if amount > 0:
            self.__fatigue[CURRENT_ID] += amount
            return True
        else:
            return False

    def remove_fatigue(self, amount: int):
        if amount > 0:
            self.__fatigue[CURRENT_ID] -= amount
            return True
        else:
            return False

    def xp(self):
        return self.__xp

    def xp_current(self):
        return self.__xp[CURRENT_ID]

    def xp_spent(self):
        return self.__xp[SPENT_ID]

    def spend_xp(self, amount: int):
        if amount > self.__xp[CURRENT_ID]:
            return False
        else:
            self.__xp[CURRENT_ID] -= amount
            self.__xp[SPENT_ID] += amount
            return True

    def get_xp(self, amount: int):
        if amount > 0:
            self.__xp[CURRENT_ID] += amount
            return True
        else:
            return False

    def xp_total(self):
        return self.__xp[CURRENT_ID] + self.__xp[SPENT_ID]

    def fate(self):
        return self.__fate

    def fate_current(self):
        return self.__fate[CURRENT_ID]

    def fate_cap(self):
        return self.__fate[CAP_ID]

    def spend_fate(self):
        if self.__fate[CURRENT_ID] > 0:
            self.__fate[CURRENT_ID] -= 1
            return True
        else:
            return False

    def burn_fate(self):
        if self.__fate[CAP_ID] > 0:
            self.__fate[CAP_ID] -= 1
            if self.__fate[CURRENT_ID] > self.__fate[CAP_ID]:
                self.__fate[CAP_ID] = self.__fate[CURRENT_ID]
            return True
        else:
            return False

    def restore_fate(self):
        self.__fate[CURRENT_ID] = self.__fate[CAP_ID]

    def gain_fate(self, amount: int):
        if amount > 0:
            self.__fate[CAP_ID] += amount

    def insanity(self):
        return self.__insanity

    def insanity_bonus(self):
        return self.__insanity // 10

    def insanity_residue(self):
        return self.__insanity % 10

    # TODO: rework for the case when single gain changes bonus more than on 1
    def gain_insanity(self, amount: int):
        if amount > 0:
            old_bonus = self.insanity_bonus()
            self.__insanity += amount
            if (self.insanity_bonus() > self.ip_tests()) and (self.insanity_bonus() > old_bonus):
                for i in range(self.ip_tests() + 1, self.insanity_bonus() + 1):
                    if (i % 4 == 0) or (i % 6 == 0):
                        self.__pending.append({"command": "GainDisorderIP"})
                    else:
                        self.__pending.append({"command": "GainTraumaIP"})

    def remove_insanity(self, amount: int):
        if amount > 0:
            self.__insanity -= amount
            if self.__insanity < 0:
                self.__insanity = 0

    def corruption(self):
        return self.__corruption

    def corruption_bonus(self):
        return self.__corruption // 10

    def corruption_residue(self):
        return self.__corruption % 10

    # TODO: rework for the case when single gain changes bonus more than on 1
    def gain_corruption(self, amount: int):
        if amount > 0:
            old_bonus = self.corruption_bonus()
            self.__corruption += amount
            if (self.corruption_bonus() > self.cp_tests()) and (self.corruption_bonus() > old_bonus):
                for i in range(self.cp_tests() + 1, self.corruption_bonus() + 1):
                    if i % 3 == 0:
                        self.__pending.append({"command": "GainMutationRollCP"})
                    else:
                        self.__pending.append({"command": "GainMalignancyRollCP"})

    def remove_corruption(self, amount: int):
        if amount > 0:
            self.__corruption -= amount
            if self.__corruption < 0:
                self.__corruption = 0

    def pr(self):
        return self.__pr

    def gain_pr(self):
        self.__pr += 1

    def aptitudes(self):
        return self.__apts

    def add_apt(self, apt: str):
        if (apt != '') and not (apt in self.__apts):
            self.__apts.append(apt)

    def stats(self):
        return self.__stats

    def upgrade_stat(self, stat: str):
        if stat in self.__stats.keys():
            if self.__stats.get(stat).is_upgradeable():
                self.__stats.get(stat).upgrade()

    def improve_stat(self, stat: str, amount: int):
        if (stat in self.__stats.keys()) and (amount > 0):
            self.__stats.get(stat).improve(amount)

    def damage_stat(self, stat: str, amount: int):
        if (stat in self.__stats.keys()) and (amount > 0):
            self.__stats.get(stat).damage(amount)

    def skills(self):
        return self.__skills

    def improve_skill(self, sk_tag: str):
        if sk_tag in self.__skills.keys():
            if self.__skills.get(sk_tag).upgradeable():
                self.__skills.get(sk_tag).upgrade()
        else:
            self.__skills[sk_tag] = Skill(sk_tag, 1)

    def improve_skill_subtag(self, sk_tag: str, sk_subtag: str, facade):
        if sk_tag in self.__skills.keys():
            if self.__skills.get(sk_tag).upgradeable_subtag(sk_subtag):
                self.__skills.get(sk_tag).upgrade_subtag(sk_subtag)
        else:
            if facade.skill_descriptions().get(sk_tag).is_specialist():
                skill = Skill(sk_tag, {sk_subtag: 1})
                self.__skills[sk_tag] = skill

    def get_skill_diff(self, sk_tag: str, stat: str):
        if (sk_tag not in self.__skills.keys()) or (stat not in self.__stats.keys()):
            return None
        diff = self.__stats.get(stat).value() + self.__skills.get(sk_tag).get_adv_bonus()
        return diff

    def get_subskill_diff(self, sk_tag: str, subskill: str, stat: str):
        if (sk_tag not in self.__skills.keys()) \
                or (subskill not in self.__skills.get(sk_tag).advances().keys()) \
                or (stat not in self.__stats.keys()):
            return None
        diff = self.__stats.get(stat).value() + self.__skills.get(sk_tag).get_adv_bonus_subtag(subskill)
        return diff

    def has_skill(self, sk_tag: str, adv=1):
        return (sk_tag in self.__skills.keys()) and (self.__skills.get(sk_tag).advances() >= adv)

    def has_subskill(self, sk_tag: str, sk_subtag: str, adv=1):
        return (sk_tag in self.__skills.keys()) and (self.__skills.get(sk_tag).get_subskill_advance(sk_subtag) >= adv)

    def talents(self):
        return self.__talents

    def gain_talent(self, tl_tag: str, facade):
        if tl_tag in facade.talent_descriptions().keys():
            if not facade.talent_descriptions().get(tl_tag).is_specialist():
                if tl_tag not in self.__talents.keys():
                    talent = Talent(tl_tag, 1)
                    self.__talents[tl_tag] = talent
                elif facade.talent_descriptions().get(tl_tag).is_stackable():
                    self.__talents.get(tl_tag).take(facade)

    def gain_talent_subtag(self, tl_tag: str, tl_subtag: str, facade):
        if tl_tag in facade.talent_descriptions().keys():
            if facade.talent_descriptions().get(tl_tag).is_specialist():
                if tl_tag in self.__talents.keys():
                    self.__talents.get(tl_tag).take_subtag(facade, tl_subtag)
                else:
                    talent = Talent(tl_tag, {tl_subtag: 1})
                    self.__talents[tl_tag] = talent

    def has_talent(self, tl_tag: str):
        return tl_tag in self.__talents.keys()

    def has_talent_subtag(self, tl_tag: str, tl_subtag: str):
        return (tl_tag in self.__talents.keys()) and (self.__talents.get(tl_tag).taken_subtag(tl_subtag) > 0)

    def traits(self):
        return self.__traits

    def gain_trait(self, tr_tag: str, facade):
        if tr_tag in facade.trait_descriptions().keys():
            if tr_tag in self.__traits.keys():
                self.__traits.get(tr_tag).take(facade)
            else:
                trait = Trait(tr_tag, 1)
                self.__traits[tr_tag] = trait

    def gain_trait_subtag(self, tr_tag: str, tr_subtag: str, facade):
        if tr_tag in facade.trait_descriptions().keys():
            if facade.trait_descriptions().get(tr_tag).is_specialist():
                if tr_tag in self.__traits.keys():
                    self.__traits.get(tr_tag).take_subtag(facade, tr_subtag)
                else:
                    trait = Trait(tr_tag, {tr_subtag: 1})
                    self.__traits[tr_tag] = trait

    def has_trait(self, tr_tag: str):
        return tr_tag in self.__traits.keys()

    def has_trait_subtag(self, tr_tag: str, tr_subtag: str):
        return (tr_tag in self.__traits.keys()) and (self.__traits.get(tr_tag).taken_subtag(tr_subtag))

    def psy_powers(self):
        return self.__psy

    def equipment(self):
        return self.__equipment

    def disorders(self):
        return self.__disorders

    def malignances(self):
        return self.__malignancies

    def mutations(self):
        return self.__mutations

    def pending(self):
        return self.__pending

    def completed(self):
        return self.__completed

    def used_stats(self):
        return self.__used_stats

    def cp_tests(self):
        return self.__cp_tests

    def inc_cp_tests(self):
        self.__cp_tests += 1

    def ip_tests(self):
        return self.__ip_tests

    def inc_ip_tests(self):
        self.__ip_tests += 1

    def cmd_count(self):
        return self.__cmd_count

    def inc_cmd_count(self):
        self.__cmd_count += 1

    def half_move(self):
        return self.__stats['ST_AG'].bonus()

    def full_move(self):
        if self.has_talent('TL_SPRN'):
            return self.__stats['ST_AG'].bonus() * 3
        return self.__stats['ST_AG'].bonus() * 2

    def charge(self):
        if self.has_talent('TL_PRSP'):
            return self.run()
        return self.__stats['ST_AG'].bonus() * 3

    def run(self):
        return self.__stats['ST_AG'].bonus() * 6

    # TODO - add psy powers!!!

    def make_hookups(self, facade: RTFacade):
        hookups = dict()
        hw_name = dict()
        for lang in ['ru', 'en']:
            hw_name[lang] = facade.rt_homeworlds().get(self.__hw_id).get_bonus().get_name(lang)
        map_hints(hookups, facade.rt_homeworlds().get(self.__hw_id).get_bonus().get_hints(), hw_name)
        trial_name = dict()
        for lang in ['ru', 'en']:
            trial_name[lang] = facade.trials().get(self.__trial_id).name().get(lang)
        map_hints(hookups, facade.trials().get(self.__trial_id).hints(), trial_name)
        motivation_name = dict()
        for lang in ['ru', 'en']:
            motivation_name[lang] = facade.motivations().get(self.__motivation_id).name().get(lang)
        map_hints(hookups, facade.motivations().get(self.__motivation_id).hints(), motivation_name)
        career_name = dict()
        for lang in ['ru', 'en']:
            career_name[lang] = facade.careers().get(self.__career_id).name().get(lang)
        map_hints(hookups, facade.careers().get(self.__career_id).hints(), career_name)
        div_name = dict()
        for lang in ['ru', 'en']:
            div_name[lang] = facade.divinations().get(self.__div_id).get_name(lang)
        map_hints(hookups, facade.divinations().get(self.__div_id).get_hints(), div_name)
        for tl_tag in self.__talents.keys():
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.talent_descriptions().get(tl_tag).get_name(lang)
            map_hints(hookups, facade.talent_descriptions().get(tl_tag).get_hints(), tmp_name)
        for tr_tag in self.__traits.keys():
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.trait_descriptions().get(tr_tag).get_name(lang)
            map_hints(hookups, facade.trait_descriptions().get(tr_tag).get_hints(), tmp_name)
        for malign in self.__malignancies:
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.malignancies().get(malign).get_name(lang)
            map_hints(hookups, facade.malignancies().get(malign).get_hints(), tmp_name)
        for mutation in self.__mutations:
            tmp_name = dict()
            for lang in ['ru', 'en']:
                tmp_name[lang] = facade.mutations().get(mutation).get_name(lang)
            map_hints(hookups, facade.mutations().get(mutation).get_hints(), tmp_name)
        return hookups

    def make_upg_costs(self, flyweights: RTFacade):
        upg_costs = {'stats': {}, 'skills': {}, 'talents': {}}

        for st_tag, stat in self.stats().items():
            if stat.is_upgradeable():
                apts = flyweights.count_stat_apt_matches(st_tag, self.aptitudes())
                colour = 'success'
                if apts == 1:
                    colour = 'warning'
                if apts == 0:
                    colour = 'danger'
                upg_costs.get('stats')[st_tag] = {'cost': flyweights.stat_upg_cost(
                    stat.get_upgrades() + 1, apts), 'colour': colour}

        for sk_tag, skill in self.skills().items():
            apts = flyweights.count_skill_apt_matches(sk_tag, self.aptitudes())
            colour = 'success'
            if apts == 1:
                colour = 'warning'
            if apts == 0:
                colour = 'danger'
            if skill.is_specialist():
                upg_costs.get('skills')[sk_tag] = dict()
                upg_costs.get('skills').get(sk_tag)['colour'] = colour
                for subtag, adv in skill.advances().items():
                    if skill.upgradeable_subtag(subtag):
                        upg_costs.get('skills').get(sk_tag)[subtag] = flyweights.skill_upg_cost(
                            skill.get_subskill_advance(subtag) + 1, apts)
                upg_costs.get('skills').get(sk_tag)['SK_ANY'] = flyweights.skill_upg_cost(1, apts)
            else:
                if skill.upgradeable():
                    upg_costs.get('skills')[sk_tag] = {'cost': flyweights.skill_upg_cost(
                        skill.advances() + 1, apts), 'colour': colour}
        for sk_tag in flyweights.spec_skills():
            if sk_tag not in upg_costs.get('skills').keys():
                apts = flyweights.count_skill_apt_matches(sk_tag, self.aptitudes())
                colour = 'success'
                if apts == 1:
                    colour = 'warning'
                if apts == 0:
                    colour = 'danger'
                upg_costs.get('skills')[sk_tag] = {'SK_ANY': flyweights.skill_upg_cost(1, apts), 'colour': colour}

        for tl_tag, talent in flyweights.talent_descriptions().items():
            if talent.is_specialist():
                flg = True
                apts = flyweights.count_talent_apt_matches(tl_tag, self.aptitudes())
                colour = 'success'
                cost = flyweights.talent_upg_cost(talent.get_tier(), apts)
                if apts == 1:
                    colour = 'warning'
                if apts == 0:
                    colour = 'danger'
                if not self.has_talent(tl_tag):
                    for prereq in talent.get_prerequisites():
                        if not prereq.matched(self):
                            flg = False
                            break
                if flg:
                    if 'available' not in upg_costs.get('talents').keys():
                        upg_costs.get('talents')['available'] = dict()
                    if talent.get_tier() not in upg_costs.get('talents').get('available').keys():
                        upg_costs.get('talents').get('available')[talent.get_tier()] = dict()
                    upg_costs.get('talents').get('available').get(talent.get_tier())[tl_tag] = dict()
                    upg_costs.get('talents').get('available').get(talent.get_tier()).get(tl_tag)['colour'] = colour
                    if self.has_talent(tl_tag):
                        if talent.is_stackable():
                            for subtag in self.talents().get(talent.tag()).taken().keys():
                                upg_costs.get('talents').get('available').get(talent.get_tier()).get(tl_tag)[subtag] = \
                                    cost
                    upg_costs.get('talents').get('available').get(talent.get_tier()).get(tl_tag)['TL_ANY'] = cost
                else:
                    if 'unavailable' not in upg_costs.get('talents').keys():
                        upg_costs.get('talents')['unavailable'] = dict()
                    if talent.get_tier() not in upg_costs.get('talents').get('unavailable').keys():
                        upg_costs.get('talents').get('unavailable')[talent.get_tier()] = dict()
                    upg_costs.get('talents').get('unavailable').get(talent.get_tier())[tl_tag] = dict()
                    upg_costs.get('talents').get('unavailable').get(talent.get_tier()).get(tl_tag)['colour'] = colour
                    if self.has_talent(tl_tag):
                        if talent.is_stackable():
                            for subtag in self.talents().get(talent.tag()).taken().keys():
                                upg_costs.get('talents').get('unavailable') \
                                    .get(talent.get_tier()).get(tl_tag)[subtag] = cost
                    upg_costs.get('talents').get('unavailable').get(talent.get_tier()).get(tl_tag)['TL_ANY'] = cost
            else:
                if (not self.has_talent(tl_tag)) or (talent.is_stackable()):
                    flg = True
                    apts = flyweights.count_talent_apt_matches(tl_tag, self.aptitudes())
                    colour = 'success'
                    cost = flyweights.talent_upg_cost(talent.get_tier(), apts)
                    if apts == 1:
                        colour = 'warning'
                    if apts == 0:
                        colour = 'danger'
                    if not self.has_talent(tl_tag):
                        for prereq in talent.get_prerequisites():
                            if not prereq.matched(self):
                                flg = False
                                break
                    if flg:
                        if 'available' not in upg_costs.get('talents').keys():
                            upg_costs.get('talents')['available'] = dict()
                        if talent.get_tier() not in upg_costs.get('talents').get('available').keys():
                            upg_costs.get('talents').get('available')[talent.get_tier()] = dict()
                        upg_costs.get('talents').get('available').get(talent.get_tier())[tl_tag] = \
                            {'cost': cost, 'colour': colour}
                    else:
                        if 'unavailable' not in upg_costs.get('talents').keys():
                            upg_costs.get('talents')['unavailable'] = dict()
                        if talent.get_tier() not in upg_costs.get('talents').get('unavailable').keys():
                            upg_costs.get('talents').get('unavailable')[talent.get_tier()] = dict()
                        upg_costs.get('talents').get('unavailable').get(talent.get_tier())[tl_tag] = \
                            {'cost': cost, 'colour': colour}

        if self.has_ea_id('EA_PSY'):
            upg_costs['pr'] = flyweights.pr_upg_cost(self.pr() + 1)
            upg_costs['psy'] = {'available': dict(), 'unavailable': dict()}
            for psy_tag, psy_power in flyweights.psy_powers().items():
                if psy_tag not in self.psy_powers():
                    flg = True
                    for prereq in psy_power.prerequisites():
                        if not prereq.matched(self):
                            flg = False
                            break
                    if flg:
                        if psy_power.school() not in upg_costs.get('psy').get('available').keys():
                            upg_costs.get('psy').get('available')[psy_power.school()] = dict()
                        upg_costs.get('psy').get('available').get(psy_power.school())[psy_tag] = psy_power.cost()
                    else:
                        if psy_power.school() not in upg_costs.get('psy').get('unavailable').keys():
                            upg_costs.get('psy').get('unavailable')[psy_power.school()] = dict()
                        upg_costs.get('psy').get('unavailable').get(psy_power.school())[psy_tag] = psy_power.cost()

        upg_costs['ea'] = {'available': dict(), 'unavailable': dict()}
        for ea_id, ea in flyweights.elite_advances().items():
            if (ea_id not in self.ea_id()) and (ea_id not in flyweights.bad_eas()):
                flg = True
                for prereq in ea.prerequisites():
                    if not prereq.matched(self):
                        flg = False
                        break
                if flg:
                    upg_costs.get('ea').get('available')[ea_id] = ea.cost()
                else:
                    upg_costs.get('ea').get('unavailable')[ea_id] = ea.cost()
        return upg_costs

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        if 'cp_teste_passed' in data.keys():
            data['cp_tests'] = data['cp_teste_passed']
            data.pop('cp_teste_passed', 0)
        if 'ip_tests_passed' in data.keys():
            data['ip_tests'] = data['ip_tests_passed']
            data.pop('ip_tests_passed', 0)
        stats = dict()
        for stat_key, stat in data['stats'].items():
            stats[stat_key] = Stat.from_json(stat)
        data['stats'] = stats
        skills = dict()
        for skill_key, skill in data['skills'].items():
            skills[skill_key] = Skill.from_json(skill)
        data['skills'] = skills
        talents = dict()
        for talent_key, talent in data['talents'].items():
            talents[talent_key] = Talent.from_json(talent)
        data['talents'] = talents

        traits = dict()
        for trait_key, trait in data['traits'].items():
            traits[trait_key] = Trait.from_json(trait)
        data['traits'] = traits
        return cls(**data)

    def toJSON(self):
        fields_preset = self.__dict__
        fields = dict()
        spec_fields = ['stats', 'skills', 'talents', 'traits']
        for key, val in fields_preset.items():
            field_key = key[19:]
            if field_key == 'ea_id':
                if not isinstance(val, list):
                    if val == -1:
                        fields[field_key] = list()
            if field_key == 'cp_teste_passed':
                field_key = 'cp_tests'
                fields[field_key] = val
            if field_key == 'ip_tests_passed':
                field_key = 'ip_tests'
                fields[field_key] = val
            if field_key in spec_fields:
                if field_key == 'stats':
                    stats = dict()
                    for skey, sval in self.stats().items():
                        stats[skey] = sval.toJSON()
                    fields['stats'] = stats
                if field_key == 'skills':
                    skills = dict()
                    for skey, sval in self.skills().items():
                        skills[skey] = sval.toJSON()
                    fields['skills'] = skills
                if field_key == 'talents':
                    talents = dict()
                    for tkey, tval in self.talents().items():
                        talents[tkey] = tval.toJSON()
                    fields['talents'] = talents
                if field_key == 'traits':
                    traits = dict()
                    for tkey, tval in self.traits().items():
                        traits[tkey] = tval.toJSON()
                    fields['traits'] = traits
            else:
                fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=4)
