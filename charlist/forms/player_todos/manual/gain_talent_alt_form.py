from django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class GainTalentAltForm(Form):
    def __init__(self, cmd, flyweights: Facade, *args, **kwargs):
        super(GainTalentAltForm, self).__init__(*args, **kwargs)
        choices = list()
        for tag in cmd.get('tags'):
            choices.append((tag, flyweights.talent_descriptions().get(tag).get_name_en()))
        self.fields['choices'].choices = choices

    choices = forms.ChoiceField(label=u'Выберите талант')

