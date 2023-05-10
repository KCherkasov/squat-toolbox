from django import forms
from django.forms import Form


class FateControlsForm(Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
