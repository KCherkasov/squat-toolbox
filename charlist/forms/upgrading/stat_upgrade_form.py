from django.forms import Form
from django import forms


class StatUpgradeForm(Form):
    def __init__(self, stat_tag: str, stat_value: int, cost: int, colour: str, *args, **kwargs):
        super(StatUpgradeForm, self).__init__(*args, **kwargs)
        self.__stat_tag = stat_tag
        self.__stat_value = stat_value
        self.__cost = cost
        self.__colour = colour

    def stat_tag(self):
        return self.__stat_tag

    def stat_value(self):
        return self.__stat_value

    def stat_value_new(self):
        return self.__stat_value + 5

    def cost(self):
        return self.__cost

    def colour(self):
        return self.__colour
