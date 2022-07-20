# -*- coding: utf-8 -*-

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import ValidationError

from charlist.models import CharsheetUser


class UserCreationForm(forms.ModelForm):
    password_set = forms.CharField(label=u'Пароль', min_length=10, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label=u'Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = CharsheetUser
        fields = ('id', 'email', 'is_master')

    def clean_password_confirm(self):
        cleaned_data = self.cleaned_data
        pwd = cleaned_data.get('password_set')
        pwd2 = cleaned_data.get('password_confirm')
        if pwd and pwd2 and pwd != pwd2:
            raise ValidationError(u'Пароли не совпадают')
        return pwd2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password_set'))
        if commit:
            user.save()
        return user
