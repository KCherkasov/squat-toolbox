from django import forms
from django.forms import Form

from charlist.constants.tags import STAT_APTS


class GainStatAptitudeForm(Form):
    def __init__(self, character, flyweights, cmd: dict = None, *args, **kwargs):
        super(GainStatAptitudeForm, self).__init__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')
        choices = list()
        for key, value in flyweights.aptitudes().items():
            if (key not in character.aptitudes()) and (key in STAT_APTS):
                choices.append((key, value.get_name_en()))
        self.fields['choices'].choices = choices

    def cmd_id(self):
        return self.__cmd_id

    choices = forms.ChoiceField(label=u'Выберите склонность')
