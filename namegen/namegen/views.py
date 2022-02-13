# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from .models import MaleScand, FemaleScand
from .forms2 import NamegenForm

import random


def main(request):
    return HttpResponseRedirect(reverse('index'))


def index(request):
    if request.method == 'POST':
        form = NamegenForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            gender = data['gender']
            lang = data['lang']
            count = data['count']
            if lang == 'SC':
                names = list()
                first_parts_male = MaleScand.objects.get_first_parts_list()
                second_parts_male = MaleScand.objects.get_second_parts_list()
                first_parts_female = FemaleScand.objects.get_first_parts_list()
                second_parts_female = FemaleScand.objects.get_second_parts_list()
                if count == 1:
                    names.append(generate_name_scand(gender, first_parts_male, second_parts_male,
                                                     first_parts_female, second_parts_female))
                else:
                    names = generate_names_scand(gender, first_parts_male, second_parts_male,
                                                 first_parts_female, second_parts_female, count)
                return render(request, 'index.html', {'form': form, 'names': names, })
    else:
        form = NamegenForm()
        return render(request, 'index.html', {'form': form, })


def d100():
    return random.randint(1, 100)


def generate_name_scand(gender, first_parts_male, second_parts_male, first_parts_female, second_parts_female):
    gender_tail = ''
    if gender == 'R':
        dice = d100()
        if dice <= 50:
            gender = 'M'
            gender_tail = ' (муж.)'
        else:
            gender = 'F'
            gender_tail = ' (жен.)'
    if gender == 'M':
        name = MaleScand.objects.get_random_name(first_parts_male, second_parts_male)
    else:
        name = FemaleScand.objects.get_random_name(first_parts_female, second_parts_female)
    name += ' '
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
    return name + surname + gender_tail


def generate_names_scand(gender, first_parts_male, second_parts_male,
                         first_parts_female, second_parts_female, count=10):
    names = list()
    for i in range(count):
        names.append(generate_name_scand(gender, first_parts_male, second_parts_male,
                                         first_parts_female, second_parts_female))
    return names
