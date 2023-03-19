from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class GainMutationChoiceForm(Form):
    def __init__(self, flyweights: Facade, cmd: dict = None, *args, **kwargs):
        super(GainMutationChoiceForm, self).__init__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')
        choices = list()
        for key, value in flyweights.mutations().items():
            choices.append((key, value.get_name_en()))
        self.fields['choices'].choices = choices

    def cmd_id(self):
        return self.__cmd_id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    choices = forms.ChoiceField(label=u'Выберите мутацию')
