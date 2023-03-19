from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class IncreaseStatAltForm(Form):
    def __init__(self, cmd: dict, flyweights: Facade, *args, **kwargs):
        super(IncreaseStatAltForm, self).__init__(*args, **kwargs)
        self.__cmd_id = cmd.get('cmd_id')
        choices = [(cmd.get('tag1'), flyweights.stat_descriptions().get(cmd.get('tag1')).get_name_en()),
                   (cmd.get('tag2'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en())]
        self.__amount = cmd.get('amount')
        self.fields['choices'].choices = choices

    def cmd_id(self):
        return self.__cmd_id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    def amount(self):
        return self.__amount

    choices = forms.ChoiceField(label=u'Выберите характеристику, которая будет увеличена')
