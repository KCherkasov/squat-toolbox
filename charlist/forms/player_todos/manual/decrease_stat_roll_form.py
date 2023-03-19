from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class DecreaseStatRollForm(Form):
    def __init__(self, cmd: dict, flyweights: Facade, *args, **kwargs):
        super(DecreaseStatRollForm, self).__init__(*args, **kwargs)
        self.__stat_name = flyweights.stat_descriptions().get(cmd.get('tag')).get_name_en()
        self.__cmd_id = cmd.get('cmd_id')

    def stat_name(self):
        return self.__stat_name

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['cmd_id'] = self.__cmd_id
        return cleaned_data

    roll_value = forms.IntegerField(min_value=1, max_value=10, label=u'Урон характеристике')
