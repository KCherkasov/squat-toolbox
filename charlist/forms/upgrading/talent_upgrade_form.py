from django import forms
from django.forms import Form


class TalentUpgradeForm(Form):
    def __init__(self, tl_tag: str, cost: int, colour: str, taken: int = -1, *args, **kwargs):
        super(TalentUpgradeForm, self).__init__(*args, **kwargs)
        self.__tl_tag = tl_tag
        self.__cost = cost
        self.__colour = colour
        self.__taken = taken

    def tl_tag(self):
        return self.__tl_tag

    def cost(self):
        return self.__cost

    def colour(self):
        return self.__colour

    def taken(self):
        return self.__taken

    def is_stackable(self):
        return self.__taken > 0

    def new_taken(self):
        return self.__taken + 1
