from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class DecreaseStatAltForm(Form):
    def __init__(self, cmd, flyweights: Facade, *args, **kwargs):
        super(DecreaseStatAltForm, self).__init__(*args, **kwargs)
        choices = [(cmd.get('tag1'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en()),
                   (cmd.get('tag2'), flyweights.stat_descriptions().get(cmd.get('tag2')).get_name_en())]
        self.fields['choices'].choices = choices
        self.__amount = cmd.get('amount')

    def amount(self):
        return self.__amount

    choices = forms.ChoiceField(label=u'Выберите характеристику, которая будет уменьшена')
