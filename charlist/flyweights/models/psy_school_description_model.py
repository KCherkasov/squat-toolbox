from typing import Dict


class PsySchoolDescriptionModel(object):
    def __init__(self, tag:str, name: Dict[str, str], description: Dict[str, str]):
        self.tag = tag
        self.name = name
        self.description = description

    @classmethod
    def from_json(cls, data):
        return cls(**data)
