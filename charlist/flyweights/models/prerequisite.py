# -*- coding: utf-8 -*-

from typing import Dict, List


class Prerequisite(object):
    def __init__(self, tag: str, value: int, subtag: List[str] = None, alt: Dict = None):
        self.tag = tag
        self.subtag = subtag
        self.value = value
        self.alt = alt

    def has_subtag(self):
        return not (self.subtag is None)

    def has_alt(self):
        return not (self.alt is None)

    def is_alt_list(self):
        return isinstance(self.alt, list)

    def get_alt_tag(self):
        return self.alt.get('tag')

    def alt_has_subtag(self):
        return 'subtag' in self.alt.keys()

    def get_alt_subtag(self):
        return self.alt.get('subtag')

    def get_alt_value(self):
        return self.alt.get('value')

    def get_alt(self):
        return self.alt

    @classmethod
    def from_json(cls, data):
        return cls(**data)
