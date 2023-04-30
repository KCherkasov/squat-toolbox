# -*- coding: utf-8 -*-
import json


class Talent(object):
    def __init__(self, tag: str, taken):
        self.__tag = tag
        self.__taken = taken

    def is_specialist(self):
        return isinstance(self.__taken, dict)

    def is_stackable(self, facade):
        talents = facade.talent_descriptions()
        if talents and (self.__tag in talents.keys()):
            return talents.get(self.__tag).is_stackable()
        else:
            return None

    def tag(self):
        return self.__tag

    def taken(self):
        return self.__taken

    def taken_subtag(self, subtag: str):
        if self.is_specialist():
            if subtag in self.__taken.keys():
                return self.__taken.get(subtag)
            else:
                return False
        else:
            return False

    def take(self, facade):
        if not self.is_specialist() and self.is_stackable(facade):
            self.__taken += 1

    def take_subtag(self, facade, subtag: str):
        if self.is_specialist():
            if subtag in self.__taken.keys():
                if self.is_stackable(facade):
                    self.__taken[subtag] += 1
            else:
                self.__taken[subtag] = 1

    @classmethod
    def from_json(cls, sdata):
        data = json.loads(sdata)
        return cls(**data)

    def toJSON(self):
        fields = dict()
        for key, val in self.__dict__.items():
            field_key = key[9:]
            fields[field_key] = val
        return json.dumps(self, default=lambda o: fields,
                          sort_keys=True, indent=4)
