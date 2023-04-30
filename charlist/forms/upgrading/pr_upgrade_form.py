from django.forms import Form


class PRUpgrageForm(Form):
    def __init__(self, pr: int, cost: int, *args, **kwargs):
        super(PRUpgrageForm, self).__init__(*args, **kwargs)
        self.__pr = pr
        self.__cost = cost

    def pr(self):
        return self.__pr

    def pr_new(self):
        return self.__pr + 1

    def cost(self):
        return self.__cost
