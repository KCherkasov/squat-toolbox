# -*- coding: utf-8 -*-

import random

D100 = 100
D10 = 10
D5 = 5


def roll(dice=D100):
    return random.randint(1, dice) + 1


def d100():
    return roll()


def d10():
    return roll(D10)


def d5():
    return roll(D5)
