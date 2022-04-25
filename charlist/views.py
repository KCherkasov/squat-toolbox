# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render, reverse


from .flyweights import *
from .constants import *

data = json.load(open('static/json/aptitudes.json', 'r'))
aptitudes = Aptitude.from_file(data)
print(data, file=sys.stderr)


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes, })
