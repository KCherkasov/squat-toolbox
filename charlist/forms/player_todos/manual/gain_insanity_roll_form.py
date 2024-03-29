from django import forms
from django.forms import Form


class GainInsanityRollForm(Form):
    def __init__(self, cmd: dict = None, *args, **kwargs):
        super(GainInsanityRollForm, self).__init__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    roll_value = forms.IntegerField(min_value=1, max_value=100, label=u'Очки Безумия')
