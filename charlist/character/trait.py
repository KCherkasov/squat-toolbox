# -*- coding: utf-8 -*-
import json

from charlist.flyweights.flyweights import Facade


class Trait(object):
    def __init__(self, tag: str, taken):
        self.__tag = tag
        self.__taken = taken

    def tag(self):
        return self.__tag

    def is_specialist(self):
        return isinstance(self.__taken, dict)

    def is_stackable(self, facade):
        traits = facade.trait_descriptions()
        if traits and (self.__tag in traits.keys()):
            return traits.get(self.__tag).is_stackable()

    def taken(self):
        return self.__taken

    def taken_subtag(self, subtag: str):
        if self.is_specialist():
            if subtag in self.__taken.keys():
                return self.__taken.get(subtag)
            else:
                return 0
        else:
            return None

    def take(self, facade):
        if not self.is_specialist() and self.is_stackable(facade):
            self.__taken += 1

    def take_subtag(self, facade, subtag: str):
        if self.taken_subtag(subtag) > 0:
            if self.is_stackable(facade):
                self.__taken[subtag] += 1
        elif self.taken_subtag(subtag) == 0:
            self.__taken[subtag] = 1

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        return cls(**data)

    def toJSON(self):
        fields = dict()
        for key, val in self.__dict__.items():
            field_key = key[8:]
            fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=4)
