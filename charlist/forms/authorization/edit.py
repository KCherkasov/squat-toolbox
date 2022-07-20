# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from charlist.models import CharsheetUser


class UserEditForm(forms.ModelForm):
    password = forms.PasswordInput()

    class Meta:
        model = CharsheetUser
        fields = ('id', 'email', 'password', 'is_master')
