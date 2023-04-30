# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder

from charlist.character.character import CharacterModel
from charlist.character.rt_character import RTCharacterModel


class CharacterEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CharacterModel):
            return json.dumps(obj)
        if isinstance(obj, RTCharacterModel):
            return json.dumps(obj)
