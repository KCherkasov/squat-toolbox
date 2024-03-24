# -*- coding: utf-8 -*-
import json

from typing import Dict

from charlist.constants.tags import *
from charlist.constants.maledictum.constants import *


class MalSpecializationDescriptionModel(object):
    def __init__(self, tag: str, name: Dict[str, str],
                 description: Dict[str, str], parent: str,
                 restricted: bool, forbidden: bool):
        self.tag = tag
        self.name = name
        self.description = description
        self.parent = parent
        self.restricted = restricted
        self.forbidden = forbidden

    @classmethod
    def from_json(cls, data):
        return cls(**data)