from typing import Dict, List

from django.forms import Form


class GainExtraOriginCommand(Form):
    def __init__(self, cmd: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cost = cmd.get('cost')
        self.cmd_id = cmd.get('cmd_id')
        self.description = cmd.get('description')

