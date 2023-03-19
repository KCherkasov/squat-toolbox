from django import forms
from django.forms import Form


class GainCorruptionRollForm(Form):
    def __init__(self, cmd=None, *args, **kwargs):
        super().__init__(GainCorruptionRollForm, self).__init__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    roll_value = forms.IntegerField(min_value=1, max_value=100, label=u'Очки Порчи')

