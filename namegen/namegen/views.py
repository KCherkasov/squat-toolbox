# -*- coding: utf-8 -*-
from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .models import MaleScand, FemaleScand, MaleLatin, FemaleLatin, CognomenLatin, MaleSpanish, FemaleSpanish
from .forms2 import NamegenForm

import random

version = '1.2.5'

CONSONANTS = 'бвгджзйклмнпрстфхшщчц'
RIGHT_CONSONANTS = 'йнрс'
VOWELS = 'аеёиоуыэюя'


def main(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    if request.method == 'POST':
        form = NamegenForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            gender = data['gender']
            lang = data['lang']
            nobility = data['nobility']
            count = data['count']
            names = list()
            if lang == 'SC':
                first_parts_male = MaleScand.objects.get_first_parts_list()
                second_parts_male = MaleScand.objects.get_second_parts_list()

                first_parts_female = FemaleScand.objects.get_first_parts_list()
                second_parts_female = FemaleScand.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female))
                else:
                    names = generate_names_scand(gender, nobility, first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female, count)
            elif lang == 'LAT':
                first_parts_male = MaleLatin.objects.get_first_parts_list()
                second_parts_male = MaleLatin.objects.get_second_parts_list()

                first_parts_female = FemaleLatin.objects.get_first_parts_list()
                second_parts_female = FemaleLatin.objects.get_second_parts_list()

                cognomen_first_parts = CognomenLatin.objects.get_first_parts_list()
                cognomen_second_parts_male = CognomenLatin.objects.get_second_parts_male_list()
                cognomen_second_parts_female = CognomenLatin.objects.get_second_parts_female_list()

                if count == 1:
                    names.append(generate_name_latin(gender, nobility,
                                                     first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female,
                                                     cognomen_first_parts, cognomen_second_parts_male,
                                                     cognomen_second_parts_female))
                else:
                    names = generate_names_latin(gender, nobility, count,
                                                 first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female,
                                                 cognomen_first_parts, cognomen_second_parts_male,
                                                 cognomen_second_parts_female)
            elif lang == 'SP':
                first_parts_male = MaleSpanish.objects.get_first_parts_list()
                second_parts_male = MaleSpanish.objects.get_second_parts_list()

                first_parts_female = FemaleSpanish.objects.get_first_parts_list()
                second_parts_female = FemaleSpanish.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_spanish(gender, nobility,
                                                       first_parts_male, second_parts_male,
                                                       first_parts_female, second_parts_female))
                else:
                    names = generate_names_spanish(gender, nobility, count,
                                                   first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female)
            return render(request, 'index.html', {'form': form, 'names': names, 'version': version, })

    else:
        form = NamegenForm()
        return render(request, 'index.html', {'form': form, 'version': version, })


def d100():
    return random.randint(1, 100)


def generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female):
    gender_tail = ''
    if gender == 'R':
        dice = d100()
        if dice <= 50:
            gender = 'M'
            gender_tail = u' (муж.)'
        else:
            gender = 'F'
            gender_tail = u' (жен.)'
    noble_tail = ''
    if nobility == 'R':
        gender_tail += ' '
        if d100() <= 50:
            nobility = 'N'
            noble_tail = u'(благородное)'
        else:
            nobility = 'S'
            noble_tail = u'(простое)'
    if gender == 'M':
        name = MaleScand.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = FemaleScand.objects.get_random_name(first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == 'N':
        if d100() <= 50:
            middle_name = MaleScand.objects.get_random_name(first_parts_male, second_parts_male)
        else:
            middle_name = FemaleScand.objects.get_random_name(first_parts_female, second_parts_female)
        middle_name += ' '
    dice = d100()
    if dice <= 50:
        surname = MaleScand.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        surname = FemaleScand.objects.get_random_name(first_parts_female, second_parts_female)
    dice = d100()
    if gender == 'M':
        if dice <= 50:
            surname += 'ссон'
        else:
            surname += 'снеф'
    else:
        if dice <= 50:
            surname += 'сдоттир'
        else:
            surname += 'сниз'
    return name + middle_name + surname + gender_tail + noble_tail


def generate_names_scand(gender, nobility, first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female, count=10):
    names = list()
    for i in range(count):
        names.append(generate_name_scand(gender, nobility,
                                         first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female))
    return names


def generate_name_latin(gender, nobility,
                        first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female,
                        cognomen_first_parts, cognomen_second_parts_male,
                        cognomen_second_parts_female):
    gender_tail = ''
    if gender == 'R':
        if d100() <= 50:
            gender_tail = '(муж.)'
            gender = 'M'
        else:
            gender_tail = '(жен.)'
            gender = 'F'
    noble_tail = ''
    if nobility == 'R':
        gender_tail += ' '
        if d100() <= 50:
            nobility = 'N'
            noble_tail = u'(благородное)'
        else:
            nobility = 'S'
            noble_tail = u'(простое)'
    if gender == 'M':
        name = MaleLatin.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = FemaleLatin.objects.get_random_name(first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == 'N':
        if gender == 'M':
            middle_name = MaleLatin.objects.get_random_name(first_parts_male, second_parts_male)
        else:
            middle_name = FemaleLatin.objects.get_random_name(first_parts_female, second_parts_female)
        middle_name += ' '
        if d100() <= 50:
            if gender == 'M':
                middle_name = middle_name + MaleLatin.objects.get_random_name(first_parts_male, second_parts_male)
            else:
                middle_name = middle_name + \
                              FemaleLatin.objects.get_random_name(first_parts_female, second_parts_female)
            middle_name += ' '
        if d100() <= 25:
            if gender == 'M':
                middle_name = middle_name + MaleLatin.objects.get_random_name(first_parts_male, second_parts_male)
            else:
                middle_name = middle_name + \
                              FemaleLatin.objects.get_random_name(first_parts_female, second_parts_female)
            middle_name += ' '
    if gender == 'M':
        cognomen = CognomenLatin.objects.get_random_cognomen(cognomen_first_parts, cognomen_second_parts_male)
    else:
        cognomen = CognomenLatin.objects.get_random_cognomen(cognomen_first_parts, cognomen_second_parts_female)
    cognomen += ' '
    return name + middle_name + cognomen + gender_tail + noble_tail


def generate_names_latin(gender, nobility, count,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female,
                         cognomen_first_parts, cognomen_second_parts_male,
                         cognomen_second_parts_female):
    names = list()
    for i in range(count):
        names.append(generate_name_latin(gender, nobility, first_parts_male,
                                         second_parts_male, first_parts_female,
                                         second_parts_female, cognomen_first_parts,
                                         cognomen_second_parts_male, cognomen_second_parts_female))
    return names


def generate_name_spanish(gender, nobility,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female):
    gender_tail = ''
    if gender == 'R':
        if d100() <= 50:
            gender_tail = '(муж.)'
            gender = 'M'
        else:
            gender_tail = '(жен.)'
            gender = 'F'
    noble_tail = ''
    if nobility == 'R':
        gender_tail += ' '
        if d100() <= 50:
            nobility = 'N'
            noble_tail = u'(благородное)'
        else:
            nobility = 'S'
            noble_tail = u'(простое)'
    name = ''
    if gender == 'M':
        name = MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
    name += ' '
    if nobility == 'N':
        threshold = 75
    else:
        threshold = 50
    for i in range(choice([1, 2, 3])):
        if d100() <= threshold:
            if gender == 'M':
                name += MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
            else:
                name += FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
            name += ' '
    surname = ''
    if d100() <= 50:
        surname = MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        surname = FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
    if surname[-1:] in VOWELS:
        surname = surname[:-1]
    dice = d100()
    if dice <= 25:
        if surname[-1:] != 'л':
            if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                surname += 'и'
            if d100() <= 50:
                surname += 'хас'
            else:
                surname += 'гас'
        else:
            surname += 'ас'
    elif dice <= 50:
        if surname[-1:] != 'л':
            if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                surname += 'и'
            if d100() <= 50:
                surname += 'хес'
            else:
                surname += 'гес'
        else:
            surname += 'ес'
    elif dice <= 75:
        if surname[-1:] != 'з':
            if surname[-1:] != 'т':
                surname += 'сия'
            else:
                surname = surname[:-1] + 'ция'
        else:
            surname += 'ия'
    if d100() <= threshold:
        if nobility == 'N':
            if d100() <= 33:
                surname = ' ла ' + surname
            elif d100() <= 67:
                surname = ' де ' + surname
            else:
                surname = ' де ла ' + surname
        surname += '-и-'
        if d100() <= 50:
            surname += MaleSpanish.objects.get_random_name(first_parts_male, second_parts_male)
        else:
            surname += FemaleSpanish.objects.get_random_name(first_parts_female, second_parts_female)
        if surname[-1:] in VOWELS:
            surname = surname[:-1]
        dice = d100()
        if dice <= 25:
            if surname[-1:] != 'л':
                if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                    surname += 'и'
                if d100() <= 50:
                    surname += 'хас'
                else:
                    surname += 'гас'
            else:
                surname += 'ас'
        elif dice <= 50:
            if surname[-1:] != 'л':
                if surname[-1:] not in RIGHT_CONSONANTS and surname[-1:] not in VOWELS:
                    surname += 'и'
                if d100() <= 50:
                    surname += 'хес'
                else:
                    surname += 'гес'
            else:
                surname += 'ес'
        elif dice <= 75:
            if surname[-1:] != 'з':
                if surname[-1:] != 'т':
                    surname += 'сия'
                else:
                    surname = surname[:-1] + 'ция'
            else:
                surname += 'ия'
    else:
        if nobility == 'N':
            if d100() <= 33:
                surname = ' ла ' + surname
            elif d100() <= 67:
                surname = ' де ' + surname
            else:
                surname = ' де ла ' + surname
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_spanish(gender, nobility, count,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female):
    names = list()
    for i in range(count):
        names.append(generate_name_spanish(gender, nobility,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female))
    return names
