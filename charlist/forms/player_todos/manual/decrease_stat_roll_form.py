from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class DecreaseStatRollForm(Form):
    def __init__(self, cmd: dict, flyweights, *args, **kwargs):
        super(DecreaseStatRollForm, self).__init__(*args, **kwargs)
        self.__stat_name = flyweights.stat_descriptions().get(cmd.get('tag')).get_name_en()
        self.__cmd_id = cmd.get('cmd_id')

    def cmd_id(self):
        return self.__cmd_id

    def stat_name(self):
        return self.__stat_name

    roll_value = forms.IntegerField(min_value=1, max_value=10, label=u'Урон характеристике')
