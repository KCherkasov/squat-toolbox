from  django import forms
from django.forms import Form

from charlist.flyweights.flyweights import Facade


class GainMalignancyChoiceForm(Form):
    def __init__(self, flyweights: Facade, *args, **kwargs):
        super(GainMalignancyChoiceForm, self).__init__(*args, **kwargs)
        choices = list()
        for key, value in flyweights.malignancies().items():
            choices.append((key, value.get_name_en()))
        self.choices.choices = choices

    choices = forms.ChoiceField(label=u'Выберите малигнацию')
