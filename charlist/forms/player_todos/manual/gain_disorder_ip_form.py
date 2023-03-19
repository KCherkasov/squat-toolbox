from django import forms
from django.forms import Form


class GainDisorderIPForm(Form):
    def __init__(self, cmd: dict = None, *args, **kwargs):
        super(GainDisorderIPForm, self).__init__(*args, **kwargs)
        self.__cmd_id = -1
        if cmd is not None:
            self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    disorder_description = forms.CharField(max_length=1000, required=False, label=u'Описание психического расстройства')
