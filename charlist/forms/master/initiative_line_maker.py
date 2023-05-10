from django import forms
from django.forms import Form

from charlist.constants.tags import *


INITIATIVE_STATS = [ST_AGILITY, ST_INTELLIGENCE, ST_PERCEPTION]


class InitiativeLineMaker(Form):
    def __init__(self, characters, facade, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = list()
        self.group_names = dict()
        for stat in INITIATIVE_STATS:
            choices.append((stat, facade.stat_descriptions().get(stat).get_name('en')))
        for character in characters:
            roll_field = 'roll-c-' + str(character.pk)
            stat_field = 'stat-c-' + str(character.pk)
            group = 'c-' + str(character.pk)
            self.group_names[group] = character.data_to_model().name()
            self.fields[roll_field] = forms.IntegerField(min_value=1, max_value=25,
                                                         label=u'Бросок на инициативу (со всеми модификаторами)')
            self.fields[roll_field].group = group
            self.fields[stat_field] = forms.ChoiceField(label=u'Характеристика, от которой сделан бросок')
            self.fields[stat_field].choices = choices
            self.fields[stat_field].group = group
        self.group_names['prompt'] = u'Другие участники боя (имя-бросок-параметр, от которого бросали)'
        self.fields['prompt'] = forms.CharField(max_length=3000, label=u'NPC, враги и прочие, угодившие в замес')
