# -**- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

import charlist.character.character
from charlist.character.json.decoders.character_decoder import CharacterDecoder
import json


class CharsheetUserManager(BaseUserManager):
    def all(self):
        return super(CharsheetUserManager, self).all()

    def create_user(self, id, email, is_master, password=None):
        if not email:
            raise ValueError('Необходимо ввести email')
        email = self.normalize_email(email)
        user = self.model(id, self.normalize_email(email), is_master)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, email, is_master, password=None):
        user = self.create_user(id, email, is_master, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class CharsheetUser(AbstractBaseUser):
    id = models.CharField(verbose_name=u'Логин',max_length=40, unique=True, primary_key=True)
    email = models.EmailField(max_length=40, unique=True)
    is_master = models.BooleanField(verbose_name=u'Мастер', default=False)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = CharsheetUserManager()

    USERNAME_FIELD = 'id'
    EMAIL_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class CharacterQuerySet(models.QuerySet):
    def with_owner(self):
        return self.prefetch_related('owner')


class CharacterManager(models.Manager):
    def queryset(self):
        query = CharacterQuerySet(self.model, using=self._db)
        return query.with_owner()

    def by_uid(self, uid):
        return self.filter(owner=uid)


class Character(models.Model):
    owner = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    character_data = models.CharField(max_length=2500)  # TODO - encoder/decoder!

    objects = CharsheetUserManager()

    def data_to_model(self):
        return CharacterDecoder.decode(str(self.character_data))
