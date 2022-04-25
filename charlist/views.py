# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render, reverse

from .flyweights import *
from .constants import *


def apts():
    data = json.load(open('static/json/aptitudes.json', 'r', encoding='utf-8'))
    return Aptitude.from_file(data)


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': apts(), })
