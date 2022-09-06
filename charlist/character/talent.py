# -*- coding: utf-8 -*-
import json

from charlist.flyweights.flyweights import Facade


class Talent(object):
    def __init__(self, tag: str, taken):
        self.__tag = tag
        self.__taken = taken

    def is_specialist(self, facade: Facade):
        talents = facade.talent_descriptions()
        if talents is None or self.__tag not in talents.keys():
            return None
        else:
            return talents.get(self.__tag).is_specialist()

    def is_stackable(self, facade: Facade):
        talents = facade.talent_descriptions()
        if talents and (self.__tag in talents.keys()):
            return talents.get(self.__tag).is_stackable()
        else:
            return None

    def tag(self):
        return self.__tag

    def taken(self):
        return self.__taken

    def taken_subtag(self, facade: Facade, subtag: str):
        if self.is_specialist(facade):
            if subtag in self.__taken.keys():
                return self.__taken.get(subtag)
            else:
                return False
        else:
            return None

    def take(self, facade: Facade):
        if not self.is_specialist(facade) and self.is_stackable(facade):
            self.__taken += 1

    def take_subtag(self, facade: Facade, subtag: str):
        if self.is_specialist(facade):
            if subtag in self.__taken.keys():
                if self.is_stackable(facade):
                    self.__taken[subtag] += 1
            else:
                self.__taken[subtag] = 1

    @classmethod
    def from_json(cls, data):
        return cls(**data)

    def toJSON(self):
        fields = dict()
        for key, val in self.__dict__.items():
            field_key = key[9:]
            fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=4)
