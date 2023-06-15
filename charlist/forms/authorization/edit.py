# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from charlist.models import CharsheetUser


# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from charlist.models import CharsheetUser

choices = (['ru', u'Русский'], ['en', 'English'])


class UserEditForm(forms.Form):
    password_set = forms.CharField(label=u'Пароль', min_length=10, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=u'Подтверждение пароля', widget=forms.PasswordInput)
    preferable_language = forms.ChoiceField(label=u'Предпочитаемый язык', choices=choices)

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        pwd = cleaned_data.get('password_set')
        pwd2 = cleaned_data.get('password_confirm')
        if pwd and pwd2 and pwd != pwd2:
            raise ValidationError(u'Пароли не совпадают')
        return pwd2
