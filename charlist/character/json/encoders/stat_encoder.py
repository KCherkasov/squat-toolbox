# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder

from charlist.character.stat import Stat


class StatEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Stat):
            return json.dumps(obj)
        return super().default(obj)
