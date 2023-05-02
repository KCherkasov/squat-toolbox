from django.forms import Form


class EliteAdvanceUpgradeForm(Form):
    def __init__(self, ea_tag: str, cost: int, available: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ea_tag = ea_tag
        self.cost = cost
        self.available = available
