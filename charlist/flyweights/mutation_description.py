from typing import Dict, List

from charlist.flyweights.models.mutation_model import MutationModel
from charlist.flyweights.core.hint import Hint
from charlist.flyweights.core.hinted_description import HintedDescription


class MutationDescription(HintedDescription):
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
    def from_model(cls, model: MutationModel):
        hints = list()
        for hint in model.hints:
            hints.append(Hint.from_model(hint))
        return cls(model.tag, model.name, model.description, hints, model.commands, model.rolls_range)

    @classmethod
    def from_file(cls, fdata):
        muts = list()
        for model in fdata['mutations']:
            muts.append(MutationModel.from_json(model))
        if len(muts) > 0:
            mutations = list()
            for model in muts:
                mutations.append(MutationDescription.from_model(model))
            return mutations
        else:
            return None
