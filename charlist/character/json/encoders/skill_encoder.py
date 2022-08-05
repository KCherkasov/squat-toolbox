# -*- coding: utf-8 -*-

import json
from django.core.serializers.json import DjangoJSONEncoder
from charlist.character.skill import Skill


class SkillEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Skill):
            return json.dumps(obj)
        return super().default(obj)
