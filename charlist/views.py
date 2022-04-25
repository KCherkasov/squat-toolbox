# -*- coding: utf-8 -*-
import sys

from django.shortcuts import render, reverse
import logging

from .flyweights import *
from .constants import *

logging.debug('reading apts')
data = json.load(open('static/json/aptitudes.json', 'r'))
logging.debug('apts read, making apt objects from\n')
logging.debug(data)
aptitudes = Aptitude.from_file(data)


def aptitudes_test(request):
    return render(request, 'charlist_test.html', {'version': VERSION, 'apts': aptitudes, })
