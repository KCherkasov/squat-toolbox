from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class DecreaseStatAltForm(Form):
    def __init__(self, cmd: dict, flyweights: Facade, *args, **kwargs):
        super(DecreaseStatAltForm, self).__init__(*args, **kwargs)
        choices = [(cmd.get('tag1'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en()),
                   (cmd.get('tag2'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en())]
        self.fields['choices'].choices = choices
        self.__amount = cmd.get('amount')
        self.__cmd_id = cmd.get('cmd_id')

    def amount(self):
        return self.__amount

    def cmd_id(self):
        return self.__cmd_id

    choices = forms.ChoiceField(label=u'Выберите характеристику, которая будет уменьшена')
