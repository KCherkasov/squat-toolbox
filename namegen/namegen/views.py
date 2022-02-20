# -*- coding: utf-8 -*-
from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .models import MaleScand, FemaleScand, MaleLatin, FemaleLatin, CognomenLatin,\
    MaleSpanish, FemaleSpanish, MaleItalian, FemaleItalian, SurnamesItalian
from .forms2 import NamegenForm

import random

version = '1.3.1'

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
            elif lang == 'IT':
                first_parts_male = MaleItalian.objects.get_first_parts_list()
                second_parts_male = MaleItalian.objects.get_second_parts_list()

                first_parts_female = FemaleItalian.objects.get_first_parts_list()
                second_parts_female = FemaleItalian.objects.get_second_parts_list()

                surnames_first_part = SurnamesItalian.objects.get_first_parts_list()
                surnames_second_part = SurnamesItalian.objects.get_second_parts_list()

                if count == 1:
                    names.append(generate_name_italian(gender, nobility,
                                                       first_parts_male, second_parts_male,
                                                       first_parts_female, second_parts_female,
                                                       surnames_first_part, surnames_second_part))
                else:
                    names = generate_names_italian(gender, nobility, count,
                                                   first_parts_male, second_parts_male,
                                                   first_parts_female, second_parts_female,
                                                   surnames_first_part, surnames_second_part)
            return render(request, 'index.html', {'form': form, 'names': names, 'version': version, })

    else:
        form = NamegenForm()
        return render(request, 'index.html', {'form': form, 'version': version, })


def d100():
    return random.randint(1, 100)


def generate_name_scand(gender, nobility, first_parts_male, second_parts_male,
                        first_parts_female, second_parts_female):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleScand, FemaleScand, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == 'N':
        if d100() <= 50:
            middle_name = generate_name(MaleScand, FemaleScand, 'M',
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
        else:
            middle_name = generate_name(MaleScand, FemaleScand, 'F',
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
        middle_name += ' '
    surname = generate_scand_surname(gender, first_parts_male, second_parts_male,
                                     first_parts_female, second_parts_female) + ' '
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
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleLatin, FemaleLatin, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    middle_name = ''
    if nobility == 'N':
        middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                    first_parts_male, second_parts_male,
                                    first_parts_female, second_parts_female)
        middle_name += ' '
        if d100() <= 50:
            middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
            middle_name += ' '
        if d100() <= 25:
            middle_name = generate_name(MaleLatin, FemaleLatin, gender,
                                        first_parts_male, second_parts_male,
                                        first_parts_female, second_parts_female)
            middle_name += ' '
    cognomen = generate_cognomen(gender, cognomen_first_parts,
                                 cognomen_second_parts_male,
                                 cognomen_second_parts_female)
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
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleSpanish, FemaleSpanish, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    if nobility == 'N':
        threshold = 75
    else:
        threshold = 50
    for i in range(choice([1, 2, 3])):
        if d100() <= threshold:
            name = generate_name(MaleSpanish, FemaleSpanish, gender,
                                 first_parts_male, second_parts_male,
                                 first_parts_female, second_parts_female)
            name += ' '

    surname = generate_spanish_surname(nobility, first_parts_male, second_parts_male,
                                       first_parts_female, second_parts_female) + ' '
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


def generate_name_italian(gender, nobility,
                          first_parts_male, second_parts_male,
                          first_parts_female, second_parts_female,
                          surnames_first_parts, surnames_second_part):
    [nobility, gender, gender_tail, noble_tail] = resolve_randomness(gender, nobility)
    name = generate_name(MaleItalian, FemaleItalian, gender,
                         first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female)
    name += ' '
    for i in range(choice([1, 2, 3])):
        if d100() <= 50:
            name += generate_name(MaleItalian, FemaleItalian, 'M',
                                  first_parts_male, second_parts_male,
                                  first_parts_female, second_parts_female)
        else:
            name += generate_name(MaleItalian, FemaleItalian, 'F',
                                  first_parts_male, second_parts_male,
                                  first_parts_female, second_parts_female)
    surname = generate_italian_surname(nobility, surnames_first_parts, surnames_second_part)
    surname += ' '
    return name + surname + gender_tail + noble_tail


def generate_names_italian(gender, nobility, count,
                           first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female,
                           surnames_first_parts, surnames_second_part):
    names = list()
    for i in range(count):
        names.append(generate_name_italian(gender, nobility,
                                           first_parts_male, second_parts_male,
                                           first_parts_female, second_parts_female,
                                           surnames_first_parts, surnames_second_part))
    return names


def determine_gender(gender):
    if gender == 'R':
        if d100() <= 50:
            gender = 'M'
        else:
            gender = 'F'
    return gender


def determine_nobility(nobility):
    if nobility == 'R':
        if d100() <= 50:
            nobility = 'N'
        else:
            nobility = 'S'
    return nobility


def resolve_randomness(gender, nobility):
    gender_tail = ''
    if gender == 'R':
        gender = determine_gender(gender)
        if gender == 'M':
            gender_tail = '(муж.)'
        else:
            gender_tail = '(жен.)'
    noble_tail = ''
    if nobility == 'R':
        nobility = determine_nobility(nobility)
        gender_tail += ' '
        if nobility == 'N':
            noble_tail = u'(благородное)'
        else:
            noble_tail = u'(простое)'
    return [nobility, gender, gender_tail, noble_tail]


def generate_cognomen(gender, first_parts, male, female):
    if gender == 'M':
        return CognomenLatin.objects.get_random_cognomen(first_parts, male)
    else:
        return CognomenLatin.objects.get_random_cognomen(first_parts, female)


def generate_name(lang_male, lang_female, gender,
                  first_parts_male, second_parts_male,
                  first_parts_female, second_parts_female):
    if gender == 'M':
        name = lang_male.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = lang_female.objects.get_random_name(first_parts_female, second_parts_female)
    return name


def generate_scand_surname(gender, first_parts_male, second_parts_male,
                           first_parts_female, second_parts_female):
    surname = ''
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
    return surname


def generate_spanish_surname(nobility, first_parts_male, second_parts_male,
                             first_parts_female, second_parts_female):
    surname = ''
    if nobility == 'N':
        threshold = 75
    else:
        threshold = 50
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
            if surname[-1:] not in 'тд':
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
                if surname[-1:] not in 'тд':
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
    return surname


def generate_italian_surname(nobility, first_parts, second_parts):
    surname = ''
    surname = SurnamesItalian.objects.get_random_name(first_parts, second_parts)
    if nobility == 'N':
        if d100() <= 50:
            if surname[1:].lower() in VOWELS:
                if d100() <= 50:
                    surname = 'Д\'' + surname
                else:
                    surname = 'ди ' + surname
            else:
                surname = 'ди ' + surname
        else:
            surname = 'ла ' + surname
    return surname
