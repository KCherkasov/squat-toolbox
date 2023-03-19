from django import forms
from django.forms import Form


class GetTraumaIPForm(Form):
    def __int__(self, cmd: dict = None, *args, **kwargs):
        super().__int__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    roll_result = forms.IntegerField(min_value=1, max_value=210, required=False,
                                     label=u'Результат броска на психическую травму')
