# -*- coding: utf-8 -*-
from random import choice

from django.db import models

import charlist.models

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


class MaleJapanese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleJapanese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesJapanese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class TechDesignationsManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_letters(self):
        return self.queryset().all().values_list('letters')

    def get_text_numbers(self):
        return self.queryset().all().values_list('text_numbers')

    def get_random_element(self, elements):
        return choice(elements)[0]


class TechDesignations(models.Model):
    objects = TechDesignationsManager()

    letters = models.CharField(max_length=15)
    text_numbers = models.CharField(max_length=15)


class RanksCultsManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_ranks_simple(self):
        return self.queryset().all().values_list('rank_simple')

    def get_ranks_noble_logi(self):
        return self.queryset().all().values_list('rank_noble_logi')

    def get_ranks_noble_artisan(self):
        return self.queryset().all().values_list('rank_noble_artisan')

    def get_ranks_noble_myrmidon(self):
        return self.queryset().all().values_list('rank_noble_myrmidon')

    def get_ranks_noble_genetor(self):
        return self.queryset().all().values_list('rank_noble_genetor')

    def get_ranks_noble_magi(self):
        return self.queryset().all().values_list('rank_noble_magi')

    def get_cults(self):
        return self.queryset().all().values_list('cult')

    def get_random_element(self, elements):
        return choice(elements)[0]


class MechanicusRanksNCults(models.Model):
    objects = RanksCultsManager()

    rank_simple = models.CharField(max_length=30)
    rank_noble_magi = models.CharField(max_length=30)
    rank_noble_genetor = models.CharField(max_length=30)
    rank_noble_logi = models.CharField(max_length=30)
    rank_noble_artisan = models.CharField(max_length=30)
    rank_noble_myrmidon = models.CharField(max_length=30)
    cult = models.CharField(max_length=30)


class MaleHungarian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleHungarian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MaleRomanian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleRomanian(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesRomanianManager(models.Manager):
    def queryset(self):
        return models.QuerySet(self.model, using=self._db)

    def get_random_element(self, elements):
        return choice(elements)[0]

    def get_firsts_list(self):
        return self.queryset().all().values_list('first')

    def get_seconds_list(self):
        return self.queryset().all().values_list('second')


class SurnamesRomanian(models.Model):
    objects = SurnamesRomanianManager()

    first = models.CharField(max_length=15)
    second = models.CharField(max_length=15)


class MaleChinese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleChinese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesChinese(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MaleGerman(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleGerman(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesGerman(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MaleFrance(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleFrance(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class SurnamesFrance(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class MaleArabic(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)


class FemaleArabic(models.Model):
    objects = NameManager()

    first_part = models.CharField(max_length=15)
    second_part = models.CharField(max_length=15)
