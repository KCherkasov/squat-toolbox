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
                if count == 1:
                    names.append(generate_name_scand(gender))
                else:
                    names = generate_names_scand(gender, count)
                return render(request, 'index.html', {'form': form, 'names': names, })
    else:
        form = NamegenForm()
        return render(request, 'index.html', {'form': form, })


def d100():
    return random.randint(1, 100)


def generate_name_scand(gender):
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
        name = MaleScand.objects.get_random_name()
    else:
        name = FemaleScand.objects.get_random_name()
    name += ' '
    dice = d100()
    if dice <= 50:
        surname = MaleScand.objects.get_random_name()
    else:
        surname = FemaleScand.objects.get_random_name()
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


def generate_names_scand(gender, count=10):
    names = list()
    for i in range(count):
        names.append(generate_name_scand(gender))
    return names
