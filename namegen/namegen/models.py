# -*- coding: utf-8 -*-
from random import choice

from django.db import models


class NameManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_random_part(self, nameparts):
        return choice(nameparts)[0]

    def get_random_name(self):
        first = ''
        second = ''
        first_part = list(self.queryset().all().values_list('first_part'))
        second_parts = list(self.queryset().all().values_list('second_part'))
        while first.lower() == second.lower():
            first = self.get_random_part(first_part)
            second = self.get_random_part(second_parts)
        return first + second


class MaleScand(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleScand(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)
