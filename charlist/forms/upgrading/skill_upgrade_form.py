from django import forms
from django.forms import Form


class SkillUpgradeForm(Form):
    def __init__(self, sk_tag: str, cost: int, advance: int, colour: str, *args, **kwargs):
        super(SkillUpgradeForm, self).__init__(*args, **kwargs)
        self.__sk_tag = sk_tag
        self.__cost = cost
        self.__advance = advance
        self.__colour = colour

    def skill_tag(self):
        return self.__sk_tag

    def cost(self):
        return self.__cost

    def advance(self):
        return self.__advance

    def advance_new(self):
        if self.__advance < 0:
            return 0
        else:
            return self.__advance + 10

    def colour(self):
        return self.__colour

