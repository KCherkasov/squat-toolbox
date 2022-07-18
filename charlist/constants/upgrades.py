# -*- coding: utf-8 -*-
from typing import List

STAT_UPGRADES = [[500, 750, 1000, 1500, 2500], [250, 500, 750, 1000, 1500], [100, 250, 500, 750, 1250]]


SKILL_UPGRADES = [[300, 600, 900, 1200], [200, 400, 600, 800], [100, 200, 300, 400]]


TALENT_UPGRADES = [[600, 900, 1200], [300, 450, 600], [200, 300, 400]]


PR_COST_BASE = 200


def match_aptitudes(ch_apts: List[str], tgt_apts: List[str]):
    res = 0
    for tapt in tgt_apts:
        for capt in ch_apts:
            if tapt == capt:
                res += 1
                break
    if res > 2:
        res = 2
    return res
