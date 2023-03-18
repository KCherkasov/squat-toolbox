from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class IncreaseStatAltForm(Form):
    def __init__(self, cmd, flyweights: Facade, *args, **kwargs):
        super(IncreaseStatAltForm, self).__init__(*args, **kwargs)
        choices = [(cmd.get('tag1'), flyweights.stat_descriptions().get(cmd.get('tag1')).get_name_en()),
                   (cmd.get('tag2'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en())]
        self.__amount = cmd.get('amount')
        self.fields['choices'].choices = choices

    def amount(self):
        return self.__amount

    choices = forms.ChoiceField(label=u'Выберите характеристику, которая будет увеличена')
