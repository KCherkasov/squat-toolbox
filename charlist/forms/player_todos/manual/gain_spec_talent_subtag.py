from django import forms
from django.forms import Form


class GainSpecTalentForm(Form):
    def __init__(self, flyweights, cmd: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sk_tag = cmd.get('tag')
        self.cmd_id = cmd.get('cmd_id')
        self.tl_name = flyweights.talent_descriptions().get(cmd.get('tag')).name().get('en')

    subtag = forms.CharField(max_length=100, label=u'Специализация')
