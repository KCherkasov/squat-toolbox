# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from charlist.models import CharsheetUser


class SignInForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите логин', }),
      max_length=30,
      label=u'Логин')
    password = forms.CharField(widget=forms.PasswordInput(
      attrs={'class': 'form-control', 'placeholder': u'Введите пароль', }),
      label=u'Пароль')

    def clean(self):
        data = self.cleaned_data
        user = authenticate(username=data.get('login'), password=data.get('password'))
        if user is not None:
            if user.is_active:
                data['user'] = user
            else:
                raise forms.ValidationError('Учетная запись не активна')
        else:
            raise forms.ValidationError('Неверный логин и/или пароль')
