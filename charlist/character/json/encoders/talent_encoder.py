# -*- coding: utf-8 -*-

import json

from django.core.serializers.json import DjangoJSONEncoder

from charlist.character.talent import Talent


class TalentEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Talent):
            return json.dumps(obj)
        return super().default(obj)
