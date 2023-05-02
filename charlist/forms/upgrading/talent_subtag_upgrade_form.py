from django import forms
from django.forms import Form


class TalentUpgradeSubtagForm(Form):
    def __init__(self, tl_tag: str, subtag: str, cost: int, available: bool, taken: int = -1, *args, **kwargs):
        super(TalentUpgradeSubtagForm, self).__init__(*args, **kwargs)
        self.__tl_tag = tl_tag
        self.__subtag = subtag
        self.__cost = cost
        self.__taken = taken
        self.available = available
        if subtag == 'TL_ANY':
            self.fields['subtag'] = forms.CharField(max_length=100, min_length=1)

    def tl_tag(self):
        return self.__tl_tag

    def subtag(self):
        return self.__subtag

    def cost(self):
        return self.__cost

    def taken(self):
        return self.__taken

    def is_stackable(self):
        return self.__taken > 0

    def new_taken(self):
        return self.__taken + 1
