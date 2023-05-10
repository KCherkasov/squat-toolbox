from django import forms
from django.forms import Form


class CreateSessionForm(Form):
    def __init__(self, group, characters, is_crossover, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groups = list()
        self.group_descriptions = dict()
        self.group_names = dict()
        if is_crossover:
            self.groups.append(u'Беспартийные_элементы')
            self.group_names[self.groups[0]] = u'Беспартийные элементы'
            self.group_descriptions[self.groups[0]] = 'У них нет совести, нет чести, нет духа коллективизма!'

        self.fields['name'].group = 'bgroup-data'
        self.group_names['bgroup-data'] = u'Параметры сессии'
        self.group_descriptions['bgroup-data'] = u''

        search_area = characters
        if not is_crossover:
            search_area = search_area.objects.by_group(group)

        for character in search_area:
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

    name = forms.CharField(label=u'Название сессии (необязательно)', max_length=100)
