from django.forms import Form


class PsyPowerUpgradeForm(Form):
    def __init__(self, pp_tag: str, cost: int, available: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pp_tag = pp_tag
        self.cost = cost
        self.available = available
