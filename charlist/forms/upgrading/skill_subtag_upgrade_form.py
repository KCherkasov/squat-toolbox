from django import forms
from django.forms import Form


class SkillSubtagUpgradeForm(Form):
    def __init__(self, sk_tag: str, subtag: str, cost: int, advance: int, *args, **kwargs):
        super(SkillSubtagUpgradeForm, self).__init__(*args, **kwargs)
        self.__sk_tag = sk_tag
        self.__subtag_skill = subtag
        self.__cost = cost
        self.__advance = advance
        if subtag == 'SK_ANY':
            self.fields['subtag'] = forms.CharField(label=u"Новая специализация", max_length=100, min_length=1)

    def skill_tag(self):
        return self.__sk_tag

    def subtag_skill(self):
        return self.__subtag_skill

    def cost(self):
        return self.__cost

    def advance(self):
        return self.__advance

    def advance_new(self):
        if self.__advance < 0:
            return 0
        else:
            return self.__advance + 10

