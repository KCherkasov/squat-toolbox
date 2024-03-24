# -*- coding: utf-8 -*-

JSON_INDENT = 4

IM_ZERO = 0
IM_ONE = 1
IM_TWO = 2

IM_CUR_ID = 0
IM_CAP_ID = 1
IM_SPENT_ID = 1

IM_DEFAULT_ADVANCE = 0
IM_ADVANCE_STEP = 1

IM_SKILL_ADVANCE = 5
IM_SKILL_ADV_CAP = 4

IM_BASE_STAT = 20
IM_STAT_CAP_HUMAN = 60
IM_STAT_CAP_EXT = 80
IM_STAT_CAP = 100
IM_STAT_ADV_FIVE = 5
IM_STAT_ADV_TEN = 10

IM_D10 = 10
IM_D100 = 100

STAT_UPG_COSTS = {
    25: 20,
    30: 25,
    35: 30,
    40: 40,
    45: 60,
    50: 80,
    55: 110,
    60: 140,
    65: 180,
    70: 220,
    75: 270,
    80: 320
}

RESOURCES_PATH = 'static/json/'

STATS_DESCR_ID = 0
SKILL_DESCR_ID = 1
SPEC_DESCR_ID = 2

MAL_RESOURCES = [
    "im_stat_descriptions.json",
    "im_skill_descriptions.json",
    "im_specialization_descriptions.json"
]

MAL_LANGS = ['ru', 'en']
