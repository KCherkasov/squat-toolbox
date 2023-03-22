from django import forms
from django.forms import Form


class SkillSubtagUpgradeForm(Form):
    def __init__(self, sk_tag: str, subtag: str, cost: int, advance: int, *args, **kwargs):
        super(SkillSubtagUpgradeForm, self).__init__(*args, **kwargs)
        self.__sk_tag = sk_tag
        self.__subtag = subtag
        self.__cost = cost
        self.__advance = advance
        if subtag == 'SK_ANY':
            self.fields['subtag'] = forms.CharField(max_length=100, min_length=1, label=u'Новая специализация')

    def skill_tag(self):
        return self.__sk_tag

    def subtag(self):
        return self.__subtag

    def cost(self):
        return self.__cost

    def advance(self):
        return self.__advance
