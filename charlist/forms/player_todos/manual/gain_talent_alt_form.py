from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class GainTalentAltForm(Form):
    def __init__(self, cmd: dict, flyweights: Facade, *args, **kwargs):
        super(GainTalentAltForm, self).__init__(*args, **kwargs)
        self.__cmd_id = cmd.get('cmd_id')
        choices = list()
        for tag in cmd.get('tags'):
            choices.append((tag, flyweights.talent_descriptions().get(tag).get_name_en()))
        self.fields['choices'].choices = choices

    def cmd_id(self):
        return self.__cmd_id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    choices = forms.ChoiceField(label=u'Выберите талант')

