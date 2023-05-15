from django import forms
from django.forms import Form


class AddDocLinkForm(Form):
    link = forms.CharField(max_length=1500, label=u'Ссылка на Google Doc')
