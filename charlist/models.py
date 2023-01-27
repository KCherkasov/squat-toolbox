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
    notes = models.TextField(max_length=10000, default="")

    objects = CharsheetUserManager()

    def data_to_model(self):
        return CharacterDecoder.decode(str(self.character_data))


class CreationDataQuerySet(models.QuerySet):
    def with_owner(self):
        self.prefetch_related('owner')


class CreationDataManager(models.Manager):
    def queryset(self):
        query = CreationDataQuerySet(self.model, using=self._db)
        return query.with_owner()

    def by_uid(self, uid):
        return self.filter(owner=uid)


class CreationData(models.Model):
    owner = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    last_mod_date = models.DateField(auto_now_add=True)

    name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    starting_xp = models.IntegerField(blank=True, null=True)
    characteristic_base = models.CharField(blank=True, null=True)

    homeworld = models.CharField(blank=True, null=True)

    weapon_skill = models.IntegerField(blank=True, null=True)
    ballistic_skill = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    toughness = models.IntegerField(blank=True, null=True)
    agility = models.IntegerField(blank=True, null=True)
    intelligence = models.IntegerField(blank=True, null=True)
    perception = models.IntegerField(blank=True, null=True)
    willpower = models.IntegerField(blank=True, null=True)
    fellowship = models.IntegerField(blank=True, null=True)
    influence = models.IntegerField(blank=True, null=True)

    background = models.CharField(blank=True, null=True)

    role = models.CharField(blank=True, null=True)

    background_apt = models.CharField(blank=True, null=True) #TODO: double-check!
    role_apt = models.CharField(blank=True, null=True) #TODO: double-check!
    bg_skill_1 = models.IntegerField(blank=True, null=True)
    bg_skill_1_subtag = models.CharField(blank=True, null=True)
    bg_skill_2 = models.IntegerField(blank=True, null=True)
    bg_skill_2_subtag = models.CharField(blank=True, null=True)
    bg_talent = models.IntegerField(blank=True, null=True)
    role_talent = models.CharField(blank=True, null=True)
    bg_trait = models.CharField(blank=True, null=True)
    hw_bonus_talent = models.CharField(blank=True, null=True)

    apt_1 = models.CharField(blank=True, null=True)
    apt_2 = models.CharField(blank=True, null=True)

    divination_roll = models.IntegerField(blank=True, null=True)
    wound_roll = models.IntegerField(blank=True, null=True)
    fate_roll = models.IntegerField(blank=True, null=True)

    spec_skill_subtag_1 = models.CharField(blank=True, null=True)
    spec_skill_subtag_2 = models.CharField(blank=True, null=True)

    objects = CreationDataManager()


class LogEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    data = models.CharField(max_length=1000)


def make_character_creation_entry(user_id, char_id):
    data = dict()
    data['user'] = user_id
    data['character'] = char_id
    entry = LogEntry(data=json.dumps(data))
    entry.save()
