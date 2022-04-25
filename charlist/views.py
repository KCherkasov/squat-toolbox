# -*- coding: utf-8 -*-


from django.shortcuts import render, reverse


from .flyweights import *
from .constants import *

import os
print(os.getcwd())
aptitudes = Aptitude.from_file(json.load(open('../../static/json/aptitudes.json', 'r')))


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes, })
