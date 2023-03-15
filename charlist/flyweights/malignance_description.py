from typing import Dict, List

from charlist.flyweights.core.hint import Hint
from charlist.flyweights.core.hinted_description import HintedDescription
from charlist.flyweights.models.malignance_model import MalignanceModel


class MalignanceDescription(HintedDescription):
    def __init__(self, tag: str, name: Dict[str, str], description: Dict[str, str], hints: List[Hint],
                 commands: List[Dict], rolls_range: List[int]):
        super().__init__(tag, name, description, hints)
        self.__commands = commands
        self.__rolls_range = rolls_range

    def get_commands(self):
        return self.__commands

    def get_rolls_range(self):
        return self.__rolls_range

    @classmethod
    def from_model(cls, model: MalignanceModel):
        hints = list()
        for model in model.hints:
            hints.append(Hint.from_model(model))
        return cls(model.tag, model.name, model.description, hints, model.commands, model.rolls_range)

    @classmethod
    def from_file(cls, fdata):
        maligns = list()
        for mal in fdata['malignancies']:
            maligns.append(MalignanceModel.from_json(mal))
        if len(maligns) > 0:
            malignancies = list()
            for mal in maligns:
                malignancies.append(MalignanceDescription.from_model(mal))
            return malignancies
        else:
            return None
