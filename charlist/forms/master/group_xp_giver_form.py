from django import forms
from django.forms import Form

from charlist.models import Character, CharacterGroup


class GroupXPGiverForm(Form):
    def __init__(self, group: CharacterGroup, *args, **kwargs):
        super().__init__(*args, **kwargs)
        group_members = Character.objects.by_group(group)
        self.fields['amount'] = forms.IntegerField(min=1, max=10000, label=u'Сколько опыта дать')
        self.fields['amount'].group = 'how-many'
        for character in group_members:
            field_name = 'c' + str(character.id)
            self.fields[field_name] = forms.BooleanField(label=character.data_to_model().name(), required=False)
            self.fields[field_name].group = 'to-whom'
        self.fields['all'] = forms.BooleanField(label=u'Всем', required=False)
        self.fields['all'].group = 'to-whom'
        self.group_names = {'how-many': u'Сколько', 'to-whom': u'Кому'}

