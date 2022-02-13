# -*- coding: utf-8 -*-
from random import choice

from django.db import models


class NameManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_first_parts_list(self):
        return list(self.queryset().all().values_list('first_part'))

    def get_second_parts_list(self):
        return list(self.queryset().all().values_list('second_part'))

    def get_random_part(self, nameparts):
        return choice(nameparts)[0]

    def get_random_name(self, first_parts, second_parts):
        first = ''
        second = ''
        while first.lower() == second.lower():
            first = self.get_random_part(first_parts)
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
