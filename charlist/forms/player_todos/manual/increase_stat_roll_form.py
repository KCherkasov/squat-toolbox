from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade

class IncreaseStatRollForm(Form):
    def __init__(self, cmd, flyweights: Facade, *args, **kwargs):
        super(IncreaseStatRollForm, self).__init__(*args, **kwargs)
        self.__stat_name = flyweights.stat_descriptions().get(cmd.get('tag')).get_name_en()

    def stat_name(self):
        return self.__stat_name

    roll_value = forms.IntegerField(min_value=1, max_value=10, label=u'Результат броска на увеличение характеристики')
