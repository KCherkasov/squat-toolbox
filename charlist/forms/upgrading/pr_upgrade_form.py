from django.forms import Form


class PRUpgrageForm(Form):
    def __init__(self, pr: int, cost: int, *args, **kwargs):
        super(PRUpgrageForm, self).__init__(*args, **kwargs)
        self.pr = pr
        self.cost = cost

    def pr_new(self):
        return self.pr + 1
