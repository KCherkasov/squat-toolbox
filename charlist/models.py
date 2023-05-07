# -**- coding: utf-8 -*-

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models import Count
from django.urls import reverse

import charlist.character.character
from charlist.character.json.decoders.character_decoder import CharacterDecoder
from charlist.character.rt_creation_data import RTCreationDataModel
from urllib.parse import unquote
import json
import re


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
    id = models.CharField(verbose_name=u'Логин', max_length=40, unique=True, primary_key=True)
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

    def get_char_creation_link(self):
        return unquote(reverse('create-character-start', kwargs={'user_id': self.pk}),
                       encoding='utf-8', errors='replace')

    def get_season_creation_link(self):
        pass

    def get_group_creation_link(self):
        pass


class SeasonQuerySet(models.QuerySet):
    def with_creator(self):
        return self.prefetch_related('creator')

    def with_groups(self):
        return self.prefetch_related('character_groups')


class SeasonManager(models.Manager):
    def queryset(self):
        query = SeasonQuerySet(self.model, using=self._db)
        return query.with_creator()

    def by_uid(self, uid):
        return self.queryset().filter(creator=uid)

    def by_name_id(self, name_id):
        return self.queryset().get(name_id=name_id)


class Season(models.Model):
    name = models.CharField(max_length=100, default=u'')
    name_id = models.CharField(max_length=200, default=u'', unique=True)
    description = models.TextField(max_length=5000, default=u'', verbose_name=u'Краткое описание')
    creator = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    master_notes = models.CharField(max_length=1000, default=u'', blank=True)

    objects = SeasonManager()

    def get_url(self):
        return unquote(reverse('season', kwargs={'season_id': self.name_id, }), encoding='utf-8', errors='replace')

    def get_edit_link(self):
        return unquote(reverse('edit-season', kwargs={'season_id': self.name_id, }),
                       encoding='utf-8', errors='replace')

    def get_delete_link(self):
        return unquote(reverse('delete-season', kwargs={'season_id': self.name_id, }),
                       encoding='utf-8', errors='replace')

    def get_create_group_link(self):
        return unquote(reverse('create-group', kwargs={'season_id': self.name_id, }),
                       encoding='utf-8', errors='replace')

    def make_name_id(self):
        return re.sub(' +', '_', self.name)


class CharacterGroupManager(models.Manager):
    def group_size(self):
        return self.annotate(group_size=Count('character'))

    def order_by_size(self):
        return self.group_size().order_by('-group_size')

    def get_by_season(self, season):
        return self.order_by_size().filter(season=season)

    def get_by_name(self, name):
        return self.get(name=name)

    def get_by_name_id(self, name_id):
        return self.get(name_id=name_id)


class CharacterGroup(models.Model):
    creator = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    name_id = models.CharField(max_length=120, default=u'', unique=True)
    name = models.CharField(max_length=60, verbose_name=u'Название группы')
    description = models.TextField(max_length=1000, verbose_name=u'Описание группы')
    master_notes_url = models.TextField(max_length=500, default='', blank=True)
    group_notes_url = models.TextField(max_length=500, default='', blank=True)
    is_rt = models.BooleanField(default=False)
    group_ifl = models.PositiveIntegerField(default=25)

    objects = CharacterGroupManager()

    def get_url(self):
        return unquote(reverse('group', kwargs={'group_id': self.name_id}), encoding='utf-8', errors='replace')

    def get_edit_link(self):
        return unquote(reverse('edit-group', kwargs={'group_id': self.name_id}), encoding='utf-8', errors='replace')

    def get_delete_link(self):
        return unquote(reverse('delete-group', kwargs={'group_id': self.name_id}), encoding='utf-8', errors='replace')

    def make_name_id(self):
        return self.season.name_id + '_' + re.sub(' +', '_', self.name)


class CharacterQuerySet(models.QuerySet):
    def with_owner(self):
        return self.prefetch_related('owner')

    def with_groups(self):
        return self.prefetch_related('groups')


class CharacterManager(models.Manager):
    def queryset(self):
        query = CharacterQuerySet(self.model, using=self._db)
        return query.with_owner().with_groups()

    def by_uid(self, uid):
        return self.filter(owner=uid)


class Character(models.Model):
    owner = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    groups = models.ManyToManyField(CharacterGroup, blank=True, default=None)
    creation_date = models.DateField(auto_now_add=True)
    character_data = models.CharField(max_length=25000)
    notes = models.TextField(max_length=1000, default="", blank=True)
    is_rt = models.BooleanField(default=False)

    objects = CharacterManager()

    def data_to_model(self):
        return CharacterDecoder.decode(str(self.character_data), self.is_rt)

    def get_view_url(self):
        return unquote(reverse('character-details', kwargs={'char_id': self.pk}), encoding='utf-8', errors='replace')

    def get_upgrade_url(self):
        return unquote(reverse('character-upgrade', kwargs={'char_id': self.pk}), encoding='utf-8', errors='replace')

    def get_delete_url(self):
        return unquote(reverse('character-delete', kwargs={'char_id': self.pk}), encoding='utf-8', errors='replace')


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
    curr_stage = models.CharField(max_length=15, default='init')

    name = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    starting_xp = models.IntegerField(blank=True, null=True)
    characteristic_base = models.CharField(max_length=15, blank=True, null=True)

    homeworld = models.CharField(max_length=15, blank=True, null=True)

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

    background = models.CharField(max_length=15, blank=True, null=True)

    role = models.CharField(max_length=15, blank=True, null=True)

    background_apt = models.CharField(max_length=15, blank=True, null=True)
    role_apt = models.CharField(max_length=15, blank=True, null=True)
    bg_skill_1 = models.IntegerField(blank=True, null=True)
    bg_skill_1_subtag = models.CharField(max_length=30, blank=True, null=True)
    bg_skill_2 = models.IntegerField(blank=True, null=True)
    bg_skill_2_subtag = models.CharField(max_length=30, blank=True, null=True)
    bg_talent = models.IntegerField(blank=True, null=True)
    role_talent = models.CharField(max_length=15, blank=True, null=True)
    bg_trait = models.CharField(max_length=15, blank=True, null=True)
    hw_bonus_talent = models.CharField(max_length=15, blank=True, null=True)

    apt_1 = models.CharField(max_length=15, blank=True, null=True)
    apt_2 = models.CharField(max_length=15, blank=True, null=True)

    divination_roll = models.IntegerField(blank=True, null=True)
    wound_roll = models.IntegerField(blank=True, null=True)
    fate_roll = models.IntegerField(blank=True, null=True)

    spec_skill_subtag_1 = models.CharField(max_length=30, blank=True, null=True)
    spec_skill_subtag_2 = models.CharField(max_length=30, blank=True, null=True)

    objects = CreationDataManager()

    def get_edit_url(self):
        return unquote(reverse('char-data-edit', kwargs={'creation_id': self.pk}), encoding='utf-8', errors='replace')

    def get_delete_url(self):
        return unquote(reverse('char-data-delete', kwargs={'creation_id': self.pk}), encoding='utf-8', errors='replace')


class RTCreationData(models.Model):
    owner = models.ForeignKey(CharsheetUser, on_delete=models.CASCADE)
    last_mod_date = models.DateField(auto_now_add=True)
    curr_stage = models.CharField(max_length=15, default='init')
    name = models.CharField(max_length=50, default='')

    character_data = models.CharField(max_length=25000)

    objects = CreationDataManager()

    def data_to_model(self):
        return RTCreationDataModel.from_json(str(self.character_data))

    def get_edit_url(self):
        return unquote(reverse('rt-char-data-edit', kwargs={'creation_id': self.pk}),
                       encoding='utf-8', errors='replace')

    def get_delete_url(self):
        return unquote(reverse('rt-char-data-delete', kwargs={'creation_id': self.pk}),
                       encoding='utf-8', errors='replace')


class LogEntry(models.Model):
    date = models.DateField(auto_now_add=True)
    data = models.CharField(max_length=1000)


def make_character_creation_entry(user_id, char_id):
    data = dict()
    data['user'] = user_id
    data['character'] = char_id
    entry = LogEntry(data=json.dumps(data))
    entry.save()
