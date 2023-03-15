from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade
from charlist.character.character import CharacterModel
from charlist.constants.tags import STAT_APTS


class GainStatAptitudeForm(Form):
    def __init__(self, character: CharacterModel, flyweights: Facade, *args, **kwargs):
        super(GainStatAptitudeForm, self).__init__(*args, **kwargs)
        choices = list()
        for key, value in flyweights.aptitudes().items():
            if (key not in character.aptitudes()) and (key in STAT_APTS):
                choices.append((key, value.get_name_en()))
        self.choices.choices = choices

    choices = forms.ChoiceField(label=u'Выберите склонность')
