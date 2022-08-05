# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder

from charlist.character.character import CharacterModel


class CharacterEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, CharacterModel):
            return json.dumps(obj)
