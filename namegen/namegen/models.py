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


class MaleLatin(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleLatin(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class CognomenManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_random_part(self, nameparts):
        return choice(nameparts)[0]

    def get_first_parts_list(self):
        return list(self.queryset().all().values_list('first_part'))

    def get_second_parts_male_list(self):
        return list(self.queryset().all().values_list('second_part_male'))

    def get_second_parts_female_list(self):
        return list(self.queryset().all().values_list('second_part_female'))

    def get_random_cognomen(self, first_parts, second_parts):
        first = ''
        second = ''
        while first.lower() == second.lower():
            first = self.get_random_part(first_parts)
            second = self.get_random_part(second_parts)
        return first + second


class CognomenLatin(models.Model):
    objects = CognomenManager()

    first_part = models.CharField(max_length=15)
    second_part_male = models.CharField(max_length=15)
    second_part_female = models.CharField(max_length=15)


class MaleSpanish(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleSpanish(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MaleItalian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleItalian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesItalian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MalePolish(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemalePolish(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesPolish(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class PolishEndingsManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_male_endings(self):
        return self.queryset().all().values_list('male')

    def get_female_endings(self):
        return self.queryset().all().values_list('female')

    def random_ending(self, endings):
        return choice(endings)[0]


class SurnamesPolishEnd(models.Model):
    objects = PolishEndingsManager()

    male = models.CharField(max_length=15)
    female = models.CharField(max_length=15)
