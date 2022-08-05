# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder

from charlist.character.trait import Trait


class TraitEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Trait):
            return json.dumps(obj)
        return super().default(obj)
