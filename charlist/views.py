# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render, reverse


from .flyweights import *
from .constants import *


aptitudes = Aptitude.from_file(json.load(open('static/json/aptitudes.json', 'r')))
print(aptitudes, file=sys.stdin)


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes, })
