from django import forms
from django.forms import Form


class CreateGroupForm(Form):
    def __init__(self, characters, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.groups = list()
        self.group_descriptions = dict()
        self.groups.append(u'Беспартийные_элементы')
        self.group_names = dict()
        self.group_names[self.groups[0]] = u'Беспартийные элементы'
        self.group_descriptions[self.groups[0]] = 'У них нет совести, нет чести, нет духа коллективизма!'

        self.fields['name'].group = 'group-data'
        self.fields['description'].group = 'group-data'
        self.fields['is_rt'].group = 'group-data'
        self.group_names['group-data'] = u'Параметры группы'
        self.group_descriptions['group-data'] = u''

        for character in characters:
            field_name = 'c' + str(character.pk)
            model = character.data_to_model()
            self.fields[field_name] = forms.BooleanField(label=model.name(), required=False)
            if len(character.groups.all()) > 0:
                for group in character.groups.all():
                    if group.name_id not in self.groups:
                        self.groups.append(group.name_id)
                        self.group_names[self.groups[len(self.groups) - 1]] = group.name
                        self.group_descriptions[self.groups[len(self.groups) - 1]] = group.description
                    self.fields[field_name].group = group.name_id
                    break
            else:
                self.fields[field_name].group = self.groups[0]

    name = forms.CharField(label=u'Название группы', max_length=100)
    description = forms.CharField(label=u'Краткое описание', max_length=100)
    is_rt = forms.BooleanField(label=u'Они будут строить из себя вольников?', required=False)
