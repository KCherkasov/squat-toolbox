from django import forms
from django.forms import Form


class GainMalignancyRollForm(Form):
    def __init__(self, cmd=None, *args, **kwargs):
        super(GainMalignancyRollForm, self).__init_(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    roll_result = forms.IntegerField(min_value=1, max_value=100, required=False,
                                     label=u'Результат броска на малигнацию')
